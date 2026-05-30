# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Falsification: systematic search for zeros off the critical line.

Any zero ρ with Re(ρ) ≠ 1/2 would disprove the Riemann Hypothesis.
"""

from riemann.zeros import off_line_search
import mpmath as mp


def run_search(
    sigmas: list[float] | None = None,
    t_start: float = 10.0,
    t_end: float = 100.0,
    t_step: float = 0.5,
    dps: int = 30,
):
    """Run off-line search at multiple σ values."""
    if sigmas is None:
        sigmas = [0.3, 0.4, 0.6, 0.7]

    all_candidates = []
    for sigma in sigmas:
        candidates = off_line_search(sigma, t_start, t_end, t_step, dps)
        if candidates:
            print(f"  *** CANDIDATES at σ={sigma}: {len(candidates)} points ***")
            all_candidates.extend(candidates)
        else:
            print(f"  σ={sigma}: no candidates (expected)")

    return all_candidates


if __name__ == "__main__":
    print("Off-critical-line zero search (falsification harness):")
    candidates = run_search()
    if not candidates:
        print("\nResult: No off-line zeros found (consistent with RH)")
    else:
        print(f"\n*** {len(candidates)} CANDIDATE(S) FOUND — INVESTIGATE ***")
