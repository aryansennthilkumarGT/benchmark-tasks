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

The native PhysX configuration uses 32 position iterations, 8 velocity iterations and a mass-normalized actor sleep threshold of 0.005 m²/s². The sleep threshold matches the installed Isaac Lab pick-and-place asset configuration. Bodies retain native contact dynamics and wake in response to applied forces and robot manipulation. Paired keyed/unkeyed 3 N probes test load retention separately from resting stability.

This task uses480Hz native physics with20Hz robot actions. The task-scoped Arena environment callback sets24 physics substeps per action. This increases temporal resolution for the small spring contacts. The installed robot, simulator and fixed host driver are used directly.


An earlier480Hz,64-position/32-velocity configuration passed two captured-preload fixtures but produced excessive measured stepping overhead during control diagnostics. The240Hz,32-position/8-velocity trial failed the unchanged speed conditions. The current480Hz,32-position/8-velocity configuration requires fresh native contact, preload-retention and robot-control validation. Driver565.57.01 remains fixed.


The twelve terminal springs have500N/m stiffness and8N·s/m damping. A24g cell plus2g terminal has an isolated critical-damping estimate of7.21N·s/m before plate load sharing. The earlier2N·s/m configuration was underdamped for this combined mass. At240Hz it failed the unchanged10mm/s cell-speed condition in both captured-pack probes. Fresh probes must verify the new passive damping, preload retention and keyed/unkeyed load response.

Each preloaded cell has two additional transverse guide walls, 24 by 4 by 44 mm, centred 9.7 mm to either side of its row centre and 25 mm above the holder root. Together with the existing longitudinal walls they form an 15.4 by 15.4 mm clear sleeve. These fused holder guides keep cells upright before plate compression. The earlier holder constrained only the x direction. Recorded native cell 4 toppled laterally before the plate arrived, leaving its terminal unloaded. The initial native stability case now runs 20 seconds and checks every cell within 3 mm of its setup position and 0.08 rad of its declared axis.


Physical-build surrogate material specification: inert metal AA-shaped dummy cells and an aluminium cross-key are intended proxies. Holder, plate and contact-shoe proxies are plastic fixture components. The simulation treats these as rigid bodies with the listed assigned masses and common friction coefficients; these are design estimates, not calibrated material measurements. Electrical and chemical behavior is outside scope. The repeated grid in task.json exactly indexes all twelve contacts and all twelve loaded cells; this table and scene.json retain their individual transforms.
