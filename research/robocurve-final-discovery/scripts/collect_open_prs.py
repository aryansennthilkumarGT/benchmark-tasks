"""Read-only current GitHub HTML PR ledger. No API credentials or task execution."""
import argparse,concurrent.futures,datetime,hashlib,json,re,time,urllib.request
from pathlib import Path

def decode(s):
 for x in re.findall(r'<script[^>]+type="application/json"[^>]*>(.*?)</script>',s,re.S):
  try:
   d=json.loads(x)
   p=d.get('payload',{}).get('repoPullsDashboardContentRoute')
   if p is not None:return p
  except (ValueError,TypeError):pass
 raise ValueError('GitHub PR dashboard embedded payload missing')

def fetch(page,cache):
 url=f'https://github.com/robocurve/benchmark-tasks/pulls?q=is%3Apr+is%3Aopen&page={page}'
 b=urllib.request.urlopen(url,timeout=35).read();cache.mkdir(parents=True,exist_ok=True);(cache/f'open-page{page}.html').write_bytes(b)
 d=decode(b.decode());results=[]
 for x in d['results']:
  results.append({k:x.get(k) for k in ['number','title','state','displayState','headSha','createdAt','updatedAt','permalink']})
 return dict(page=page,url=url,sha256=hashlib.sha256(b).hexdigest(),rows=results)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--cache',type=Path,default=Path('/workspace/final-discovery-cache'));p.add_argument('--pages',type=int,default=18);a=p.parse_args();rows=[];fail=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(fetch,i,a.cache):i for i in range(1,a.pages+1)}
  for f in concurrent.futures.as_completed(fs):
   try:rows.append(f.result());print('page',fs[f],'rows',len(rows[-1]['rows']),flush=True)
   except Exception as e:fail.append(dict(page=fs[f],error=str(e)));print('page',fs[f],'FAILED',str(e),flush=True)
 unique={x['number']:x for r in rows for x in r['rows']};out=dict(retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),requested_pages=a.pages,successful_pages=len(rows),failures=fail,count=len(unique),pulls=sorted(unique.values(),key=lambda x:x['number'],reverse=True),pages=[{k:v for k,v in r.items() if k!='rows'} for r in sorted(rows,key=lambda x:x['page'])],limitation='Concurrent public HTML snapshot,not immutable all-PR/ownership ledger. New PRs may shift page boundaries. Targeted final competitor checks required.')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print('unique openPRs',len(unique),flush=True)
if __name__=='__main__':main()
