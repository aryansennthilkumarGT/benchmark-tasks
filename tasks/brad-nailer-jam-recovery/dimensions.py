"""Original reproducible service fixture; no claimed OEM hardware dimensions.

Only documented operation, supported fastener range,18GA class and external latch topology are attributed
to DeWalt. The numerical design below is BENCHMARK_AUTHORED, with derived draw
lengths explicitly computed. No manufacturer or measured mode silently falls
back to this design.
"""
import math
MODE='BENCHMARK_AUTHORED'
TABLE=.7475
ROOT=[.23,.06,.805]
BASE_Q=[1.,0.,0.,0.]  # nose+X, service face-Y; gravity is local+Z
DOOR_PIVOT=[0.,.0035,0.]
LEVER_PIVOT=[.055,.0072,0.]
ECCENTRIC=[-.005,-.00115,0.]
PIN_RADIUS=.0011
HOOK_UNDER=.0082
NOMINAL_PIN_CLOSED=[.0946,.0066,0.]  # authored guide target within 1mm hook throat
INITIAL_CONTACT_DEFLECTION=.000005  # authored numerical elastic-contact initialization, not a machined solid overlap
PIN_CLOSED=[NOMINAL_PIN_CLOSED[0]-INITIAL_CONTACT_DEFLECTION,HOOK_UNDER-PIN_RADIUS,0.]  # loaded lip contact
END_PRELOAD=.0005
PIN_LENGTH=.052  # authored exposed end for stock-gripper access; not an OEM measurement
BAIL_HALF_SPAN=.018
SPRING=20000.
HINGE_POINT=[DOOR_PIVOT[i]+LEVER_PIVOT[i] for i in range(3)]
ECCENTRIC_CLOSED=[HINGE_POINT[i]+ECCENTRIC[i] for i in range(3)]
DRAW_VECTOR=[PIN_CLOSED[i]-ECCENTRIC_CLOSED[i] for i in range(3)]
DRAW_LENGTH=math.hypot(DRAW_VECTOR[0],DRAW_VECTOR[1])
DRAW_REST=DRAW_LENGTH-END_PRELOAD
BAIL_CLOSED=math.atan2(DRAW_VECTOR[1],DRAW_VECTOR[0])
LEVER_GRIP=[-.028,.002,-.019]
DOOR_GRIP=[.025,0.,-.022]
PIN_GRIP=[0.,0.,-.023]
INITIAL={'door_rotation':0.,'lever_rotation':0.,'bail_rotation':BAIL_CLOSED,'bail_extension':END_PRELOAD}


def validate_mode(mode=MODE,measurement_evidence=None,manufacturer_evidence=None):
 if mode=='BENCHMARK_AUTHORED':return dict(mode=mode,independently_measured=False,manufacturer_dimensions_claimed=False)
 if mode=='INDEPENDENTLY_MEASURED':
  if not measurement_evidence:raise ValueError('Genuine measurement records required; authored geometry cannot establish measurements')
  raise ValueError('Measured-mode fixture is not implemented from authenticated measurement data')
 if mode=='MANUFACTURER_DOCUMENTED':
  if not manufacturer_evidence:raise ValueError('Manufacturer dimensional evidence required')
  raise ValueError('Manufacturer instructions do not specify this fixture geometry')
 raise ValueError('Unknown geometry provenance mode')
