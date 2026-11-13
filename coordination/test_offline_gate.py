"""Evidence-integrity fixtures only; never robotics, GPU or external review."""
import hashlib
import pytest
from engine import atomic,read,Incomplete
from offline_gate import verify,PASSES,REQUIRED_REPORTS


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def fixture(root):
 review_passes={};reports={}
 for name in PASSES:
  p=root/(name+'.json');atomic(p,dict(kind='INTERNAL_ENGINEERING_REVIEW_PASS',review_pass=name,passed=True,scope='ORCHESTRATION_FORMAT_FIXTURE',findings=['Synthetic format check, not a robotics review'],decision='FORMAT_ONLY'))
  review_passes[name]=dict(passed=True,evidence=p.name,sha256=digest(p))
 for name in REQUIRED_REPORTS:
  p=root/('report-'+name+'.json');atomic(p,dict(kind='ORCHESTRATION_FORMAT_FIXTURE_NOT_PHYSICS',passed=True,tests=dict(passed=1,failed=0)))
  reports[name]=dict(path=p.name,sha256=digest(p),passed=True)
 d=dict(slug='fixture',published_commit='a'*40,tested_source_commit='a'*40,decision='OFFLINE READY',fundamental_open_risks=[],review_passes=review_passes,reports=reports,physics_executed=False,source_manifest_sha256='b'*64)
 p=root/'bundle.json';atomic(p,d);task=dict(slug='fixture',commit='a'*40,offline_evidence=dict(path=p.name,sha256=digest(p)))
 return task,d,p


def refresh(task,d,p):
 atomic(p,d);task['offline_evidence']['sha256']=digest(p)


def test_complete_hashed_format_fixture_passes_without_launching_anything(tmp_path):
 t,d,p=fixture(tmp_path);assert verify(t,tmp_path)['slug']=='fixture'


def test_review_file_change_and_missing_file_are_not_hidden_by_bundle_label(tmp_path):
 t,d,p=fixture(tmp_path);f=tmp_path/d['review_passes']['technical']['evidence'];f.write_text('changed')
 with pytest.raises(Incomplete,match='missing or changed'):verify(t,tmp_path)
 f.unlink()
 with pytest.raises(Incomplete,match='missing or changed'):verify(t,tmp_path)


def test_failed_review_with_rehashed_receipt_still_fails(tmp_path):
 t,d,p=fixture(tmp_path);row=d['review_passes']['technical'];f=tmp_path/row['evidence'];actual=read(f);actual['passed']=False;atomic(f,actual);row['sha256']=digest(f);refresh(t,d,p)
 with pytest.raises(Incomplete,match='claimed pass'):verify(t,tmp_path)


def test_wrong_named_review_cannot_be_reused_for_another_pass(tmp_path):
 t,d,p=fixture(tmp_path);d['review_passes']['technical']=d['review_passes']['final_readiness'].copy();refresh(t,d,p)
 with pytest.raises(Incomplete,match='claimed pass|reused'):verify(t,tmp_path)


def test_failing_report_cannot_be_whitewashed_by_wrapper_passed_true(tmp_path):
 t,d,p=fixture(tmp_path);row=d['reports']['fk_path'];f=tmp_path/row['path'];atomic(f,dict(passed=False));row['sha256']=digest(f);refresh(t,d,p)
 with pytest.raises(Incomplete,match='contains failure'):verify(t,tmp_path)


def test_nested_failed_checks_are_rejected(tmp_path):
 t,d,p=fixture(tmp_path);row=d['reports']['geometry'];f=tmp_path/row['path'];atomic(f,dict(passed=True,checks=[dict(passed=False)]));row['sha256']=digest(f);refresh(t,d,p)
 with pytest.raises(Incomplete,match='failed check'):verify(t,tmp_path)


def test_zero_or_failed_unit_count_cannot_establish_qualification(tmp_path):
 t,d,p=fixture(tmp_path);row=d['reports']['unit'];f=tmp_path/row['path'];atomic(f,dict(passed=True,tests=dict(passed=1,failed=1)));row['sha256']=digest(f);refresh(t,d,p)
 with pytest.raises(Incomplete,match='Unit report'):verify(t,tmp_path)
