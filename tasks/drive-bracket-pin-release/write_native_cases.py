"""Standalone contact/control probes; initialized states are not demonstrations."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent;s=json.loads((p/'scene.json').read_text());plan=json.loads((p/'controller.json').read_text())
cases={'physics':[
 dict(name='closed-pins-resist-straight-lift',forces=[dict(assembly='drive_asset',body='drive',force=[0,0,2.])],steps=20,settle_steps=20,assertions=[dict(kind='coordinate',body='drive',axis=2,min=s['score_spec']['initial_drive'][2]-.0003,max=s['score_spec']['initial_drive'][2]+.0015),dict(kind='penetration',max=.00035),dict(kind='score',max=0,success=False)]),
 dict(name='force-opens-compliant-rail',forces=[dict(assembly='bracket_asset',body='release_rail',force=[0,1.08,0])],steps=40,settle_steps=0,assertions=[dict(kind='joint',joint='rail_flexure',min=.005,max=.0071),dict(kind='valid'),dict(kind='penetration',max=.00035)]),
 dict(name='released-rail-returns',initialize_joints=[dict(assembly='bracket_asset',joint='rail_flexure',value=.006)],steps=80,settle_steps=20,assertions=[dict(kind='joint',joint='rail_flexure',min=-.0002,max=.0005),dict(kind='score',max=0,success=False),dict(kind='penetration',max=.00035)])], 'control':[]}
for name,label,limit in [('release-and-opposite-pin-prefix','Slide away from opposite locating pins',3500),('removal-and-stage-prefix','Withdraw extraction gripper',6500)]:
 i=next(i for i,x in enumerate(plan['phases']) if x['label']==label)
 assertions=[dict(kind='valid'),dict(kind='penetration',max=.00035)]
 if 'stage' in name:assertions.append(dict(kind='pose',body='drive',pos=s['score_spec']['target_drive'],tolerance=.0015,quat=[0,0,0,1],angle=.025))
 else:assertions.append(dict(kind='joint',joint='rail_flexure',min=.0045,max=.0071))
 cases['control'].append(dict(name=name,through_phase=i,through_label=label,max_steps=limit,assertions=assertions))
(p/'native-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
