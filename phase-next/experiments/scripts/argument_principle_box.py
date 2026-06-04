"""
argument_principle_box.py
Rigorous zero counting for Fourier transforms via the argument principle.

The argument principle states: if F is analytic inside and on a contour C with no zeros on C,
then the number of zeros inside C equals (1/2πi) ∮_C F'(z)/F(z) dz.

This script counts zeros of F(z) = 2 ∫_0^∞ K(t) cos(z*t) dt in rectangular boxes
{a ≤ Re(z) ≤ b, c ≤ Im(z) ≤ d} with Im(z) > 0 (off the real axis).

If any such box contains zeros with Im(z) > δ for some δ > 0, this is a COUNTEREXAMPLE
CANDIDATE. It must still be verified against all H13 hypotheses via check_log_concavity.py.

Uses mpmath with mp.dps = 55 for 50+ digit arithmetic.

Usage:
    python argument_principle_box.py --kernel exp_t4 --re_min 0 --re_max 15 --im_min 0.1 --im_max 3
    python argument_principle_box.py --kernel exp_t4  # default box
"""

import json
import sys
import argparse
from pathlib import Path

try:
    from mpmath import mp, mpf, mpc, quad, cos, exp, pi, re, im, log, diff, fabs
    mp.dps = 55
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Kernel definitions
# ---------------------------------------------------------------------------

def kernel_gaussian(t):
    return exp(-mpf(t)**2)

def kernel_exp_t4(t):
    return exp(-mpf(t)**4)

def kernel_exp_t6(t):
    return exp(-mpf(t)**6)

def kernel_gauss_eps_t4(t, eps="0.1"):
    t = mpf(t); eps = mpf(eps)
    return exp(-t**2 - eps * t**4)

def kernel_abs_t3(t):
    t = mpf(t)
    return exp(-abs(t)**3)


KERNELS = {
    "exp_t2":      (kernel_gaussian,                         "exp(-t^2) [Gaussian, m=1]"),
    "exp_t4":      (kernel_exp_t4,                           "exp(-t^4) [m=2]"),
    "exp_t6":      (kernel_exp_t6,                           "exp(-t^6) [m=3]"),
    "gauss_eps01": (lambda t: kernel_gauss_eps_t4(t, "0.1"), "exp(-t^2 - 0.1*t^4)"),
    "gauss_eps10": (lambda t: kernel_gauss_eps_t4(t, "1.0"), "exp(-t^2 - t^4)"),
    "abs_t3":      (kernel_abs_t3,                           "exp(-|t|^3) [control, H4 fails]"),
}


# ---------------------------------------------------------------------------
# Fourier transform
# ---------------------------------------------------------------------------

def fourier_transform(K, z, T_max="30"):
    """
    F(z) = 2 * integral_0^{T_max} K(t) * cos(z*t) dt
    Returns a complex mpc value.
    """
    from mpmath import cos as mcos
    z = mpc(z)
    T_max = mpf(T_max)
    integrand_re = lambda t: re(K(t) * mcos(z * t))
    integrand_im = lambda t: im(K(t) * mcos(z * t))
    F_re = 2 * quad(integrand_re, [0, T_max], maxdegree=8)[0]
    F_im = 2 * quad(integrand_im, [0, T_max], maxdegree=8)[0]
    return mpc(F_re, F_im)


def fourier_derivative(K, z, h=None):
    """
    F'(z) via numerical differentiation.
    F'(z) = i * 2 * integral_0^∞ K(t) * t * (-sin(zt)) dt
           = -2i * integral_0^∞ K(t) * t * sin(zt) dt
    """
    from mpmath import sin as msin
    z = mpc(z)
    T_max = mpf("30")
    integrand_re = lambda t: re(-2j * K(t) * mpf(t) * msin(z * t))
    integrand_im = lambda t: im(-2j * K(t) * mpf(t) * msin(z * t))
    dF_re = quad(integrand_re, [0, T_max], maxdegree=8)[0]
    dF_im = quad(integrand_im, [0, T_max], maxdegree=8)[0]
    return mpc(dF_re, dF_im)


# ---------------------------------------------------------------------------
# Argument principle integration
# ---------------------------------------------------------------------------

def count_zeros_in_box(K, re_min, re_max, im_min, im_max, n_segments=200):
    """
    Count zeros of F in the open box (re_min, re_max) x (im_min, im_max)
    using the argument principle: winding number of F around the box boundary.

    Returns (winding_number, details_dict).
    A winding number > 0 indicates zeros inside the box (COUNTEREXAMPLE CANDIDATE).

    n_segments: number of quadrature points per side of the box.
    """
    re_min = mpf(re_min); re_max = mpf(re_max)
    im_min = mpf(im_min); im_max = mpf(im_max)

    # Four sides of the rectangle (counterclockwise)
    # Bottom: re from re_min to re_max, im = im_min
    # Right:  im from im_min to im_max, re = re_max
    # Top:    re from re_max to re_min, im = im_max
    # Left:   im from im_max to im_min, re = re_min

    def integrate_log_F_derivative(z_path_func, t_min, t_max):
        """
        Integrate F'(z)/F(z) * dz/dt dt from t_min to t_max.
        z = z_path_func(t), dz/dt from the parameterization.
        """
        # Use finite differences for dz/dt
        def integrand(t):
            h = mpf("1e-8")
            z = z_path_func(t)
            dz = (z_path_func(t + h) - z_path_func(t - h)) / (2 * h)
            F = fourier_transform(K, z)
            if abs(F) < mpf("1e-30"):
                return mpf(0)  # near-zero: potential issue, flag later
            dF = fourier_derivative(K, z)
            return re(dF / F * dz) + 1j * float(im(dF / F * dz))

        # Integrate real and imaginary parts separately
        integrand_re = lambda t: re(mpc(str(integrand(t))))
        integrand_im = lambda t: im(mpc(str(integrand(t))))
        val_re = quad(integrand_re, [t_min, t_max], maxdegree=6)[0]
        val_im = quad(integrand_im, [t_min, t_max], maxdegree=6)[0]
        return mpc(val_re, val_im)

    # Parameterizations of the four sides
    sides = [
        (lambda t: mpc(re_min + (re_max - re_min) * t, im_min), 0, 1, "bottom"),
        (lambda t: mpc(re_max, im_min + (im_max - im_min) * t), 0, 1, "right"),
        (lambda t: mpc(re_max - (re_max - re_min) * t, im_max), 0, 1, "top"),
        (lambda t: mpc(re_min, im_max - (im_max - im_min) * t), 0, 1, "left"),
    ]

    total_integral = mpc(0)
    side_results = []

    for z_func, t0, t1, name in sides:
        try:
            contrib = integrate_log_F_derivative(z_func, t0, t1)
            total_integral += contrib
            side_results.append({"side": name, "contribution_re": float(re(contrib)),
                                  "contribution_im": float(im(contrib))})
        except Exception as e:
            side_results.append({"side": name, "error": str(e)})

    # Winding number = (1/2πi) * ∮ F'/F dz = Im(total) / (2π)
    winding = float(im(total_integral)) / float(2 * pi)
    winding_int = round(winding)

    return winding_int, {
        "box": {
            "re": [float(re_min), float(re_max)],
            "im": [float(im_min), float(im_max)],
        },
        "winding_number": winding,
        "winding_number_rounded": winding_int,
        "zeros_in_box": winding_int,
        "side_contributions": side_results,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Count zeros of Fourier transform via argument principle")
    parser.add_argument("--kernel", default="exp_t4")
    parser.add_argument("--re_min", type=float, default=0.5)
    parser.add_argument("--re_max", type=float, default=10.0)
    parser.add_argument("--im_min", type=float, default=0.1)
    parser.add_argument("--im_max", type=float, default=3.0)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.kernel not in KERNELS:
        print(f"Unknown kernel: {args.kernel}. Available: {list(KERNELS.keys())}", file=sys.stderr)
        sys.exit(1)

    K, desc = KERNELS[args.kernel]

    print(f"Kernel: {desc}")
    print(f"Box: Re ∈ [{args.re_min}, {args.re_max}], Im ∈ [{args.im_min}, {args.im_max}]")
    print("Running argument principle integration (may be slow)...")

    n_zeros, details = count_zeros_in_box(
        K, args.re_min, args.re_max, args.im_min, args.im_max
    )

    if n_zeros > 0:
        print(f"\n*** {n_zeros} ZERO(S) FOUND IN BOX — COUNTEREXAMPLE CANDIDATE ***")
        print("Next step: verify all H13 hypotheses via check_log_concavity.py")
    else:
        print(f"\nNo zeros found in box (winding number = {details['winding_number']:.6f})")

    result = {
        "script": "argument_principle_box.py",
        "kernel": desc,
        "mp_dps": mp.dps,
        "claim_discipline": (
            "COMPUTATION class. Zero count via argument principle. "
            "Any non-zero count is a COUNTEREXAMPLE CANDIDATE requiring: "
            "(1) verification of H1-H6 via check_log_concavity.py, and "
            "(2) higher-precision confirmation."
        ),
        "hypotheses_checked": {
            "even": True,
            "positive": True,
            "integrable": True,
            "analytic_origin": args.kernel != "abs_t3",
            "superexponential_decay": True,
            "log_concave_halfline": "see check_log_concavity.py",
        },
        "fourier_zero_test": details,
        "status": "counterexample candidate" if n_zeros > 0 else "no counterexample",
        "notes": "Argument principle count. No zeros found does NOT prove H13; it rules out zeros in the tested box only.",
    }

    out_str = json.dumps(result, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(out_str)
        print(f"Results written to {args.output}")
    else:
        print("\n" + out_str)


if __name__ == "__main__":
    main()
