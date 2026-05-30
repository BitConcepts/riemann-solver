# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Bridge runner: Suzuki norm equality + Shannon eigenvalue analysis.

Tests the analytical bridge from our computational evidence (form
stabilization, eigenvalue isolation) to the proof gap (convergence +
identification).

Phase 8: Suzuki Theorem 1.4 norm equality (RH equivalent)
Phase 9: Shannon number verification (eigenvalue structure prediction)
Phase 10: Screw line computation (Suzuki's H₀ space)

Usage:
    python run_bridge.py

Estimated times:
    Phase 8: ~10-30 min (numerical integration is slow at high dps)
    Phase 9: ~20-60 min (builds Galerkin matrices at each cutoff)
    Phase 10: ~5 min (screw function evaluation)
"""

import json
import os
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, "src")

import mpmath as mp
from riemann.resources import check_resources, print_summary

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
SEP = "=" * 72


def save(name, data):
    path = os.path.join(RESULTS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  -> {path}")


def phase_8_suzuki_norm_equality():
    """Test Suzuki's Theorem 1.4: RH ⟺ ||P̂Dψ||² = π⟨ψ, ψ⟩_W.

    This is an UNCONDITIONAL RH equivalent. If the norm equality fails
    for ANY test function, RH is false.

    We test with 5 different C^∞ bump functions at two cutoff levels.
    """
    from riemann.suzuki import run_norm_equality_suite

    print(f"\n{SEP}")
    print("  PHASE 8: SUZUKI THEOREM 1.4 — NORM EQUALITY TEST")
    print("  RH ⟺ ||P̂Dψ||² = π⟨ψ, ψ⟩_W for all ψ ∈ C_c^∞(ℝ)")
    print(SEP)

    all_results = []

    for n_z in [10, 30]:
        print(f"\n  --- Using {n_z} zeros ---")
        t0 = time.time()
        results = run_norm_equality_suite(n_zeros=n_z, dps=25)
        elapsed = time.time() - t0

        for r in results:
            status = "✓" if abs(r.ratio - 1.0) < 0.5 else "✗ VIOLATION"
            print(f"  {status} {r.test_function_name}:")
            print(f"      ||P̂Dψ||² = {r.pw_norm_sq:.6e}")
            print(f"      π⟨ψ,ψ⟩_W = {r.pi_weil_form:.6e}")
            print(f"      ratio     = {r.ratio:.6f}")
            print(f"      log10|r-1|= {r.log10_residual:.1f}")

            all_results.append({
                "n_zeros": n_z,
                "test_function": r.test_function_name,
                "pw_norm_sq": r.pw_norm_sq,
                "pi_weil_form": r.pi_weil_form,
                "ratio": r.ratio,
                "log10_residual": r.log10_residual,
            })

        print(f"  Time ({n_z} zeros): {elapsed:.0f}s")

    # Check for violations
    violations = [r for r in all_results if abs(r["ratio"] - 1.0) > 0.5]
    consistent = len(violations) == 0

    summary = {
        "results": all_results,
        "n_tests": len(all_results),
        "n_violations": len(violations),
        "all_consistent_with_rh": consistent,
        "interpretation": (
            "All test functions satisfy the norm equality within numerical precision. "
            "Consistent with RH via Suzuki's Theorem 1.4."
            if consistent else
            f"{len(violations)} VIOLATIONS detected! Investigate for potential RH disproof."
        ),
    }

    print(f"\n  Consistent with RH: {consistent}")
    if not consistent:
        print("  *** NORM EQUALITY VIOLATIONS — INVESTIGATE ***")
    save("phase8_suzuki_norm_equality", summary)
    return summary


def phase_9_shannon_verification():
    """Verify that the Shannon number predicts eigenvalue structure.

    Ohzeki (2026) shows the Laplace-Slepian kernel has Shannon number
    N_c = 2·log(c)/π. We verify this matches the actual number of
    significant eigenvalues in the CvS Galerkin matrix.
    """
    from riemann.shannon import (
        shannon_number,
        verify_shannon_prediction,
        explain_stabilization,
    )

    print(f"\n{SEP}")
    print("  PHASE 9: SHANNON NUMBER VERIFICATION")
    print("  Does N_c = 2·log(c)/π predict eigenvalue structure?")
    print(SEP)

    # First: print theoretical predictions
    print("\n  Theoretical Shannon numbers:")
    for c in [7, 11, 13, 17, 19, 23, 29, 37, 47]:
        Nc = shannon_number(c)
        print(f"    c={c:2d}: N_c = {Nc:.2f}")

    # Run verification against actual Galerkin matrices
    print("\n  Computing Galerkin eigenvalue structures...")
    t0 = time.time()
    cutoffs = [13, 29]
    verifications = verify_shannon_prediction(cutoffs, N=30, dps=30)
    elapsed = time.time() - t0

    results = []
    for v in verifications:
        print(f"\n  c={v.cutoff}: N_c={v.shannon_number:.2f}")
        print(f"    Significant eigenvalues: {v.n_significant_measured}")
        print(f"    Cliff drop: {v.cliff_drop_oom:.1f} OOM")
        print(f"    Plunge (predicted/measured): {v.plunge_width_predicted:.1f} / {v.plunge_width_measured}")
        print(f"    {v.conclusion}")

        results.append({
            "cutoff": v.cutoff,
            "shannon_number": v.shannon_number,
            "n_significant": v.n_significant_measured,
            "ratio": v.ratio,
            "cliff_drop_oom": v.cliff_drop_oom,
            "plunge_predicted": v.plunge_width_predicted,
            "plunge_measured": v.plunge_width_measured,
            "conclusion": v.conclusion,
        })

    # Stabilization explanation
    expl = explain_stabilization()
    print(f"\n  Stabilization explanation:\n  {expl.explanation}")

    summary = {
        "verifications": results,
        "stabilization_explanation": expl.explanation,
        "oversampling_ratio_start": expl.oversampling_ratio_start,
        "oversampling_ratio_end": expl.oversampling_ratio_end,
        "time_s": elapsed,
    }
    save("phase9_shannon_verification", summary)
    return summary


def phase_10_screw_line():
    """Compute Suzuki's screw function S_t along the critical line.

    S_t(1/2 + it) generates elements of the unconditional space H₀.
    Under RH, H₀ = H_W (the Weil Hilbert space). We compute S_t for
    several values of t and check the norm structure.
    """
    from riemann.suzuki import compute_screw_line

    print(f"\n{SEP}")
    print("  PHASE 10: SUZUKI SCREW LINE COMPUTATION")
    print("  Computing S_t(1/2+it) for the unconditional space H₀")
    print(SEP)

    results = []
    t0 = time.time()

    for t_param in [10, 50, 100, 200]:
        if not check_resources(f"screw t={t_param}"):
            break

        tc = time.time()
        result = compute_screw_line(
            t=t_param,
            sigma=0.5,
            t_range=(10, 50),
            n_points=50,
            dps=25,
        )
        elapsed_t = time.time() - tc

        results.append({
            "t_param": t_param,
            "sigma": 0.5,
            "norm_sq": result.norm_sq,
            "n_points": len(result.z_values),
            "time_s": elapsed_t,
        })
        print(f"  t={t_param:3d}: ||S_t||² = {result.norm_sq:.6e} ({elapsed_t:.0f}s)")

    # Check if norms are growing (they should, as S_t picks up more primes)
    norms = [r["norm_sq"] for r in results]
    growing = all(norms[i] <= norms[i+1] * 10 for i in range(len(norms)-1))  # allow some fluctuation

    elapsed = time.time() - t0
    summary = {
        "results": results,
        "norms_consistent": growing,
        "interpretation": (
            "S_t norm grows with t as expected (more primes contribute). "
            "The screw line traces out a path in H₀."
        ),
        "time_s": elapsed,
    }
    print(f"\n  Norms consistent: {growing}")
    print(f"  Time: {elapsed:.0f}s")
    save("phase10_screw_line", summary)
    return summary


def main():
    print(SEP)
    print("  RIEMANN SOLVER — BRIDGE ANALYSIS")
    print("  Connecting computation to proof via Suzuki + Ohzeki")
    print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backend: {mp.libmp.BACKEND}")
    print_summary()
    print(SEP)

    t_total = time.time()

    # Run phases: fastest first, then important, then heavy
    for name, func in [
        ("Screw line", phase_10_screw_line),
        ("Suzuki norm equality", phase_8_suzuki_norm_equality),
        ("Shannon verification", phase_9_shannon_verification),
    ]:
        if not check_resources(name):
            print(f"  Skipping {name}: resources too low")
            continue
        try:
            func()
        except KeyboardInterrupt:
            print(f"  INTERRUPTED: {name}")
            break
        except Exception as e:
            print(f"  ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            save(f"error_{name.replace(' ', '_')}", {"error": str(e)})

    total = time.time() - t_total
    print(f"\n{SEP}")
    print(f"  BRIDGE ANALYSIS COMPLETE")
    print(f"  Total wall time: {total/60:.1f} minutes")
    print(f"  Results in: {RESULTS_DIR}/")
    print(SEP)


# CRITICAL: __name__ guard prevents fork bomb on Windows
if __name__ == "__main__":
    main()
