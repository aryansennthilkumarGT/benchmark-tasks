"""Original full-size interface, manufacturer-compatible eye, no OEM internals claim."""
MODE='BENCHMARK_AUTHORED'
TABLE=.7475
ROOT=[.24,0.,.805]
INCH=.0254
# Manufacturer-documented compatibility bounds, XL-PH351 RevF p1.
EYE_ID_RANGE=[2.375*INCH,3.*INCH]
EYE_BAR_RANGE=[1.25*INCH,1.625*INCH]
MOUNT_WIDTH=4.5*INCH
BOLT_SPAN_Y=3.38*INCH
BOLT_SPAN_Z=1.75*INCH
BOLT_DIAMETER=.5*INCH
# Authored selections within those bounds, not manufacturer measurements.
EYE_ID=2.5*INCH
EYE_BAR=1.25*INCH
EYE_MAJOR=(EYE_ID+EYE_BAR)/2
EYE_MINOR=EYE_BAR/2
EYE_FACETS=64
BAR_FACETS=16
HORN_X=.108
HORN_TOP=.092
HORN_WIDTH=.034
SEAT_TOP=.010
EYE_SEAT=[HORN_X,0.,SEAT_TOP+EYE_MINOR]
EYE_START=[ROOT[0]+HORN_X,-.23,ROOT[2]+EYE_SEAT[2]]
LATCH_PIVOT=[.015,0.,.110]
LOCK_PIVOT=[.015,0.,.012]
LATCH_OPEN=-1.5
LOCK_OPEN=-.65
LOCK_SPRING=.14
LOCK_DAMPING=.002
INITIAL={'latch_rotation':0.,'lock_rotation':0.}
STEM_GRIP=[.108,0.,0.]
LOCK_GRIP=[.035,0.,.002]


def validate_mode(mode=MODE,measurement_evidence=None,manufacturer_evidence=None):
 if mode=='BENCHMARK_AUTHORED':return dict(mode=mode,independently_measured=False,manufacturer_cad_claimed=False)
 if mode=='INDEPENDENTLY_MEASURED':
  raise ValueError('No independently measured fixture dataset exists; arbitrary evidence cannot relabel authored geometry')
 if mode=='MANUFACTURER_DOCUMENTED':
  raise ValueError('The manual supplies compatibility/envelope data, not full internal CAD or contact parameters')
 raise ValueError('Unknown geometry provenance mode')
