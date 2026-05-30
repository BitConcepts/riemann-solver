# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Run all solver attack vectors and falsification harnesses."""

import sys
import time

sys.path.insert(0, ".")
import mpmath as mp

SEPARATOR = "=" * 72


def run_1_zeros():
    """Zero verification against Odlyzko tables."""
    from benchmarks.bench_zeros import run_benchmark

    print(SEPARATOR)
    print("RUN 1: ZERO VERIFICATION vs ODLYZKO TABLES (20 zeros, 30 dps)")
    print(SEPARATOR)
    mp.mp.dps = 30
    t0 = time.time()
    results = run_benchmark(20, dps=30)
    elapsed = time.time() - t0
    for r in results:
        s = "MATCH" if r["match"] else "**MISMATCH**"
        idx = r["index"]
        t_val = mp.nstr(r["computed"], 18)
        err = mp.nstr(r["error"], 4)
        print(f"  rho_{idx:2d}  t={t_val:>26s}  err={err:>12s}  {s}")
    all_ok = all(r["match"] for r in results)
    max_err = max(r["error"] for r in results)
    print(f"\n  All match: {all_ok}")
    print(f"  Max error: {mp.nstr(max_err, 6)}")
    print(f"  Time: {elapsed:.2f}s")
    return all_ok


def run_2_li():
    """Li criterion: compute lambda_1 through lambda_10."""
    from riemann.li_criterion import li_coefficient

    print(f"\n{SEPARATOR}")
    print("RUN 2: LI CRITERION (lambda_1 through lambda_10, 50 zeros)")
    print(SEPARATOR)
    mp.mp.dps = 25
    t0 = time.time()
    coeffs = []
    for n in range(1, 11):
        c = li_coefficient(n, dps=25, num_zeros=50)
        coeffs.append(c)
        sign = "+" if c.positive else "NEGATIVE"
        print(f"  lambda_{n:2d} = {mp.nstr(c.value, 15):>22s}  [{sign}]")
    elapsed = time.time() - t0
    all_pos = all(c.positive for c in coeffs)
    print(f"\n  All positive: {all_pos}")
    print(f"  Verdict: {'consistent_with_rh' if all_pos else 'RH_VIOLATED'}")
    print(f"  Time: {elapsed:.2f}s")
    return all_pos


def run_3_offline():
    """Off-critical-line falsification search."""
    from riemann.zeros import off_line_search

    print(f"\n{SEPARATOR}")
    print("RUN 3: OFF-LINE FALSIFICATION SEARCH")
    print(SEPARATOR)
    mp.mp.dps = 30
    t0 = time.time()
    sigmas = [0.3, 0.4, 0.6, 0.7]
    total_candidates = 0
    for sigma in sigmas:
        candidates = off_line_search(sigma, 10, 100, 0.5, 30, 1e-6)
        total_candidates += len(candidates)
        status = f"{len(candidates)} candidates" if candidates else "clean"
        print(f"  sigma={sigma}: {status}")
        for c in candidates:
            print(f"    *** t={mp.nstr(c[1], 10)}, |zeta|={mp.nstr(c[2], 6)} ***")
    elapsed = time.time() - t0
    print(f"\n  Total off-line candidates: {total_candidates}")
    print(f"  Verdict: {'NO_COUNTEREXAMPLE' if total_candidates == 0 else 'INVESTIGATE'}")
    print(f"  Time: {elapsed:.2f}s")
    return total_candidates == 0


def run_4_gram():
    """Gram violation analysis."""
    from falsification.gram_violations import find_gram_violations

    print(f"\n{SEPARATOR}")
    print("RUN 4: GRAM VIOLATION ANALYSIS (n < 500)")
    print(SEPARATOR)
    mp.mp.dps = 15
    t0 = time.time()
    violations = find_gram_violations(500)
    elapsed = time.time() - t0
    print(f"  Violations found: {len(violations)}")
    for v in violations[:15]:
        print(f"    n={v['index']:4d}  g={v['gram_point']:12.6f}  Z={v['z_value']:+.8f}")
    if len(violations) > 15:
        print(f"    ... and {len(violations) - 15} more")
    print(f"\n  First violation at n={violations[0]['index']} (literature: n=126)")
    print(f"  Time: {elapsed:.2f}s")
    return True


def run_5_lehmer():
    """Lehmer pair search."""
    from riemann.dbn_constant import find_lehmer_pairs

    print(f"\n{SEPARATOR}")
    print("RUN 5: LEHMER PAIR SEARCH (first 200 zeros, threshold=0.6)")
    print(SEPARATOR)
    mp.mp.dps = 25
    t0 = time.time()
    pairs = find_lehmer_pairs(1, 200, threshold=0.6, dps=25)
    elapsed = time.time() - t0
    print(f"  Close pairs found: {len(pairs)}")
    for p in pairs:
        print(
            f"    zeros {p.index}/{p.index+1}: "
            f"gap={mp.nstr(p.gap, 8)}, "
            f"normalized={mp.nstr(p.normalized_gap, 5)}"
        )
    print(f"\n  Time: {elapsed:.2f}s")
    return True


def run_6_spacing():
    """Zero spacing statistics (GUE)."""
    from riemann.zeros import compute_zeros, normalized_spacing

    print(f"\n{SEPARATOR}")
    print("RUN 6: ZERO SPACING STATISTICS (100 zeros, GUE comparison)")
    print(SEPARATOR)
    mp.mp.dps = 20
    t0 = time.time()
    zeros = compute_zeros(1, 100, dps=20)
    nsp = normalized_spacing(zeros)
    elapsed = time.time() - t0

    fsp = [float(s) for s in nsp]
    mean_s = sum(fsp) / len(fsp)
    var_s = sum((s - mean_s) ** 2 for s in fsp) / len(fsp)
    min_s = min(fsp)
    max_s = max(fsp)

    print(f"  Zeros computed: {len(zeros)}")
    print(f"  Spacings: {len(nsp)}")
    print(f"  Mean normalized spacing: {mean_s:.6f} (expect 1.0)")
    print(f"  Variance: {var_s:.6f}")
    print(f"  Min spacing: {min_s:.6f}")
    print(f"  Max spacing: {max_s:.6f}")
    print(f"  Time: {elapsed:.2f}s")
    return True


def run_7_li_monitor():
    """Li coefficient sign monitor."""
    from riemann.li_criterion import li_coefficient

    print(f"\n{SEPARATOR}")
    print("RUN 7: LI SIGN MONITOR (n=1..20, falsification)")
    print(SEPARATOR)
    mp.mp.dps = 20
    t0 = time.time()
    violations = []
    for n in range(1, 21):
        c = li_coefficient(n, dps=20, num_zeros=30)
        if not c.positive:
            violations.append(n)
            print(f"  *** lambda_{n} = {mp.nstr(c.value, 12)} < 0  -- RH VIOLATED ***")
        else:
            print(f"  lambda_{n:2d} = {mp.nstr(c.value, 12):>20s}  [+]")
    elapsed = time.time() - t0
    print(f"\n  Violations: {len(violations)}")
    print(f"  Verdict: {'consistent_with_rh' if not violations else 'RH_VIOLATED'}")
    print(f"  Time: {elapsed:.2f}s")
    return len(violations) == 0


def main():
    print(SEPARATOR)
    print("  RIEMANN HYPOTHESIS SOLVER — FULL RUN")
    print("  Target: Clay Millennium Prize ($1,000,000)")
    print(SEPARATOR)
    t_total = time.time()

    results = {}
    results["zeros"] = run_1_zeros()
    results["li"] = run_2_li()
    results["offline"] = run_3_offline()
    results["gram"] = run_4_gram()
    results["lehmer"] = run_5_lehmer()
    results["spacing"] = run_6_spacing()
    results["li_monitor"] = run_7_li_monitor()

    elapsed_total = time.time() - t_total

    print(f"\n{SEPARATOR}")
    print("  AGGREGATE RESULTS")
    print(SEPARATOR)
    print(f"  Zero verification:    {'PASS' if results['zeros'] else 'FAIL'}")
    print(f"  Li criterion:         {'PASS' if results['li'] else 'FAIL'}")
    print(f"  Off-line search:      {'PASS (no counterexample)' if results['offline'] else 'INVESTIGATE'}")
    print(f"  Gram violations:      DOCUMENTED")
    print(f"  Lehmer pairs:         DOCUMENTED")
    print(f"  Spacing statistics:   COMPUTED")
    print(f"  Li sign monitor:      {'PASS' if results['li_monitor'] else 'FAIL'}")
    print(f"\n  Total time: {elapsed_total:.1f}s")

    all_pass = all([results["zeros"], results["li"], results["offline"], results["li_monitor"]])
    if all_pass:
        print(f"\n  VERDICT: All verification criteria CONSISTENT WITH RH.")
        print(f"  VERDICT: All falsification harnesses found NO COUNTEREXAMPLE.")
        print(f"  STATUS:  Computational evidence supports RH.")
        print(f"  NOTE:    This is NOT a proof. A rigorous proof is required for the CMI prize.")
    else:
        print(f"\n  *** ANOMALY DETECTED — INVESTIGATION REQUIRED ***")


if __name__ == "__main__":
    main()
