"""Synthetic assignment/trajectory counterexamples, never physical-run evidence."""
import copy,unittest
from test_scoring import S,SPEC,target_frame,finish

SLOTS=[g for g in SPEC['goals'] if 'candidate_bodies' in g]
POOL=SLOTS[0]['candidate_bodies']
def permute(frame):
    result=copy.deepcopy(frame)
    for name,other in zip(POOL,POOL[1:]+POOL[:1]):result['bodies'][name]=copy.deepcopy(frame['bodies'][other])
    return result
class PermutedScorer(S.Scorer):
    def update(self,frame):return super().update(permute(frame))

class InterchangeabilityTests(unittest.TestCase):
    def test_valid_permuted_parts_reach_semantic_goal(self):
        result,_=finish(PermutedScorer(copy.deepcopy(SPEC)))
        self.assertTrue(result.success);self.assertEqual(result.score,1.)
    def test_one_body_cannot_earn_two_slot_credits(self):
        spec=copy.deepcopy(SPEC);slots=[g for g in spec['goals'] if 'candidate_bodies' in g];a,b=slots[:2]
        b['all']=[dict(p,body=b['template_body']) if p.get('body')==a['template_body'] else copy.deepcopy(p) for p in a['all']]
        sc=S.Scorer(spec);sc.turns={t['body']:3.5 for t in spec.get('threads',[])}
        active=sc.completed_goals(target_frame())
        self.assertEqual(len(active&{a['name'],b['name']}),1)
        self.assertNotIn(spec['goals'][-1]['name'],active)
    def test_permutation_does_not_bypass_axis_requirement(self):
        sc=PermutedScorer(copy.deepcopy(SPEC));result,_=finish(sc);self.assertTrue(result.success)
        frame=copy.deepcopy(sc.last_frame);name=POOL[0]
        import numpy as np
        local=next(p.get('local_axis',[0,0,1]) for p in SLOTS[0]['all'] if p['kind']=='axis')
        axis=np.cross(local,[0,0,1] if abs(local[2])<.9 else [1,0,0]);axis=axis/np.linalg.norm(axis)
        frame['bodies'][name]['quat']=list(S.multiply(frame['bodies'][name]['quat'],[*axis,0]))
        self.assertLess(len(sc.completed_goals(frame)),len(SPEC['goals']))
    def test_changing_stud_resets_accumulated_turns(self):
        if not SPEC.get('threads'):self.skipTest('No threaded components')
        sc=S.Scorer(copy.deepcopy(SPEC));result,frame=finish(sc);self.assertTrue(result.success)
        thread=SPEC['threads'][0];name=thread['body'];ref=frame['bodies'][thread['reference']]
        local,_=S.relative(frame['bodies'][name],ref);local=list(local);local[:2]=thread['xy_options'][1]
        frame['bodies'][name]['pos']=list(S.add(ref['pos'],S.rotate(ref['quat'],local)))
        frame['time']=sc.last_time+.05;sc.update(frame)
        self.assertEqual(sc.turns[name],0.)

if __name__=='__main__':unittest.main()
