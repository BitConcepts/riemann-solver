# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Benchmark: zero spacing statistics vs GUE prediction."""

from riemann.zeros import compute_zeros, normalized_spacing
import mpmath as mp


def run_benchmark(count: int = 100, dps: int = 25):
    """Compute normalized spacings and compare to GUE."""
    zeros = compute_zeros(1, count, dps)
    nspacings = normalized_spacing(zeros)

    # Basic statistics
    mean_s = sum(float(s) for s in nspacings) / len(nspacings)
    var_s = sum((float(s) - mean_s) ** 2 for s in nspacings) / len(nspacings)
    min_s = min(float(s) for s in nspacings)
    max_s = max(float(s) for s in nspacings)

    return {
        "count": count,
        "mean_spacing": mean_s,
        "variance": var_s,
        "min": min_s,
        "max": max_s,
        "expected_mean": 1.0,  # by definition of normalization
    }


if __name__ == "__main__":
    stats = run_benchmark(100)
    print("GUE spacing benchmark:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
