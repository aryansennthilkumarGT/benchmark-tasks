"""Consolidate operation leads; keep unverified leads distinct from read procedures."""
import json
from pathlib import Path
D=Path(__file__).resolve().parents[1]
spec={'robot_build':['initial20','additional_discovery'],'datacenter':['initial20','expansion_operations'],'electrical_construction':['initial_20','extension_10','final_bounded_pass'],'food_warehouse':['initial_20'],'care_cleaning':['initial_candidates']}
rows=[]
def first(x,keys,default='Not specified in lead; see investigation'):
 for k in keys:
  if k in x and x[k] not in [None,'']:return x[k]
 return default
for n,keys in spec.items():
 d=json.loads((D/'agents'/f'{n}.json').read_text())
 for k in keys:
  for x in d.get(k,[]):
   rows.append(dict(id=first(x,['id','ID']),domain=n,title=first(x,['title','operation']),source=first(x,['real_procedure_url','procedure_url','source_url','sourceURL','source','sources'],''),read_status=first(x,['procedure_status','read_status','source_status','procedure_read','readstatus','status']),disposition=first(x,['disposition','decision','screen']),reason=first(x,['reason','why','screen_reason','rejection_reason','blocker']),original_ledger=f'agents/{n}.json',record=x))
# Explicit semantic duplicates across independent domains, retained for audit but not counted.
dup={'RB09':'DC21','DC19':'RB11','RB21':'EC32','EC33':'RB02','DC13':'RB20','DC05':'RB05','RB23':'DC10'}
seen=set();count=0
for x in rows:
 key=x['title'].strip().casefold();isdup=x['id'] in dup or key in seen
 x['independent_counted']=not isdup
 if x['id'] in dup:x['duplicate_of']=dup[x['id']]
 seen.add(key)
 count+=not isdup
out={'source_records':len(rows),'conservative_distinct_count':count,'count_note':'Known cross-domain duplicates excluded. This counts screened operations, not verified finalists. Extension manual source lists are not automatically counted as operations.','candidates':rows}
(D/'evidence'/'initial-bank.json').write_text(json.dumps(out,indent=2)+'\n')
def cell(v):
 if isinstance(v,(dict,list)):v=json.dumps(v,ensure_ascii=False)
 return str(v).replace('|','/').replace('\n',' ')[:500]
s=['# Initial operation bank','',f'**{len(rows)} screened records; {count} conservatively counted distinct operations.** Broad unverified leads are included and labeled; this is not a claim that every procedure was read or every operation qualifies. The first screen was expanded after active ownership and source failures. Parked concepts were not silently substituted.','', '| ID | Domain | Actual operation | Source/read status | Disposition and reason | Counted |','|---|---|---|---|---|---|']
for r in rows:
 source=r['source'];link=f'[{cell(r["read_status"])}]({source})' if isinstance(source,str) and source.startswith('http') else cell(r['read_status'])
 s.append(f'| {cell(r["id"])} | {r["domain"]} | {cell(r["title"])} | {link} | {cell(r["disposition"])}: {cell(r["reason"])} | '+('yes' if r['independent_counted'] else 'cross-domain duplicate')+' |')
s+=['','The raw ledgers preserve source URLs, source failures, exact dispositions and fuller reasoning. Detailed household/robot extensions and critic exclusions are also retained; they are not required to reach80. Counts are a discovery coverage metric, never an acceptance argument.','']

extra=[]
for name,key in [('food_extension','screen'),('care_extension','initial_extension_candidates')]:
 d=json.loads((D/'agents'/f'{name}.json').read_text())
 for x in d[key]:extra.append(dict(ledger=f'agents/{name}.json',record=x))
s+=['## Additional bounded extension screens','',f'{len(extra)} further records are preserved below. They are not added to the conservative distinct count above because some revisit cross-domain leads.','']
for row in extra:
 x=row['record'];s.append('- **'+str(x.get('id',''))+' '+str(x.get('title',x.get('operation','')))+'** — '+str(x.get('disposition',x.get('decision','See source ledger')))+'. '+str(x.get('reason',''))+' ['+row['ledger']+']('+row['ledger']+')')

(D/'INITIAL_80_PLUS_CANDIDATES.md').write_text('\n'.join(s))
print(len(rows),'records',count,'distinct after explicit duplicate exclusion')
