"""Author diagnostic probes. Initializations are never expert evidence."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
s=json.loads((p/'scene.json').read_text());plan=json.loads((p/'controller.json').read_text())
ss=s['score_spec'];d=s['parameters'];names=ss['retainers']
carrier=dict(assembly='carrier_asset',pos=[.24,0.,ss['carrier_seat_z']],quat=[0,0,0,1])
first=ss['studs'][0];final=first['tip_z']-d['retainer_height']/2
nut=dict(assembly='nut0_asset',pos=[*first['axis_xy'],final],quat=[0,0,0,1])
cases={'physics':[
 dict(name='prepared-layout-gravity-reset',steps=80,settle_steps=20,assertions=[dict(kind='displacement',body='carrier',min=0,max=.002),dict(kind='penetration',max=.00035),dict(kind='score',min=0,max=0,success=False),dict(kind='valid')]),
 dict(name='unloaded-carrier-seat',initialize_bodies=[carrier],steps=100,settle_steps=20,assertions=[dict(kind='coordinate',body='carrier',axis=2,min=ss['carrier_seat_z']-.0005,max=ss['carrier_seat_z']+.0005),dict(kind='penetration',max=.00035),dict(kind='score',min=.25,max=.25,success=False)]),
 dict(name='threaded-retainer-axial-retention',initialize_bodies=[carrier,nut],forces=[dict(assembly='nut0_asset',body='nut0',force=[0,0,2.])],steps=40,settle_steps=20,assertions=[dict(kind='coordinate',body='nut0',axis=2,min=final-.0006,max=final+.0006),dict(kind='penetration',max=.00035),dict(kind='score',max=.25,success=False)]),
 dict(name='no-rotation-press-through',initialize_bodies=[carrier,dict(assembly='nut0_asset',pos=[*first['axis_xy'],first['tip_z']+d['retainer_height']/2],quat=[0,0,0,1])],forces=[dict(assembly='nut0_asset',body='nut0',force=[0,0,-2.])],steps=40,settle_steps=20,assertions=[dict(kind='coordinate',body='nut0',axis=2,min=first['tip_z']+d['retainer_height']/2-d['retainer_thread_pitch'],max=first['tip_z']+d['retainer_height']/2+.001),dict(kind='penetration',max=.00035),dict(kind='score',max=.25,success=False)])
 ],'control':[]}
for name,label,maxsteps in [('carrier-placement-prefix','Park carrier arm',6000),('first-retainer-prefix','Withdraw from retainer 1',16000)]:
 index=next(i for i,x in enumerate(plan['phases']) if x['label']==label)
 assertions=[dict(kind='coordinate',body='carrier',axis=2,min=ss['carrier_seat_z']-.0005,max=ss['carrier_seat_z']+.0005),dict(kind='valid'),dict(kind='penetration',max=.00035)]
 if 'retainer' in name:assertions.append(dict(kind='coordinate',body='nut0',axis=2,min=final-.0003,max=final+.0003))
 cases['control'].append(dict(name=name,through_phase=index,through_label=label,max_steps=maxsteps,assertions=assertions))
(p/'native-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
