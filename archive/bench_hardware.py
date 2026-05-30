# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Benchmark this machine's hardware for Riemann solver workloads.

IMPORTANT: Must be run as `python bench_hardware.py`, not imported.
The multiprocessing section requires the __name__ == '__main__' guard.
"""

import os
import time

import numpy as np


def _digamma_batch(t_values):
    """Worker function — must be top-level for pickling."""
    import mpmath as mp
    mp.mp.dps = 150
    for t_val in t_values:
        mp.digamma(mp.mpc(0.25, t_val))


def run_benchmark():
    from riemann.resources import get_config, print_summary

    print("=" * 60)
    print("  HARDWARE BENCHMARK FOR RIEMANN SOLVER")
    print("=" * 60)

    print("\nResource Configuration:")
    print_summary()
    cfg = get_config()

    # Eigendecomposition benchmark (no multiprocessing, always safe)
    for n in [201, 501]:
        A = np.random.randn(n, n)
        A = (A + A.T) / 2
        t0 = time.time()
        np.linalg.eigh(A)
        t_cpu = time.time() - t0
        print(f"\n{n}x{n} symmetric eigh (CPU): {t_cpu * 1000:.1f}ms")

    # Digamma single-core
    import mpmath as mp
    mp.mp.dps = 150
    t_values = [float(i) for i in range(200)]
    t0 = time.time()
    for t_val in t_values:
        mp.digamma(mp.mpc(0.25, t_val))
    t_single = time.time() - t0
    print(f"\n200 digamma evals at 150 dps:")
    print(f"  Single-core: {t_single * 1000:.0f}ms ({t_single / 200 * 1000:.2f}ms/eval)")

    # Multi-core with SAFE worker count
    import multiprocessing
    n_workers = cfg.max_workers
    chunks = [t_values[i::n_workers] for i in range(n_workers)]
    t0 = time.time()
    with multiprocessing.Pool(n_workers) as pool:
        pool.map(_digamma_batch, chunks)
    t_multi = time.time() - t0
    speedup = t_single / t_multi if t_multi > 0 else 0
    print(f"  {n_workers}-worker: {t_multi * 1000:.0f}ms  (speedup: {speedup:.1f}x)")

    # Projections
    single_rate = 200 / t_single
    multi_rate = 200 / t_multi if t_multi > 0 else 1
    for label, elems in [("N=50", 101 * 101), ("N=100", 201 * 201)]:
        print(f"\n  CvS build {label}:")
        print(f"    Single: ~{elems / single_rate:.0f}s  |  {n_workers}-worker: ~{elems / multi_rate:.0f}s")


# ━━ This guard is CRITICAL on Windows. Without it: fork bomb → lockup. ━━
if __name__ == "__main__":
    run_benchmark()
