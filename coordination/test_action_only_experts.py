"""Synthetic guard inputs only; these tests do not simulate native physics."""
import tempfile
from pathlib import Path
import unittest
import copy
from verify_action_only_experts import completion_tick, verify_actions, policy_audit


class ActionOnlyGuards(unittest.TestCase):
    def setUp(self):
        self.case=dict(name='probe',through_phase=0,through_label='Seat',max_steps=21,assertions=[])
        self.phases=[dict(label='Seat')]
        self.program=dict(control_hz=20,action_dim=14,terminal_hold_actions=2,
            actions=[[0.]*14],checkpoints=[dict(source_phase=0,label='Seat',post_action_frame_index=21)])
        self.events=[dict(event='SCRIPTED_ACTION_CHECKPOINT',source_phase=0,label='Seat',
                         post_action_frame_index=21,action_index=20,state_time=1.)]

    def test_actual_authored_checkpoint_checks_post_action_frame(self):
        self.assertEqual(completion_tick(self.case,self.phases,self.events,self.program),21)

    def test_measured_event_is_not_an_authored_checkpoint(self):
        self.events[0]['event']='MEASURED_PHASE_COMPLETE'
        with self.assertRaisesRegex(ValueError,'ambiguous'):
            completion_tick(self.case,self.phases,self.events,self.program)

    def test_off_timeline_checkpoint_and_fixture_case_fail_closed(self):
        self.events[0]['state_time']=1.02
        with self.assertRaisesRegex(ValueError,'timeline'):
            completion_tick(self.case,self.phases,self.events,self.program)
        self.case['initialize_joints']=[]
        with self.assertRaisesRegex(ValueError,'fixture'):
            completion_tick(self.case,self.phases,self.events,self.program)

    def test_actual_actions_and_fixed_hold_must_match_exactly(self):
        actions=[dict(t=i,action=[0.]*14) for i in range(3)]
        verify_actions(actions,self.program)
        actions[1]['action'][0]=.001
        with self.assertRaisesRegex(ValueError,'differs'):verify_actions(actions,self.program)
        with self.assertRaisesRegex(ValueError,'exceed'):
            verify_actions([dict(t=i,action=[0.]*14) for i in range(4)],self.program)

    def test_hidden_state_controller_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'expert.py';p.write_text('def act(): return runtime.LATEST\n')
            with self.assertRaisesRegex(ValueError,'privileged'):policy_audit(p)
            p.write_text('from .feedback import Controller\n')
            with self.assertRaisesRegex(ValueError,'privileged'):policy_audit(p)

    def test_official_guarded_actions_are_exact_and_modified_limits_rejected(self):
        import numpy as np
        from inspect_robots.guard import ClampGuard, DeltaLimitGuard
        from inspect_robots_yam.config import action_box
        from yam_arena import ik
        space=action_box(np.tile(np.r_[ik.LOWER,0.],2),np.tile(np.r_[ik.UPPER,1.],2))
        guards=[ClampGuard(space),DeltaLimitGuard(space)]
        recorded=dict(type='inspect_robots.guard.GuardChain',names=['clamp','delta-limit'],
            guards=[dict(type=type(g).__module__+'.'+type(g).__name__,config=g.config()) for g in guards])
        program=copy.deepcopy(self.program)
        program['actions']=[[0.]*14,[0.]*6+[1.]+[0.]*7]
        executed=[dict(t=0,action=[0.]*14),dict(t=1,action=[0.]*6+[.05]+[0.]*7)]
        verify_actions(executed,program,recorded)
        executed[1]['action'][6]=.051
        with self.assertRaisesRegex(ValueError,'differs'):verify_actions(executed,program,recorded)
        recorded['guards'][1]['config']['max_delta'][6]=1.
        with self.assertRaisesRegex(ValueError,'safety chain'):verify_actions(executed,program,recorded)


if __name__=='__main__':unittest.main()
