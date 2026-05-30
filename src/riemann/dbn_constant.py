# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""De Bruijn-Newman constant Λ: bounds and Lehmer pair analysis.

RH ⟺ Λ ≤ 0. Known: 0 ≤ Λ ≤ 0.22.

The constant Λ is the infimum of t such that H_t(z) has only real zeros,
where H_t(z) = ∫_0^∞ e^{tu²} Φ(u) cos(zu) du.

References:
    - de Bruijn (1950), Duke Math. J.
    - Rodgers & Tao (2018), arXiv:1801.05914
    - Csordas, Smith & Varga (1994), Lehmer pair method
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


# Known bounds
LAMBDA_LOWER = mp.mpf(0)       # Rodgers-Tao 2018
LAMBDA_UPPER = mp.mpf("0.22")  # Polymath 15


@dataclass
class LehmerPair:
    """A pair of consecutive zeros that are unusually close together."""

    index: int  # index of first zero
    gamma_k: mp.mpf  # imaginary part of k-th zero
    gamma_k1: mp.mpf  # imaginary part of (k+1)-th zero
    gap: mp.mpf  # gamma_{k+1} - gamma_k
    mean_spacing: mp.mpf  # local average spacing ~ 2π/log(t/2π)
    normalized_gap: mp.mpf  # gap / mean_spacing
    lambda_lower_bound: mp.mpf | None  # implied lower bound on Λ


def local_mean_spacing(t: float | mp.mpf) -> mp.mpf:
    """Estimated local mean zero spacing at height t.

    By the Riemann-von Mangoldt formula, the average spacing at height t is:
        Δ ≈ 2π / log(t / 2π)
    """
    t = mp.mpf(t)
    if t <= 10:
        return mp.mpf(5)  # rough estimate for small t
    return 2 * mp.pi / mp.log(t / (2 * mp.pi))


def find_lehmer_pairs(
    start: int,
    count: int,
    threshold: float = 0.5,
    dps: int = 50,
) -> list[LehmerPair]:
    """Find Lehmer pairs among consecutive zeros.

    A Lehmer pair is a pair of consecutive zeros whose gap is less than
    `threshold` times the local mean spacing.

    Args:
        start: starting zero index
        count: number of zeros to scan
        threshold: normalized gap threshold (< 1.0 means closer than average)
        dps: decimal precision
    """
    pairs = []
    with mp.workdps(dps):
        prev_t = mp.im(mp.zetazero(start))
        for n in range(start + 1, start + count):
            curr_t = mp.im(mp.zetazero(n))
            gap = curr_t - prev_t
            mean_sp = local_mean_spacing((prev_t + curr_t) / 2)
            norm_gap = gap / mean_sp

            if norm_gap < threshold:
                pairs.append(
                    LehmerPair(
                        index=n - 1,
                        gamma_k=prev_t,
                        gamma_k1=curr_t,
                        gap=gap,
                        mean_spacing=mean_sp,
                        normalized_gap=norm_gap,
                        lambda_lower_bound=None,  # TODO: CSV bound computation
                    )
                )
            prev_t = curr_t
    return pairs


def summarize_bounds() -> dict:
    """Return current known bounds on the de Bruijn-Newman constant."""
    return {
        "lambda_lower": float(LAMBDA_LOWER),
        "lambda_upper": float(LAMBDA_UPPER),
        "rh_status": "Λ = 0 ⟺ RH; currently 0 ≤ Λ ≤ 0.22",
        "source_lower": "Rodgers-Tao (2018)",
        "source_upper": "Polymath 15 (2019)",
    }
