"""Actual future native probes; initialized states are not demonstrations."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent;s=json.loads((p/'scene.json').read_text());plan=json.loads((p/'controller.json').read_text());target=s['score_spec']['target']
cases={'physics':[
 dict(name='prepared-cradle-gravity',steps=60,settle_steps=20,assertions=[dict(kind='displacement',body='collet',min=0,max=.001),dict(kind='penetration',max=.00035),dict(kind='score',max=0,success=False),dict(kind='valid')]),
 dict(name='supported-preassembly-is-not-history',initialize_bodies=[dict(assembly='collet_asset',pos=target,quat=[0,0,0,1])],steps=60,settle_steps=20,assertions=[dict(kind='pose',body='collet',pos=target,tolerance=.0006),dict(kind='penetration',max=.00035),dict(kind='score',max=0,success=False)]),
 dict(name='cam-contact-descent-probe',initialize_bodies=[dict(assembly='collet_asset',pos=[target[0],target[1],target[2]+.012],quat=[0,0,0,1])],forces=[dict(assembly='collet_asset',body='collet',force=[0,0,-1.])],steps=20,settle_steps=20,assertions=[dict(kind='coordinate',body='collet',axis=2,min=target[2]-.001,max=target[2]+.014),dict(kind='penetration',max=.00035)])], 'control':[]}
for name,label,limit in [('eccentric-hook-prefix','Engage groove at eccentric hook',1200),('supported-preassembly-prefix','Withdraw above preassembly',2400)]:
 i=next(i for i,x in enumerate(plan['phases']) if x['label']==label)
 assertions=[dict(kind='valid'),dict(kind='penetration',max=.00035)]
 if name.startswith('supported'):assertions.append(dict(kind='pose',body='collet',pos=target,tolerance=.0007))
 cases['control'].append(dict(name=name,through_phase=i,through_label=label,max_steps=limit,assertions=assertions))
(p/'native-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
