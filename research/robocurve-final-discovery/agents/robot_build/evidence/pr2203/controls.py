"""Exercise the benchmark's mechanism and outcome gates independently of IK."""
import argparse
import csv
import json
from pathlib import Path

from mechanics import HOLD_TOLERANCE, Rig, TEST_FORCE, midspan_deflection, span_tension

CASES = {
    "nominal": (0.11038, 2, True, 0.0001, 1.0),
    "slack": (0.10975, 2, True, 0.0001, 0.25),
    "overtight": (0.11061, 2, True, 0.0001, 0.25),
    "single-bolt-slip": (0.11038, 1, True, 0.0001, 0.0),
    "release-before-tightening": (0.11038, 0, True, 0.0001, 0.0),
    "unseated": (0.11038, 2, False, 0.0001, 0.0),
    "misaligned": (0.11038, 2, True, 0.0012, 0.0),
}


def trial(span, bolts, seated, offset):
    rig = Rig(seated=seated, offset=offset)
    history = []

    def step(phase, count, **inputs):
        for _ in range(count):
            rig.step(**inputs)
            history.append(dict(
                seconds=len(history) / 20, phase=phase, span_mm=rig.span * 1000,
                bolt_1_n=rig.clamp[0], bolt_2_n=rig.clamp[1], gauge_mm=rig.checked_mm,
                gauge_loaded=rig.gauge_loaded, held=rig.held, score=rig.outcome(),
            ))

    step("pull to target", 50, pull=span)
    before = rig.span
    before_deflection = midspan_deflection(before)
    for i in range(bolts):
        step(f"tighten bolt {i + 1}", 45, pull=span, bolt=i, clockwise=2.13 / 45)
    step("release", 20)
    step("check under 2.5 N", 14, gauge=True)
    step("release gauge", 12)
    return dict(
        model="reduced-order contact model",
        pre_release_mm=round(before * 1000, 5), final_span_mm=round(rig.span * 1000, 5),
        pre_release_deflection_mm=round(before_deflection * 1000, 4),
        deflection_mm=None if rig.checked_mm is None else round(rig.checked_mm, 4),
        retention_drift_mm=round(rig.drift * 1000, 5),
        slip_mm=round(rig.slip * 1000, 5), clamp_n=[round(n, 2) for n in rig.clamp],
        seated=rig.seated, alignment_mm=round(rig.offset * 1000, 4), score=rig.outcome(),
    ), history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name, (*values, expected) in CASES.items():
        result, trace = trial(*values)
        assert result["score"] == expected, (name, result)
        summary[name] = result
        if args.out:
            with (args.out / f"{name}.csv").open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=trace[0].keys())
                writer.writeheader()
                writer.writerows(trace)
    assert summary["release-before-tightening"]["slip_mm"] > 0.2
    assert 1.4 <= summary["release-before-tightening"]["pre_release_deflection_mm"] <= 1.95
    assert summary["single-bolt-slip"]["slip_mm"] > HOLD_TOLERANCE * 1000
    print(json.dumps({"test_force_n": TEST_FORCE, "trials": summary}, indent=2))
    if args.out:
        (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
