"""Render final comparative portfolio from preserved investigations and root decisions."""
import json,re
from pathlib import Path
D=Path(__file__).resolve().parents[1]
def load(n):return json.loads((D/'agents'/f'{n}.json').read_text())
def rec(n,k,id):return next(x for x in load(n)[k] if x['id']==id)
def get(d,keys,default='Not established; see stated gate.'):
 for k in keys:
  if k in d and d[k] not in [None,'',[]]:return d[k]
 return default
B='BUILD-READY FOR CPU PREFLIGHT';G='PROMISING BUT SOURCE-GATED';H='HIGH-RISK RESERVE'
spec=[
 ('robot_build','strongest_candidates','RB25','YUBI glove return-spring loop',[20,22,19,11,12],B),
 ('robot_build','strongest_candidates','RB01','Faze4 paired cycloidal reducer closure',[19,20,19,13,12],B),
 ('root','root','ROOT01','Toshiba driven turntable and roller carrier',[17,20,16,14,12],B),
 ('food_warehouse','deep_investigations','F06','Chefman spring-wire basket handle',[16,22,17,10,12],B),
 ('food_warehouse','deep_investigations','F07','Oster blade-retaining sealing annulus',[17,19,17,11,12],B),
 ('datacenter','deep_investigations','DC24','CELLO leader-arm rotary brake tuning',[19,19,18,9,10],B),
 ('care_extension','finalists','CE01','Opentrons 2G11 lamp socket and remote clip',[19,20,16,8,11],B),
 ('robot_build','strongest_candidates','RB02','ODRI helical inserts and tang recovery',[19,21,17,6,10],G),
 ('root','root','ROOT02','Hamilton Beach loaded rotisserie installation',[14,19,15,10,12],G),
 ('robot_build','strongest_candidates','RB04','OpenHand F3 tendon routing and zeroing',[19,18,18,6,9],H),
 ('care_cleaning','deep_assessments','CC21','Create3 rear-caster capture and retaining tab',[19,19,18,5,8],H),
 ('datacenter','deep_investigations','DC21','ODRI compliant optical-foot assembly',[19,19,18,4,8],H),
 ('robot_build','strongest_candidates','RB03','ODRI annular rotor landing and hub clamping',[19,19,15,5,9],G),
 ('datacenter','deep_investigations','DC06','DYNAMIXEL430 hollow-idler assembly',[19,18,15,5,9],G),
 ('food_extension','investigated_reserve','FX01','Ninja BL610 folding-handle lid retention',[15,17,16,7,10],H),
]
roots=json.loads((D/'evidence/household/root-dossiers.json').read_text());rows=[]
for rank,(domain,key,id,title,score,cl) in enumerate(spec,1):
 if domain=='root':o=next(x for x in roots if x['id']==id)
 elif key=='investigated_reserve':o=load(domain)[key];id=o['id']
 else:o=rec(domain,key,id)
 c=dict(rank=rank,id=id,title=title,full_title=o['title'],category='Societal relatability' if domain in ['root','food_warehouse','food_extension'] else 'Impact on AI timelines',score=sum(score),score_components=dict(zip(['importance_20','novelty_25','source_mechanism_20','YAM_fidelity_20','scoring_economy_15'],score)),classification=cl,original_classification=o.get('classification'),original_score=get(o,['score','score_total','weighted_score','weighted_components'],None),source_ledger='evidence/household/root-dossiers.json' if domain=='root' else f'agents/{domain}.json',original_record=o)
 c['importance']=get(o,['importance','importance_exact_workflow','importance_claim'])
 c['sources']=get(o,['source_provenance','sources','real_procedure','source','source_facts'])
 c['hardware']=get(o,['hardware','verified_hardware_inventory','inventory','hardware_inventory','authentic_inventory','authentic_hardware'])
 c['initial']=get(o,['starting_state','starting_configuration','initial_configuration','initial_state'],get(c['hardware'] if isinstance(c['hardware'],dict) else {},['starting_state','initial_state','state','initial','installed_initial_state','starting_configuration','initial_configuration'],get(o.get('scoring',o.get('physical_scoring',{})),['initial'])))
 c['instruction']=get(o,['instruction'])
 c['ability']=get(o,['essential_skill','central_physical_ability','core_ability','essential_ability'])
 c['bimanual']=get(o,['bimanual_challenge','bimanual_or_horizon','bimanual_or_long_horizon','bimanual_requirement','bimanual'])
 c['scoring']=get(o,['physical_scoring','scoring','partial_full_scoring'])
 c['reset']=get(o,['reset'],get(c['scoring'] if isinstance(c['scoring'],dict) else {},['reset']))
 c['wrong_solutions']=get(o,['wrong_solutions','incorrect_solutions_blocked','incorrect_solutions_caught','incorrect_solutions'],get(c['scoring'] if isinstance(c['scoring'],dict) else {},['wrong_solutions_prevented','wrong_solutions']))
 c['competitors']=get(o,['closest_official_tasks','closest_competitors','closest_official_prs','closest_official_competitors','competitors'])
 c['external']=get(o,['external_neighbors','external_benchmark_comparison','external_benchmark_audit'],'See independent external-suite audit; no exhaustive ecosystem-clearance claim.')
 c['yam']=get(o,['YAM','YAM_screen','yam_screen','yam','feasibility'])
 c['verified']=get(o,['executed_checks','feasibility','proof_of_what_ran','evidence_verified','verified_evidence'],get(o.get('sources',{}),['read_status'],'Specific read/provenance statements above; no task implementation was executed.'))
 c['uncertainty']=get(o,['remaining_uncertainty','essential_missing_inputs','specific_source_issue','exact_gate','hard_blockers','hard_blocker'],get(c['hardware'] if isinstance(c['hardware'],dict) else {},['unknown','known_vs_unknown']))
 c['hard_blockers']=o.get('hard_blockers',o.get('hard_blocker',[]))
 c['falsifier']=get(o,['cheapest_falsifier','cheapest_falsification'])
 c['effort']=get(o,['relative_effort','effort'])
 c['critic']=get(o,['adversarial_strongest_rejection','strongest_adversarial_rejection','adversarial_review','strongest_reviewer_rejection','critic'])
 rows.append(c)
# Root reconciles investment decisions without rewriting investigator evidence.
notes={
 'RB25':'First finite investment. CAD and finger hook are source-bound; the holder-hook saddle is not yet unambiguously identified. Executed screen:28 static placements of630 actual robot hulls against45 source occurrence envelopes; all were inconclusive. Exact CAD narrow phase of the least-overlapping pose found26.395mm³ of real right-finger/FLAP_R overlap. That direct-hand pose is rejected, not the entire operation. No grasp/route/material pass; the next coupon must use a valid different approach or ordinary held tool. Root lowered score88 to84 after this result.',
 'RB01':'Cost-adjusted below investigator86: source analytic parts exist, but print-frame registration and closed rolling-loop contact are still work. STEP feature offset1.503mm is not the independently measured approximately1.5mm eccentricity. One disk can yield11:1; functional ratio never proves two disks are present.',
 'ROOT01':'Topology/sequence are sufficient for a small parameterized rigid coupon. Missing scalar dimensions do not require perfect OEM CAD; full tray purchase, cavity and physical hub inspection remain unverified.',
 'F06':'Root upgrades only to a bounded parameterized contact study: manufacturer establishes squeeze/prongs/holes/cuffs and load path. Unknown force/gauge can be declared ranges. Actual escape/capture geometry must remain; no spring latch invented to make a demo.',
 'F07':'Root upgrades only to a bounded internal-groove tuck/retention study. Unknown stiffness/dimensions are parameters; a rigid ring or proximity attachment is forbidden. The original source-gated investigator dissent remains visible.',
 'DC24':'Small source-guided brake study justified, conditional on genuine loose-brake sag and a useful hold/backdrive window. No artificial load, hidden brake flag or generic service-arm substitute. Component CAD inspection is not assembled robot validation.',
 'CE01':'Small socket/clip mechanism study must keep the original UNDERSIDE orientation. Manufacturer places module on Flex first and parks gantry back-right. A face-up bench module is invalid; a source-oriented coupon cannot certify installed robot reach. Full enclosure/gantry access remains a kill condition.',
 'RB02':'No coil/mandrel/tang drawing package recovered. Source mechanism is real, but tool geometry and submillimetre handling dominate; do not start a speculative helical simulation.',
 'ROOT02':'The exact donor/SKU and matched cavity/spit/drive geometry are a specific gate. Preserve at least the real1.4kg roast mass/envelope; an empty rod is not equivalent.',
 'RB04':'Source-complete research reserve, not next investment. Full-scale thin tendon and flexible rest state, source license and tiny anchor handling are substantial cost.',
 'CC21':'Preserve investigator dissent: recommended_for_top15 was false without tiny-retainer access. Kept as a distinctly sourced HIGH-RISK reserve, never promoted to build readiness. Unscaled7×11.41×1.8mm tab purchase and screw access must pass before investment.',
 'DC21':'Actual product fixes authenticity, not the manipulation cost of12 tiny springs. Keep opposed centering/precompression and foot travel; an insert-counting puzzle or fixed springs erase the mechanism.',
 'RB03':'Motor STEP filename is misleading: it contains only the customshaft. Spoke/hub/winding driver corridor is the specific essential geometry gate; no further speculative rotor model.',
 'DC06':'Treat assembly and reverse release as one family. Release-button instructions begin with rear case removed; do not invent access through the fully assembled motor. Source hook/undercut section remains the single package needed.',
 rows[-1]['id']:'Replacement for OpenMV, whose active#346 optical-focus overlap is too strong for this portfolio. RealAppliance091 genuinely includes generic close(lid); no claim of object/endpoint non-overlap. Inspected external definitions score planning/next-action selection, without folding-handle/tab capture or retained pull-test requirement. This physical ability distinction is defensible but contested; preserve linkage uncertainty, never invent an over-center cam.'}
for c in rows:c['root_decision']=notes[c['id']]
assert len(rows)==15 and len({c['id'] for c in rows})==15
(D/'evidence/final-portfolio.json').write_text(json.dumps({'ranking_basis':'Root comparative cost/risk adjustments; not acceptance probability','finalists':rows},indent=2)+'\n')
# Render useful content; huge copied file-manifest arrays stay in the machine-readable ledgers.
skip={'actual_files','source_files','inspected_files','files','read_files','source_paths','current_search_coverage'}
def render(v):
 if isinstance(v,str):return v
 if v is None:return 'Unknown.'
 if isinstance(v,bool):return 'Yes.' if v else 'No.'
 if isinstance(v,list):return '\n'.join('- '+render(x).replace('\n',' ') for x in v)
 if isinstance(v,dict):return '\n'.join('**'+k.replace('_',' ')+'**: '+render(x).replace('\n',' ') for k,x in v.items() if k not in skip)
 return str(v)
def comp(v):
 if not isinstance(v,list):return render(v)
 out=[]
 for x in v:
  pr=get(x,['pr','PR','number'],{'close-a-swing-top-bottle':1973,'detent-latch-bottle':1087,'dual-latch-lid':42,'snapfit-close':32}.get(x.get('family')));status=get(x,['current_status','current_state_at_retrieval','current_state','state','status'],'See pinned ledger')
  why=get(x,['semantic_comparison','legitimate_semantic_comparison','legitimate_scope_comparison','comparison','operation_comparison','why_different','scope_comparison'],'See actual source-file comparison in investigator ledger.')
  head=get(x,['head','sha','head_sha'],'Recorded in source manifest')
  label=f'[#{pr}](https://github.com/robocurve/benchmark-tasks/pull/{pr})' if pr is not None else f'[{x.get("family","accepted task")}]'+'(https://github.com/robocurve/benchmark-tasks/tree/c82d718b83f44a49ed9e7bdb2a49d8434563e103/tasks/'+x.get('family','')+')'
  out.append(f'- {label} — {status}; `{head}`. {render(why)}')
 return '\n'.join(out)
lines=['# Fifteen ranked, source-backed task concepts','', '**Verified refers to identified evidence, not fifteen passed feasibility gates.** Seven finite CPU studies are justified; the others are specifically source-gated or high-risk reserves. None is GPU-ready, implemented, accepted or ownership-cleared. Scores are relative research judgments.','', 'The source/importance verification and the adversarial decision are separated. Original investigator classifications remain in the JSON; root cost/risk adjustments below govern the final investment order. All precise scorer tolerances proposed by investigators are authored benchmark choices unless explicitly sourced.','']
for c in rows:
 lines += [f'## {c["rank"]}. {c["title"]} — {c["score"]}/100', '',f'**{c["category"]} · {c["classification"]}**', '', '**Final decision.** '+c['root_decision'],'', '**Importance, real work and consequence.** '+render(c['importance']), '', '**Manufacturer/designer procedure and provenance.**', '',render(c['sources']),'', '**Authentic hardware, size/material, interfaces, tools and support.**', '',render(c['hardware']),'', '**Initial state.** '+render(c['initial']),'', '**Robot instruction.** '+render(c['instruction']),'', '**Essential physical ability.** '+render(c['ability']),'', '**Bimanual/long-horizon challenge.** '+render(c['bimanual']),'', '**Physical scoring, measurement and invalid outcomes.**', '',render(c['scoring']),'', '**Reset.** '+render(c['reset']),'', '**Incorrect solutions and prevention.**','',render(c['wrong_solutions']),'', '**Current official comparison and semantic novelty.**','',comp(c['competitors']),'','**External benchmark comparison.** '+render(c['external']),'','**Stock-YAM and fidelity screen.**','',render(c['yam']),'','**What was verified.** '+render(c['verified']),'','**Remaining uncertainty / hard gate.** '+render(c['uncertainty']),'','**Cheapest falsification test.** '+render(c['falsifier']),'','**Relative implementation effort.** '+render(c['effort']),'','**Strongest reviewer rejection.** '+render(c['critic']),'', '**Weighted components** (importance, novelty, source, YAM/fidelity, scoring/economy): '+', '.join(str(z) for z in c['score_components'].values())+f' = **{c["score"]}**. [Full original record]({c["source_ledger"]}).','']
(D/'TOP_15_VERIFIED_TASKS.md').write_text('\n'.join(lines))
m=['# Source and feasibility matrix','','No source or score establishes native readiness. All task-level grasps, material calibration and released expert demonstrations remain unexecuted. Exact inputs and tests are linked below.','', '|Rank|Task / score|Importance|Procedure/mechanism evidence|CPU investment class|Specific risk / next falsifier|','|---|---|---|---|---|---|']
for c in rows:
 m.append(f'|{c["rank"]}|{c["title"]} / {c["score"]}|{c["category"]}|Original manufacturer/designer source read; provenance in dossier|{c["classification"]}|{c["root_decision"].replace("|","/")}|')
m+=['','## Evidence separation','','- Manufacturer procedure: read for each finalist; source is a named designer/manufacturer or explicitly attributed original-PDF mirror.','- Importance:10 direct robot/robot-lab operations and5 household Societal-relatability operations; no restaurant employment borrowed for household-only products.','- Novelty: close official actual files/status checked, with unresolved challenges retained; no exhaustive ownership certificate. Ninja has real external endpoint overlap.','- Construct validity: causal contacts and completion roles specified; proposed simplifications are not validated physics.','- Physical measurement: proposed per dossier, with thresholds explicitly benchmark-authored where unsourced.','- Robot feasibility: source scale/purchase/tool and collision risks assessed. Only selected YUBI empty-hand source-envelope screen executed; it is not a grasp or route proof.','- Materials/forces: no manufacturer force values invented, no physical force calibration performed.','']
(D/'TOP_15_SOURCE_AND_FEASIBILITY_MATRIX.md').write_text('\n'.join(m))
audit=['# Official semantic competitor audit','','Initial snapshot: official main `c82d718b83f44a49ed9e7bdb2a49d8434563e103`,180 accepted task folders. Final refresh: `09e98131a30421420540230ea0804ce43a484919`,183 accepted folders; three additions inspected in evidence/final-main-delta/REVIEW.md. Fresh targeted PR pages and read-only fetched heads supplement this snapshot. Source pins, filenames and hashes are preserved in the agent ledgers and critic evidence.','', 'The first dashboard page contained25 of440 open PRs. An18-page automated crawl hit429 and collected zero pages; its failure ledger is retained. **This is not an exhaustive pending-PR census or a guarantee of ownership.** We used semantic synonym searches and actual close-task files instead. A live recheck immediately before any later submission is mandatory.','', 'No novelty claim dismisses a competitor because it was rejected or implemented simplified physics. Earlier legitimate operations are compared. Shared elementary movements or adjustment/test reasoning alone are insufficient for duplication under Version21.','']
for c in rows:audit += [f'## {c["rank"]}. {c["title"]}','',comp(c['competitors']),'',c['root_decision'],'']
audit += ['## Decisive eliminations and external checks','','- Heater-Shaker deck anchoring: source-rich but accepted#1283 already counterholds and drives a transverse screw clamp beneath a mounting lip. Excluded from final15.','- Create3 faceplate: real four-pin twist retention repeats accepted#34 bayonet cap ability. Excluded.','- OpenMV lens focus: actual OEM source and robot use verified, but current active#346 optical focus/revision is a serious semantic ownership risk. Replaced with Ninja mechanical lever-latch task.','- Hobart mixer beater/bowl, meat grinder and dicer: current#2185/#1426/#2315/#1608 constrain legitimate scope; component-count chaining did not establish novelty.','- RealAppliance exact definitions for006/008/039/055/069/080/091 and its actual task measurements were read.039/055/008/080 do not define proposed assembly endpoints.091 DOES define generic close(lid); only the new required mechanical handle/tab retention ability supports a conditional difference. Source manuals alone do not make that novelty certain.','- Source inspections of external suites and known broader gear/insertion tasks are bounded; no claim of complete global benchmark search. See critic evidence for exact definitions rather than search-result titles.','']
(D/'OFFICIAL_COMPETITOR_AUDIT.md').write_text('\n'.join(audit))
print('rendered15',[(c['rank'],c['id'],c['score']) for c in rows])
