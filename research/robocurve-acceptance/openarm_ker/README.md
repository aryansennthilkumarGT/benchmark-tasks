# OpenArm KER: actual-CAD CPU gate

**Decision: [HOLD](GO_NO_GO.md).** Actual official CAD/BOM were downloaded and used; static geometric diagnostics ran. No causal snap-fit/loaded assembly trial or complete robot-access path ran.

Required reports:

- [SOURCE_CAD_AND_BOM_MANIFEST.md](SOURCE_CAD_AND_BOM_MANIFEST.md)
- [ACTUAL_INTERFACE_AND_DATUM_GEOMETRY.md](ACTUAL_INTERFACE_AND_DATUM_GEOMETRY.md)
- [ROBOT_ACCESS_PREFLIGHT.md](ROBOT_ACCESS_PREFLIGHT.md)
- [NOVELTY_AND_IMPORTANCE.md](NOVELTY_AND_IMPORTANCE.md)
- [PHYSICAL_SCORING_AND_NEGATIVE_CONTROLS.md](PHYSICAL_SCORING_AND_NEGATIVE_CONTROLS.md)
- [GO_NO_GO.md](GO_NO_GO.md)

Python3.12, OCP7.8.1.1/CadQuery2.7.0, NumPy/SciPy and Matplotlib were available; no new CAD/physics package was installed. The real BOM was read with openpyxl. All work was CPU-only. The official simplified source geometry is attributed under [the included publisher license](LICENSE.openarm_hardware.txt).

From the repository root:

```bash
python research/robocurve-acceptance/openarm_ker/FETCH_SOURCE.py --output /tmp/ker-source
XDG_CACHE_HOME=/tmp/ker-cache python research/robocurve-acceptance/openarm_ker/INSPECT_CAD.py --source-dir /tmp/ker-source
python research/robocurve-acceptance/openarm_ker/CHECK_ACCESS_INPUTS.py
MPLCONFIGDIR=/tmp/ker-mpl XDG_CACHE_HOME=/tmp/ker-cache python research/robocurve-acceptance/openarm_ker/PLOT_CAD.py --source-dir /tmp/ker-source
```

The source fetch verifies the pinned official archive hash and extracts selected CAD/BOM/license files. If the archive is already available, supply `--archive /path/openarm-hardware-2.0.0.tar.gz` to avoid downloading it again. Raw assets are not committed. `INSPECT_CAD.py --output-dir /tmp/ker-results` preserves the committed results; use `CHECK_ACCESS_INPUTS.py --results /tmp/ker-results` with that output.

**Expected access-gate exit is2**, because an actual registered articulated KER configuration and full procedure/tool paths are missing. That is not a failed collision run. Original robot FK/hull infrastructure is imported unchanged. The CAD script checks actual units/file hashes, occurrence-transform bounds and static diagnostic distinctions; it does not implement latch dynamics, successful task motion or damage calibration.

[Source jig render](results/JIG_CAD.png) uses display tessellation only; it is not a collision or force certificate. Face/occurrence inventories are gzip-compressed JSON. [CAD numeric summary](results/CAD_SUMMARY.json), [static diagnostics](results/CAD_CONTACT_DIAGNOSTICS.json), [actual command log](results/CAD_EXECUTION.txt), [access input result](results/ACCESS_INPUT_GATE.json).
