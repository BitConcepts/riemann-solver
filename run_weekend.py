"""Weekend runner: deep CvS Galerkin computation + full verification sweep.

Run this overnight or over the weekend for the heavy computations:
  python run_weekend.py

Estimated times (with gmpy2 + python-flint):
  Phase 1: CvS sweep c=13..29, N=50      ~20 min
  Phase 2: CvS c=13, N=100, dps=150      ~30 min (55-digit γ₁)
  Phase 3: CvS c=17, N=100, dps=150      ~45 min
  Phase 4: Even-dominance certs λ=10..100 ~15 min
  Phase 5: DH control test                ~5 min
  Phase 6: Full falsification suite       ~10 min
  Total: ~2-3 hours

Results are saved to results/ directory as JSON.
"""

import json
import math
import os
import sys
import time

sys.path.insert(0, ".")

import mpmath as mp

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
SEP = "=" * 72


def save_result(name, data):
    """Save result to JSON file."""
    path = os.path.join(RESULTS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  -> Saved to {path}")


def phase_1_cvs_sweep():
    """CvS Galerkin sweep at small cutoffs."""
    from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros

    print(f"\n{SEP}")
    print("  PHASE 1: CvS GALERKIN SWEEP (c=13,14,17,19,23,29, N=50)")
    print(SEP)

    cutoffs = [13, 14, 17, 19, 23, 29]
    results = []
    for c in cutoffs:
        t0 = time.time()
        Q = build_galerkin_matrix(c=c, N=50, T=400, dps=80)
        lam_min, eigvec = compute_ground_state(Q)
        zeros = extract_zeros(eigvec, L=math.log(c), n_zeros=1, dps=80)
        elapsed = time.time() - t0

        gamma1_err = float(zeros[0]["error"]) if zeros[0]["error"] else None
        log_lam = float(mp.log10(abs(lam_min)))
        result = {
            "c": c, "N": 50, "dps": 80,
            "lambda_min": str(lam_min),
            "log10_lambda_min": log_lam,
            "gamma1_error": gamma1_err,
            "time_s": elapsed,
        }
        results.append(result)
        print(f"  c={c:2d}: log10|λ_min|={log_lam:.1f}, |γ₁ err|={gamma1_err:.2e}, {elapsed:.0f}s")

    save_result("phase1_cvs_sweep", results)
    return results


def phase_2_cvs_deep_13():
    """CvS Galerkin at c=13, N=100 for higher precision."""
    from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros

    print(f"\n{SEP}")
    print("  PHASE 2: CvS DEEP (c=13, N=100, dps=150)")
    print(SEP)

    t0 = time.time()
    Q = build_galerkin_matrix(c=13, N=100, T=800, dps=150)
    lam_min, eigvec = compute_ground_state(Q)
    zeros = extract_zeros(eigvec, L=math.log(13), n_zeros=5, dps=150)
    elapsed = time.time() - t0

    results = {
        "c": 13, "N": 100, "dps": 150,
        "lambda_min": str(lam_min),
        "log10_lambda_min": float(mp.log10(abs(lam_min))),
        "zeros": [],
        "time_s": elapsed,
    }
    for z in zeros:
        digits = -float(mp.log10(abs(z["error"]))) if z["error"] else None
        results["zeros"].append({
            "k": z["k"],
            "gamma_detected": str(z["gamma_detected"]),
            "error": str(z["error"]),
            "matching_digits": digits,
        })
        print(f"  γ_{z['k']}: {digits:.0f} matching digits" if digits else f"  γ_{z['k']}: not detected")

    print(f"  Total: {elapsed:.0f}s")
    save_result("phase2_cvs_deep_c13", results)
    return results


def phase_3_even_dominance():
    """Reproduce Geiger's even-dominance certificates."""
    from riemann.even_dominance import reproduce_geiger_certificates

    print(f"\n{SEP}")
    print("  PHASE 3: GEIGER EVEN-DOMINANCE CERTIFICATES")
    print(SEP)

    t0 = time.time()
    certs = reproduce_geiger_certificates(
        lambdas=[10.0, 14.0, 20.0, 30.0, 50.0, 100.0],
        N=20, dps=30,
    )
    elapsed = time.time() - t0

    results = []
    for c in certs:
        status = "EVEN" if c.even_dominates else "ODD"
        results.append({
            "lambda": c.lam, "c": c.c,
            "min_even": str(c.lambda_min_even),
            "min_odd": str(c.lambda_min_odd),
            "even_dominates": c.even_dominates,
            "safety_factor": c.safety_factor,
        })
        print(f"  λ={c.lam:.0f}: {status} (safety={c.safety_factor:.1f}x)")

    print(f"  Total: {elapsed:.0f}s")
    save_result("phase3_even_dominance", results)
    return results


def phase_4_dh_control():
    """Davenport-Heilbronn control test."""
    from riemann.davenport_heilbronn import run_dh_control

    print(f"\n{SEP}")
    print("  PHASE 4: DAVENPORT-HEILBRONN CONTROL")
    print(SEP)

    t0 = time.time()
    result = run_dh_control(dps=25)
    elapsed = time.time() - t0

    print(f"  FE residual: {result['functional_equation_residual']:.2e}")
    print(f"  On-line candidates: {result['on_line_candidates']}")
    print(f"  Off-line candidates: {result['off_line_candidates']}")
    valid = "✓ VALID" if result["control_valid"] else "✗ INVALID"
    print(f"  Control: {valid}")
    print(f"  Total: {elapsed:.0f}s")

    result["time_s"] = elapsed
    save_result("phase4_dh_control", result)
    return result


def phase_5_falsification():
    """Full falsification suite on ζ(s)."""
    print(f"\n{SEP}")
    print("  PHASE 5: FULL FALSIFICATION SUITE")
    print(SEP)

    results = {}

    # Off-line search
    from riemann.zeros import off_line_search
    mp.mp.dps = 30
    t0 = time.time()
    off_line_total = 0
    for sigma in [0.3, 0.4, 0.45, 0.55, 0.6, 0.7]:
        hits = off_line_search(sigma, 10, 200, 0.5, 30, 1e-6)
        off_line_total += len(hits)
    results["off_line"] = {"candidates": off_line_total, "range": "t=[10,200]"}
    print(f"  Off-line search: {off_line_total} candidates")

    # Li sign monitor
    from riemann.li_criterion import li_coefficient
    mp.mp.dps = 20
    li_violations = []
    for n in range(1, 25):
        c = li_coefficient(n, dps=20, num_zeros=30)
        if not c.positive:
            li_violations.append(n)
    results["li_monitor"] = {"max_n": 24, "violations": li_violations}
    print(f"  Li monitor (n≤24): {len(li_violations)} violations")

    # Gram violations
    from falsification.gram_violations import find_gram_violations
    mp.mp.dps = 15
    gv = find_gram_violations(1000)
    results["gram"] = {"n_max": 1000, "violations": len(gv)}
    print(f"  Gram violations (n<1000): {len(gv)}")

    elapsed = time.time() - t0
    results["time_s"] = elapsed
    print(f"  Total: {elapsed:.0f}s")
    save_result("phase5_falsification", results)
    return results


def main():
    print(SEP)
    print("  RIEMANN SOLVER — WEEKEND DEEP RUN")
    print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backend: {mp.libmp.BACKEND}")
    try:
        import flint
        print(f"  Flint: {flint.__version__}")
    except ImportError:
        print("  Flint: not available")
    print(SEP)

    t_total = time.time()

    phase_1_cvs_sweep()
    phase_2_cvs_deep_13()
    phase_3_even_dominance()
    phase_4_dh_control()
    phase_5_falsification()

    total = time.time() - t_total
    print(f"\n{SEP}")
    print(f"  WEEKEND RUN COMPLETE")
    print(f"  Total wall time: {total/60:.1f} minutes")
    print(f"  Results in: {RESULTS_DIR}/")
    print(SEP)


if __name__ == "__main__":
    main()
