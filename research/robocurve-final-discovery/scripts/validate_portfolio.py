"""Check report/result consistency; not a simulation or acceptance test."""
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parents[1]
required=['DISCOVERY_METHODOLOGY','INITIAL_80_PLUS_CANDIDATES','OFFICIAL_COMPETITOR_AUDIT','TOP_15_VERIFIED_TASKS','TOP_15_SOURCE_AND_FEASIBILITY_MATRIX','TOP_3_DETAILED_BUILD_PLANS','ADVERSARIAL_REVIEW','BEST_TASK_FINAL_SELECTION','NEXT_IMPLEMENTATION_PLAN','README']
for name in required:assert (D/(name+'.md')).is_file(),name
rows=json.loads((D/'evidence/final-portfolio.json').read_text())['finalists']
assert len(rows)==15 and len({x['id'] for x in rows})==15
assert [x['rank'] for x in rows]==list(range(1,16))
for x in rows:
 assert sum(x['score_components'].values())==x['score']
 assert all(0<=a<=b for a,b in zip(x['score_components'].values(),[20,25,20,20,15]))
 assert len(x['wrong_solutions'])>=3,x['id']
 assert len(x['competitors'])>=3,x['id']
 assert x['initial']!='Not established; see stated gate.',x['id']
 assert x['instruction'] and x['sources'] and x['hardware']
 assert (D/x['source_ledger']).is_file()
assert [x['score'] for x in rows]==sorted([x['score'] for x in rows],reverse=True)
assert sum(x['category']=='Impact on AI timelines' for x in rows)==10
bank=json.loads((D/'evidence/initial-bank.json').read_text())
assert bank['conservative_distinct_count']>=80
corpus=json.loads((D/'evidence/official-main-tasks.json').read_text())
assert corpus['pin']=='09e98131a30421420540230ea0804ce43a484919' and len(corpus['tasks'])==183
screen=json.loads((D/'cpu_preflight/YUBI_ENVELOPE_RESULT.json').read_text())
assert screen['robot_hulls_per_arm']==315 and screen['total_robot_hulls_tested']==630
assert screen['source_occurrences_tested']==45 and len(screen['cases'])==28
assert screen['summary']['conservatively_clear']==0
assert screen['controls']['far_separated']['conservatively_clear']
assert not screen['controls']['source_grip_envelope_in_palm_negative']['conservatively_clear']
narrow=json.loads((D/'cpu_preflight/YUBI_NARROWPHASE_RESULT.json').read_text())
assert len(narrow['pairs'])==3 and all(x['source_solid_valid'] and x['hull_solid_valid'] for x in narrow['pairs'])
assert 26.39<sum(x['common_volume_mm3'] for x in narrow['pairs'])<26.40
assert rows[0]['id']=='RB25' and rows[0]['score']==84
assert '26.395' in (D/'BEST_TASK_FINAL_SELECTION.md').read_text()
print(json.dumps({'finalists':15,'source_bank_records':bank['source_records'],'conservative_distinct_operations':bank['conservative_distinct_count'],'final_accepted_task_folders':183,'cpu_static_cases':28,'clear_envelope_cases':0,'selected_direct_hand_pose':'REJECTED by actual CAD overlap','task_level_feasibility':'UNVERIFIED','result':'REPORT/RESULT CONSISTENCY CHECKS PASS'},indent=2))
