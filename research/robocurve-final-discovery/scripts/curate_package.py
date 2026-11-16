"""List a compact research package. Does not delete downloads or mutate Git.

Working clones, large originals and unused caches are intentionally not packaged.
Publisher URL/pin/hash manifests remain the authority for reacquisition.
"""
import hashlib,json,os,re,collections
from pathlib import Path
D=Path(__file__).resolve().parents[1]
selected=set()
for p in D.rglob('*'):
 if not p.is_file() or p.is_symlink():continue
 rel=p.relative_to(D)
 if rel.parts[0]!='agents' and '__pycache__' not in rel.parts and p.suffix not in ['.pyc'] and p.name!='PACKAGE_MANIFEST.json':selected.add(rel)
# Curate agent evidence without descending into cloned repository worktrees.
for root,dirs,files in os.walk(D/'agents'):
 r=Path(root)
 dirs[:]=[n for n in dirs if n not in ['.git','__pycache__','assets'] and not (r/n/'.git').exists()]
 for f in files:
  p=r/f
  if p.is_symlink():continue
  if p.suffix.lower() in ['.md','.json','.txt','.py','.rst','.scad','.svg','.stl','.step','.png'] or f.startswith('LICENSE'):
   if p.stat().st_size<=300_000:selected.add(p.relative_to(D))
# Actual next-test parts and supporting interpretations are intentionally retained.
y=D/'agents/robot_build/evidence/yubi'
for p in (y/'registered_parts').glob('*.step'):selected.add(p.relative_to(D))
for name in ['registered-features.json','assembly-occurrences.json','source-manifest.json','LICENSE','README.md','rubber-page.png']:
 selected.add((y/name).relative_to(D))
for p in (D/'agents/care_cleaning/assets/create3-source').rglob('*'):
 if p.is_file() and p.stat().st_size<2_000_000:selected.add(p.relative_to(D))
# Preserve definitions/readmes and a small central-code set per comparator, not
# complete borrowed task implementations or duplicated runtime libraries.
final=json.loads((D/'evidence/final-portfolio.json').read_text())['finalists']
relevant={str(z.get('pr',z.get('PR'))) for c in final for z in c['competitors'] if isinstance(z,dict)}
relevant.update(['1973','1087','42','32','346'])
groups=collections.defaultdict(list)
for rel in list(selected):
 text=str(rel);m=re.search(r'/pr(\d+)(?:/|[-_])',text)
 if not m and '/competitors/' in text:m=re.search(r'/competitors/(\d+)[-_]',text)
 if not m:continue
 number=m.group(1)
 if rel.suffix.lower() in ['.png','.svg','.stl','.step']:selected.discard(rel);continue
 if rel.suffix=='.py':
  selected.discard(rel);groups[(number,'/'.join(rel.parts[:2]))].append(rel)
for (number,domain),paths in groups.items():
 def priority(p):
  b=p.name
  return (0 if b=='task.py' or b.endswith('_task.py') else 1 if b in ['scoring.py','check_score.py','mechanics.py','bodykit.py','mechkit.py','ringkit.py','bottlekit.py'] else 2 if not any(k in b for k in ['demo','expert','test','yam_','make_']) else 3,len(p.parts),b)
 if number in relevant:selected.update(sorted(paths,key=priority)[:4])
# Matched compact J4 inputs only; full-arm archive is reacquired by source pin.
for rel in list(selected):
 text=str(rel)
 if '/faze4/STL_V2/' in text and '/J4 cyclo/' not in text:selected.discard(rel)
 if '/faze4/cyclo_disk_STEP_files/' in text and rel.name!='11_1 cyclo disc.STEP':selected.discard(rel)

# Remove initial failed parser output; corrected capture and crawl-failure evidence remain.
selected.discard(Path('evidence/household/semantic-searches.json'))
rows=[]
for rel in sorted(selected):
 p=D/rel
 if p.name=='PACKAGE_MANIFEST.json':continue
 rows.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
out={'purpose':'Explicit compact research package, not every acquisition cache','files':rows,'total_bytes':sum(r['bytes'] for r in rows),'omitted':'Temporary Git clones; large originals reacquirable from pinned publisher manifests; source PDF collections; archives; unused screenshots/search HTML. This does not imply unread sources were inspected.'}
(D/'PACKAGE_MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'files':len(rows),'bytes':out['total_bytes'],'MiB':round(out['total_bytes']/2**20,2)},indent=2))
