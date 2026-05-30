# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Benchmark: verify computed zeros against Odlyzko's tables."""

from riemann.zeros import compute_zeros
import mpmath as mp

# First 20 known zeros (Odlyzko's tables, 10+ digits)
ODLYZKO_ZEROS = [
    "14.134725142", "21.022039639", "25.010857580", "30.424876126",
    "32.935061588", "37.586178159", "40.918719012", "43.327073281",
    "48.005150881", "49.773832478", "52.970321478", "56.446247697",
    "59.347044003", "60.831778525", "65.112544048", "67.079810529",
    "69.546401711", "72.067157674", "75.704690699", "77.144840069",
]


def run_benchmark(count: int = 20, dps: int = 30):
    """Compare computed zeros against Odlyzko reference values."""
    zeros = compute_zeros(1, min(count, len(ODLYZKO_ZEROS)), dps)
    results = []
    for z, ref_str in zip(zeros, ODLYZKO_ZEROS):
        ref = mp.mpf(ref_str)
        error = abs(z.t - ref)
        results.append({
            "index": z.index,
            "computed": z.t,
            "reference": ref,
            "error": error,
            "match": error < mp.mpf("1e-6"),
        })
    return results


if __name__ == "__main__":
    mp.mp.dps = 30
    results = run_benchmark()
    print("Odlyzko zero benchmark:")
    for r in results:
        status = "✓" if r["match"] else "✗"
        print(f"  ρ_{r['index']:2d}: error={mp.nstr(r['error'], 5):>15s}  {status}")
