exec(open('/tmp/cargo_hold_duration.py').read().split('for k in')[0])
from kinematics import reconstruct
for teeth,k in [(8,8000.),(8,10000.),(7,12000.)]:
 spec=copy.deepcopy(base);extension=teeth*(2*np.pi/24)*spec['parameters']['authored_pinion_pitch_radius'];compression=(extension-.020)/2
 init=spec['initial_joint_values'];init.update(telescope=extension,pinion_rotation=-extension/spec['parameters']['authored_pinion_pitch_radius'],left_compliance=compression,right_compliance=-compression)
 rootpose=dict(pos=[.24,-.010-compression,.7975],quat=[0.,-2**-.5,0.,2**-.5]);poses=reconstruct(spec,rootpose,init)
 for a in spec['assemblies']:
  for j in a['joints']:
   j['initial']=init[j['name']]
   if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=k;j['damping']=2.
  for b in a['bodies']:
   if b['name'] in poses:b.update(poses[b['name']])
 xml=export(spec)
 if teeth==7:xml=xml.replace("margin=\"3e-05\"",'margin=".00003" gap=".00003"')
 m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m);initialize(m,d,spec);origin=np.array(observe(m,d,spec)['bodies']['outer_tube']['pos']);samples=[]
 for n in range(9600):
  mujoco.mj_step(m,d)
  if (n+1)%960==0:
   r=observe(m,d,spec);samples.append(dict(time=r['time'],displacement_m=float(np.linalg.norm(np.array(r['bodies']['outer_tube']['pos'])-origin)),joints=r['joints']))
 row=dict(stiffness=k,teeth=teeth,normal_load_N=compression*k,samples=samples);result.append(row);print(json.dumps(row),flush=True)
Path('/tmp/cargo-hold-soft.json').write_text(json.dumps(result,indent=2))
