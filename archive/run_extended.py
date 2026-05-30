# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Extended runs: higher-N stabilization, 55-digit CvS, Geiger safety factors.

Usage:
    python run_extended.py

Estimated time: ~3-4 hours (single-threaded mpmath)
"""

import json
import math
import os
import sys
import time

sys.path.insert(0, ".")
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


def ext1_stabilization_high_n():
    """Form stabilization at N=100 with extended cutoffs c=7..47."""
    from connes_cvs import build_galerkin_matrix, compute_ground_state

    print(f"\n{SEP}")
    print("  EXT1: FORM STABILIZATION (N=100, c=7..47)")
    print("  Does the plateau sharpen at higher N?")
    print(SEP)

    N = 100
    dps = 80
    T = 400
    cutoffs = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    results = []
    t0 = time.time()

    prev_log = None
    for c in cutoffs:
        if not check_resources(f"c={c}"):
            break
        tc = time.time()
        Q = build_galerkin_matrix(c=c, N=N, T=T, dps=dps)
        lam, _ = compute_ground_state(Q)
        log_lam = float(mp.log10(abs(lam)))
        delta = abs(log_lam - prev_log) if prev_log is not None else None
        results.append({"c": c, "N": N, "log10_lam": log_lam, "delta": delta,
                        "time_s": time.time() - tc})
        d = f"  delta={delta:.3f}" if delta else ""
        print(f"  c={c:2d}: log10|lam|={log_lam:.2f}{d}  ({time.time()-tc:.0f}s)")
        prev_log = log_lam

    elapsed = time.time() - t0
    # Analyze plateau
    post17 = [r for r in results if r["c"] >= 17 and r["delta"] is not None]
    if post17:
        avg_delta = sum(r["delta"] for r in post17) / len(post17)
        max_delta = max(r["delta"] for r in post17)
        plateau_range = max(r["log10_lam"] for r in post17) - min(r["log10_lam"] for r in post17)
    else:
        avg_delta = max_delta = plateau_range = None

    summary = {
        "N": N, "cutoffs": cutoffs, "results": results,
        "plateau_avg_delta": avg_delta, "plateau_max_delta": max_delta,
        "plateau_range_oom": plateau_range, "time_s": elapsed,
    }
    print(f"\n  Plateau (c>=17): avg_delta={avg_delta:.3f}, range={plateau_range:.2f} OOM")
    print(f"  Time: {elapsed:.0f}s")
    save("ext1_stabilization_N100", summary)
    return summary


def ext2_cvs_high_precision():
    """CvS sweep at N=100, dps=150 for 55-digit gamma_1 precision."""
    from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros

    print(f"\n{SEP}")
    print("  EXT2: CvS HIGH PRECISION (N=100, dps=150)")
    print("  Targeting 55-digit gamma_1 (Groskin reference)")
    print(SEP)

    cutoffs = [13, 17]
    results = []
    t0 = time.time()

    for c in cutoffs:
        if not check_resources(f"c={c} deep"):
            break
        tc = time.time()
        Q = build_galerkin_matrix(c=c, N=100, T=800, dps=150)
        lam, eigvec = compute_ground_state(Q)
        zeros = extract_zeros(eigvec, L=math.log(c), n_zeros=3, dps=150)
        elapsed_c = time.time() - tc

        log_lam = float(mp.log10(abs(lam)))
        zero_data = []
        for z in zeros:
            digits = -float(mp.log10(abs(z["error"]))) if z["error"] else None
            zero_data.append({"k": z["k"], "digits": digits})
            d = f"{digits:.0f}" if digits else "?"
            print(f"  c={c}: gamma_{z['k']}: {d} matching digits")

        results.append({
            "c": c, "N": 100, "dps": 150,
            "log10_lam": log_lam, "zeros": zero_data,
            "time_s": elapsed_c,
        })

    elapsed = time.time() - t0
    print(f"\n  Time: {elapsed:.0f}s")
    save("ext2_cvs_high_precision", results)
    return results


def ext3_geiger_safety():
    """Reproduce Geiger's even-dominance safety factors at larger lambda."""
    from riemann.even_dominance import check_even_dominance

    print(f"\n{SEP}")
    print("  EXT3: GEIGER SAFETY FACTOR REPRODUCTION")
    print("  Testing at lambda=100,200,500,1000 with N=30")
    print(SEP)

    lambdas = [100.0, 200.0, 500.0, 1000.0]
    results = []
    t0 = time.time()

    for lam in lambdas:
        if not check_resources(f"lam={lam}"):
            break
        tc = time.time()
        cert = check_even_dominance(lam, N=30, dps=30)
        elapsed_l = time.time() - tc
        status = "EVEN" if cert.even_dominates else "ODD"
        results.append({
            "lambda": lam, "c": cert.c,
            "min_even": str(cert.lambda_min_even),
            "min_odd": str(cert.lambda_min_odd),
            "even_dominates": cert.even_dominates,
            "safety_factor": cert.safety_factor,
            "time_s": elapsed_l,
        })
        print(f"  lam={lam:.0f}: {status}, safety={cert.safety_factor:.1f}x ({elapsed_l:.0f}s)")

    elapsed = time.time() - t0
    print(f"\n  Time: {elapsed:.0f}s")
    save("ext3_geiger_safety", results)
    return results


def main():
    print(SEP)
    print("  RIEMANN SOLVER — EXTENDED RUNS")
    print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backend: {mp.libmp.BACKEND}")
    print_summary()
    print(SEP)

    t_total = time.time()

    ext3_geiger_safety()       # ~5 min (fast, do first)
    ext1_stabilization_high_n()  # ~2-3 hours (the big one)
    ext2_cvs_high_precision()  # ~30-60 min

    total = time.time() - t_total
    print(f"\n{SEP}")
    print(f"  EXTENDED RUNS COMPLETE: {total/60:.1f} minutes")
    print(SEP)


if __name__ == "__main__":
    main()
