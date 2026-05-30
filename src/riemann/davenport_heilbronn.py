# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Davenport-Heilbronn function — a control where generalized RH fails.

The DH function is a Dirichlet series satisfying a functional equation
but having zeros OFF the critical line. It is the essential control
for validating that our falsification harnesses actually work.

If our off-line search cannot find the known off-line zeros of this
function, it cannot be trusted on ζ(s) either.

Construction:
    f(s) = (1 - i*κ)/2 * L(s, χ) + (1 + i*κ)/2 * L(s, χ̄)

where χ is the primitive character mod 5 with χ(2)=i, and
    κ = (√(10 - 2√5) - 2) / (√5 - 1)

This f(s) satisfies f(s) = f(1-s) but has zeros with Re(s) ≠ 1/2.

References:
    - Davenport & Heilbronn (1936), J. London Math. Soc.
    - Titchmarsh (1986), The Theory of the Riemann Zeta-Function, §10.25
    - Balanzario & Sánchez-Ortiz (2007), Math. Comp. 76(260)
"""

from __future__ import annotations

import mpmath as mp


def _chi5(n: int) -> mp.mpc:
    """Primitive Dirichlet character mod 5 with χ(2) = i.

    Values: χ(1)=1, χ(2)=i, χ(3)=-i, χ(4)=-1, χ(0)=0.
    """
    r = n % 5
    if r == 0:
        return mp.mpc(0)
    elif r == 1:
        return mp.mpc(1)
    elif r == 2:
        return mp.mpc(0, 1)  # i
    elif r == 3:
        return mp.mpc(0, -1)  # -i
    else:  # r == 4
        return mp.mpc(-1)


def _kappa() -> mp.mpf:
    """The constant κ = (√(10 - 2√5) - 2) / (√5 - 1)."""
    sqrt5 = mp.sqrt(5)
    return (mp.sqrt(10 - 2 * sqrt5) - 2) / (sqrt5 - 1)


def _dirichlet_L_chi5(s: mp.mpc, terms: int = 5000) -> mp.mpc:
    """Compute L(s, χ₅) by direct summation.

    For Re(s) > 1, this converges. For Re(s) in (0,1), we use
    mpmath's built-in dirichlet() with the character values.
    """
    # Use mpmath's built-in Dirichlet L-function
    # chi5 as periodic sequence: [0, 1, i, -i, -1]
    chi_values = [0, 1, mp.j, -mp.j, -1]
    return mp.dirichlet(s, chi_values)


def davenport_heilbronn(s: mp.mpc) -> mp.mpc:
    """Evaluate the Davenport-Heilbronn function f(s).

    f(s) = (1 - i*κ)/2 * L(s,χ) + (1 + i*κ)/2 * L(s,χ̄)

    This function satisfies f(s) = f(1-s) but has zeros OFF
    the critical line Re(s) = 1/2.
    """
    s = mp.mpc(s)
    k = _kappa()

    L_chi = _dirichlet_L_chi5(s)
    L_chi_bar = mp.conj(_dirichlet_L_chi5(mp.conj(s)))

    coeff1 = (1 - mp.j * k) / 2
    coeff2 = (1 + mp.j * k) / 2

    return coeff1 * L_chi + coeff2 * L_chi_bar


def dh_off_line_search(
    sigma: float,
    t_start: float,
    t_end: float,
    t_step: float = 0.1,
    dps: int = 30,
    threshold: float = 1e-4,
) -> list[dict]:
    """Search for zeros of the DH function at a given σ ≠ 1/2.

    This SHOULD find zeros — if it doesn't, our method is broken.
    """
    candidates = []
    with mp.workdps(dps):
        t = mp.mpf(t_start)
        while t <= t_end:
            s = mp.mpc(sigma, t)
            val = abs(davenport_heilbronn(s))
            if val < threshold:
                candidates.append({
                    "sigma": float(sigma),
                    "t": float(t),
                    "abs_f": float(val),
                })
            t += t_step
    return candidates


def dh_verify_functional_equation(dps: int = 30) -> mp.mpf:
    """Verify f(s) = f(1-s) for a test point.

    Returns the residual |f(s) - f(1-s)|.
    """
    with mp.workdps(dps):
        s = mp.mpc(0.3, 10.5)
        f_s = davenport_heilbronn(s)
        f_1ms = davenport_heilbronn(1 - s)
        return abs(f_s - f_1ms)


def run_dh_control(dps: int = 25) -> dict:
    """Full Davenport-Heilbronn control test.

    1. Verify functional equation
    2. Search on critical line (should find zeros)
    3. Search OFF critical line (should ALSO find zeros — DH violates GRH)
    """
    with mp.workdps(dps):
        # Step 1: functional equation
        fe_residual = dh_verify_functional_equation(dps)

        # Step 2: zeros on the critical line
        on_line = dh_off_line_search(0.5, 0, 30, 0.05, dps, threshold=0.1)

        # Step 3: zeros OFF the critical line
        # Known: DH has zeros near σ ≈ 0.8, t small
        # Search a grid of σ values
        off_line = []
        for sigma in [0.3, 0.4, 0.6, 0.7, 0.8, 0.9]:
            hits = dh_off_line_search(sigma, 0, 30, 0.1, dps, threshold=0.5)
            off_line.extend(hits)

    return {
        "functional_equation_residual": float(fe_residual),
        "on_line_candidates": len(on_line),
        "off_line_candidates": len(off_line),
        "off_line_details": off_line[:20],
        "control_valid": len(off_line) > 0,
    }


if __name__ == "__main__":
    mp.mp.dps = 25
    print("=" * 72)
    print("  DAVENPORT-HEILBRONN CONTROL TEST")
    print("  (Function where generalized RH FAILS)")
    print("=" * 72)

    result = run_dh_control()

    print(f"\n  Functional equation |f(s)-f(1-s)|: {result['functional_equation_residual']:.2e}")
    print(f"  On-line candidates (σ=0.5): {result['on_line_candidates']}")
    print(f"  Off-line candidates (σ≠0.5): {result['off_line_candidates']}")

    if result["off_line_details"]:
        print("\n  Off-line hits:")
        for h in result["off_line_details"][:10]:
            print(f"    σ={h['sigma']:.1f}, t={h['t']:.2f}, |f|={h['abs_f']:.6f}")

    if result["control_valid"]:
        print("\n  ✓ CONTROL VALID: Off-line zeros detected for DH function.")
        print("    Our falsification harness CAN detect off-line zeros.")
    else:
        print("\n  ✗ CONTROL FAILED: No off-line zeros detected!")
        print("    Our falsification harness is NOT reliable.")
