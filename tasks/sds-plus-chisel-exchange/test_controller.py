"""Executable policy contracts and meaningful bounded/stale-state failure cases."""
import copy,json
from pathlib import Path
import numpy as np,pytest
from yam_arena import ik
from yam_arena.constants import READY
from feedback import Controller,ControlFailure
from plan_controller import make_plan,scene_digest
from test_scoring import initial,SPEC
HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/'controller.json').read_text())
def configuration():return np.tile(np.r_[READY,1.],2)
def test_plan_is_pure_reproducible_and_binds_actual_scene():
 before=json.dumps(SPEC,sort_keys=True);a=make_plan(SPEC);assert a==PLAN and json.dumps(SPEC,sort_keys=True)==before
 bad=copy.deepcopy(PLAN);bad['scene_content_sha256']='0'*64
 with pytest.raises(ControlFailure,match='Stale'):Controller(bad,SPEC)
def test_first_action_is_finite_rate_bounded_and_stale_observations_stop():
 c=Controller(PLAN,SPEC);q=configuration();f=initial();out=c.step(q,f);assert out.shape==(14,) and np.isfinite(out).all()
 for i in (0,7):assert np.max(np.abs(out[i:i+6]-q[i:i+6]))<=.020001 and np.all(out[i:i+6]>ik.LOWER) and np.all(out[i:i+6]<ik.UPPER)
 with pytest.raises(ControlFailure,match='Stale'):c.step(q,f)
def test_wide_obstruction_cannot_trigger_large_blind_recovery_opening():
 c=Controller(PLAN,SPEC);i=next(i for i,p in enumerate(c.phases) if p['label']=='Grip used chisel');p=copy.deepcopy(c.phases[i]);q=configuration();c.index=i;p=c.bind(p,initial(),q);q[13]=.8
 with pytest.raises(ControlFailure,match='wide obstruction'):c.retry(p,initial(),q)
def test_native_prefixes_refer_to_real_phases_and_bounded_action_limits():
 d=json.loads((HERE/'native-cases.json').read_text());assert len(d['physics'])==7 and len(d['control'])==3
 for case in d['control']:assert PLAN['phases'][case['through_phase']]['label']==case['through_label'] and case['max_steps']<=SPEC['run_limit']
 for mode in ['physics','control']:
  for case in d[mode]:assert dict(kind='penetration',max=SPEC['penetration_limit']) in case['continuous_assertions'] and dict(kind='valid') in case['continuous_assertions']


def test_rolled_replacement_grasp_stays_centered_on_actual_stem():
 c=Controller(PLAN,SPEC);p=next(p for p in PLAN['phases'] if p['label']=='Grip replacement chisel');f=initial();bound=c.bind(p,f,configuration());body=f['bodies']['replacement_flat_chisel'];expected=np.asarray(body['pos'])+np.array([p['offset'][0],0.,p['offset'][2]])
 assert np.allclose(bound['target']['pos'],expected,atol=1e-12)
