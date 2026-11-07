"""Collision checks on nominal body paths; explicitly NOT a physics rollout.

This catches incompatible geometry before spending GPU time. Body poses are
computed in Python solely for geometric inspection, never written to a simulator.
It cannot prove grasps, forces, friction, settling, or dynamically feasible paths.
"""
import copy
import hashlib
import importlib
import json
import math
from pathlib import Path
import sys
import types
import numpy as np
from feedback import rotate,multiply,conjugate,interpolate,axis_quat,qangle


def geometry_module(folder):
    name='_geometry_audit_'+hashlib.sha256(str(folder).encode()).hexdigest()[:12]
    package=types.ModuleType(name);package.__path__=[str(folder)];sys.modules[name]=package
    return importlib.import_module(name+'.geometry')


def frames(spec,plan,linear_step=.003,include_phase_starts=False):
    states={b['name']:copy.deepcopy(b) for a in spec['assemblies'] for b in a['bodies']}
    joints={j['name']:j for a in spec['assemblies'] for j in a.get('joints',[])}
    values={name:0. for name in joints}
    yield 'initial',copy.deepcopy(states)
    grasps={}
    for phase_index,phase in enumerate(plan['phases']):
        if include_phase_starts:yield f'PHASE {phase_index}: '+phase['label'],states
        if phase['kind']=='grasp':grasps[phase['side']]=phase['body']
        if phase['kind']=='release':
            released=grasps.pop(phase['side'],None)
            spring=next((j for j in joints.values() if j['child']==released and j['kind']=='prismatic' and j.get('stiffness',0)>0),None)
            if spring:
                # Nominal unloaded return only. Native probes must establish that
                # the spring really returns; this never modifies simulator state.
                phase=dict(kind='joint',body=released,joint=spring['name'],value=0,label=phase['label']+' nominal spring return')
        kind=phase['kind'];name=phase.get('body')
        if kind not in ('carry','insert','joint','thread'):continue
        body=states[name];p0=np.array(body['pos']);q0=body['quat']
        if kind in ('carry','insert'):
            target=phase['target'];p1=np.array(target['pos']);q1=target.get('quat',[0,0,0,1])
            if target.get('relative_to'):
                reference=states[target['relative_to']]
                p1=np.array(reference['pos'])+rotate(reference['quat'],p1);q1=multiply(reference['quat'],q1)
            steps=max(1,math.ceil(np.linalg.norm(p1-p0)/linear_step),math.ceil(qangle(q0,q1)/.05))
            path=[(p0+(p1-p0)*i/steps,interpolate(q0,q1,i/steps)) for i in range(1,steps+1)]
        elif kind=='joint':
            joint=joints[phase['joint']];reference=states[joint['parent']]
            axis=rotate(reference['quat'],np.eye(3)['XYZ'.index(joint['axis'])])
            pivot=np.array(reference['pos'])+rotate(reference['quat'],joint['pivot_parent'])
            delta=phase['value']-values[phase['joint']];steps=max(1,math.ceil(abs(delta)/(.04 if joint['kind']=='revolute' else linear_step)))
            path=[]
            for i in range(1,steps+1):
                d=delta*i/steps
                if joint['kind']=='revolute':turn=axis_quat(axis,d);path.append((pivot+rotate(turn,p0-pivot),multiply(turn,q0)))
                else:path.append((p0+axis*d,q0))
            values[phase['joint']]=phase['value']
        else:
            reference=states[phase['reference']];axis=rotate(reference['quat'],[0,0,1])
            total_turns=math.ceil(phase['turns']*8)/8
            steps=math.ceil(total_turns*64);path=[]
            for i in range(1,steps+1):
                turns=total_turns*i/steps;angle=phase.get('direction',-1)*turns*2*math.pi
                path.append((p0-axis*phase['pitch']*turns,multiply(axis_quat(axis,angle),q0)))
        # Rigidly carried child mechanisms follow their parent in this geometric
        # test. Flexible cables must use a dedicated continuity/path audit.
        descendants=[];pending=[name]
        while pending:
            parent=pending.pop()
            for joint in joints.values():
                if joint['parent']==parent:
                    child=joint['child'];pending.append(child);descendants.append(child)
        initial={child:copy.deepcopy(states[child]) for child in descendants}
        for i,(p,q) in enumerate(path):
            body['pos']=list(p);body['quat']=list(q)
            turn=multiply(q,conjugate(q0))
            for child in descendants:
                old=initial[child];states[child]['pos']=list(p+rotate(turn,np.array(old['pos'])-p0));states[child]['quat']=list(multiply(turn,old['quat']))
            yield phase['label']+f' [{i+1}/{len(path)}]',states


def audit(folder):
    geometry=geometry_module(folder);spec=json.loads((folder/'scene.json').read_text());plan=json.loads((folder/'controller.json').read_text())
    worst=0.;failed=[];count=0;phase_max={};initial=None;last=None
    rigid_spec=copy.deepcopy(spec);excluded=set(spec.get('offline_deformable_bodies',[]));slack=[]
    for assembly in rigid_spec['assemblies']:assembly['bodies']=[b for b in assembly['bodies'] if b['name'] not in excluded]
    for label,states in frames(spec,plan):
        depth=geometry.maximum_penetration(spec if label=='initial' else rigid_spec,states);count+=1;worst=max(worst,depth)
        if excluded:
            for assembly in spec['assemblies']:
                links=[b for b in assembly['bodies'] if '_link_' in b['name']]
                if not links:continue
                joints=assembly['joints'];length=0.
                for link in links:
                    enter=next(j for j in joints if j['child']==link['name']);leave=next(j for j in joints if j['parent']==link['name'])
                    length+=np.linalg.norm(np.array(leave['pivot_parent'])-enter['pivot_child'])
                plug=next(b for b in assembly['bodies'] if b['name'].startswith('plug_'))
                terminal=next(j for j in joints if j['child']==plug['name']);body=states[plug['name']]
                endpoint=np.array(body['pos'])+rotate(body['quat'],terminal['pivot_child'])
                available=length-np.linalg.norm(endpoint-states[assembly['bodies'][0]['name']]['pos']);slack.append(float(available))
                if available<.003 and not any(r['phase']==assembly['name'] for r in failed):
                    failed.append(dict(phase=assembly['name'],sample=label,cable_slack_m=float(available)))
        key=label.split(' [')[0];phase_max[key]=max(phase_max.get(key,0),depth)
        if initial is None:initial=depth
        if depth>spec['penetration_limit']+1e-8 and not any(row['phase']==key for row in failed):
            failed.append(dict(phase=key,sample=label,penetration_m=depth))
        last=states
    report=dict(kind='OFFLINE_NOMINAL_BODY_GEOMETRY',physics_executed=False,robot_collisions_checked=False,
                samples=count,linear_step_m=.003,initial_penetration_m=initial,maximum_penetration_m=worst,
                phase_maxima=phase_max,failures=failed,passed=not failed)
    report.update(flexible_cable_collision_path_checked=not bool(excluded),
                  flexible_cable_minimum_endpoint_slack_m=min(slack) if slack else None)
    print(json.dumps(report,indent=2));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(audit(Path(__file__).resolve().parent))
