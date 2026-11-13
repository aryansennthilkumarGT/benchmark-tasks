# Complete parameter and reproduction table

M manufacturer-documented; A benchmark-authored; D derived. There are no independently measured values. Every expanded numeric scene value, including every solid vertex, appears in parameter-provenance.json. Raw primitive coordinates are canonical scene.json; original decomposition/formulas are in cad.py/generate_scene.py.

| Source parameter | Value (SI unless stated) | Classification | Evidence |
|---|---|---|---|
|TABLE|0.7475|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|ROOT|[0.37, 0.0, 0.86]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|BALL_DIAMETER|0.007|Manufacturer-documented|Bosch GBH2-26 parts record1903230013; SOURCES.json|
|BALL_X|0.02|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|BALL_Z|0.007824|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SHAFT_RADIUS|0.005|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SHANK_LENGTH|0.045|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|BIT_LENGTH|0.2|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|BALL_RADIUS|0.0035|Derived from other explicitly stated geometry|BALL_DIAMETER/2|
|HOLDER_INNER|0.00515|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|HOLDER_OUTER|0.0062|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|PORT_HALF|0.0031|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|COLLAR_BORE_CLOSED|0.0116|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|COLLAR_BORE_RELEASED|0.0134|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|COLLAR_OUTER|0.0185|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|COLLAR_TRAVEL|0.008|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SLOT_REAR|-0.028|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SLOT_FLOOR_REAR|-0.026|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SLOT_FLOOR_FRONT|-0.019|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SLOT_FRONT|-0.017|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|SLOT_RADIUS|0.0038|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|KEY_RADIUS|0.0038|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|OPEN_GROOVE_RADIUS|0.0036|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|STEM_INSERTION|0.04|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|OLD_GRIP|[-0.14, 0.0, 0.002]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|NEW_GRIP|[-0.13, 0.0, 0.002]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|COLLAR_GRIP|[0.02, 0.0035355339059327372, 0.0035355339059327372]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|OLD_TRAY|[0.27, -0.3, 0.7495]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|
|NEW_CRADLE|[0.27, 0.3, 0.7495]|Benchmark-authored approximation|Original inert fixture design; not OEM measurement|

| Additional authored interface | Specification |
|---|---|
| Ball race | Front center19.95mm to rear24.55mm; forward locked range19.4–21.0mm |
| Inner retaining lips | transverse half-gap3.1mm; z=6.2mm+0.10(x−20mm) overx16.9–27.6mm |
| Outer guides | lateral half-gap3.55mm; free ball rotation; no slider/weld |
| Sleeve bore |13.40mm radius throughx15mm; transition to11.60 at17; locking land17–22; rear relief to13.40 at24; rear end35mm |
| Sleeve spring |2000N/m,5N·s/m,rest−1mm; forward stop0,travel8mm;2N preload |
| Open drive interface | shank groove floor3.6mm; key inner radius3.8mm and1.4mm tangential width; starts5mm into holder |
| Running fit | nominal shankR5mm / holder boreR5.15mm;0.15mm radial authored clearance |
| Cage lateral clearance |7.1mm guide opening /7mm nominal ball;0.05mm nominal radial clearance; faceting affects actual contact |
| Materials | steel7850kg/m³; clear glass2500; clear polycarbonate1200; fixed-fixture default2700. Authored assumptions, not OEM measured properties |
| Friction | dry static0.65/dynamic0.45; lubricated0.18/0.12; restitution0 |
| Numerics |1920Hzphysics/20Hzcontrol;20um contact offset,zero rest;200um max overlap |

The gravity-biased race and relieved locking sleeve are original engineered approximations of the documented external SDS operation, not claimed OEM hidden geometry. The manufacturer establishes the procedure and7mm ball; no forces/torques or other dimensions are invented as manufacturer specifications.

| Body | Mass kg | COM m(D) | Principal inertia kg·m²(D) |
|---|---:|---|---|
|tool_holder|3.0|[0.11650922988711, -8.5223094e-07, -0.05462670990598]|[0.00945907207752, 0.01158549382427, 0.01343027435466]|
|locking_sleeve|0.04062953859164648|[0.01702260267183, -0.00045760832498, -0.00050489298208]|[8.26345694e-06, 8.61599432e-06, 9.05630921e-06]|
|locking_ball|0.0014098158832371998|[0.0, 0.0, 0.0]|[6.9081e-09, 6.9081e-09, 6.9081e-09]|
|used_point_chisel|0.15383515794547392|[-0.10225006173439, -0.0, 0.0]|[2.5795225e-06, 0.00042058577421, 0.00042060134471]|
|replacement_flat_chisel|0.1613711579454739|[-0.10640634060918, -0.0, 0.0]|[2.8743685e-06, 0.00047771211396, 0.00047793298546]|
|used_chisel_tray|0.45|[0.0, 0.0, 0.00393939393939]|[0.00037723471074, 0.00255032561983, 0.00289352727273]|
|replacement_cradle|0.45|[-0.00352414887192, 0.0, 0.00534871345438]|[0.00033888416526, 0.00231860450747, 0.00260994456074]|

Chisel/sleeve masses derive from explicit non-overlapping material volumes. Ball target mass derives from documented7mm diameter and authored7850kg/m³ density using4πr³/3. Fixed-fixture target masses are A. Compound overlaps count twice; normalized moments are not exact boolean CAD or measured hardware. Complete expanded numeric provenance: 93292 values.
