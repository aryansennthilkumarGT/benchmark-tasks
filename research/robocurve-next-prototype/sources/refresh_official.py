"""Read public GitHub search metadata and immutable official task implementations."""
from pathlib import Path
import subprocess,json,re,hashlib,urllib.parse,concurrent.futures
D=Path(__file__).resolve().parent
queries=[('friction1','is:pr friction',1),('friction2','is:pr friction',2),('friction3','is:pr friction',3),('rotary-brake','is:pr "rotary brake"',1),('joint-adjust','is:pr joint adjust',1),('foot-sensor','is:pr "foot" "sensor"',1)]
def query(a):
 tag,q,page=a;url='https://github.com/robocurve/benchmark-tasks/pulls?'+urllib.parse.urlencode({'q':q,'page':page})
 r=subprocess.run(['curl','-L','-sS','--fail','--max-time','25',url],capture_output=True)
 item=dict(query=q,page=page,url=url,exit_code=r.returncode)
 if r.returncode:item['error']=r.stderr.decode()[:250];return tag,item
 s=r.stdout.decode();m=re.search(r'<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>',s)
 if not m:item['error']='Expected structured GitHub page payload missing';return tag,item
 p=json.loads(m.group(1))['payload']['repoPullsDashboardContentRoute']
 item.update(total_count=p.get('totalCount'),total_pages=p.get('totalPages'),page_sha256=hashlib.sha256(r.stdout).hexdigest(),results=[{k:x[k] for k in ['number','state','title']} for x in p.get('results',[])])
 if item.get('total_count') is None:item['payload_keys']=list(p);item['status']='Search count unavailable; do not infer absence'
 return tag,item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: out=dict(pool.map(query,queries))
(D/'CURRENT_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n')
for k,x in out.items(): print(k,x.get('total_count'),x.get('error',''))
