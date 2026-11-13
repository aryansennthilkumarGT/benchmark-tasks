# SDS-plus chisel exchange

Exchange the used point chisel for a flat insert in an original unpowered bench holder. Seven physical bodies/6original USD assets preserve open drive grooves, closed ball grooves, a free7mm sphere, positive sleeve land/release and retained axial play. Clear physical side inserts permit grading inspection. All undocumented geometry is authored; no OEM fit or measured force is claimed. See FIDELITY.md, SOURCES.json, PARAMETERS.md, MEASUREMENT.md and REPRODUCTION.md.

Use Python3.12 and `python install_cpu.py --venv /tmp/sds-cpu`; this installs only CPU dependencies. From the task folder run:

```sh
/tmp/sds-cpu/bin/python static_check.py --output /tmp/sds-check-new
/tmp/sds-cpu/bin/python task_runner.py --output /tmp/sds-native-preview
```

The first output directory must not already exist. The second command is a preview. The complete CPU suite checks source integrity, unit/schema/provenance, exact USD reproduction/materials, inspection rays, all-pair solids, repeated supplemental contact protocols, full force cycle, actual controller execution and actual-FK/scoring replay. Rebuild with generate_scene.py/plan_controller.py/document_parameters.py only after intentional reviewed source changes; refreshing hashes does not validate changed mechanics.

The complete ideal policy uses1639actions/81.95s within3200actions/160s at20Hz. Physics timestep is1/1920s. Grasp contact, settling and quasistatic ball projection are explicit assumptions; they are not native success. GPU_VALIDATION.md gives the actual future physics/expert/Dream/media commands and source/receipt guards. No GPU provisioning, paid evaluation, upload, credentials or official PR is authorized in this offline phase.

The durable exact-source clean qualification record is offline-evidence/final/source-verification.json. Its absence/failure means the independent gate is unfinished. Native qualification and official submission remain pending regardless of CPU results.
