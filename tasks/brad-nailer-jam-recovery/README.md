# Brad-nailer nose-jam recovery

An original unpowered service fixture follows DeWalt DCN680 manual p12/FigJ steps3,4,6: open the nose, extract the bent brad into the tray, then reseat and latch the nose with the crosspin under both arms. Native robot qualification is pending. Do not treat the supplemental CPU force fixtures or ideal tracking as an expert demonstration.

Use Python3.12. Install only CPU dependencies:

```sh
python3.12 install_cpu.py --venv /tmp/nailer-cpu
/tmp/nailer-cpu/bin/python generate_scene.py
/tmp/nailer-cpu/bin/python probe_cycle_cpu.py --output guided-cycle-reference.json
/tmp/nailer-cpu/bin/python plan_controller.py
/tmp/nailer-cpu/bin/python -m pytest -q
/tmp/nailer-cpu/bin/python audit_geometry.py
/tmp/nailer-cpu/bin/python audit_controller.py > /tmp/nailer-ideal.json
```

For the full source-frozen CPU check, use `python static_check.py --output /tmp/nailer-check-new` (the output directory must not already exist). The independent native harness and Dream/media workflow default to preview:

```sh
python task_runner.py --output /tmp/nailer-native-preview
python run.py --help
python native_tests.py --help
```

Native execution requires the pinned official Isaac/YAM stack and future authorized GPU access. No GPU provisioner, service start, paid evaluation, media upload or PR creation runs in the offline workflow. No upload credentials are required or stored. Source changes require fresh native validation; historical evidence never transfers automatically.

The250s/5,000-action20Hz limit exceeds the complete ideal controller's2780actions/139s; genuine native duration still requires measurement. The physics timestep is1/1920s. See FIDELITY.md for limitations, PARAMETERS.md for every physical parameter, SOURCES.json/OCCUPATION.md for genuine primary sources and REPRODUCTION.md for preparation/reset. CPU qualification status is recorded in ENGINEERING_PROGRESS.md; this package is not qualified for official submission. See GPU_VALIDATION.md for future source-bound native qualification.
