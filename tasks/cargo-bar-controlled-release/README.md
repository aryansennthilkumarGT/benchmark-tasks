# Controlled cargo-bar release — engineering checkpoint

This independent task is in active CPU implementation. It is not offline-ready, GPU-verified or submission-ready. No official PR is authorized.

The manufacturer-grounded bounded operation releases a clamped bar using its latch/full-forward handle, controls the loaded tube while the two pawls disengage, retracts the rack and rests the shortened bar clear of both walls. It does not retension a strap or run a cargo jolt.

Implemented: original full-scale two-USD scene with rack/pinion, ratchet, two pawls, physical cams/latch, compliant feet and wall/cradle frame; passive reset targets; read-only native-state robot expert and complete authored plan; current-state scorer; isolated CPU gearing/pawl/cam probes. All27 early swing IK poses and all authored endpoint IK poses pass locally. These are not contact/grasp demonstrations.

Still required before readiness: complete native cases, full controller/geometry/FK-path/adversarial suites, mesh/material/source audits, occupational/novelty/fidelity/manufacturing/measurement documentation, independent clean HTTPS reproduction and final quality review. The existing COPIED infrastructure must be integration-tested for this mechanism.

Use Python3.12 and requirements-cpu.txt, plus mujoco3.3.7. No CUDA or paid service is needed for these commands:

```bash
python tasks/cargo-bar-controlled-release/generate_scene.py
python tasks/cargo-bar-controlled-release/plan_controller.py
python tasks/cargo-bar-controlled-release/probe_gearing_cpu.py
python tasks/cargo-bar-controlled-release/probe_pawl_cpu.py
python tasks/cargo-bar-controlled-release/mechanism_cpu.py
```

MuJoCo fixtures use explicit diagnostic actuators and cannot count as robot or Isaac evidence. The expert itself outputs14 robot joint/gripper commands, reads actual native physical telemetry without reading score, detects stalls/slips and supports bounded grasp reacquisition. It never writes part poses or task joints.

The original shackle/ER/SAC evidence and pendingPR1733 are not reused. Closest material novelty risks remain pendingPR1285 (strap tightening/latching) andPR1855 (twist-lock pole). Resolve the actual physical-skill comparison before declaring the third candidate strong.
