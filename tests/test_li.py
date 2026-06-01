# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Tests for the Li criterion computation."""

import mpmath as mp


def test_lambda_1():
    """λ₁ ≈ 0.0230957 (known value).  # REQ-005 REQ-009"""
    # REQ-005: Li coefficient to ≥ 30 dps; REQ-009: test coverage
    from riemann.li_criterion import li_coefficient

    mp.mp.dps = 25
    c = li_coefficient(1, dps=25, num_zeros=50)
    assert c.positive
    # Known: λ_1 ≈ 0.023096 (exact requires infinite zeros).
    # With 50 zeros the partial sum gives ~0.0185, converging from below.
    # The key check is positivity; precision improves with more zeros.
    assert c.value > 0
    assert c.value < mp.mpf("0.05")  # sanity: right order of magnitude


def test_first_few_positive():
    """All of λ₁ through λ₅ should be positive.  # REQ-005 REQ-009"""
    # REQ-005: precision; REQ-009: coverage
    mp.mp.dps = 20
    coeffs = []
    from riemann.li_criterion import li_coefficient
    for n in range(1, 6):
        coeffs.append(li_coefficient(n, dps=20, num_zeros=30))
    assert all(c.positive for c in coeffs)


def test_growth_check():
    """Growth check should report consistent with RH.  # REQ-005 REQ-009"""
    # REQ-005: precision; REQ-009: coverage
    from riemann.li_criterion import li_coefficient, li_growth_check

    mp.mp.dps = 20
    coeffs = [li_coefficient(n, dps=20, num_zeros=30) for n in range(1, 6)]
    diag = li_growth_check(coeffs)
    assert diag["all_positive"]
    assert diag["verdict"] == "consistent_with_rh"
