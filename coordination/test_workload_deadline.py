import unittest
from workload_deadline import owned_groups
class DeadlineOwnershipTests(unittest.TestCase):
    def test_missing_pid_marker_still_discovers_exact_producer_and_child(self):
        table=[(20,1,20,['bash','/x/producer.sh']),(21,20,21,['python','simulation.py'])]
        self.assertEqual(owned_groups('/x',table,99),({20},{20,21}))
    def test_parent_shell_text_is_not_producer_argv(self):
        self.assertEqual(owned_groups('/x',[(20,1,20,['bash','-c','bash /x/producer.sh'])],99),(set(),set()))
    def test_unrelated_process_is_not_owned_by_stale_pid_hint(self):
        self.assertEqual(owned_groups('/x',[(20,1,20,['bash','/other/producer.sh'])],99),(set(),set()))
    def test_unrelated_argument_is_not_script_execution(self):
        self.assertEqual(owned_groups('/x',[(20,1,20,['python','viewer.py','--input','/x/producer.sh'])],99),(set(),set()))
    def test_agent_and_system_groups_are_rejected(self):
        for group in [1,99]:
            with self.assertRaises(RuntimeError):owned_groups('/x',[(20,1,group,['bash','/x/producer.sh'])],99)
if __name__=='__main__':unittest.main()
