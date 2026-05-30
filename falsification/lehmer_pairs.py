# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Falsification: search for Lehmer pairs (unusually close zero pairs).

Tight Lehmer pairs provide lower bounds on the de Bruijn-Newman
constant Λ. Finding a pair implying Λ > 0 would disprove RH.
"""

from riemann.dbn_constant import find_lehmer_pairs
import mpmath as mp


def run_search(start: int = 1, count: int = 200, threshold: float = 0.5, dps: int = 30):
    """Search for Lehmer pairs among the first `count` zeros."""
    pairs = find_lehmer_pairs(start, count, threshold, dps)
    return pairs


if __name__ == "__main__":
    print("Lehmer pair search (falsification harness):")
    pairs = run_search(count=100)
    if pairs:
        print(f"  Found {len(pairs)} close pair(s):")
        for p in pairs:
            print(f"    zeros {p.index}/{p.index+1}: gap={mp.nstr(p.gap, 10)}, "
                  f"normalized={mp.nstr(p.normalized_gap, 6)}")
    else:
        print("  No unusually close pairs found in range")
