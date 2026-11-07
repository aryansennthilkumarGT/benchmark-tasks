# Correct two latched patch connections while preserving a third — physical setup

Bimanual YAM station; x forward, y left, z up; metres/kg/radians; XYZW quaternions. Tabletop z=0.7475 m. Fixed layout, seed 0, no object jitter. 

Geometry is original primitive construction. All movable components use friction 0.65 static / 0.5 dynamic and restitution 0. Joint damping, spring constants and contact pairs are specified below and in `scene.json`. Explicit inertias/centers of mass override shape-derived values where present. Extended handling tabs are part of the bench fixture, not a claim of commercial-product fidelity.

| Body | Material/type | Mass kg | Envelope m | World origin m | XYZW | Constraint |
|---|---|---:|---|---|---|---|
| `port_0` | rigid engineering plastic | 0.2 | (0.038, 0.05, 0.033) | (0.2, -0.1, 0.7825) | (0, 0, 0, 1) | anchored |
| `port_1` | rigid engineering plastic | 0.2 | (0.038, 0.05, 0.033) | (0.3, -0.1, 0.7825) | (0, 0, 0, 1) | anchored |
| `port_2` | rigid engineering plastic | 0.2 | (0.038, 0.05, 0.033) | (0.4, -0.1, 0.7825) | (0, 0, 0, 1) | anchored |
| `anchor_0` | rigid fixture material | 0.08 | (0.014, 0.012, 0.008) | (0.31, 0.26, 0.7515) | (0, 0, 0, 1) | anchored |
| `cable_0_0_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.31, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_0_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.31, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_0` | rigid fixture material | 0.0015 | (0.0168203, 0.0191908, 0.00699851) | (0.315608, 0.2525, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_1_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.321215, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_1_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.321215, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_1` | rigid fixture material | 0.0015 | (0.0166167, 0.0191269, 0.0069878) | (0.326704, 0.2375, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_2_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.332193, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_2_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.332193, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_2` | rigid fixture material | 0.0015 | (0.0162111, 0.0189954, 0.0069639) | (0.337447, 0.2225, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_3_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.3427, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_3_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.3427, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_3` | rigid fixture material | 0.0015 | (0.015606, 0.0187895, 0.00692164) | (0.347607, 0.2075, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_4_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.352514, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_4_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.352514, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_4` | rigid fixture material | 0.0015 | (0.0148026, 0.0185, 0.00685296) | (0.35697, 0.1925, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_5_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.361426, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_5_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.361426, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_5` | rigid fixture material | 0.0015 | (0.0137994, 0.0181177, 0.00674667) | (0.365335, 0.1775, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_6_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.369244, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_6_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.369244, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_6` | rigid fixture material | 0.0015 | (0.0125894, 0.0176378, 0.00658885) | (0.372523, 0.1625, 0.751505) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_7_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.375801, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_7_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.375801, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_7` | rigid fixture material | 0.0015 | (0.0111603, 0.017066, 0.00636437) | (0.378377, 0.1475, 0.751513) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_8_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.380953, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_8_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.380953, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_8` | rigid fixture material | 0.0015 | (0.00949971, 0.0164269, 0.0060604) | (0.38277, 0.1325, 0.75153) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_9_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.384588, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_9_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.384588, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_9` | rigid fixture material | 0.0015 | (0.00760575, 0.0157683, 0.00567204) | (0.385604, 0.1175, 0.751565) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_10_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.38662, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_10_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.38662, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_10` | rigid fixture material | 0.0015 | (0.00550282, 0.015157, 0.00520865) | (0.38681, 0.1025, 0.75163) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_11_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.387, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_11_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.387, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_11` | rigid fixture material | 0.0015 | (0.00667537, 0.0155067, 0.0055537) | (0.386355, 0.0875, 0.751744) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_12_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.385711, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_12_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.385711, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_12` | rigid fixture material | 0.0015 | (0.00868872, 0.0161894, 0.00610541) | (0.38424, 0.0725, 0.751935) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_13_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.382769, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_13_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.382769, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_13` | rigid fixture material | 0.0015 | (0.0104869, 0.0168839, 0.00660919) | (0.380498, 0.0575, 0.752242) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_14_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.378226, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_14_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.378226, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_14` | rigid fixture material | 0.0015 | (0.0120597, 0.0175301, 0.00708223) | (0.375195, 0.0425, 0.752718) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_15_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.372165, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_15_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.372165, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_15` | rigid fixture material | 0.0015 | (0.0134163, 0.0180905, 0.0075559) | (0.368432, 0.0275, 0.753437) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_16_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.364699, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_16_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.364699, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_16` | rigid fixture material | 0.0015 | (0.0145709, 0.0185503, 0.00807009) | (0.360335, 0.0125, 0.754493) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_17_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.355971, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_17_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.355971, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_17` | rigid fixture material | 0.0015 | (0.0155336, 0.018911, 0.00866865) | (0.351061, -0.0025, 0.756009) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_18_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.346151, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_18_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.346151, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_18` | rigid fixture material | 0.0015 | (0.0163075, 0.0191825, 0.00939699) | (0.340789, -0.0175, 0.758142) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_19_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.335428, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_19_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.335428, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_19` | rigid fixture material | 0.0015 | (0.0168898, 0.0193781, 0.0103009) | (0.329719, -0.0325, 0.761087) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_20_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.324011, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_20_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.324011, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_20` | rigid fixture material | 0.0015 | (0.017274, 0.0195114, 0.0114259) | (0.318068, -0.0475, 0.765087) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_21_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.312124, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_21_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.312124, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_link_21` | rigid fixture material | 0.0015 | (0.0174514, 0.0195954, 0.0128175) | (0.306062, -0.0625, 0.770443) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_connector_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.3, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `cable_0_connector_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.3, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `plug_0` | rigid engineering plastic | 0.016 | (0.022, 0.075, 0.019) | (0.3, -0.1, 0.7825) | (0, 0, 0, 1) | passive dynamic |
| `latch_0` | rigid engineering plastic | 0.002 | (0.014, 0.216, 0.0265) | (0.3, -0.1, 0.797) | (0, 0, 0, 1) | passive dynamic |
| `anchor_1` | rigid fixture material | 0.08 | (0.014, 0.012, 0.008) | (0.16, 0.26, 0.7515) | (0, 0, 0, 1) | anchored |
| `cable_1_0_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.16, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_0_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.16, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_0` | rigid fixture material | 0.0015 | (0.0156391, 0.0188011, 0.00692405) | (0.155074, 0.2525, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_1_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.150148, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_1_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.150148, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_1` | rigid fixture material | 0.0015 | (0.0154297, 0.0187275, 0.00690763) | (0.145341, 0.2375, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_2_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.140534, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_2_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.140534, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_2` | rigid fixture material | 0.0015 | (0.0150113, 0.0185768, 0.00687183) | (0.135962, 0.2225, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_3_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.131391, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_3_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.131391, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_3` | rigid fixture material | 0.0015 | (0.014384, 0.0183428, 0.00681055) | (0.127165, 0.2075, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_4_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.12294, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_4_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.12294, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_4` | rigid fixture material | 0.0015 | (0.0135452, 0.0180179, 0.00671443) | (0.119166, 0.1925, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_5_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.115392, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_5_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.115392, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_5` | rigid fixture material | 0.0015 | (0.0124888, 0.0175969, 0.00657096) | (0.112165, 0.1775, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_6_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.108938, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_6_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.108938, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_6` | rigid fixture material | 0.0015 | (0.0112034, 0.0170818, 0.00636543) | (0.106341, 0.1625, 0.751505) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_7_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.103744, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_7_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.103744, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_7` | rigid fixture material | 0.0015 | (0.00967554, 0.0164896, 0.00608347) | (0.10185, 0.1475, 0.751513) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_8_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0999556, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_8_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0999556, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_8` | rigid fixture material | 0.0015 | (0.00789731, 0.0158583, 0.00571565) | (0.0988204, 0.1325, 0.75153) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_9_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0976852, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_9_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0976852, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_9` | rigid fixture material | 0.0015 | (0.00588066, 0.015247, 0.00526372) | (0.0973508, 0.1175, 0.751565) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_10_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0970165, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_10_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.0970165, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_10` | rigid fixture material | 0.0015 | (0.00628688, 0.0153737, 0.00540002) | (0.0975082, 0.1025, 0.75163) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_11_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.098, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_11_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.098, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_11` | rigid fixture material | 0.0015 | (0.00835195, 0.0160469, 0.00593825) | (0.0993264, 0.0875, 0.751744) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_12_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.100653, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_12_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.100653, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_12` | rigid fixture material | 0.0015 | (0.010236, 0.0167564, 0.00642201) | (0.102805, 0.0725, 0.751935) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_13_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.104958, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_13_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.104958, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_13` | rigid fixture material | 0.0015 | (0.011916, 0.0174371, 0.00685882) | (0.107911, 0.0575, 0.752242) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_14_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.110865, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_14_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.110865, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_14` | rigid fixture material | 0.0015 | (0.0133945, 0.0180419, 0.00727246) | (0.114577, 0.0425, 0.752718) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_15_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.11829, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_15_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.11829, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_15` | rigid fixture material | 0.0015 | (0.0146843, 0.0185479, 0.00769756) | (0.122705, 0.0275, 0.753437) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_16_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.127119, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_16_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.127119, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_16` | rigid fixture material | 0.0015 | (0.0157966, 0.0189513, 0.00817451) | (0.132165, 0.0125, 0.754493) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_17_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.137211, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_17_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.137211, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_17` | rigid fixture material | 0.0015 | (0.016736, 0.01926, 0.00874626) | (0.142803, -0.0025, 0.756009) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_18_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.148395, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_18_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.148395, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_18` | rigid fixture material | 0.0015 | (0.0175005, 0.0194865, 0.00945692) | (0.154438, -0.0175, 0.758142) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_19_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.160481, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_19_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.160481, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_19` | rigid fixture material | 0.0015 | (0.0180832, 0.0196443, 0.0103513) | (0.166871, -0.0325, 0.761087) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_20_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.173262, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_20_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.173262, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_20` | rigid fixture material | 0.0015 | (0.018475, 0.0197457, 0.0114745) | (0.179887, -0.0475, 0.765087) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_21_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.186512, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_21_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.186512, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_link_21` | rigid fixture material | 0.0015 | (0.0186659, 0.0198022, 0.0128721) | (0.193256, -0.0625, 0.770443) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_connector_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.2, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `cable_1_connector_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.2, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `plug_1` | rigid engineering plastic | 0.016 | (0.022, 0.075, 0.019) | (0.2, -0.1, 0.7825) | (0, 0, 0, 1) | passive dynamic |
| `latch_1` | rigid engineering plastic | 0.002 | (0.014, 0.216, 0.0265) | (0.2, -0.1, 0.797) | (0, 0, 0, 1) | passive dynamic |
| `anchor_2` | rigid fixture material | 0.08 | (0.014, 0.012, 0.008) | (0.43, 0.26, 0.7515) | (0, 0, 0, 1) | anchored |
| `cable_2_0_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.43, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_0_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.43, 0.26, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_0` | rigid fixture material | 0.0015 | (0.0160364, 0.0189371, 0.00695249) | (0.435153, 0.2525, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_1_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.440306, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_1_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.440306, 0.245, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_1` | rigid fixture material | 0.0015 | (0.0158293, 0.0188668, 0.0069381) | (0.44534, 0.2375, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_2_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.450375, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_2_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.450375, 0.23, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_2` | rigid fixture material | 0.0015 | (0.0154158, 0.0187225, 0.00690652) | (0.455174, 0.2225, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_3_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.459973, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_3_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.459973, 0.215, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_3` | rigid fixture material | 0.0015 | (0.0147967, 0.0184977, 0.00685197) | (0.464426, 0.2075, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_4_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.468878, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_4_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.468878, 0.2, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_4` | rigid fixture material | 0.0015 | (0.0139711, 0.0181843, 0.00676551) | (0.472879, 0.1925, 0.7515) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_5_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.47688, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_5_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.47688, 0.185, 0.751501) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_5` | rigid fixture material | 0.0015 | (0.012934, 0.0177754, 0.00663501) | (0.480335, 0.1775, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_6_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.48379, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_6_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.48379, 0.17, 0.751502) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_6` | rigid fixture material | 0.0015 | (0.0116754, 0.0172704, 0.00644593) | (0.486613, 0.1625, 0.751505) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_7_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.489437, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_7_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.489437, 0.155, 0.751507) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_7` | rigid fixture material | 0.0015 | (0.0101819, 0.0166825, 0.00618347) | (0.491559, 0.1475, 0.751513) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_8_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.493681, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_8_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.493681, 0.14, 0.751518) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_8` | rigid fixture material | 0.0015 | (0.00844341, 0.0160452, 0.00583686) | (0.495043, 0.1325, 0.75153) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_9_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.496406, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_9_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.496406, 0.125, 0.751542) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_9` | rigid fixture material | 0.0015 | (0.00646671, 0.0154143, 0.00540541) | (0.496967, 0.1175, 0.751565) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_10_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.497529, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_10_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.497529, 0.11, 0.751588) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_10` | rigid fixture material | 0.0015 | (0.00569795, 0.0152092, 0.00525671) | (0.497264, 0.1025, 0.75163) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_11_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.497, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_11_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.497, 0.095, 0.751672) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_11` | rigid fixture material | 0.0015 | (0.00780468, 0.0158622, 0.00581607) | (0.495901, 0.0875, 0.751744) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_12_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.494802, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_12_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.494802, 0.08, 0.751816) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_12` | rigid fixture material | 0.0015 | (0.00973191, 0.0165667, 0.00632288) | (0.492876, 0.0725, 0.751935) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_13_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.490951, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_13_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.490951, 0.065, 0.752053) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_13` | rigid fixture material | 0.0015 | (0.01145, 0.0172551, 0.0067818) | (0.488225, 0.0575, 0.752242) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_14_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.485499, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_14_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.485499, 0.05, 0.75243) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_14` | rigid fixture material | 0.0015 | (0.0129579, 0.0178757, 0.00721464) | (0.482014, 0.0425, 0.752718) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_15_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.478528, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_15_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.478528, 0.035, 0.753007) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_15` | rigid fixture material | 0.0015 | (0.0142679, 0.0184007, 0.00765519) | (0.474341, 0.0275, 0.753437) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_16_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.470153, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_16_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.470153, 0.02, 0.753868) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_16` | rigid fixture material | 0.0015 | (0.0153926, 0.0188231, 0.00814384) | (0.465335, 0.0125, 0.754493) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_17_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.460517, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_17_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.460517, 0.005, 0.755119) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_17` | rigid fixture material | 0.0015 | (0.0163385, 0.0191489, 0.00872393) | (0.455152, -0.0025, 0.756009) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_18_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.449787, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_18_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.449787, -0.01, 0.7569) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_18` | rigid fixture material | 0.0015 | (0.0171052, 0.0193899, 0.00944003) | (0.443971, -0.0175, 0.758142) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_19_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.438155, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_19_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.438155, -0.025, 0.759384) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_19` | rigid fixture material | 0.0015 | (0.0176873, 0.0195598, 0.0103372) | (0.431992, -0.0325, 0.761087) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_20_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.425829, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_20_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.425829, -0.04, 0.762789) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_20` | rigid fixture material | 0.0015 | (0.0180763, 0.0196713, 0.0114608) | (0.419431, -0.0475, 0.765087) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_21_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.413033, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_21_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.413033, -0.055, 0.767385) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_link_21` | rigid fixture material | 0.0015 | (0.0182626, 0.0197363, 0.0128564) | (0.406517, -0.0625, 0.770443) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_connector_X` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.4, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `cable_2_connector_Z` | rigid fixture material | 0.0002 | (0.001, 0.001, 0.001) | (0.4, -0.07, 0.7735) | (0, 0, 0, 1) | passive dynamic |
| `plug_2` | rigid engineering plastic | 0.016 | (0.022, 0.075, 0.019) | (0.4, -0.1, 0.7825) | (0, 0, 0, 1) | passive dynamic |
| `latch_2` | rigid engineering plastic | 0.002 | (0.014, 0.216, 0.0265) | (0.4, -0.1, 0.797) | (0, 0, 0, 1) | passive dynamic |
| `parking_cradle` | rigid fixture material | 0.15 | (0.044, 0.042, 0.012) | (0.25, -0.025, 0.7475) | (0, 0, 0, 1) | anchored |

## Passive joints

- `cable_0_0_X_bend`: revolute X, `anchor_0` to `cable_0_0_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_0_Z_bend`: revolute Z, `cable_0_0_X` to `cable_0_0_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_0_twist`: revolute Y, `cable_0_0_Z` to `cable_0_link_0`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_1_X_bend`: revolute X, `cable_0_link_0` to `cable_0_1_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_1_Z_bend`: revolute Z, `cable_0_1_X` to `cable_0_1_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_1_twist`: revolute Y, `cable_0_1_Z` to `cable_0_link_1`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_2_X_bend`: revolute X, `cable_0_link_1` to `cable_0_2_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_2_Z_bend`: revolute Z, `cable_0_2_X` to `cable_0_2_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_2_twist`: revolute Y, `cable_0_2_Z` to `cable_0_link_2`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_3_X_bend`: revolute X, `cable_0_link_2` to `cable_0_3_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_3_Z_bend`: revolute Z, `cable_0_3_X` to `cable_0_3_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_3_twist`: revolute Y, `cable_0_3_Z` to `cable_0_link_3`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_4_X_bend`: revolute X, `cable_0_link_3` to `cable_0_4_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_4_Z_bend`: revolute Z, `cable_0_4_X` to `cable_0_4_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_4_twist`: revolute Y, `cable_0_4_Z` to `cable_0_link_4`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_5_X_bend`: revolute X, `cable_0_link_4` to `cable_0_5_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_5_Z_bend`: revolute Z, `cable_0_5_X` to `cable_0_5_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_5_twist`: revolute Y, `cable_0_5_Z` to `cable_0_link_5`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_6_X_bend`: revolute X, `cable_0_link_5` to `cable_0_6_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_6_Z_bend`: revolute Z, `cable_0_6_X` to `cable_0_6_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_6_twist`: revolute Y, `cable_0_6_Z` to `cable_0_link_6`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_7_X_bend`: revolute X, `cable_0_link_6` to `cable_0_7_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_7_Z_bend`: revolute Z, `cable_0_7_X` to `cable_0_7_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_7_twist`: revolute Y, `cable_0_7_Z` to `cable_0_link_7`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_8_X_bend`: revolute X, `cable_0_link_7` to `cable_0_8_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_8_Z_bend`: revolute Z, `cable_0_8_X` to `cable_0_8_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_8_twist`: revolute Y, `cable_0_8_Z` to `cable_0_link_8`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_9_X_bend`: revolute X, `cable_0_link_8` to `cable_0_9_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_9_Z_bend`: revolute Z, `cable_0_9_X` to `cable_0_9_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_9_twist`: revolute Y, `cable_0_9_Z` to `cable_0_link_9`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_10_X_bend`: revolute X, `cable_0_link_9` to `cable_0_10_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_10_Z_bend`: revolute Z, `cable_0_10_X` to `cable_0_10_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_10_twist`: revolute Y, `cable_0_10_Z` to `cable_0_link_10`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_11_X_bend`: revolute X, `cable_0_link_10` to `cable_0_11_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_11_Z_bend`: revolute Z, `cable_0_11_X` to `cable_0_11_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_11_twist`: revolute Y, `cable_0_11_Z` to `cable_0_link_11`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_12_X_bend`: revolute X, `cable_0_link_11` to `cable_0_12_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_12_Z_bend`: revolute Z, `cable_0_12_X` to `cable_0_12_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_12_twist`: revolute Y, `cable_0_12_Z` to `cable_0_link_12`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_13_X_bend`: revolute X, `cable_0_link_12` to `cable_0_13_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_13_Z_bend`: revolute Z, `cable_0_13_X` to `cable_0_13_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_13_twist`: revolute Y, `cable_0_13_Z` to `cable_0_link_13`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_14_X_bend`: revolute X, `cable_0_link_13` to `cable_0_14_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_14_Z_bend`: revolute Z, `cable_0_14_X` to `cable_0_14_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_14_twist`: revolute Y, `cable_0_14_Z` to `cable_0_link_14`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_15_X_bend`: revolute X, `cable_0_link_14` to `cable_0_15_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_15_Z_bend`: revolute Z, `cable_0_15_X` to `cable_0_15_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_15_twist`: revolute Y, `cable_0_15_Z` to `cable_0_link_15`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_16_X_bend`: revolute X, `cable_0_link_15` to `cable_0_16_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_16_Z_bend`: revolute Z, `cable_0_16_X` to `cable_0_16_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_16_twist`: revolute Y, `cable_0_16_Z` to `cable_0_link_16`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_17_X_bend`: revolute X, `cable_0_link_16` to `cable_0_17_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_17_Z_bend`: revolute Z, `cable_0_17_X` to `cable_0_17_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_17_twist`: revolute Y, `cable_0_17_Z` to `cable_0_link_17`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_18_X_bend`: revolute X, `cable_0_link_17` to `cable_0_18_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_18_Z_bend`: revolute Z, `cable_0_18_X` to `cable_0_18_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_18_twist`: revolute Y, `cable_0_18_Z` to `cable_0_link_18`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_19_X_bend`: revolute X, `cable_0_link_18` to `cable_0_19_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_19_Z_bend`: revolute Z, `cable_0_19_X` to `cable_0_19_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_19_twist`: revolute Y, `cable_0_19_Z` to `cable_0_link_19`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_20_X_bend`: revolute X, `cable_0_link_19` to `cable_0_20_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_20_Z_bend`: revolute Z, `cable_0_20_X` to `cable_0_20_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_20_twist`: revolute Y, `cable_0_20_Z` to `cable_0_link_20`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_21_X_bend`: revolute X, `cable_0_link_20` to `cable_0_21_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_21_Z_bend`: revolute Z, `cable_0_21_X` to `cable_0_21_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_21_twist`: revolute Y, `cable_0_21_Z` to `cable_0_link_21`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_0_connector_X_bend`: revolute X, `cable_0_link_21` to `cable_0_connector_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_connector_Z_bend`: revolute Z, `cable_0_connector_X` to `cable_0_connector_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_0_connector_twist`: revolute Y, `cable_0_connector_Z` to `plug_0`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `latch_slide_0`: prismatic Z, `plug_0` to `latch_0`; limits [-0.006, 0]; stiffness 150, damping 0.4. Full joint frames are in `scene.json`.
- `cable_1_0_X_bend`: revolute X, `anchor_1` to `cable_1_0_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_0_Z_bend`: revolute Z, `cable_1_0_X` to `cable_1_0_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_0_twist`: revolute Y, `cable_1_0_Z` to `cable_1_link_0`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_1_X_bend`: revolute X, `cable_1_link_0` to `cable_1_1_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_1_Z_bend`: revolute Z, `cable_1_1_X` to `cable_1_1_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_1_twist`: revolute Y, `cable_1_1_Z` to `cable_1_link_1`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_2_X_bend`: revolute X, `cable_1_link_1` to `cable_1_2_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_2_Z_bend`: revolute Z, `cable_1_2_X` to `cable_1_2_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_2_twist`: revolute Y, `cable_1_2_Z` to `cable_1_link_2`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_3_X_bend`: revolute X, `cable_1_link_2` to `cable_1_3_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_3_Z_bend`: revolute Z, `cable_1_3_X` to `cable_1_3_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_3_twist`: revolute Y, `cable_1_3_Z` to `cable_1_link_3`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_4_X_bend`: revolute X, `cable_1_link_3` to `cable_1_4_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_4_Z_bend`: revolute Z, `cable_1_4_X` to `cable_1_4_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_4_twist`: revolute Y, `cable_1_4_Z` to `cable_1_link_4`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_5_X_bend`: revolute X, `cable_1_link_4` to `cable_1_5_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_5_Z_bend`: revolute Z, `cable_1_5_X` to `cable_1_5_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_5_twist`: revolute Y, `cable_1_5_Z` to `cable_1_link_5`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_6_X_bend`: revolute X, `cable_1_link_5` to `cable_1_6_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_6_Z_bend`: revolute Z, `cable_1_6_X` to `cable_1_6_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_6_twist`: revolute Y, `cable_1_6_Z` to `cable_1_link_6`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_7_X_bend`: revolute X, `cable_1_link_6` to `cable_1_7_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_7_Z_bend`: revolute Z, `cable_1_7_X` to `cable_1_7_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_7_twist`: revolute Y, `cable_1_7_Z` to `cable_1_link_7`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_8_X_bend`: revolute X, `cable_1_link_7` to `cable_1_8_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_8_Z_bend`: revolute Z, `cable_1_8_X` to `cable_1_8_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_8_twist`: revolute Y, `cable_1_8_Z` to `cable_1_link_8`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_9_X_bend`: revolute X, `cable_1_link_8` to `cable_1_9_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_9_Z_bend`: revolute Z, `cable_1_9_X` to `cable_1_9_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_9_twist`: revolute Y, `cable_1_9_Z` to `cable_1_link_9`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_10_X_bend`: revolute X, `cable_1_link_9` to `cable_1_10_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_10_Z_bend`: revolute Z, `cable_1_10_X` to `cable_1_10_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_10_twist`: revolute Y, `cable_1_10_Z` to `cable_1_link_10`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_11_X_bend`: revolute X, `cable_1_link_10` to `cable_1_11_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_11_Z_bend`: revolute Z, `cable_1_11_X` to `cable_1_11_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_11_twist`: revolute Y, `cable_1_11_Z` to `cable_1_link_11`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_12_X_bend`: revolute X, `cable_1_link_11` to `cable_1_12_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_12_Z_bend`: revolute Z, `cable_1_12_X` to `cable_1_12_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_12_twist`: revolute Y, `cable_1_12_Z` to `cable_1_link_12`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_13_X_bend`: revolute X, `cable_1_link_12` to `cable_1_13_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_13_Z_bend`: revolute Z, `cable_1_13_X` to `cable_1_13_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_13_twist`: revolute Y, `cable_1_13_Z` to `cable_1_link_13`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_14_X_bend`: revolute X, `cable_1_link_13` to `cable_1_14_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_14_Z_bend`: revolute Z, `cable_1_14_X` to `cable_1_14_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_14_twist`: revolute Y, `cable_1_14_Z` to `cable_1_link_14`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_15_X_bend`: revolute X, `cable_1_link_14` to `cable_1_15_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_15_Z_bend`: revolute Z, `cable_1_15_X` to `cable_1_15_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_15_twist`: revolute Y, `cable_1_15_Z` to `cable_1_link_15`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_16_X_bend`: revolute X, `cable_1_link_15` to `cable_1_16_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_16_Z_bend`: revolute Z, `cable_1_16_X` to `cable_1_16_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_16_twist`: revolute Y, `cable_1_16_Z` to `cable_1_link_16`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_17_X_bend`: revolute X, `cable_1_link_16` to `cable_1_17_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_17_Z_bend`: revolute Z, `cable_1_17_X` to `cable_1_17_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_17_twist`: revolute Y, `cable_1_17_Z` to `cable_1_link_17`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_18_X_bend`: revolute X, `cable_1_link_17` to `cable_1_18_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_18_Z_bend`: revolute Z, `cable_1_18_X` to `cable_1_18_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_18_twist`: revolute Y, `cable_1_18_Z` to `cable_1_link_18`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_19_X_bend`: revolute X, `cable_1_link_18` to `cable_1_19_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_19_Z_bend`: revolute Z, `cable_1_19_X` to `cable_1_19_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_19_twist`: revolute Y, `cable_1_19_Z` to `cable_1_link_19`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_20_X_bend`: revolute X, `cable_1_link_19` to `cable_1_20_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_20_Z_bend`: revolute Z, `cable_1_20_X` to `cable_1_20_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_20_twist`: revolute Y, `cable_1_20_Z` to `cable_1_link_20`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_21_X_bend`: revolute X, `cable_1_link_20` to `cable_1_21_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_21_Z_bend`: revolute Z, `cable_1_21_X` to `cable_1_21_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_21_twist`: revolute Y, `cable_1_21_Z` to `cable_1_link_21`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_1_connector_X_bend`: revolute X, `cable_1_link_21` to `cable_1_connector_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_connector_Z_bend`: revolute Z, `cable_1_connector_X` to `cable_1_connector_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_1_connector_twist`: revolute Y, `cable_1_connector_Z` to `plug_1`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `latch_slide_1`: prismatic Z, `plug_1` to `latch_1`; limits [-0.006, 0]; stiffness 150, damping 0.4. Full joint frames are in `scene.json`.
- `cable_2_0_X_bend`: revolute X, `anchor_2` to `cable_2_0_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_0_Z_bend`: revolute Z, `cable_2_0_X` to `cable_2_0_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_0_twist`: revolute Y, `cable_2_0_Z` to `cable_2_link_0`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_1_X_bend`: revolute X, `cable_2_link_0` to `cable_2_1_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_1_Z_bend`: revolute Z, `cable_2_1_X` to `cable_2_1_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_1_twist`: revolute Y, `cable_2_1_Z` to `cable_2_link_1`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_2_X_bend`: revolute X, `cable_2_link_1` to `cable_2_2_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_2_Z_bend`: revolute Z, `cable_2_2_X` to `cable_2_2_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_2_twist`: revolute Y, `cable_2_2_Z` to `cable_2_link_2`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_3_X_bend`: revolute X, `cable_2_link_2` to `cable_2_3_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_3_Z_bend`: revolute Z, `cable_2_3_X` to `cable_2_3_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_3_twist`: revolute Y, `cable_2_3_Z` to `cable_2_link_3`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_4_X_bend`: revolute X, `cable_2_link_3` to `cable_2_4_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_4_Z_bend`: revolute Z, `cable_2_4_X` to `cable_2_4_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_4_twist`: revolute Y, `cable_2_4_Z` to `cable_2_link_4`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_5_X_bend`: revolute X, `cable_2_link_4` to `cable_2_5_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_5_Z_bend`: revolute Z, `cable_2_5_X` to `cable_2_5_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_5_twist`: revolute Y, `cable_2_5_Z` to `cable_2_link_5`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_6_X_bend`: revolute X, `cable_2_link_5` to `cable_2_6_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_6_Z_bend`: revolute Z, `cable_2_6_X` to `cable_2_6_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_6_twist`: revolute Y, `cable_2_6_Z` to `cable_2_link_6`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_7_X_bend`: revolute X, `cable_2_link_6` to `cable_2_7_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_7_Z_bend`: revolute Z, `cable_2_7_X` to `cable_2_7_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_7_twist`: revolute Y, `cable_2_7_Z` to `cable_2_link_7`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_8_X_bend`: revolute X, `cable_2_link_7` to `cable_2_8_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_8_Z_bend`: revolute Z, `cable_2_8_X` to `cable_2_8_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_8_twist`: revolute Y, `cable_2_8_Z` to `cable_2_link_8`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_9_X_bend`: revolute X, `cable_2_link_8` to `cable_2_9_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_9_Z_bend`: revolute Z, `cable_2_9_X` to `cable_2_9_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_9_twist`: revolute Y, `cable_2_9_Z` to `cable_2_link_9`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_10_X_bend`: revolute X, `cable_2_link_9` to `cable_2_10_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_10_Z_bend`: revolute Z, `cable_2_10_X` to `cable_2_10_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_10_twist`: revolute Y, `cable_2_10_Z` to `cable_2_link_10`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_11_X_bend`: revolute X, `cable_2_link_10` to `cable_2_11_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_11_Z_bend`: revolute Z, `cable_2_11_X` to `cable_2_11_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_11_twist`: revolute Y, `cable_2_11_Z` to `cable_2_link_11`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_12_X_bend`: revolute X, `cable_2_link_11` to `cable_2_12_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_12_Z_bend`: revolute Z, `cable_2_12_X` to `cable_2_12_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_12_twist`: revolute Y, `cable_2_12_Z` to `cable_2_link_12`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_13_X_bend`: revolute X, `cable_2_link_12` to `cable_2_13_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_13_Z_bend`: revolute Z, `cable_2_13_X` to `cable_2_13_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_13_twist`: revolute Y, `cable_2_13_Z` to `cable_2_link_13`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_14_X_bend`: revolute X, `cable_2_link_13` to `cable_2_14_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_14_Z_bend`: revolute Z, `cable_2_14_X` to `cable_2_14_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_14_twist`: revolute Y, `cable_2_14_Z` to `cable_2_link_14`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_15_X_bend`: revolute X, `cable_2_link_14` to `cable_2_15_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_15_Z_bend`: revolute Z, `cable_2_15_X` to `cable_2_15_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_15_twist`: revolute Y, `cable_2_15_Z` to `cable_2_link_15`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_16_X_bend`: revolute X, `cable_2_link_15` to `cable_2_16_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_16_Z_bend`: revolute Z, `cable_2_16_X` to `cable_2_16_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_16_twist`: revolute Y, `cable_2_16_Z` to `cable_2_link_16`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_17_X_bend`: revolute X, `cable_2_link_16` to `cable_2_17_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_17_Z_bend`: revolute Z, `cable_2_17_X` to `cable_2_17_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_17_twist`: revolute Y, `cable_2_17_Z` to `cable_2_link_17`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_18_X_bend`: revolute X, `cable_2_link_17` to `cable_2_18_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_18_Z_bend`: revolute Z, `cable_2_18_X` to `cable_2_18_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_18_twist`: revolute Y, `cable_2_18_Z` to `cable_2_link_18`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_19_X_bend`: revolute X, `cable_2_link_18` to `cable_2_19_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_19_Z_bend`: revolute Z, `cable_2_19_X` to `cable_2_19_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_19_twist`: revolute Y, `cable_2_19_Z` to `cable_2_link_19`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_20_X_bend`: revolute X, `cable_2_link_19` to `cable_2_20_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_20_Z_bend`: revolute Z, `cable_2_20_X` to `cable_2_20_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_20_twist`: revolute Y, `cable_2_20_Z` to `cable_2_link_20`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_21_X_bend`: revolute X, `cable_2_link_20` to `cable_2_21_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_21_Z_bend`: revolute Z, `cable_2_21_X` to `cable_2_21_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_21_twist`: revolute Y, `cable_2_21_Z` to `cable_2_link_21`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `cable_2_connector_X_bend`: revolute X, `cable_2_link_21` to `cable_2_connector_X`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_connector_Z_bend`: revolute Z, `cable_2_connector_X` to `cable_2_connector_Z`; limits [-1.3, 1.3]; stiffness 0.0007, damping 8e-05. Full joint frames are in `scene.json`.
- `cable_2_connector_twist`: revolute Y, `cable_2_connector_Z` to `plug_2`; limits [-2.8, 2.8]; stiffness 0.0002, damping 5e-05. Full joint frames are in `scene.json`.
- `latch_slide_2`: prismatic Z, `plug_2` to `latch_2`; limits [-0.006, 0]; stiffness 150, damping 0.4. Full joint frames are in `scene.json`.

## Mass distribution overrides


