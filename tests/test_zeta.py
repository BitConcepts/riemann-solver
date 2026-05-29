"""Tests for the zeta function wrappers."""

import mpmath as mp


def test_zeta_known_values():
    """Test ζ at known special values."""
    from riemann.zeta import zeta

    mp.mp.dps = 30
    # ζ(2) = π²/6
    assert abs(zeta(2) - mp.pi**2 / 6) < mp.mpf("1e-25")
    # ζ(0) = -1/2
    assert abs(zeta(0) + 0.5) < mp.mpf("1e-25")
    # ζ(-1) = -1/12
    assert abs(zeta(-1) + mp.mpf(1) / 12) < mp.mpf("1e-25")


def test_hardy_z_sign_change():
    """Z(t) should change sign near each zero."""
    from riemann.zeta import hardy_z

    mp.mp.dps = 25
    # First zero is near t ≈ 14.1347
    z_before = hardy_z(14.0)
    z_after = hardy_z(14.2)
    # Should have opposite signs (sign change = zero between them)
    assert z_before * z_after < 0


def test_gram_point():
    """Test Gram point computation."""
    from riemann.zeta import gram_point, siegel_theta

    mp.mp.dps = 25
    g10 = gram_point(10)
    # θ(g_10) should ≈ 10π
    assert abs(siegel_theta(g10) - 10 * mp.pi) < mp.mpf("1e-20")


def test_stieltjes():
    """Test Stieltjes constant γ₀ = Euler-Mascheroni constant."""
    from riemann.zeta import stieltjes_constant

    mp.mp.dps = 25
    gamma0 = stieltjes_constant(0)
    assert abs(gamma0 - mp.euler) < mp.mpf("1e-20")
