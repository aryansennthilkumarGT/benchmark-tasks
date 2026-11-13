# Fixture parameters and provenance

Geometry mode: **BENCHMARK_AUTHORED**. None of the component geometry or material parameters in this fixture is independently measured LuK hardware. No measurement evidence is claimed. `uncertainty=0` denotes exact authored numerical input, not zero physical uncertainty. Target manufacturing tolerance is ±0.05 mm on mating dimensions, ±5 g on authored masses; assembly clearances and scorer tolerances are independent.

The three-stud count and 120° spacing are manufacturer-documented. Manufacturer kit data supports the availability of flywheel-side thread families; choosing an M8×1.25 prepared lower interface is authored, and does not determine the separate custom upper thread. No undocumented value is silently inferred from a kit label or photograph.

| Parameter | Value | Unit | Classification / basis |
|---|---|---|---|
| stud_circle_radius | 0.062 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| stud_tip_height | 0.09 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| stud_thread_length | 0.018 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_thickness | 0.008 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_slot_inner_radius | 0.044 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_slot_outer_radius | 0.08 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_slot_width | 0.014 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_centre_bore | 0.02 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retracted_spindle_inner_bore | 0.019 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| centring_tool_outer_diameter | 0.015 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| carrier_mass | 0.46 | kg | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_diameter | 0.028 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_height | 0.012 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_thread_length | 0.012 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_mass | 0.047 | kg | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_thread_major | 0.012 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| retainer_thread_pitch | 0.003 | m | Benchmark-authored approximation; fixture-profile.json / dimensions.py |
| flywheel_thread_major | 0.008 | m | Manufacturer-documented available family; benchmark-selected application; fixture-profile.json / dimensions.py |
| flywheel_thread_pitch | 0.00125 | m | Manufacturer-documented available family; benchmark-selected application; fixture-profile.json / dimensions.py |
| stud_count | 3 | count | Manufacturer-documented; LuK section 10.6 p28 |
| stud_angular_spacing | 120 | degree | Manufacturer-documented; LuK section 10.6 p28 |
| upper_thread_segments_per_turn | 64 | count | Benchmark-authored approximation; generate_scene.helix |
| upper_thread_flank_relief | 0.0002 | m | Benchmark-authored approximation; generate_scene.helix |
| upper_thread_root_radial_clearance | 0.0002 | m | Derived from other explicitly stated geometry; female inner 4.9 mm - male root 4.7 mm |
| upper_thread_shell_radial_clearance | 0.00035 | m | Derived from other explicitly stated geometry; female shell bore 6.35 mm - male crest 6 mm |
| slot_diametral_clearance | 0.002 | m | Derived from other explicitly stated geometry; 14 mm slot - 12 mm upper stud |
| spindle_mandrel_diametral_clearance | 0.004 | m | Derived from other explicitly stated geometry; 19 mm bore - 15 mm mandrel |
| carrier_mandrel_diametral_clearance | 0.005 | m | Derived from other explicitly stated geometry; 20 mm carrier bore - 15 mm mandrel |
| fixture_mass | 5.0 | kg | Benchmark-authored approximation; generate_scene.py |
| carrier_tray_mass | 1.0 | kg | Benchmark-authored approximation; generate_scene.py |
| retainer_tray_mass | 1.0 | kg | Benchmark-authored approximation; generate_scene.py |
| static_friction | 0.65 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| dynamic_friction | 0.5 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| restitution | 0.0 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| steel_density | 7850.0 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| contact_offset | 3e-05 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| rest_offset | 0.0 | SI | Benchmark-authored approximation; scene.json material / build_assets.py / arena_runtime.py |
| gravity | [0, 0, -9.81] | m/s^2 | Benchmark-authored approximation; standard station choice |
| physics_dt | 0.0020833333333333333 | s | Benchmark-authored approximation; native integration setting |
| control_hz | 20 | Hz | Benchmark-authored approximation; YAM policy interface |
| run_limit | 42000 | actions | Benchmark-authored approximation; pending native timing |
| table_top | 0.7475 | m | Benchmark-authored approximation; pinned station table convention |
| scoring.carrier_seat_z | 0.8215000000000001 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.retainer_top_offset | 0.006 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.pitch | 0.003 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.lateral_tolerance | 0.00065 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.axial_tolerance | 0.0003 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.tilt_tolerance | 0.025 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.hold_seconds | 2.0 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.penetration_limit | 0.00035 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.thread_phase_tolerance | 0.35 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.fixture_tolerance | 0.001 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.control_hz | 20 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.speed_limit | 0.008 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.spin_limit | 0.15 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.release_clearance | 0.02 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |
| scoring.loss_plane | 0.7275 | SI | Benchmark-authored approximation; score_spec; numerical benchmark acceptance tolerance |

`parameters.csv` additionally enumerates every body initial pose, quaternion, bounding extent, inertia and local collider dimension/pose, all generated from the stated construction recipe. `scene.json` contains exact machine-readable complete bodies. `generate_scene.py` is the manufacturing geometry source; `assets/*.usda` is its collision/visual export. No hidden simplified solid bore, grasp joint, attractive magnet or success-triggered drive is present.
