"""Tests for the CPSC constraint-projection bridge."""

import mpmath as mp


def test_projection():
    """Project a point near the first zero onto the critical line."""
    from riemann.constraint import project_to_critical_line

    # Start near the first zero (σ=0.5, t≈14.1)
    result = project_to_critical_line(0.5, 14.0, dps=25)
    # Should converge to the first zero
    assert result.on_manifold
    assert abs(result.projected_t - mp.mpf("14.134725141734693")) < mp.mpf("1e-10")


def test_cas_model():
    """CAS model should have required keys."""
    from riemann.constraint import build_cas_model

    model = build_cas_model()
    assert "constraint_architecture" in model
    assert "projection" in model
    assert "verification" in model
    assert "li_criterion" in model
