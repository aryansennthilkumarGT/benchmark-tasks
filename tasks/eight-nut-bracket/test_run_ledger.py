"""Regression checks for live-balance timing using explicitly synthetic fixtures."""
import tempfile
from pathlib import Path
import unittest
from run_ledger import Budget, Incomplete, atomic


class BudgetTests(unittest.TestCase):
    def test_live_balance_and_lifetime_cap_use_their_own_timestamps(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'synthetic-budget.json'
            atomic(path, {'hourly_usd': 2, 'balance_usd': 35, 'spent_before_start_usd': 0,
                          'instance_started_unix': 1000, 'balance_observed_unix': 37000,
                          'instance_id': 'test-instance', 'gpu_uuid': 'test-gpu',
                          'provider_evidence': 'synthetic unit-test fixture'})
            budget = Budget(path, clock=lambda: 40600)
            self.assertEqual(budget.check(3600)['projected_balance_usd'], 31)
            with self.assertRaises(Incomplete):
                budget.check(7200)

    def test_legacy_receipt_keeps_the_original_balance_epoch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'synthetic-budget.json'
            atomic(path, {'hourly_usd': 2, 'balance_usd': 200, 'spent_before_start_usd': 0,
                          'instance_started_unix': 1000, 'instance_id': 'test-instance',
                          'gpu_uuid': 'test-gpu', 'provider_evidence': 'synthetic unit-test fixture'})
            budget = Budget(path, clock=lambda: 1000+84*3600)
            self.assertEqual(budget.check()['estimated_instance_charge_usd'], 168)
            with self.assertRaises(Incomplete):
                budget.check(3601)
