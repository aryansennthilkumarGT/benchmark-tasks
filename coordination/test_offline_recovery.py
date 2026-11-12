"""Real local archive/test execution; no physics or network fixtures."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

from engine import Incomplete, Ledger
from offline_recovery import extract, junit_counts, run_task


class RecoveryTests(unittest.TestCase):
    def test_no_tests_all_skipped_and_failure_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'tests.xml'
            for cases in ('', '<testcase><skipped/></testcase>',
                          '<testcase><failure/></testcase>', '<testcase><error/></testcase>'):
                path.write_text('<testsuite>'+cases+'</testsuite>')
                with self.assertRaises(Incomplete):
                    junit_counts(path)
            path.write_text('<testsuite><testcase/><testcase><skipped/></testcase></testsuite>')
            self.assertEqual(junit_counts(path), dict(tests=2, passed=1, skipped=1, failed=0))

    def test_archive_links_and_path_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, (name, kind) in enumerate((('../escape', tarfile.REGTYPE),
                                                ('tasks/example/link', tarfile.SYMTYPE),
                                                ('other.txt', tarfile.REGTYPE))):
                archive = root/f'{index}.tar'
                with tarfile.open(archive, 'w') as stream:
                    entry = tarfile.TarInfo(name); entry.type = kind
                    entry.linkname = '/etc/passwd'
                    stream.addfile(entry, io.BytesIO(b''))
                with self.assertRaises(Incomplete):
                    extract(archive, root/f'source{index}', 'tasks/example')

    def test_real_branch_runs_resume_and_tamper_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); repo = root/'repo'; repo.mkdir()
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()
            git('init', '-q'); git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'user.name', 'Offline fixture')
            (repo/'README').write_text('Local orchestration fixture, not physics')
            git('add', '.'); git('commit', '-qm', 'baseline')
            baseline = git('rev-parse', 'HEAD')
            folder = repo/'tasks/example'; folder.mkdir(parents=True)
            (folder/'test_value.py').write_text('def test_value():\n assert sum([2,3]) == 5\n')
            (folder/'task.json').write_text(json.dumps(dict(title='Archive fixture',category='Other',
                instruction='Fixture',setup='Fixture',scoring='Fixture',run_limit='0',
                fidelity='No simulation',scores='NOT RUN',media='')))
            (folder/'source_manifest.json').write_text(json.dumps({'files':{
                p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()}}))
            git('add','.');git('commit','-qm','task')
            task=dict(slug='example', branch='draft/example', folder='tasks/example', commit=git('rev-parse','HEAD'))
            evidence = root/'evidence'
            inputs = dict(task=task)
            receipt = Ledger(evidence).stage('example','offline',inputs,
                lambda out:run_task(repo,task,out,False,baseline))
            self.assertEqual(receipt['result']['tests']['passed'], 1)
            self.assertFalse(receipt['result']['ready_for_submission'])
            def forbidden(out):
                raise AssertionError('Successful stage was rerun')
            Ledger(evidence,resume=True).stage('example','offline',inputs,forbidden)
            stored = next(evidence.rglob('tests.xml'))
            stored.write_text('tampered')
            with self.assertRaisesRegex(Incomplete,'changed'):
                Ledger(evidence,resume=True).stage('example','offline',inputs,forbidden)


if __name__ == '__main__':
    unittest.main()
