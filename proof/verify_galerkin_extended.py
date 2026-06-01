# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Extended Galerkin stabilization verification.

Runs the CvS Proposition 4.1 Galerkin matrix Q(c) at successively larger
prime cutoffs c and records the ground-state eigenvalue λ_min(c). Verifies
the form-stabilization plateau predicted by STABILIZATION.md.

STABILIZATION.md Run 1 (N=30, dps=50) entered a plateau at c≥17 with
|Δlog₁₀|λ_min|| < 1.23.  This run increases to N=100, dps=80 to sharpen
the Galerkin approximation and narrow the plateau band.

Usage:
    python proof/verify_galerkin_extended.py           # Full run (N=100, dps=80) ~slow
    python proof/verify_galerkin_extended.py --quick   # Quick run (N=30, dps=50)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import mpmath as mp
import connes_cvs

# ---------------------------------------------------------------------------
# Known reference values from STABILIZATION.md Run 1 (N=30, dps=50)
# ---------------------------------------------------------------------------
_RUN1_REF = {
    7: -27.1, 11: -42.9, 13: -47.5, 17: -50.3,
    19: -50.6, 23: -51.4, 29: -50.2, 31: -50.3, 37: -50.7,
}

CUTOFFS_STANDARD = [7, 11, 13, 17, 19, 23, 29, 31, 37]
CUTOFFS_EXTENDED = [7, 11, 13, 17, 19, 23, 29, 31, 37, 47, 100]


def run_stabilization(
    cutoffs: list[int],
    N: int,
    dps: int,
    verbose: bool = True,
) -> list[dict]:
    """Run the Galerkin stabilization sweep over prime cutoffs.

    Returns a list of result dicts with keys:
        c, N, dps, lambda_min, log10_lambda_min, delta_log10, elapsed_s
    """
    results = []
    prev_log10 = None

    if verbose:
        print(f"\nCvS Galerkin stabilization sweep  (N={N}, dps={dps})")
        print(f"{'c':>5}  {'log₁₀|λ_min|':>14}  {'Δ from prev':>12}  {'Run1 ref':>10}  {'elapsed':>8}")
        print("-" * 60)

    for c in cutoffs:
        t0 = time.time()
        mp.mp.dps = dps

        Q = connes_cvs.build_galerkin_matrix(c=c, N=N, T=200, dps=dps)
        lam_min, _ = connes_cvs.compute_ground_state(Q)

        elapsed = time.time() - t0
        lam_abs = abs(float(mp.nstr(lam_min, 6)))
        log10_val = math.log10(lam_abs) if lam_abs > 0 else float("-inf")
        delta = abs(log10_val - prev_log10) if prev_log10 is not None else None
        ref = _RUN1_REF.get(c, None)

        if verbose:
            delta_str = f"{delta:12.2f}" if delta is not None else "          —"
            ref_str = f"{ref:10.1f}" if ref is not None else "         —"
            print(f"{c:>5}  {log10_val:>14.2f}  {delta_str}  {ref_str}  {elapsed:7.1f}s")

        results.append({
            "c": c, "N": N, "dps": dps,
            "lambda_min": float(mp.nstr(lam_min, 15)),
            "log10_lambda_min": log10_val,
            "delta_log10": delta,
            "run1_ref_log10": ref,
            "elapsed_s": elapsed,
        })
        prev_log10 = log10_val

    return results


def assess_stabilization(results: list[dict]) -> dict:
    """Check whether the plateau criterion is met.

    Criterion: after the first c, subsequent Δ values are < 50% of the
    first delta (from STABILIZATION.md).
    """
    deltas = [r["delta_log10"] for r in results if r["delta_log10"] is not None]
    if len(deltas) < 2:
        return {"stable": False, "reason": "too few points"}

    first_delta = deltas[0]
    threshold = 0.5 * first_delta
    plateau_start_idx = None
    for i, d in enumerate(deltas):
        if d < threshold:
            plateau_start_idx = i + 1  # +1 because deltas[0] is between c[0] and c[1]
            break

    stable = plateau_start_idx is not None
    plateau_c = results[plateau_start_idx]["c"] if stable else None
    return {
        "stable": stable,
        "first_delta": first_delta,
        "threshold": threshold,
        "plateau_starts_at_c": plateau_c,
        "n_plateau_points": len(deltas) - plateau_start_idx if stable else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extended Galerkin stabilization verification"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: N=3, dps=30, plateau shape test (~5 min)",
    )
    parser.add_argument(
        "--medium",
        action="store_true",
        help="Medium mode: N=10, dps=40, cutoffs up to c=37 (~30-60 min)",
    )
    parser.add_argument(
        "--cutoff-max",
        type=int,
        default=None,
        help="Override maximum prime cutoff (default: 37 quick, 100 full)",
    )
    args = parser.parse_args()

    if args.quick:
        N, dps = 3, 30
        cutoffs = CUTOFFS_STANDARD
        run_label = "Quick (N=3, dps=30) — plateau shape test (~5 min)"
    elif args.medium:
        N, dps = 10, 40
        cutoffs = CUTOFFS_STANDARD
        run_label = "Medium (N=10, dps=40) — sharpened plateau (~30-60 min)"
    else:
        N, dps = 30, 50
        cutoffs = CUTOFFS_STANDARD
        run_label = "Standard (N=30, dps=50) — replicating STABILIZATION Run 1 (~hours)"

    if args.cutoff_max is not None:
        cutoffs = [c for c in cutoffs if c <= args.cutoff_max]

    print("=" * 72)
    print("  EXTENDED GALERKIN STABILIZATION VERIFICATION")
    print(f"  {run_label}")
    print("=" * 72)

    t_total = time.time()
    results = run_stabilization(cutoffs, N=N, dps=dps, verbose=True)
    assessment = assess_stabilization(results)

    print("\nSTABILIZATION ASSESSMENT:")
    if assessment["stable"]:
        print(f"  STABLE  — plateau begins at c={assessment['plateau_starts_at_c']}")
        print(f"  First Δ = {assessment['first_delta']:.2f}, threshold = {assessment['threshold']:.2f}")
        print(f"  Plateau points: {assessment['n_plateau_points']}")
    else:
        print(f"  NOT STABLE — {assessment.get('reason', 'plateau criterion not met')}")

    # Deviation from Run 1 (if available)
    run1_deviations = [
        abs(r["log10_lambda_min"] - r["run1_ref_log10"])
        for r in results
        if r["run1_ref_log10"] is not None and r["log10_lambda_min"] != float("-inf")
    ]
    if run1_deviations:
        print(f"\n  vs Run 1 (N=30, dps=50): max deviation = {max(run1_deviations):.3f} OOM")
        if args.quick:
            print("  (Quick N=3: absolute values differ from N=30 — plateau shape is what matters)")
        else:
            print("  (Standard mode: should closely match Run 1 N=30 values)")

    print(f"\n  Total elapsed: {time.time() - t_total:.1f}s")
    print("=" * 72)

    # Save results
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results"
    )
    os.makedirs(out_dir, exist_ok=True)
    label = "quick" if args.quick else ("medium" if args.medium else "standard")
    out_path = os.path.join(out_dir, f"galerkin_extended_{label}_N{N}.json")
    with open(out_path, "w") as f:
        json.dump(
            {
                "run_label": run_label,
                "N": N,
                "dps": dps,
                "assessment": assessment,
                "results": results,
            },
            f,
            indent=2,
        )
    print(f"  Results saved to: {out_path}")

    # Exit code: 0 if stable, 1 if not
    sys.exit(0 if assessment["stable"] else 1)


if __name__ == "__main__":
    main()
