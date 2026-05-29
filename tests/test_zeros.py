"""Tests for zero finding and verification."""

import mpmath as mp


def test_first_zero():
    """Verify the first non-trivial zero."""
    from riemann.zeros import compute_zero

    z = compute_zero(1, dps=50)
    # First zero: ρ₁ = 1/2 + 14.1347251417...i
    mp.mp.dps = 50
    assert abs(z.t - mp.mpf("14.134725141734693790457251983562")) < mp.mpf("1e-15")
    assert z.verified


def test_first_few_zeros():
    """Compute and verify the first 5 zeros."""
    from riemann.zeros import compute_zeros

    zeros = compute_zeros(1, 5, dps=25)
    assert len(zeros) == 5
    assert all(z.verified for z in zeros)
    # Zeros should be in ascending order
    for i in range(len(zeros) - 1):
        assert zeros[i].t < zeros[i + 1].t


def test_spacing():
    """Check that zero spacings are positive and reasonable."""
    from riemann.zeros import compute_zeros, zero_spacing

    zeros = compute_zeros(1, 10, dps=25)
    spacings = zero_spacing(zeros)
    assert len(spacings) == 9
    assert all(s > 0 for s in spacings)
