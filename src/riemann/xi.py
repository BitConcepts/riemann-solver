# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Riemann xi function ξ(s) and related computations.

    ξ(s) = ½ s(s-1) π^{-s/2} Γ(s/2) ζ(s)

The xi function is entire, satisfies ξ(s) = ξ(1-s), and its zeros are
exactly the non-trivial zeros of the Riemann zeta function.

References:
    - Edwards (2001), Chapter 1
    - Bombieri & Lagarias (1999)
"""

from __future__ import annotations

import mpmath as mp


def xi(s: complex | mp.mpf | mp.mpc) -> mp.mpc:
    """Evaluate the Riemann xi function ξ(s).

        ξ(s) = ½ s(s-1) π^{-s/2} Γ(s/2) ζ(s)
    """
    s = mp.mpc(s)
    return mp.mpf(0.5) * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def xi_over_xi_derivative(s: complex | mp.mpf | mp.mpc) -> mp.mpc:
    """Compute ξ'(s)/ξ(s), the logarithmic derivative of ξ.

    This has simple poles at the non-trivial zeros of ζ.
    """
    s = mp.mpc(s)
    xi_val = xi(s)
    if xi_val == 0:
        return mp.inf
    # Numerical differentiation
    h = mp.power(10, -(mp.mp.dps // 2))
    xi_deriv = (xi(s + h) - xi(s - h)) / (2 * h)
    return xi_deriv / xi_val


def xi_derivative(s: complex | mp.mpf | mp.mpc, n: int = 1) -> mp.mpc:
    """Compute the n-th derivative of ξ(s) numerically."""
    return mp.diff(xi, s, n)


def xi_at_half(t: float | mp.mpf) -> mp.mpf:
    """Evaluate ξ(1/2 + it) on the critical line.

    This equals the Riemann Ξ function (capital Xi) up to normalization.
    """
    s = mp.mpc(0.5, t)
    return mp.re(xi(s))


def capital_xi(t: float | mp.mpf) -> mp.mpf:
    """Evaluate Ξ(t) = ξ(1/2 + it).

    The Riemann Hypothesis is equivalent to: all zeros of Ξ(t) are real.
    """
    return xi_at_half(t)
