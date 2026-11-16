"""External-measurement protocol. No case name, installedflag or action count input.
All limits are authored coupon criteria, NOT Toshiba tolerances.
"""
import math

def physical_score(before,after,input_rotation,output_rotation,seated_height=.0145):
 def seated(o,tolerance,tilt):
  return (abs(o['tray_center_z_m']-seated_height)<tolerance and o['tilt_deg']<tilt and o['radial_offset_m']<.002 and len(o['wheel_contacts'])==3 and o['external_support_contacts']==0)
 pre=seated(before,.0004,1.)
 tracking=abs(output_rotation-input_rotation)<.25 and abs(output_rotation)>2*math.pi
 retained=seated(after,.0005,1.2)
 rolling=len(before['wheel_angles_rad'])==3 and all(abs(after['wheel_angles_rad'].get(k,0)-a)>.05 for k,a in before['wheel_angles_rad'].items())
 score=1. if pre and tracking and retained and rolling else (.25 if len(before['wheel_contacts'])==3 and before['external_support_contacts']==0 and before['tilt_deg']<1 else 0.)
 return dict(score=score,released_seated_before_drive=pre,driven_transmission=tracking,retained_after_drive=retained,all_three_wheels_roll=rolling)
