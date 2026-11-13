"""Explicit provenance for an original SDS-plus inspired inert test fixture.

M means genuinely manufacturer documented, A benchmark authored, D derived.
No measured hardware mode is enabled without real measurement evidence.
"""
from enum import Enum
import math
class GeometryMode(str,Enum):
 BENCHMARK_AUTHORED='BENCHMARK_AUTHORED'
 MEASURED_HARDWARE='MEASURED_HARDWARE'
MODE=GeometryMode.BENCHMARK_AUTHORED
TABLE=.7475
ROOT=[.37,0.,.86]
BALL_DIAMETER=.007  # M: Bosch GBH2-26 parts1903230013 DIN5401-Ø7MM-III-ST
BALL_X=.020
BALL_Z=.007824
SHAFT_RADIUS=.005  # A: nominal10mm benchmark shank, no claimed OEM dimensional compatibility
SHANK_LENGTH=.045
BIT_LENGTH=.200
BALL_RADIUS=BALL_DIAMETER/2
HOLDER_INNER=.00515
HOLDER_OUTER=.00620
PORT_HALF=.00310
COLLAR_BORE_CLOSED=.01160
COLLAR_BORE_RELEASED=.01340
COLLAR_OUTER=.01850
COLLAR_TRAVEL=.008
SLOT_REAR=-.028
SLOT_FLOOR_REAR=-.026
SLOT_FLOOR_FRONT=-.019
SLOT_FRONT=-.017
SLOT_RADIUS=.00380
KEY_RADIUS=.00380
OPEN_GROOVE_RADIUS=.00360
STEM_INSERTION=.040
OLD_GRIP=[-.140,0.,.002]
NEW_GRIP=[-.130,0.,.002]
COLLAR_GRIP=[.020,.005/math.sqrt(2),.005/math.sqrt(2)]
OLD_TRAY=[.27,-.30,TABLE+.002]
NEW_CRADLE=[.27,.30,TABLE+.002]
PARAMETERS={n:dict(value=v,classification=('Manufacturer-documented' if n=='BALL_DIAMETER' else 'Derived from other explicitly stated geometry' if n=='BALL_RADIUS' else 'Benchmark-authored approximation'),source=('Bosch GBH2-26 parts record1903230013; SOURCES.json' if n=='BALL_DIAMETER' else 'BALL_DIAMETER/2' if n=='BALL_RADIUS' else 'Original inert fixture design; not OEM measurement')) for n,v in list(globals().items()) if n.isupper() and isinstance(v,(int,float,list))}

def validate(mode=MODE,measurement_evidence=None):
 mode=GeometryMode(mode)
 if mode==GeometryMode.MEASURED_HARDWARE:
  raise ValueError('This authored fixture has no independently measured parameter dataset; a mode switch or arbitrary evidence dict cannot create one')
 if not all(p['classification'] and p['source'] for p in PARAMETERS.values()):raise ValueError('Unclassified parameter')
 assert BALL_RADIUS==BALL_DIAMETER/2 and HOLDER_INNER>SHAFT_RADIUS>OPEN_GROOVE_RADIUS
 assert SLOT_REAR<SLOT_FLOOR_REAR<SLOT_FLOOR_FRONT<SLOT_FRONT<0
 assert 0<COLLAR_BORE_CLOSED-BALL_RADIUS<SHAFT_RADIUS+BALL_Z
 return True
