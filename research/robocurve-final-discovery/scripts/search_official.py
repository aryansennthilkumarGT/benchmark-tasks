"""Read-only public GitHub semantic-search capture. A failed search is not zero hits."""
import argparse, datetime, hashlib, json, re, urllib.parse, urllib.request
from pathlib import Path

def search(query):
    url = 'https://github.com/search?' + urllib.parse.urlencode({'q': query, 'type': 'issues'})
    row = {'query': query, 'url': url, 'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        data = urllib.request.urlopen(url, timeout=30).read()
        row['html_sha256'] = hashlib.sha256(data).hexdigest()
        for s in re.findall(r'<script[^>]+type="application/json"[^>]*>(.*?)</script>', data.decode(), re.S):
            d = json.loads(s)
            payload = d.get('payload', {})
            p = payload.get('blackbirdSearchRoute', payload)
            if 'result_count' in p and 'results' in p:
                row['result_count'] = p['result_count']
                row['page_count'] = p.get('page_count')
                row['results'] = [{k: v.get(k) for k in ['number', 'hl_title', 'state', 'merged', 'labels', 'created', 'reviewable_state']} for v in p['results']]
                return row
        raise ValueError('Expected embedded search results missing; not interpreted as no matches')
    except Exception as e:
        row['error'] = str(e)
        return row

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--output', type=Path, required=True)
    a.add_argument('terms', nargs='+')
    args = a.parse_args()
    rows = [search('repo:robocurve/benchmark-tasks is:pr ' + term) for term in args.terms]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2) + '\n')
    for r in rows:
        print(r['query'], r.get('result_count', r.get('error')), [(x['number'], re.sub('<.*?>','',x.get('hl_title',''))) for x in r.get('results',[])])
