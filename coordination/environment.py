"""Inspect or build the officially pinned Arena stack without changing drivers."""
from __future__ import annotations
import importlib.metadata as metadata
from importlib.util import find_spec
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from engine import Incomplete, atomic, execute, read, digest


def capture(args, cwd=None):
    proc = subprocess.run([str(a) for a in args], cwd=cwd, text=True, capture_output=True,
                          timeout=60, stdin=subprocess.DEVNULL)
    if proc.returncode:
        raise Incomplete(f'{args[0]} failed ({proc.returncode}): {proc.stderr[-1200:]}')
    return proc.stdout.strip()


def hardware():
    result = {'platform': platform.platform(), 'machine': platform.machine(),
              'python': platform.python_version(), 'gpu': [], 'problems': [], 'warnings': []}
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        result['problems'].append('Native stack requires Linux x86_64')
    if shutil.which('nvidia-smi'):
        try:
            rows = capture(['nvidia-smi', '--query-gpu=name,uuid,driver_version,memory.total,memory.free,utilization.gpu',
                            '--format=csv,noheader,nounits'])
            result['gpu'] = [dict(zip(('name','uuid','driver','memory_mib','free_mib','utilization'),
                                     [x.strip() for x in line.split(',')], strict=True)) for line in rows.splitlines()]
            supported = [g for g in result['gpu'] if any(s in g['name'] for s in ('L40S', 'RTX 4090', 'RTX 5090'))]
            if not supported:
                result['problems'].append('No verified ray-tracing GPU profile (L40S / RTX 4090 / RTX 5090)')
            elif int(supported[0]['free_mib']) < 16000:
                result['problems'].append('Less than 16 GiB GPU memory free')
            result['selected_gpu'] = supported[0] if supported else None
            if supported:
                selected = supported[0]
                driver = tuple(int(v) for v in selected['driver'].split('.'))
                result['driver_status'] = 'meets_recommendation'
                if driver < (580, 95, 5):
                    result['driver_status'] = 'below_recommendation_unvalidated'
                    result['warnings'].append('Driver is below the Isaac Lab 3.0 recommendation 580.95.05')
                    if 'L40S' in selected['name'] and selected['driver'] == '565.57.01':
                        result['driver_status'] = 'fixed_driver_smoke_required'
                    else:
                        result['problems'].append('Driver is outside the configured compatibility-test profile')
                result['driver_reference']='https://isaac-sim.github.io/IsaacLab/v3.0.0-EA/source/setup/installation/index.html'
                result['isaacsim_61_tested_driver']='595.58.03'
        except (Incomplete, ValueError) as exc:
            result['problems'].append(str(exc))
    else:
        result['problems'].append('nvidia-smi unavailable')
    if sys.platform=='linux':
        fields={line.split(':',1)[0]:int(line.split()[1])*1024 for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemTotal:','MemAvailable:'))}
        result['ram']=fields
        if fields.get('MemTotal',0)<31*1024**3:result['problems'].append('Isaac Sim minimum is 32 GB system RAM')
        if fields.get('MemAvailable',0)<24*1024**3:result['problems'].append('Need at least 24 GiB available system RAM')
    result['credentials_present'] = {
        'dream': bool(os.getenv('DREAM_API_KEY')) or (Path.home()/'.dreamlabs/credentials').is_file(),
        'robocurve': bool(os.getenv('ROBOCURVE_TOKEN')),
        'github_cli': bool(shutil.which('gh')),
    }
    return result


def package_versions():
    names = ('isaacsim','isaaclab','isaaclab-arena','yam-arena','inspect-robots','inspect-robots-yam',
             'inspect-robots-dream','numpy')
    values = {}
    for name in names:
        try:
            values[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            values[name] = None
    return values


def clone_pinned(item, target, evidence, budget):
    target = Path(target)
    if not target.exists():
        command = ['git','clone']
        if item.get('branch'):
            command += ['--branch',item['branch']]
        execute(command+[item['url'], str(target)], target.parent, evidence/(target.name+'-clone.log'),
                1800, budget=budget)
    if capture(['git','rev-parse','HEAD'], target) != item['commit']:
        if capture(['git','status','--porcelain'], target):
            raise Incomplete(f'Dependency checkout has local changes: {target}')
        execute(['git','fetch','origin',item['commit']], target, evidence/(target.name+'-fetch.log'),600,budget=budget)
        if item.get('branch'):
            # This is the runner-owned dependency clone. The vendor setup checks
            # the branch name, so pin that LOCAL branch without changing a remote.
            execute(['git','checkout','-B',item['branch'],item['commit']],target,evidence/(target.name+'-checkout.log'),60)
        else:
            execute(['git','checkout','--detach',item['commit']], target,evidence/(target.name+'-checkout.log'),60)
    if capture(['git','rev-parse','HEAD'],target) != item['commit']:
        raise Incomplete('Dependency revision verification failed')


def bootstrap(root, lock, evidence, budget):
    """Use the official adapter setup in an isolated project tree, no desktop option.

    The official launchable already accepts its NVIDIA EULA during deployment. Bare
    machines must have their operator accept it via the vendor's normal setup first.
    """
    if sys.platform != 'linux':
        raise Incomplete('Bootstrap requires the official Linux GPU environment')
    if not (os.getenv('ACCEPT_EULA') == 'Y' or os.getenv('OMNI_KIT_ACCEPT_EULA') == 'YES'):
        raise Incomplete('NVIDIA EULA acceptance is not configured; use the official authorized Brev launchable')
    if not shutil.which('uv') or not shutil.which('git'):
        raise Incomplete('Official Brev setup must provide uv and git')
    root = Path(root).resolve(); root.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(root).free < 250 * 1024**3:
        raise Incomplete('Need 250 GiB free for the isolated stack, three raw camera streams, repeated trials and retained evidence')
    adapter, arena = root/'yam-isaac-lab-arena', root/'IsaacLab-Arena'
    clone_pinned(lock['adapter'], adapter, evidence, budget)
    clone_pinned(lock['arena'], arena, evidence, budget)
    env = {'ARENA_DIR': str(arena), 'DREAM_SPEC': 'git+'+lock['dream']['url']+'@'+lock['dream']['commit'],
           'UV_CACHE_DIR': str(root/'cache'), 'UV_TOOL_DIR': str(root/'tools'),
           'UV_PYTHON_INSTALL_DIR':str(root/'python'),
           'UV_TOOL_BIN_DIR': str(root/'bin'), 'PATH': str(root/'bin')+os.pathsep+os.environ['PATH']}
    execute(['bash', str(adapter/'setup.sh')], root, evidence/'official-setup.log', 7200, env, budget)
    # Same narrowly scoped asset-root correction as launchable/setup.sh lines 118-120.
    nucleus = arena/'isaaclab_arena/assets/nucleus.py'
    source = nucleus.read_text()
    old = 'ARENA_NUCLEUS_DIR: str = ISAACLAB_NUCLEUS_DIR.replace("omniverse-content-production", "omniverse-content-staging")'
    new = 'ARENA_NUCLEUS_DIR: str = ISAACLAB_NUCLEUS_DIR'
    if old not in source and new not in source:
        raise Incomplete('Official asset-root patch no longer matches the pinned source')
    nucleus.write_text(source.replace(old,new))
    python = arena/'.venv/bin/python'
    execute(['uv','pip','install','--python',str(python),'--override',str(adapter/'overrides.txt'),
             'inspect-robots @ git+'+lock['inspect']['url']+'@'+lock['inspect']['commit'],
             'inspect-robots-yam=='+lock['inspect_robots_yam']],
            root,evidence/'inspect-pin.log',1800,env,budget)
    execute([str(python),str(Path(__file__).resolve()),'--versions'],root,evidence/'versions.json',60)
    versions = read(evidence/'versions.json')
    if versions['isaacsim'] != lock['isaacsim'] or versions['numpy'] != lock['numpy']:
        raise Incomplete('Installed simulator/numpy differ from official lock')
    if versions['inspect-robots'] != lock['inspect']['version']:
        raise Incomplete('Inspect Robots version differs from lock')
    if versions['inspect-robots-yam'] != lock['inspect_robots_yam']:
        raise Incomplete('Inspect Robots YAM version differs from lock')
    execute([str(python.parent/'inspect-robots'),'list','embodiments'],root,evidence/'embodiments.log',60)
    execute([str(python.parent/'inspect-robots'),'list','policies'],root,evidence/'policies.log',60)
    if 'yam_arena' not in (evidence/'embodiments.log').read_text() or 'dream' not in (evidence/'policies.log').read_text():
        raise Incomplete('Official embodiment or Dream policy not registered')
    freeze = capture(['uv','pip','freeze','--python',str(python)])
    (evidence/'installed-lock.txt').write_text(freeze+'\n')
    return {'python': str(python), 'versions': versions, 'arena_lock_sha256': digest(arena/'uv.lock'),
            'adapter_commit': lock['adapter']['commit'], 'asset_root_patch': 'official production bucket'}


def launchable_runtime(root, lock, require_dream=True):
    """Verify the active Launchable venv without changing the installed stack."""
    root = Path(root).resolve()
    arena = root/'IsaacLab-Arena'
    lab = arena/'submodules/IsaacLab'
    inspect = root/'inspect-robots'
    python = arena/'.venv/bin/python'
    if not python.is_file():
        raise Incomplete('Existing Launchable Arena venv not found')
    checkouts = {'adapter': (root/'yam-isaac-lab-arena', lock['adapter']['commit']),
                 'arena': (arena, lock['arena']['commit']),
                 'isaaclab': (lab, lock['isaaclab_commit']),
                 'inspect': (inspect, lock['inspect']['commit'])}
    for name, (checkout, commit) in checkouts.items():
        if capture(['git', 'rev-parse', 'HEAD'], checkout) != commit:
            raise Incomplete('Launchable source revision differs from lock: ' + name)
        changes = capture(['git', 'status', '--porcelain', '--untracked-files=no'], checkout)
        if changes and (name != 'arena' or changes != 'M isaaclab_arena/assets/nucleus.py'):
            raise Incomplete('Launchable has modified tracked sources: ' + name)
    origins = json.loads(capture([python, __file__, '--origins']))
    expected = {'isaaclab': lab/'source/isaaclab/isaaclab/__init__.py',
                'isaaclab_arena': arena/'isaaclab_arena/__init__.py',
                'yam_arena': root/'yam-isaac-lab-arena/yam_arena/__init__.py'}
    for name, source in expected.items():
        if Path(origins[name]).resolve() != source.resolve():
            raise Incomplete('Unexpected active package source: ' + name)
    source = inspect/'src/inspect_robots'
    installed = Path(origins['inspect_robots']).parent
    for path in source.rglob('*.py'):
        counterpart = installed/path.relative_to(source)
        if not counterpart.is_file() or digest(counterpart) != digest(path):
            raise Incomplete('Installed Inspect Robots Python source differs: ' + str(path.relative_to(source)))
    if require_dream and origins['dream_commit'] != lock['dream']['commit']:
        raise Incomplete('Installed Dream plugin revision differs from lock')
    versions = json.loads(capture([python, __file__, '--versions']))
    expected_versions = {'isaacsim': lock['isaacsim'], 'numpy': lock['numpy'],
                         'inspect-robots': lock['inspect']['version'],
                         'inspect-robots-yam': lock['inspect_robots_yam']}
    if any(versions[name] != version for name, version in expected_versions.items()):
        raise Incomplete('Launchable package versions differ from lock')
    runtime = {'python': str(python), 'versions': versions, 'origins': origins,
               'arena_lock_sha256': digest(arena/'uv.lock'), 'launchable_root': str(root)}
    verify_runtime(runtime, root, lock)
    return runtime


def verify_runtime(result,root,lock):
    """A cached receipt does not authorize silently changed installed dependencies."""
    root=Path(root)
    for key,folder in [('adapter','yam-isaac-lab-arena'),('arena','IsaacLab-Arena')]:
        if capture(['git','rev-parse','HEAD'],root/folder)!=lock[key]['commit']:
            raise Incomplete('Installed dependency revision changed: '+key)
    if digest(root/'IsaacLab-Arena/uv.lock')!=result['arena_lock_sha256']:
        raise Incomplete('Installed Arena lock changed')
    versions=json.loads(capture([result['python'],str(Path(__file__).resolve()),'--versions']))
    if versions!=result['versions']:raise Incomplete('Installed package versions changed after bootstrap')
    nucleus=(root/'IsaacLab-Arena/isaaclab_arena/assets/nucleus.py').read_text()
    if 'ARENA_NUCLEUS_DIR: str = ISAACLAB_NUCLEUS_DIR\n' not in nucleus:
        raise Incomplete('Official production asset-root correction changed')
    return versions


if __name__ == '__main__':
    if '--origins' in sys.argv:
        origins = {name: find_spec(name).origin for name in
                   ('isaaclab', 'isaaclab_arena', 'yam_arena', 'inspect_robots')}
        try:direct_url = metadata.distribution('inspect-robots-dream').read_text('direct_url.json')
        except metadata.PackageNotFoundError:direct_url=None
        origins['dream_commit'] = json.loads(direct_url or '{}').get('vcs_info', {}).get('commit_id')
        print(json.dumps(origins))
    else:
        print(json.dumps(package_versions() if '--versions' in sys.argv else hardware(), indent=2))
