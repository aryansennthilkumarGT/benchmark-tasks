"""Source-equivalence and fail-closed guards; no synthetic result is a rollout."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('proof_template',Path(__file__).parent/'templates/feasibility_v2.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class ProofGuards(unittest.TestCase):
    def test_gate_change_does_not_change_expert_launcher_fingerprint(self):
        a=b'def feasible(): return 1\ndef command(): return 7\n'
        b=b'def feasible(): return 2\ndef command(): return 7\n'
        c=b'def feasible(): return 2\ndef command(): return 8\n'
        key='run.py#excluding_feasible'
        self.assertEqual(module.component_hash(key,a),module.component_hash(key,b))
        self.assertNotEqual(module.component_hash(key,a),module.component_hash(key,c))

    def test_controller_metadata_is_separate_from_actual_phase_parameters(self):
        key='controller.json#phases'
        a=json.dumps(dict(status='draft',phases=[dict(speed=1)])).encode()
        b=json.dumps(dict(status='verified',phases=[dict(speed=1)])).encode()
        c=json.dumps(dict(status='verified',phases=[dict(speed=2)])).encode()
        self.assertEqual(module.component_hash(key,a),module.component_hash(key,b))
        self.assertNotEqual(module.component_hash(key,a),module.component_hash(key,c))

    def test_changed_source_component_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'scoring.py';p.write_text('pass\n')
            component=dict(files={'scoring.py':module.sha(p)})
            module.verify_components(root,component)
            p.write_text('changed\n')
            with self.assertRaisesRegex(ValueError,'differs'):module.verify_components(root,component)

    def test_legacy_feedback_proof_is_not_an_action_only_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'feasibility.json';p.write_text(json.dumps(dict(commit='sha')))
            with self.assertRaisesRegex(ValueError,'format'):module.check(p,'sha',root)


if __name__=='__main__':unittest.main()
