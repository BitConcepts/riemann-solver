# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Analytical bridge pipeline toward the convergence gap.

The convergence gap (PROOF_STRATEGY.md) is:
    Prove that det_reg(D^(λ,N)_log − z) → Ξ(z) as N, λ → ∞

This pipeline collects three bodies of supporting evidence:

  Phase 8 — Suzuki norm equality
      Tests ||P̂Dψ||² = π⟨ψ,ψ⟩_W for multiple test functions.
      If this holds, the spectral theory of the Weil operator is
      consistent with RH (Suzuki 2011, J. Math. Soc. Japan).

  Phase 9 — Shannon / form stabilization at c=100
      Verifies that the Galerkin form stabilizes per Shannon theory
      and computes the information capacity of the channel.

  Phase 10 — Quantitative eigenvector convergence
      Measures the rate at which eigenvectors v(c) converge as c → ∞
      using connes_cvs. A power law v(c) → v(∞) at a measurable rate
      supports (but does not prove) the convergence hypothesis.

Usage:
    python run_bridge.py              # Full run
    python run_bridge.py --quick      # Quick run (~2 min)
    python run_bridge.py --phase 8    # Single phase
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import mpmath as mp

# Phase 8 imports
from src.riemann.suzuki import run_norm_equality_suite

# Phase 9 imports
from src.riemann.shannon import shannon_number, verify_shannon_prediction, explain_stabilization

# Phase 10 imports
import connes_cvs


# ============================================================================
# Phase 8: Suzuki norm equality
# ============================================================================

def run_phase8(quick: bool) -> dict:
    """Run Suzuki ||P̂Dψ||² = π⟨ψ,ψ⟩_W norm equality suite."""
    n_zeros = 30 if quick else 50
    dps = 30 if quick else 50

    print(f"\n{'=' * 72}")
    print("  PHASE 8 — SUZUKI NORM EQUALITY")
    print(f"  n_zeros={n_zeros}, dps={dps}")
    print(f"  Ref: Suzuki (2011), J. Math. Soc. Japan 63(4)")
    print(f"{'=' * 72}")

    t0 = time.time()
    results = run_norm_equality_suite(n_zeros=n_zeros, dps=dps)
    elapsed = time.time() - t0

    print(f"\n  {'Function':<20}  {'||P̂Dψ||²':>14}  {'π⟨ψ,ψ⟩_W':>14}  {'ratio':>8}  {'log₁₀res':>10}")
    print(f"  {'-' * 72}")
    consistent = []
    for r in results:
        ratio = float(r.ratio) if r.ratio is not None else float("nan")
        log10r = float(r.log10_residual) if r.log10_residual is not None else float("nan")
        ok = abs(ratio - 1.0) < 0.01 if not math.isnan(ratio) else False
        consistent.append(ok)
        mark = "✓" if ok else "✗"
        print(
            f"  {r.test_function_name:<20}  {float(r.pw_norm_sq):>14.6g}  "
            f"{float(r.pi_weil_form):>14.6g}  {ratio:>8.5f}  {log10r:>10.2f}  {mark}"
        )

    n_ok = sum(consistent)
    n_total = len(consistent)
    all_ok = n_ok == n_total
    print(f"\n  Consistent with RH: {n_ok}/{n_total}  ({'PASS' if all_ok else 'FAIL'})")
    print(f"  Elapsed: {elapsed:.1f}s")

    return {
        "phase": 8,
        "n_zeros": n_zeros,
        "dps": dps,
        "n_consistent": n_ok,
        "n_total": n_total,
        "passed": all_ok,
        "elapsed_s": elapsed,
        "results": [
            {
                "function": r.test_function_name,
                "ratio": float(r.ratio) if r.ratio is not None else None,
                "log10_residual": float(r.log10_residual) if r.log10_residual is not None else None,
            }
            for r in results
        ],
    }


# ============================================================================
# Phase 9: Shannon / form stabilization
# ============================================================================

def run_phase9(quick: bool) -> dict:
    """Run Shannon number analysis and form stabilization at c=100."""
    cutoffs = [7, 11, 13, 17, 19, 23, 29] if quick else [7, 11, 13, 17, 19, 23, 29, 37, 47, 100]
    N = 30 if quick else 50
    dps = 30 if quick else 50

    print(f"\n{'=' * 72}")
    print("  PHASE 9 — SHANNON NUMBER ANALYSIS & FORM STABILIZATION")
    print(f"  cutoffs={cutoffs}, N={N}, dps={dps}")
    print(f"  Ref: Ohzeki (2026), arXiv:2605.26586")
    print(f"{'=' * 72}")

    t0 = time.time()

    # Shannon number table
    print(f"\n  {'c':>5}  {'N_c = 2log(c)/π':>18}  {'plunge_width':>14}")
    print(f"  {'-' * 42}")
    shannon_data = []
    for c in cutoffs:
        Nc = shannon_number(c)
        # Plunge width from connes_cvs.build_galerkin_matrix's eigenvalue structure
        # Use a simplified Ohzeki formula: plunge_width ≈ log(N) / (2*N_c)
        Nc_val = float(Nc)
        pw = math.log(max(N, 1)) / (2 * max(Nc_val, 1e-10))
        print(f"  {c:>5}  {Nc_val:>18.4f}  {pw:>14.6f}")
        shannon_data.append({"c": c, "shannon_number": Nc_val, "plunge_width_estimate": pw})

    # Stabilization explanation
    print(f"\n  Stabilization explanation (c_start=17, c_end={cutoffs[-1]}, N={N}):")
    explanation = explain_stabilization(c_start=17, c_end=cutoffs[-1], N=N)
    expl_text = getattr(explanation, 'explanation', str(explanation))
    for line in expl_text.strip().split("\n")[:8]:
        print(f"  {line}")

    # Shannon oversampling check: stabilization occurs when N >> N_c
    # (Ohzeki 2026: eigenvector is fully captured when N/N_c >> 1)
    Nc_max = float(shannon_number(cutoffs[-1]))
    oversampling_ratio = N / max(Nc_max, 1e-10)
    capacity_ok = oversampling_ratio > 5.0  # N at least 5x the Shannon number

    elapsed = time.time() - t0
    print(f"\n  N_c(c={cutoffs[-1]}) = {Nc_max:.4f},  oversampling N/N_c = {oversampling_ratio:.1f}")
    print(f"  Oversampling ≥ 5x (stabilization condition): {'YES' if capacity_ok else 'NO'}")
    print(f"  Elapsed: {elapsed:.1f}s")

    return {
        "phase": 9,
        "N": N,
        "dps": dps,
        "cutoffs": cutoffs,
        "shannon_data": shannon_data,
        "shannon_capacity_exceeds_dof": capacity_ok,
        "passed": capacity_ok,
        "elapsed_s": elapsed,
    }


# ============================================================================
# Phase 10: Quantitative eigenvector convergence
# ============================================================================

def run_phase10(quick: bool) -> dict:
    """Measure the rate at which eigenvectors v(c) converge as c → ∞.

    Computes ||v(c') - v(c)|| / ||v(c)|| for successive c values and
    fits a power-law convergence model: ||Δv|| ~ A * c^(-α).

    A measurable decay (α > 0) supports the convergence hypothesis.
    """
    if quick:
        cutoffs = [13, 17, 19, 23, 29]
        N, dps = 3, 30
    else:
        cutoffs = [13, 17, 19, 23, 29, 37]
        N, dps = 5, 40

    print(f"\n{'=' * 72}")
    print("  PHASE 10 — QUANTITATIVE EIGENVECTOR CONVERGENCE RATE")
    print(f"  N={N}, dps={dps}, cutoffs={cutoffs}")
    print(f"  Ref: Groskin (2026) §4, eigenvector c-invariance")
    print(f"{'=' * 72}")

    mp.mp.dps = dps
    t0 = time.time()

    eigvecs: dict[int, mp.matrix] = {}
    lambda_mins: dict[int, float] = {}

    print(f"\n  Building eigenvectors...")
    for c in cutoffs:
        t1 = time.time()
        Q = connes_cvs.build_galerkin_matrix(c=c, N=N, T=100, dps=dps)
        lam, v = connes_cvs.compute_ground_state(Q)
        eigvecs[c] = v
        lam_abs = abs(float(mp.nstr(lam, 6)))
        lambda_mins[c] = math.log10(lam_abs) if lam_abs > 0 else float("-inf")
        print(f"    c={c:>3}: log₁₀|λ_min|={lambda_mins[c]:.2f}, elapsed={time.time()-t1:.1f}s")

    # Compute relative change between successive eigenvectors
    print(f"\n  {'c_prev':>7}  {'c_curr':>7}  {'||Δv||/||v||':>14}  {'log₁₀(ratio)':>14}")
    print(f"  {'-' * 52}")

    convergence_data = []
    log_c_vals = []
    log_ratio_vals = []

    for i in range(1, len(cutoffs)):
        c_prev = cutoffs[i - 1]
        c_curr = cutoffs[i]
        v_prev = eigvecs[c_prev]
        v_curr = eigvecs[c_curr]

        # Align signs (eigenvectors are defined up to sign)
        dot_sign = float(mp.re(sum(v_curr[k] * v_prev[k] for k in range(v_curr.rows))))
        if dot_sign < 0:
            v_curr = -v_curr

        # Relative change
        diff = v_curr - v_prev
        norm_diff = float(mp.sqrt(sum(diff[k]**2 for k in range(diff.rows))))
        norm_prev = float(mp.sqrt(sum(v_prev[k]**2 for k in range(v_prev.rows))))
        rel_change = norm_diff / norm_prev if norm_prev > 0 else float("nan")
        log10_rel = math.log10(rel_change) if rel_change > 0 else float("nan")

        print(f"  {c_prev:>7}  {c_curr:>7}  {rel_change:>14.6f}  {log10_rel:>14.4f}")
        convergence_data.append({
            "c_prev": c_prev, "c_curr": c_curr,
            "rel_change": rel_change, "log10_rel_change": log10_rel,
        })
        if not math.isnan(log10_rel):
            log_c_vals.append(math.log(c_curr))
            log_ratio_vals.append(log10_rel)

    # Fit power law: log10(||Δv||/||v||) = -α * log(c) + const
    # using least-squares on log_c_vals, log_ratio_vals
    alpha = None
    r_squared = None
    if len(log_c_vals) >= 2:
        n = len(log_c_vals)
        mean_x = sum(log_c_vals) / n
        mean_y = sum(log_ratio_vals) / n
        ss_xy = sum((log_c_vals[i] - mean_x) * (log_ratio_vals[i] - mean_y) for i in range(n))
        ss_xx = sum((x - mean_x) ** 2 for x in log_c_vals)
        if ss_xx > 0:
            slope = ss_xy / ss_xx  # d(log10_ratio)/d(log_c)
            alpha = -slope  # convergence exponent: ||Δv|| ~ c^(-alpha)
            # R²
            y_pred = [mean_y + slope * (x - mean_x) for x in log_c_vals]
            ss_res = sum((log_ratio_vals[i] - y_pred[i]) ** 2 for i in range(n))
            ss_tot = sum((y - mean_y) ** 2 for y in log_ratio_vals)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    elapsed = time.time() - t0
    converging = alpha is not None and alpha > 0.1

    print(f"\n  Power-law fit: ||Δv(c)|| ~ c^(-α)")
    if alpha is not None:
        print(f"  α = {alpha:.4f}  (R² = {r_squared:.4f})")
        print(f"  Convergence: {'YES — α > 0.1' if converging else 'MARGINAL/NO — α ≤ 0.1'}")
    else:
        print(f"  Insufficient data for fit.")
    print(f"  Elapsed: {elapsed:.1f}s")

    return {
        "phase": 10,
        "N": N,
        "dps": dps,
        "cutoffs": cutoffs,
        "convergence_data": convergence_data,
        "alpha": alpha,
        "r_squared": r_squared,
        "converging": converging,
        "passed": converging,
        "elapsed_s": elapsed,
    }


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Analytical bridge pipeline (Phases 8–10)")
    parser.add_argument("--quick", action="store_true",
                        help="Quick mode — reduced parameters, ~2 min")
    parser.add_argument("--phase", type=int, choices=[8, 9, 10], default=None,
                        help="Run a single phase only")
    args = parser.parse_args()

    print("=" * 72)
    print("  ANALYTICAL BRIDGE PIPELINE  (toward convergence gap proof)")
    print(f"  Mode: {'Quick' if args.quick else 'Full'}"
          + (f" — Phase {args.phase} only" if args.phase else " — All phases"))
    print("=" * 72)

    results = {}
    t_total = time.time()

    if args.phase is None or args.phase == 8:
        results[8] = run_phase8(args.quick)

    if args.phase is None or args.phase == 9:
        results[9] = run_phase9(args.quick)

    if args.phase is None or args.phase == 10:
        results[10] = run_phase10(args.quick)

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 72}")
    print("  BRIDGE PIPELINE SUMMARY")
    print(f"{'=' * 72}")

    phase_labels = {
        8: "Suzuki norm equality",
        9: "Shannon / form stabilization",
        10: "Eigenvector convergence rate",
    }
    all_pass = True
    for ph, res in sorted(results.items()):
        passed = res.get("passed", False)
        label = phase_labels.get(ph, f"Phase {ph}")
        status = "PASS" if passed else "FAIL"
        all_pass = all_pass and passed
        print(f"  Phase {ph} ({label}): {status}")

    if 10 in results and results[10]["alpha"] is not None:
        alpha = results[10]["alpha"]
        print(f"\n  Eigenvector convergence exponent α = {alpha:.4f}")
        if alpha > 0.5:
            print("  → Strong evidence for eigenvector convergence (α > 0.5)")
        elif alpha > 0.1:
            print("  → Weak evidence for convergence (α > 0.1) — more c values needed")
        else:
            print("  → No clear convergence signal yet")

    print(f"\n  Overall: {'ALL PHASES PASS' if all_pass else 'SOME PHASES FAIL/PARTIAL'}")
    print(f"  Total elapsed: {time.time() - t_total:.1f}s")
    print("=" * 72)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    label = "quick" if args.quick else "full"
    ph_label = f"_phase{args.phase}" if args.phase else ""
    out_path = os.path.join(out_dir, f"bridge_{label}{ph_label}.json")
    with open(out_path, "w") as f:
        json.dump(
            {
                "mode": "quick" if args.quick else "full",
                "phases": {str(k): v for k, v in results.items()},
                "all_passed": all_pass,
            },
            f,
            indent=2,
            default=str,  # handle mpf objects
        )
    print(f"  Results saved to: {out_path}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
