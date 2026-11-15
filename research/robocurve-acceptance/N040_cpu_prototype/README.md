# First N040 CPU contact coupon

**Exploratory mechanism implementation, not authenticated Hyundai physics or full-door/YAM feasibility.** Start with [SOURCE_AND_GEOMETRY.md](SOURCE_AND_GEOMETRY.md), actual [numerical results](results/summary.csv), [sensitivity](PARAMETER_SENSITIVITY.md), and [remaining gates](LIMITATIONS_AND_NEXT_GATES.md).

Requires Python 3.10+, NumPy and SciPy. Matplotlib is optional for the figure/report script. The environment already supplied these; no GPU or new physics package was installed.

From the repository root:

```bash
python research/robocurve-acceptance/N040_cpu_prototype/run_experiments.py
python -m unittest discover -s research/robocurve-acceptance/N040_cpu_prototype -p 'test_*.py' -v
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/n040-mpl XDG_CACHE_HOME=/tmp/n040-cache python research/robocurve-acceptance/N040_cpu_prototype/make_report.py
```

The runner writes per-increment CSVs, JSON with every parameter and solver diagnostic, a comparison CSV, and a runtime/version/code-hash manifest. It is deterministic up to floating-point/library optimizer differences. To preserve committed results, use `run_experiments.py --output /tmp/n040-reproduction` and compare its summaries; the recorded-result tests deliberately check the committed code hashes. No source fetching or native simulator is part of reproduction. `results/EXECUTION.txt` and `results/TESTS.txt` archive the executed command output.

`mechanism.py` solves four generalized coordinates with bounded SciPy L-BFGS-B continuation: panel uplift, axial root extraction, and two leg deflections. At each increment it minimizes beam/panel incremental elastoplastic energy, unilateral carrier and contact penalties, regularized friction dissipation and a small numerical continuation term. It does not implement a release animation, proximity trigger or latch opening. The observational audit can be replaced without changing any trajectory (tested).

The existing [robot preflight](../preflight/N040_ACCESS_TEST.py), its actual YAM collision assets, [inputs](../preflight/inputs/N040.json) and [blocked result](../preflight/results/N040_ACCESS_RESULT.json) remain unchanged. No replacement robot model or repeated 20-control robot-preflight claim is included here.
