import urllib.request,urllib.parse,json,pathlib,re,concurrent.futures,hashlib,datetime
out=pathlib.Path(__file__).parent
qs={'b114r':'B114R in:readme','halo':'"HALO" "torsion" in:readme','bifold':'"Johnson" "bifold" in:readme','leviton':'"Leviton" "5320" in:readme'}
def f(it):
 k,q=it;u='https://github.com/search?'+urllib.parse.urlencode({'q':q,'type':'repositories'});d={'id':k,'query':q,'url':u,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=20) as r:b=r.read();d['status']=r.status
  (out/(k+'-mirror-search.html')).write_bytes(b);d['sha256']=hashlib.sha256(b).hexdigest()
  for s in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',b.decode(),re.S):
   try:
    a=json.loads(s)
    if 'payload' in a:d['payload']=a['payload']
   except:pass
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:r=list(ex.map(f,qs.items()))
(out/'source-mirror-search.json').write_text(json.dumps(r,indent=2))
for x in r: print(x['id'],str(x)[:10000])
