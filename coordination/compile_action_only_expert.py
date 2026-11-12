"""Author fixed robot commands from a genuine development record.

This is source preparation, never successful demonstration evidence. Two new
whole cold physical episodes must establish feasibility of the authored program.
"""
import argparse,hashlib,json,math,subprocess
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compile_program(folder,trial):
    proof=json.loads((trial/'validated-rollout.json').read_text())
    assert proof['kind']=='REAL_INSPECT_ROLLOUT' and proof['mode']=='expert' and proof['score']==1
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=folder,text=True).strip()==proof['commit']
    log=Path(proof['log']);assert sha(log)==proof['log_sha256']
    streams=list((trial/'actions').glob('*/*.jsonl'));assert len(streams)==1
    rows=[json.loads(s) for s in streams[0].read_text().splitlines()]
    assert rows[0]['action_dim']==14 and len(rows)-1==proof['steps']
    for i,row in enumerate(rows[1:]):
        assert row['t']==i and len(row['action'])==14
        assert all(isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v) for v in row['action'])
    events=[json.loads(s) for s in (trial/'expert-events.jsonl').read_text().splitlines()]
    checkpoints=[{'source_phase':e['phase'],'label':e['label'],'post_action_frame_index':round(e['time']*20)+1} for e in events if e['event']=='MEASURED_PHASE_COMPLETE']
    data={'kind':'FIXED_ROBOT_JOINT_ACTION_TRAJECTORY','control_hz':20,'action_dim':14,'source_record_id':proof['record_id'],'source_runtime_commit':proof['commit'],'source_log_sha256':proof['log_sha256'],'source_action_stream_sha256':sha(streams[0]),'provenance':'Authored offline from a real successful feedback development episode. New complete cold fixed-action executions are required; this compilation gives no demonstration credit. Checkpoints are authored indices, not measured phase-completion events.','terminal_hold_actions':40,'actions':[r['action'] for r in rows[1:]],'checkpoints':checkpoints}
    (folder/'expert_joint_trajectory.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    (folder/'expert.py').write_bytes((Path(__file__).parent/'templates/action_only_expert.py').read_bytes())
    f=folder/'source_manifest.json';m=json.loads(f.read_text());m['files']['expert_joint_trajectory.json']='';m['files']={k:hashlib.sha256((folder/k).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for k in m['files']};f.write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({'kind':'AUTHORED_FIXED_ACTION_PROGRAM_NOT_VALIDATED_DEMONSTRATION','source_record_id':proof['record_id'],'actions':len(data['actions']),'cold_validation_required':True}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True);p.add_argument('--trial',type=Path,required=True);a=p.parse_args();compile_program(a.folder,a.trial)
