import urllib.request,urllib.parse,concurrent.futures,pathlib,json,hashlib,datetime
import re,html
out=pathlib.Path('research/robocurve-final-discovery/agents/electrical_construction')
qs={'strut':'is:pr strut','channelnut':'is:pr "channel nut"','conduit':'is:pr conduit','box':'is:pr "electrical box"','breaker':'is:pr breaker','fuse':'is:pr fuse','sash':'is:pr sash','hinge':'is:pr hinge','lockset':'is:pr lockset','raceway':'is:pr raceway','twistlock':'is:pr "twist lock"','receptacle':'is:pr receptacle','oldwork':'is:pr "old work"','window':'is:pr window','punch':'is:pr knockout'}
def f(it):
 k,q=it;u='https://github.com/robocurve/benchmark-tasks/pulls?'+urllib.parse.urlencode({'q':q});d={'id':k,'query':q,'url':u,'attempted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=25) as r:b=r.read();d['status']=r.status
  (out/(k+'-search.html')).write_bytes(b);s=b.decode();d['sha256']=hashlib.sha256(b).hexdigest();d['hits']=[{'title':html.unescape(re.sub('<[^>]+>','',m[1])),'url':m[0]} for m in re.findall(r'<a[^>]*href="([^"]+)"[^>]*data-testid="listitem-title-link"[^>]*>(.*?)</a>',s,re.S)];d['next']=re.findall(r'href="([^"]+)"[^>]*rel="next"',s)
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:rs=list(ex.map(f,qs.items()))
(out/'queries.json').write_text(json.dumps(rs,indent=2)+'\n')
for x in rs:print(x['id'],x.get('error',x.get('hits')))
