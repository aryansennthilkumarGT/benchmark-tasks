# Final RoboCurve discovery portfolio

**First choice: Toyota YUBI glove return-spring installation,84/100, for one bounded CPU contact coupon.** Faze4 reducer closure83 and Toshiba turntable reassembly79 are the next two. No candidate is declared fully feasible, accepted or GPU-ready.

The consolidated initial bank contains130 screened records,123 conservatively counted distinct operations after explicit duplicate exclusions, with22 further extension screens preserved separately. The final15 comprise10 direct robot/robot-lab operations and5 household operations under Societal relatability. Seven justify finite CPU studies; four have a specific source gate and four are high-risk reserves.

## Read in this order

1. [Ranked fifteen and full task dossiers](TOP_15_VERIFIED_TASKS.md)
2. [Source/feasibility matrix](TOP_15_SOURCE_AND_FEASIBILITY_MATRIX.md)
3. [Independent adversarial review and root resolutions](ADVERSARIAL_REVIEW.md)
4. [Three actionable CPU build blueprints](TOP_3_DETAILED_BUILD_PLANS.md)
5. [Single best selection](BEST_TASK_FINAL_SELECTION.md) and [finite next implementation unit](NEXT_IMPLEMENTATION_PLAN.md)
6. [Official competitor audit](OFFICIAL_COMPETITOR_AUDIT.md), [method/rule limits](DISCOVERY_METHODOLOGY.md), [initial operation bank](INITIAL_80_PLUS_CANDIDATES.md)

Machine-readable records: [final portfolio](evidence/final-portfolio.json), [initial bank](evidence/initial-bank.json), [current accepted corpus](evidence/official-main-tasks.json), [initial accepted snapshot](evidence/initial-official-main-tasks.json), and original investigator JSON/Markdown under`agents/`. Original investigator scores/classifications are preserved; final root scores reflect comparative engineering cost and later negative evidence.

## What actually ran

- Shell/Git access and clean starting branch at`9cc7e816191528ebdea8b3356f29a0cb249140a6` verified; latest origin research checkpoint fetched without resetting existing work.
- Official main fetched initially at`c82d718b83f44a49ed9e7bdb2a49d8434563e103`(180accepted task folders), then at`09e98131a30421420540230ea0804ce43a484919`(183). [Three-task delta review](evidence/final-main-delta/REVIEW.md) includes new foil-lid/needle scopes. Authoring README/AGENTS did not change.
- Original manufacturer/designer documents and named attributed PDF mirrors were inspected; current close PR task/README/scoring sources and external RealAppliance definitions were read. Hash/pin/file ledgers preserve provenance. Not every initial search lead reached an inspected manual.
- Source CAD inspection includes Faze4 analytic surfaces/STL bounds, YUBI46 registered occurrence frames and actual finger-hook/pivot, Create3 parts, CELLO five-body drum-brake section and ODRI foot geometry. Bounds are not access passes.
- [One YUBI geometry study](cpu_preflight/README.md):28 static placements,630 actual YAM hulls,45 source occurrence envelopes. Zero envelope-certified clear poses. Exact CAD resolution rejects one tested direct-hand pose with26.395mm³ fingertip/flap intersection. Both geometry controls behaved as expected. No rubber-band/contact/retention simulation or full assembly route ran.

## Reproduce the committed results

Run from repository root in a CPU Python environment. NumPy/SciPy are needed for the envelope study; exact narrow phase/source-frame extraction additionally uses CadQuery/OCCT. The existing YAM preflight provides the unchanged source-bound robot reference.

```bash
python research/robocurve-final-discovery/scripts/consolidate_bank.py
python research/robocurve-final-discovery/scripts/build_portfolio.py
python research/robocurve-final-discovery/cpu_preflight/yubi_envelope_screen.py
python research/robocurve-final-discovery/agents/robot_build/evidence/fetch_yubi_pinned.py --out /tmp/yubi-pinned-source
python research/robocurve-final-discovery/cpu_preflight/narrowphase_best_case.py --source '/tmp/yubi-pinned-source/STEP/glove/YUBI Glove Assy_ver2_R.STEP'
python research/robocurve-final-discovery/scripts/validate_portfolio.py
```

The source fetcher checks out no branch; it fetches immutable publisher objects into a temporary repository. The exact original STEP SHA256 is checked by narrow phase. [Toyota source manifest](agents/robot_build/evidence/yubi/source-manifest.json) and [curated inputs](agents/robot_build/evidence/YUBI_CURATED_INPUTS.json) identify originals and derived files. Large working clones/archives are omitted from the research commit; relevant source excerpts, figures, manifests, actual comparison files and measured outputs are preserved. The preserved ledgers may name optional uncommitted acquisition-cache paths: their source URLs/pins/hashes are the reproducible authority, not an assertion that every downloaded asset is packaged.

For a live semantic status check, for example:

```bash
python research/robocurve-final-discovery/scripts/search_official.py --output /tmp/robocurve-current-elastic.json '"rubber"' '"elastic"' '"glove"' '"spring-return"'
git fetch --no-tags https://github.com/robocurve/benchmark-tasks.git 8c10b6f0e80f49908d5d0afdc1ae3092f3ce3729
git ls-tree -r --name-only FETCH_HEAD
```

Use the exact task paths in investigator competitor manifests with`git show FETCH_HEAD:path`. Fetching an earlier head reproduces the inspected scope; search/pages must be refreshed separately for current status. Public HTML searches can return429. The failed18-page open-PR crawl is retained, never treated as zero pending tasks. The cached first page had25 of440 open PRs; this is not an exhaustive ownership ledger.

## Unverified gates and resource boundary

The live review-agent page and many OEM/BLS/O*NET domains were blocked. Version21 is the complete retained user-provided source; no newer inaccessible live rubric is ruled out. Employment/Core checks used identified dated mirrors; no live agency verification is claimed. Household products do not borrow commercial job counts.

Full stock-YAM grasps, tool wrench capacity, continuous bimanual paths, material calibration, native experts, model runs and official reviewer decisions remain unverified. Ninja has an explicit same-object external`close(lid)` overlap; its proposed distinct physical lever-retention ability remains a rejection risk. HEPA access must preserve the mounted underside and parked gantry. No GPU, Brev, Dream, paid evaluation, purchase, official PR or unrelated task modification occurred.
