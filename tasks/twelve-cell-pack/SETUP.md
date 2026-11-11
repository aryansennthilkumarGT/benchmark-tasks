# Twelve-cell preload closure setup

The fixed starting layout contains twelve loaded AA-cell surrogates, the holder and its twelve independent spring contacts, a loose pressure plate, a loose capture key and the existing empty loading supports. Coordinates use x forward, y left and z up. Dimensions are metres and masses are kilograms. Quaternions use XYZW order. The table surface is at z=0.7475 m. Seed 0 and zero object jitter define the trial. Gravity settling follows reset.

| Body | Material | Mass kg | Collision envelope m | Authored world origin m | XYZW |
|---|---|---:|---|---|---|
| `holder` | rigid engineering plastic | 0.7 | (0.31, 0.162, 0.0845) | (0.225, 0, 0.7475) | (0.0, 0.0, 0.0, 1.0) |
| `contact_0` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.1, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_1` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.15, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_2` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.2, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_3` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.25, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_4` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.3, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_5` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.35, -0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_6` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.1, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_7` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.15, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_8` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.2, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_9` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.25, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_10` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.3, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `contact_11` | rigid engineering plastic | 0.002 | (0.012, 0.012, 0.002) | (0.35, 0.028, 0.7555) | (0.0, 0.0, 0.0, 1.0) |
| `cell_0` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.1, -0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_1` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.15, -0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `cell_2` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.2, -0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_3` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.25, -0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `cell_4` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.3, -0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_5` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.35, -0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `cell_6` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.1, 0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_7` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.15, 0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `cell_8` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.2, 0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_9` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.25, 0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `cell_10` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.3, 0.028, 0.78225) | (0.0, 0.0, 0.0, 1.0) |
| `cell_11` | rigid AA cell surrogate; no electrical or chemical simulation | 0.024 | (0.0145, 0.0145, 0.0518) | (0.35, 0.028, 0.78355) | (1.0, 0.0, 0.0, 0.0) |
| `retaining_plate` | rigid engineering plastic | 0.18 | (0.308, 0.114, 0.0487) | (0.285, 0.23, 0.7515) | (0.0, 0.0, 0.0, 1.0) |
| `capture_key` | rigid fixture surrogate | 0.08 | (0.014, 0.156, 0.014) | (0.385, -0.24, 0.7547) | (0, 0, 0, 1) |

Every collision primitive and local transform is enumerated in `scene.json`. Cell axes alternate between +Z and -Z as listed. Each contact has 2 mm prismatic travel, a 500 N/m spring and 0.5 N·s/m damping. All movable surfaces use static friction 0.65, dynamic friction 0.5 and restitution 0. The holder is anchored. The loose plate and key provide the demonstrated load-transfer mechanism.

The capture-key side walls have centres y=±79.75 mm and thickness 2.5 mm. Their inner faces are ±78.5 mm, giving the 156 mm cross-key 0.5 mm clearance per side at the scored centred position. Terminal spring damping is 2.0 N s/m with stiffness 500 N/m. These are declared simulation surrogate parameters.
