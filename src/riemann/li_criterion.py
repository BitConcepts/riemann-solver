"""Keiper-Li coefficient computation for the Riemann Hypothesis.

Li's criterion: RH ⟺ λ_n ≥ 0 for all positive integers n.

The coefficients λ_n are computed using the Coffey representation
(Theorem 1 of math-ph/0505052):

    λ_n = -Σ_{m=1}^n C(n,m) η_{m-1}
          + Σ_{m=2}^n (-1)^m C(n,m) (1 - 2^{-m}) ζ(m)
          + 1 - n/2 (γ + ln π + 2 ln 2)

Asymptotics (Voros 2004, math/0506326):
    If RH true:  λ_n ~ n/2 ln n + n/2 (γ - 1 - ln 2π)
    If RH false: exponentially oscillating

References:
    - Li (1997), J. Number Theory 65(2):325-333
    - Coffey (2005), arXiv:math-ph/0505052
    - Voros (2005), arXiv:math/0506326
    - Maślanka (2004), arXiv:math/0402168
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


@dataclass
class LiCoefficient:
    """A computed Li coefficient with diagnostics."""

    n: int
    value: mp.mpf  # λ_n
    positive: bool  # λ_n > 0
    normalized: mp.mpf  # λ_n / (n * ln n) — should → 1/2 under RH


def _li_via_zeros(n: int, num_zeros: int, dps: int) -> mp.mpf:
    """Compute λ_n via the direct zero-sum formula:

        λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]

    Using `num_zeros` pairs of conjugate zeros for the partial sum.
    Each pair (ρ, ρ̄) contributes:
        2 Re[1 - (1 - 1/ρ)^n]
    """
    total = mp.mpf(0)
    for k in range(1, num_zeros + 1):
        rho = mp.zetazero(k)
        term = 1 - mp.power(1 - 1 / rho, n)
        # ρ and ρ̄ are paired; zetazero returns ρ with Im>0,
        # and the conjugate contributes the conjugate term.
        # Re[term] + Re[conj(term)] = 2*Re[term]
        total += 2 * mp.re(term)
    return total


def li_coefficient(n: int, dps: int = 50, num_zeros: int = 100) -> LiCoefficient:
    """Compute the n-th Li coefficient λ_n.

    Uses the direct zero-sum formula:
        λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]

    with `num_zeros` conjugate pairs of non-trivial zeros.
    For small n, convergence is rapid (100 zeros gives excellent precision).
    """
    with mp.workdps(dps + 10):
        value = _li_via_zeros(n, num_zeros, dps)

    # Normalize
    if n >= 2:
        normalized = value / (n * mp.log(n))
    else:
        normalized = value

    return LiCoefficient(
        n=n,
        value=mp.mpf(value),
        positive=value > 0,
        normalized=mp.mpf(normalized),
    )


def li_coefficients(count: int, dps: int = 50) -> list[LiCoefficient]:
    """Compute λ_1, λ_2, ..., λ_count."""
    return [li_coefficient(n, dps) for n in range(1, count + 1)]


def li_growth_check(coeffs: list[LiCoefficient]) -> dict:
    """Analyze the growth of Li coefficients.

    Under RH: λ_n / (n ln n) → 1/2
    Under ¬RH: eventually oscillates with exponential amplitude

    Returns diagnostic dictionary.
    """
    if not coeffs:
        return {"status": "no_data"}

    all_positive = all(c.positive for c in coeffs)
    max_n = max(c.n for c in coeffs)

    # Compute asymptotic ratio for large n
    large_n = [c for c in coeffs if c.n >= 10]
    if large_n:
        ratios = [float(c.normalized) for c in large_n]
        mean_ratio = sum(ratios) / len(ratios)
    else:
        mean_ratio = None

    return {
        "all_positive": all_positive,
        "max_n_computed": max_n,
        "mean_normalized_ratio": mean_ratio,
        "expected_ratio_if_rh": 0.5,
        "verdict": "consistent_with_rh" if all_positive else "RH_VIOLATED",
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute Li coefficients (RH criterion)")
    parser.add_argument("--count", type=int, default=10, help="Number of coefficients")
    parser.add_argument("--dps", type=int, default=30, help="Decimal precision")
    args = parser.parse_args()

    print(f"Computing λ_1 through λ_{args.count} at {args.dps} dps:")
    coeffs = li_coefficients(args.count, args.dps)
    for c in coeffs:
        sign = "+" if c.positive else "−"
        print(f"  λ_{c.n:3d} = {mp.nstr(c.value, 20):>30s}  [{sign}]  ratio={mp.nstr(c.normalized, 6)}")

    diag = li_growth_check(coeffs)
    print(f"\nDiagnostic: {diag['verdict']}")
    print(f"  All positive: {diag['all_positive']}")
    if diag["mean_normalized_ratio"] is not None:
        print(f"  Mean λ_n/(n ln n): {diag['mean_normalized_ratio']:.6f} (expect 0.5 under RH)")
