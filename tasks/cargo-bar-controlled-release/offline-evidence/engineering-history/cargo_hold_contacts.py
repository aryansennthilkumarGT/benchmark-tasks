exec(open('/tmp/cargo_hold_duration.py').read().split('for k in')[0])
spec=copy.deepcopy(base)
for a in spec['assemblies']:
 for j in a['joints']:
  if j['name'] in ('left_compliance','right_compliance'):j['stiffness']=24000.
m=mujoco.MjModel.from_xml_string(export(spec));d=mujoco.MjData(m);initialize(m,d,spec)
for n in range(960):mujoco.mj_step(m,d)
result=[]
for i,c in enumerate(d.contact[:d.ncon]):
 names=[mujoco.mj_id2name(m,mujoco.mjtObj.mjOBJ_BODY,m.geom_bodyid[g]) for g in [c.geom1,c.geom2]]
 if not set(names)&{'left_pad','right_pad'}:continue
 f=np.zeros(6);mujoco.mj_contactForce(m,d,i,f)
 result.append(dict(bodies=names,pos=c.pos.tolist(),frame=c.frame.tolist(),wrench=f.tolist(),friction=c.friction.tolist(),depth=c.dist,dim=c.dim,efc_state=d.efc_state[c.efc_address:c.efc_address+4].tolist()))
print(json.dumps(result,indent=2));print('ncon',d.ncon,'nv',m.nv,'efc',d.nefc,'qvel',d.qvel[:6])
