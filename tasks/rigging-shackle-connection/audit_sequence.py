"""Run the real controller against ideal joint tracking and assumed jaw contact.

This catches IK branch failures, timeouts and action-limit overruns. Synthetic
contact apertures are fixtures, not evidence that a physical grasp succeeds.
"""
import json
from pathlib import Path
import numpy as np
from yam_arena.constants import READY
from feedback import Controller,ControlFailure,rotate


def audit(folder):
    spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    controller=Controller(plan,spec);q=np.tile(np.r_[READY,1.],2)
    record=dict(kind='OFFLINE_IDEAL_JOINT_TRACKING_WITH_SYNTHETIC_CONTACT_APERTURES',
                physics_executed=False,grasps_validated=False,passed=False)
    try:
        for step in range(spec['run_limit']):
            command=controller.step(q,{'time':step/spec['control_hz']})
            q=command.copy()
            for side,p in controller.targets.items():
                if p['opening']>=.3:continue
                if p['contact_body']=='shackle':width=.016
                else:
                    jaw=rotate(p['target']['quat'],[1,0,0]);bq=p['nominal_bodies']['pin']['quat']
                    width=sum(abs(float(np.dot(jaw,rotate(bq,axis))))*length
                        for axis,length in [([1,0,0],.024),([0,1,0],.012)])
                i=6 if side=='left' else 13
                q[i]=max(q[i],width/.0939)
            if controller.done:
                record.update(passed=True,actions=step+1,simulated_seconds=(step+1)/spec['control_hz']);break
        else:record['error']='Controller did not complete within action limit'
    except ControlFailure as exc:record['error']=str(exc)
    record.update(last_phase=controller.index,phase_count=len(plan['phases']),events=controller.events)
    print(json.dumps(record,indent=2));return 0 if record['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
