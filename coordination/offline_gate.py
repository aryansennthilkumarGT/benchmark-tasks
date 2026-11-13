"""Check exact-source offline qualification bundles before future paid stages.

Manual acceptance review remains a documented engineering judgment, never an
external acceptance decision. Native physics and real demonstrations are absent
from this gate and cannot be inferred from synthetic/kinematic reports.
"""
import hashlib,json
from pathlib import Path
from engine import Incomplete,read,within

PASSES={'technical','occupation_and_novelty','scoring_and_measurement','independent_reproduction','final_readiness'}
REQUIRED_REPORTS={'unit','assets','ik','geometry','endpoint_collisions','fk_path','ideal_controller','clean_checkout'}


def verify(task,root):
    ref=task.get('offline_evidence')
    if not isinstance(ref,dict):raise Incomplete('Offline evidence bundle missing: '+task['slug'])
    path=within(root,Path(root)/ref['path'])
    if hashlib.sha256(path.read_bytes()).hexdigest()!=ref.get('sha256'):raise Incomplete('Offline evidence bundle changed')
    d=read(path)
    if d.get('slug')!=task['slug'] or d.get('published_commit')!=task['commit']:raise Incomplete('Offline source identity mismatch')
    if d.get('decision')!='OFFLINE READY' or d.get('fundamental_open_risks')!=[]:raise Incomplete('Offline quality gate remains open')
    if set(d.get('review_passes',{}))!=PASSES or any(not x.get('passed') or not x.get('evidence') for x in d['review_passes'].values()):
        raise Incomplete('Distinct documented review passes are incomplete')
    reports=d.get('reports',{})
    if set(reports)!=REQUIRED_REPORTS:raise Incomplete('Offline report coverage incomplete')
    for name,r in reports.items():
        f=within(root,Path(root)/r['path'])
        if hashlib.sha256(f.read_bytes()).hexdigest()!=r['sha256']:raise Incomplete('Offline report changed: '+name)
        if r.get('passed') is not True:raise Incomplete('Offline check did not pass: '+name)
    if d.get('physics_executed') is not False:raise Incomplete('This is an offline gate, not GPU evidence')
    if not d.get('source_manifest_sha256') or not d.get('tested_source_commit'):raise Incomplete('Exact tested source missing')
    return d
