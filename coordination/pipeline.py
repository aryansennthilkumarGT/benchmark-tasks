"""Sequential RoboCurve pipeline with immutable evidence and exact revision worktrees.

Exit 0: all requested mandatory stages passed; 2: incomplete/failed tasks;
3: environment/preflight blocker; 4: configuration error. Dry-run success only
means a plan was printed. No command in this module creates an upstream PR.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from engine import Incomplete, Ledger, Budget, atomic, digest, execute, exclusive, fingerprint, read, utc
from environment import hardware, bootstrap, capture, verify_runtime, launchable_runtime
from evidence import public_text, require

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FORK = 'https://github.com/aryansennthilkumarGT/benchmark-tasks.git'
BASELINE = '7df8bd8ad8cb19df51718e5ff46d4d610a9da6f1'
STAGES = ('MECHANICS_COMPLETE','STATIC_TESTS_PASSED','NATIVE_PHYSICS_PASSED','ROBOT_CONTROL_PASSED',
          'EXPERT_DEMO_1_PASSED','EXPERT_DEMO_2_PASSED','CLEAN_CHECKOUT_EXPERT_PASSED','MODEL_EVALUATED','MEDIA_RENDERED','MEDIA_VERIFIED',
          'MEDIA_UPLOADED','EXACT_COMMIT_VERIFIED','READY_FOR_PR')


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--all',action='store_true')
    scope.add_argument('--task')
    scope.add_argument('--preflight',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--offline',action='store_true',help='Run cheap source/asset/controller checks only; never claims physical completion')
    parser.add_argument('--retry-failed',metavar='REASON')
    parser.add_argument('--no-upload',action='store_true',help='Preserve local verified media; report incomplete')
    parser.add_argument('--no-push',action='store_true',help='Preserve upload metadata locally; report incomplete')
    parser.add_argument('--run-root',type=Path,default=Path(os.getenv('ROBOCURVE_RUN_ROOT',str(REPO/'.robocurve-runs'))))
    parser.add_argument('--budget-file',type=Path,default=Path(os.getenv('ROBOCURVE_BUDGET_FILE',str(REPO/'.robocurve-budget.json'))))
    parser.add_argument('--launchable-root', type=Path,
                        help='Reuse the verified installed Arena and adapter under this directory')
    parser.add_argument('--deadline-unix',type=float,help='Hard wall-clock deadline; at most six hours from startup')
    parser.add_argument('--task-seconds',type=float,default=7200,help='Bound one candidate before switching to the next')
    parser.add_argument('--manifest',type=Path,default=HERE/'draft-manifest.json')
    return parser.parse_args(argv)


def selected(manifest, slug):
    tasks = manifest['tasks']
    expected=8 if manifest.get('schema_version',2)<3 else len(tasks)
    require(1<=expected<=8 and len(tasks)==expected and len({t['slug'] for t in tasks})==expected,
            'Manifest must contain one to eight independent tasks (legacy manifests require eight)')
    for task in tasks:
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',task['slug']),'Unsafe task slug')
        require(re.fullmatch(r'[0-9a-f]{40}',task['commit']),'Task commit must be a full SHA')
        require(re.fullmatch(r'(?:draft|repair|optimization)/[a-z0-9]+(?:[a-z0-9/-]*[a-z0-9])?',task['branch']),
                'Unexpected independent task branch')
        require(task['branch'] not in {'draft/twelve-cell-pack','publication/twelve-cell-pack',
                'draft/service-arm','draft/remote-battery-service','draft/node-service-closeout'},
                'Protected pending/rejected branch cannot enter replacement publication')
        require(task['task_folder']=='tasks/'+task['slug'],'Task folder mismatch')
    if slug:
        tasks=[t for t in tasks if t['slug']==slug]
        require(len(tasks)==1,'Unknown task slug')
    return tasks


def plan(tasks, root, lock):
    return {'kind':'DRY_RUN_NO_SIMULATION_OR_NETWORK', 'stack':lock,
            'estimated_storage_gib':250, 'gpu_workloads_concurrent':1,
            'budget':'Measured instance time; hard $170 cap, $30 credit reserve. No cloud provisioning.',
            'bootstrap':['official pinned adapter/setup.sh in isolated stack directory','official apple/bowl smoke'],
            'tasks':[{'slug':t['slug'],'commit':t['commit'],'branch':t['branch'],
                      'worktree':str(root/'worktrees'/t['slug']/t['commit']), 'stages':list(STAGES),
                      'commands':[['git','fetch','origin',t['commit']],
                                  ['python',t['task_folder']+'/native_tests.py','--mode','physics'],
                                  ['python',t['task_folder']+'/native_tests.py','--mode','control'],
                                  ['python',t['task_folder']+'/run.py','--mode','expert','--execute'],
                                  ['python',t['task_folder']+'/run.py','--mode','expert','--execute'],
                                  ['python',t['task_folder']+'/run.py','--mode','dream','--execute'],
                                  ['inspect-robots','video','<validated-log>','--out','<media-directory>'],
                                  ['python','tools/upload_media.py',t['task_folder'],'--video','<model.mp4>',
                                   '--demo','<demo.mp4>','--screenshot','<setup.png>']]} for t in tasks],
            'note':'Placeholders are filled by the executor from validated stage receipts; no mocked GPU or model results.'}


def checkout(task, root, evidence):
    cache=root/'source.git'; cache.parent.mkdir(parents=True,exist_ok=True)
    if not cache.exists():
        execute(['git','clone','--bare',FORK,str(cache)],root,evidence/'clone.log',600)
    require(capture(['git','remote','get-url','origin'],cache)==FORK,'Source cache remote changed')
    execute(['git','fetch','origin',task['commit']],cache,evidence/'fetch.log',600)
    destination=root/'worktrees'/task['slug']/task['commit']
    if not destination.exists():
        destination.parent.mkdir(parents=True,exist_ok=True)
        execute(['git','worktree','add','--detach',str(destination),task['commit']],cache,evidence/'worktree.log',120)
    require(capture(['git','rev-parse','HEAD'],destination)==task['commit'],'Worktree HEAD changed')
    require(not capture(['git','status','--porcelain'],destination),'Worktree contains uncommitted changes')
    changed=capture(['git','diff','--name-only',BASELINE,task['commit']],destination).splitlines()
    require(changed and all(p.startswith(task['task_folder']+'/') for p in changed),'Branch diff is not one task folder')
    atomic(evidence/'checkout.json',{'commit':task['commit'],'path':str(destination),'changed_files':changed})
    return destination


def integrity(folder, evidence, python, budget=None):
    required=('task.py','scene.json','scoring.py','run.py','expert.py','controller.json','native_tests.py',
              'mechanics-review.json','verify_assets.py','source_manifest.json','README.md')
    for name in required:
        require((folder/name).is_file(),'Missing required package file: '+name)
    for path in folder.rglob('*'):
        require(not path.is_symlink(),'Task package contains a symlink')
        if path.suffix=='.py':
            ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    manifest=read(folder/'source_manifest.json')
    hashes=manifest.get('files',manifest.get('sha256',{}))
    require(isinstance(hashes,dict) and hashes,'Source manifest has no file hashes')
    for name, expected in hashes.items():
        path=folder/name
        require(path.resolve().is_relative_to(folder.resolve()),'Source manifest escapes task folder')
        content=path.read_bytes().replace(b'\r\n',b'\n')
        require(hashlib.sha256(content).hexdigest()==expected,'Source manifest mismatch: '+name)
    # Reviewer can clone only this branch; no coordination module may be imported.
    for path in folder.glob('*.py'):
        require(not re.search(r'from coordination|import coordination|[A-Z]:\\Users\\',path.read_text()),
                'Task depends on private coordination/development paths')
    require(any(folder.glob('test_*.py')),'No executable offline tests')
    if (folder/'static_check.py').is_file():
        # New self-contained packages declare their actual audits, including full
        # controller FK sampling. Do not require unrelated legacy audit filenames.
        execute([python,str(folder/'static_check.py')],folder,evidence/'static-check.log',3600,budget=budget)
    else:
        execute([python,'-m','unittest','discover','-s',str(folder),'-p','test_*.py','-v'],folder,evidence/'unit-tests.log',900)
        for script in ('verify_assets.py','audit_control.py','audit_geometry.py','audit_grasps.py','audit_motion.py','audit_threads.py'):
            execute([python,str(folder/script)],folder,evidence/(script.replace('.py','.json')),1800)
    result=public_text(folder)
    result.update(kind='OFFLINE_STATIC_UNIT_USD_KINEMATICS_ONLY', physics_executed=False)
    atomic(evidence/'static.json',result)
    return result


def mechanics(folder, evidence):
    review=read(folder/'mechanics-review.json')
    require(review.get('implementation_review')=='COMPLETE','Mechanism implementation review is incomplete')
    require(review.get('unimplemented_mechanics')==[],'Unimplemented mechanics remain')
    require(review.get('physical_validation')=='PENDING_NATIVE_TESTS','Do not substitute an implementation review for physics evidence')
    atomic(evidence/'implementation-review.json',review)
    return review


def execute_trial(python, folder, out, mode, commit, budget, evidence_roots=None):
    spec=read(folder/'scene.json')
    required_bytes=(spec['run_limit']+1)*3*320*176*3*1.15+2*1024**3
    require(shutil.disk_usage(out).free>required_bytes,'Insufficient space to retain all three camera streams for this trial')
    command=[python,str(folder/'run.py'),'--mode',mode,'--output',str(out/'trial'),'--commit',commit,'--execute']
    if evidence_roots:
        command+=['--evidence',str(evidence_roots)]
    execute(command,folder,out/'process.log',max(1800,spec['run_limit']//20*8),budget=budget)
    execute([python,str(folder/'validate_rollout.py') if (folder/'validate_rollout.py').is_file() else str(HERE/'evidence.py'),'--directory',str(out/'trial'),'--mode',mode,
             '--limit',str(spec['run_limit']),'--commit',commit,'--folder',str(folder)],
            folder,out/'validation.log',900)
    summary=read(out/'trial/validated-rollout.json')
    return summary


def native(python, folder, out, mode, commit, budget):
    cases=read(folder/'native-cases.json')[mode]
    estimated_steps=sum(case.get('max_steps',case.get('steps',0)+case.get('settle_steps',20)) for case in cases)*2
    execute([python,str(folder/'native_tests.py'),'--mode',mode,'--output',str(out/'native'),
             '--commit',commit],folder,out/'native-tests.log',max(1800,estimated_steps//20*8),budget=budget)
    report=read(out/'native/results.json')
    require(report.get('kind')=='NATIVE_PHYSX_TESTS' and report.get('commit')==commit,'Invalid native test provenance')
    require(report.get('failed')==0 and report.get('passed',0)>0 and report.get('reset_count',0)>=2,
            'Native suite did not pass its reset/repeat checks')
    require(report.get('mode')==mode,'Native test mode mismatch')
    require(report.get('status') == 'PASS', 'Native report did not finalize successfully')
    expected={(case['name'],repeat) for case in cases for repeat in (0,1)}
    actual={(case['name'],case['repeat']) for case in report['cases'] if case['status']=='PASS'}
    require(actual==expected and len(report['cases'])==len(expected) and report['reset_count']==len(expected),
            'Native case/repeat coverage is incomplete')
    return report


def publication_record(previous,runtime,evidence,media_id):
    """Replace offline pending fields only with the completed runtime receipts."""
    public_keys=('kind','mode','score','steps','run_limit','seed','commit','record_id','log_sha256','simulated_seconds','duration_s','camera_streams','native_failure')
    public_run=lambda value:{key:value[key] for key in public_keys if key in value}
    physics=evidence['NATIVE_PHYSICS_PASSED']['result']
    control=evidence['ROBOT_CONTROL_PASSED']['result']
    value=dict(previous)
    value.update(status='MEDIA_UPLOADED',ready=False,physics='PASS',native_physics='PASS',robot_control='PASS',
        expert_trials=[public_run(v) for v in runtime['experts']],dream=public_run(runtime['dream']),
        native_physics_episodes=physics['reset_count'],robot_control_episodes=control['reset_count'],
        physics_runs=physics['reset_count']+control['reset_count'],expert_runs=len(runtime['experts']),model_runs=1,
        media_uploads=1,media_id=media_id,media_verified=True,runtime_verified_at=utc(),
        evidence_digest=fingerprint(evidence),remaining=['Exact remote publication verification; see the runtime ready-handoff.json'])
    return value


def publish(task, folder, media, out, args, evidence, runtime):
    require(not args.no_push,'Push deliberately disabled; exact remote publication incomplete')
    # Publish from a NEW worktree. The evaluated checkout is never edited.
    cache=args.run_root/'source.git'; dest=out/'publication'
    execute(['git','worktree','add','--detach',str(dest),task['commit']],cache,out/'publication-checkout.log',120)
    target=dest/task['task_folder']
    shutil.copyfile(media/'upload/task.json',target/'task.json')
    validation=publication_record(read(target/'validation.json'),runtime,evidence,read(target/'task.json')['media'])
    atomic(target/'validation.json',validation)
    source=read(target/'source_manifest.json')
    for key in ('files','sha256'):
        if key in source:
            for name in ('task.json','validation.json'):
                if name in source[key]:
                    source[key][name]=hashlib.sha256((target/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    atomic(target/'source_manifest.json',source)
    execute(['git','add',task['task_folder']],dest,out/'stage-metadata.log',60)
    execute(['git','-c','user.name=Benchmark validation','-c','user.email=benchmark-validation@localhost',
             '-c','commit.gpgsign=false','commit','-m','Record validated rollouts and official media'],dest,out/'metadata-commit.log',60)
    head=capture(['git','rev-parse','HEAD'],dest)
    diff=capture(['git','diff','--name-only',task['commit'],head],dest).splitlines()
    require(set(diff)<={task['task_folder']+'/'+x for x in ('task.json','validation.json','source_manifest.json')},
            'Publication changed evaluated executable code')
    # Lease prevents overwriting engineering changes made during a long run.
    execute(['git','push','origin',f'HEAD:refs/heads/{task["branch"]}',
             f'--force-with-lease=refs/heads/{task["branch"]}:{task["commit"]}'],dest,out/'push.log',300)
    execute(['git','fetch','origin',task['branch']],dest,out/'verify-fetch.log',300)
    require(capture(['git','rev-parse','FETCH_HEAD'],dest)==head,'Fetched remote commit differs')
    atomic(out/'remote-verified.json',{'commit':head,'evaluated_commit':task['commit'],'metadata_only_diff':diff})
    return {'commit':head,'evaluated_commit':task['commit'],'branch':task['branch'],'verified':True}


def run_task(task,args,ledger,python,lock,budget,implementation_hash):
    slug=task['slug']; completed={}; runtime={'experts':[]}
    base={'commit':task['commit'],'stack':lock,'pipeline':implementation_hash}
    if not args.offline:
        base['gpu'] = args.gpu_identity
    checkout_result=ledger.stage(slug,'CHECKOUT',base,
        lambda out: {'path':str(checkout(task,args.run_root,out))})
    tree=Path(checkout_result['result']['path']); folder=tree/task['task_folder']
    require(capture(['git','rev-parse','HEAD'],tree)==task['commit'],'Evaluated worktree revision changed')
    require(not capture(['git','status','--porcelain'],tree),'Evaluated worktree is dirty')
    def stage(name, action):
        record=ledger.stage(slug,name,dict(base,prerequisites={k:v['key'] for k,v in completed.items()}),action)
        completed[name]=record
        return record
    stage('MECHANICS_COMPLETE',lambda out:mechanics(folder,out))
    stage('STATIC_TESTS_PASSED',lambda out:integrity(folder,out,python,budget))
    if args.offline:
        return {'slug':slug,'status':'STATIC_TESTS_PASSED','ready':False,'remaining':list(STAGES[2:])}
    stage('NATIVE_PHYSICS_PASSED',lambda out:native(python,folder,out,'physics',task['commit'],budget))
    stage('ROBOT_CONTROL_PASSED',lambda out:native(python,folder,out,'control',task['commit'],budget))
    for index in (1,2):
        row=stage(f'EXPERT_DEMO_{index}_PASSED',lambda out:execute_trial(python,folder,out,'expert',task['commit'],budget))
        runtime['experts'].append(row['result'])
    require(runtime['experts'][0]['record_id']!=runtime['experts'][1]['record_id'],'Expert demonstrations reused one trial')
    def clean_expert(out):
        fresh=out/'clean-source'
        execute(['git','clone','--no-checkout',FORK,str(fresh)],out,out/'clone.log',600,budget=budget)
        execute(['git','checkout','--detach',task['commit']],fresh,out/'checkout.log',120,budget=budget)
        require(capture(['git','rev-parse','HEAD'],fresh)==task['commit'],'Independent source mismatch')
        require(not capture(['git','status','--porcelain'],fresh),'Independent checkout is dirty')
        result=execute_trial(python,fresh/task['task_folder'],out,'expert',task['commit'],budget)
        require(result['record_id'] not in {r['record_id'] for r in runtime['experts']},'Clean expert reused a prior episode')
        return dict(result,independent_https_checkout=True)
    runtime['clean_expert']=stage('CLEAN_CHECKOUT_EXPERT_PASSED',clean_expert)['result']
    require(read(folder/'mechanics-review.json').get('novelty_review',{}).get('decision')=='CLEARED',
            'Novelty review is unresolved; preserve expert evidence and defer paid model evaluation')
    proof=args.run_root/slug/'feasibility.json'
    atomic(proof,{'commit':task['commit'],'physics':completed['NATIVE_PHYSICS_PASSED'],
                  'control':completed['ROBOT_CONTROL_PASSED'],'experts':[completed['EXPERT_DEMO_1_PASSED'],completed['EXPERT_DEMO_2_PASSED']]})
    require(hardware()['credentials_present']['dream'],'Dream credential is not configured securely')
    runtime['dream']=stage('MODEL_EVALUATED',lambda out:execute_trial(python,folder,out,'dream',task['commit'],budget,proof))['result']
    def media_action(out):
        references={'experts':runtime['experts'],'dream':runtime['dream'],'task':task,
                    'camera_coverage':completed['NATIVE_PHYSICS_PASSED']['result'].get('camera_coverage') is True}
        atomic(out/'inputs.json',references)
        execute([python,str(HERE/'media.py'),'--inputs',str(out/'inputs.json'),'--folder',str(folder),
                 '--output',str(out/'media')],folder,out/'render.log',1800,budget=budget)
        result=read(out/'media/media-validation.json')
        require(result.get('status')=='PASS','Media validation incomplete')
        return dict(result,path=str(out/'media'))
    media=Path(stage('MEDIA_RENDERED',media_action)['result']['path'])
    # Missing visual review is a gate, not a failed render or an expensive retry.
    from review_media import verify_review
    review_path=args.run_root/'reviews'/(slug+'.json')
    review=verify_review(review_path,task['commit'],media)
    def reviewed(out):
        atomic(out/'visual-review.json',review)
        return {'status':'PASS','media_path':str(media),'review_sha256':digest(review_path)}
    stage('MEDIA_VERIFIED',reviewed)
    def upload_action(out):
        require(not args.no_upload,'Upload deliberately disabled')
        require(bool(os.getenv('ROBOCURVE_TOKEN')),'RoboCurve token not configured securely')
        # Use the current official uploader on a disposable metadata copy.
        dest=out/'upload';dest.mkdir();shutil.copyfile(folder/'task.json',dest/'task.json')
        data=read(dest/'task.json')
        data['scores']=f'Dream-1 ({lock["model"]}): {runtime["dream"]["score"]}; expert demos: 1.0, 1.0'
        atomic(dest/'task.json',data)
        # Uploader uses folder basename as task tag, so give it the actual slug.
        actual=dest/slug;actual.mkdir();shutil.copyfile(dest/'task.json',actual/'task.json')
        uploader = HERE.parent/'tools/upload_media.py'
        execute([python,str(uploader),str(actual),'--video',str(media/'model.mp4'),
                 '--demo',str(media/'demo.mp4'),'--screenshot',str(media/'setup.png')],tree,out/'upload.log',900,
                env={'ROBOCURVE_TEAM':'T-06','ROBOCURVE_BOARD':'https://tasks.robocurve.org'})
        updated=read(actual/'task.json');require(re.fullmatch(r'M-[A-Z0-9]+',updated.get('media','')),'Uploader returned no valid media ID')
        shutil.copyfile(actual/'task.json',dest/'task.json')
        atomic(out/'upload-confirmation.json',{'media_id':updated['media'],'task_json_sha256':digest(dest/'task.json'),
                                              'official_uploader_sha256':digest(uploader)})
        return {'media_id':updated['media'],'path':str(out)}
    uploaded=stage('MEDIA_UPLOADED',upload_action)['result']
    remote=stage('EXACT_COMMIT_VERIFIED',lambda out:publish(task,folder,Path(uploaded['path']),out,args,completed,runtime))['result']
    observed=capture(['git','ls-remote',FORK,'refs/heads/'+task['branch']],tree).split()
    require(observed and observed[0]==remote['commit'],'Remote branch changed after the publication receipt')
    def ready_action(out):
        review=read(folder/'mechanics-review.json')
        require(review.get('novelty_review',{}).get('decision')=='CLEARED','Substantive novelty review is still unresolved')
        require(set(completed)==set(STAGES[:-1]),'Mandatory stage missing')
        result={'slug':slug,'ready':True,'status':'READY_FOR_PR','title':read(folder/'task.json')['title'],
                'branch':task['branch'],'branch_url':task['branch_url'],'commit':remote['commit'],
                'expert_scores':[1.0,1.0],'dream_score':runtime['dream']['score'],'media_id':uploaded['media_id'],
                'evidence':{k:{'key':v['key'],'receipt':v['receipt']} for k,v in completed.items()}}
        atomic(out/'ready.json',result)
        return result
    return stage('READY_FOR_PR',ready_action)['result']



def verify_paid_candidates(tasks, manifest, manifest_path):
    """Reject known quality holds before hardware probes, setup or paid workloads."""
    from offline_gate import verify
    root = (Path(manifest_path).resolve().parent / manifest.get('offline_evidence_root', '.')).resolve()
    for task in tasks:
        require(task.get('offline_state') == 'OFFLINE READY',
                'Candidate is not offline qualified: ' + task['slug'])
        verify(task, root)


def smoke_validation_command(python, trial, adapter_commit):
    # Official apple/bowl smoke belongs to the coordinator, not a task package.
    return [python, str(HERE/'evidence.py'), '--directory', str(trial),
            '--mode', 'smoke', '--limit', '600', '--commit', adapter_commit]


def main(argv=None):
    args=cli(argv);args.run_root=args.run_root.resolve()
    try:
        manifest=read(args.manifest);tasks=selected(manifest,args.task);lock=read(HERE/'stack-lock.json')
        if args.dry_run:
            print(json.dumps(plan(tasks,args.run_root,lock),indent=2));return 0
        if args.preflight:
            result=hardware();result['stack_lock']=lock
            result['budget_receipt_present']=args.budget_file.is_file()
            print(json.dumps(result,indent=2));return 3 if result['problems'] else 0
        if not args.offline:
            verify_paid_candidates(tasks, manifest, args.manifest)
        implementation_hash=fingerprint({p.name:digest(p) for p in HERE.glob('*.py')})
        with exclusive(args.run_root/'pipeline.lock'):
            ledger=Ledger(args.run_root,resume=args.resume,retry_reason=args.retry_failed)
            budget=None;python=sys.executable
            if not args.offline:
                preflight=hardware();atomic(args.run_root/'preflight.json',preflight)
                require(not preflight['problems'],'; '.join(preflight['problems']))
                from session_budget import session
                budget=session(args.budget_file,args.deadline_unix)
                require(preflight['selected_gpu']['uuid']==budget.receipt['gpu_uuid'],'Budget receipt names a different GPU')
                os.environ['CUDA_VISIBLE_DEVICES']=preflight['selected_gpu']['uuid']
                if args.launchable_root:
                    installed = launchable_runtime(args.launchable_root, lock)
                    def reuse(out):
                        atomic(out/'installed-runtime.json', installed)
                        return installed
                    stack = ledger.stage('_environment', 'REUSE_LAUNCHABLE',
                                         {'stack': lock, 'runtime': installed, 'pipeline': implementation_hash}, reuse)
                else:
                    require(preflight['driver_status'] != 'fixed_driver_smoke_required',
                            'Fixed driver validation requires the installed vendor stack via --launchable-root')
                    stack = ledger.stage('_environment', 'BOOTSTRAP', {'stack': lock, 'pipeline': implementation_hash},
                                         lambda out: bootstrap(args.run_root/'stack', lock, out, budget))
                    verify_runtime(stack['result'], args.run_root/'stack', lock)
                python = stack['result']['python']
                def smoke(out):
                    atomic(out/'hardware.json', preflight)
                    trial=out/'trial';trial.mkdir()
                    execute([str(Path(python).parent/'inspect-robots'),'run','--embodiment','yam_arena',
                             '--policy','yam_scripted','-E','scene=station','-E','object_jitter=0','-E','control_hz=20',
                             '-E','cam_width=320','-E','cam_height=176','--instruction','put apple into the bowl',
                             '--scorer','success_at_end','--max-steps','600','--store-frames','--seed','0',
                             '--environment-revision',lock['adapter']['commit'],'--log-dir',str(trial)],
                            REPO,out/'smoke.log',1800,budget=budget)
                    execute(smoke_validation_command(python, trial, lock['adapter']['commit']),
                            REPO,out/'smoke-validation.log',600)
                    return read(trial/'validated-rollout.json')
                gpu_identity = {key: preflight['selected_gpu'][key] for key in ('name', 'uuid', 'driver')}
                args.gpu_identity = gpu_identity
                smoke_record = ledger.stage('_environment', 'OFFICIAL_SMOKE',
                    {'stack': lock, 'pipeline': implementation_hash, 'gpu': gpu_identity,
                     'bootstrap': stack['key']}, smoke)
                implementation_hash = fingerprint({'pipeline': implementation_hash, 'gpu': gpu_identity,
                                                   'official_smoke': smoke_record['key']})
            report={'created_at':utc(),'kind':'OFFLINE_ENGINEERING_CHECKS' if args.offline else 'GPU_PIPELINE',
                    'tasks':[],'ready':[],'complete':False}
            for task in tasks:
                try:
                    task_budget=budget.task(task.get('maximum_qualification_seconds',args.task_seconds)) if budget else None
                    row=run_task(task,args,ledger,python,lock,task_budget,implementation_hash)
                except (Incomplete,OSError,ValueError,KeyError) as exc:
                    row={'slug':task['slug'],'ready':False,'status':'INCOMPLETE','error':str(exc)}
                report['tasks'].append(row)
                if row.get('ready'):report['ready'].append(row)
                if budget:
                    try:report['compute']=budget.check()
                    except Incomplete as exc:
                        report['stop_reason']=str(exc);atomic(args.run_root/'report.json',report);break
                atomic(args.run_root/'report.json',report)
                print(f'{task["slug"]}: {row["status"]}',flush=True)
            report['complete']=len(report['ready'])==len(tasks)
            report['offline_checks_passed']=args.offline and all(t['status']=='STATIC_TESTS_PASSED' for t in report['tasks'])
            atomic(args.run_root/'report.json',report)
            atomic(args.run_root/'ready-handoff.json',{'tasks':report['ready'],'count':len(report['ready']),
                                                      'all_requested_ready':report['complete']})
            print(f'Report: {args.run_root/"report.json"}')
            return 0 if report['complete'] or report['offline_checks_passed'] else 2
    except (Incomplete,OSError,ValueError,KeyError) as exc:
        print(f'BLOCKED: {exc}',file=sys.stderr);return 3


if __name__=='__main__':
    raise SystemExit(main())
