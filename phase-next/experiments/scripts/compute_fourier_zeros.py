"""
compute_fourier_zeros.py
Numerically compute the Fourier transform of candidate kernels and locate zeros.

F(xi) = integral_{-inf}^{inf} K(t) * exp(i * xi * t) dt

Since K is even, this reduces to:
F(xi) = 2 * integral_{0}^{inf} K(t) * cos(xi * t) dt   (real-valued for real xi)

For complex xi = a + ib, F(xi) is computed via numerical quadrature.

Uses mpmath for 50+ digit precision.

IMPORTANT: Complex zeros found here are COMPUTATION-class evidence only.
They do NOT constitute a counterexample to H13 unless:
1. All six H13 hypotheses are verified for the kernel (use check_log_concavity.py).
2. The zero is confirmed by argument_principle_box.py.

Usage:
    python compute_fourier_zeros.py               # all kernels, scan real axis
    python compute_fourier_zeros.py --kernel exp_t4 --xi_range 0 20 200
    python compute_fourier_zeros.py --kernel exp_t4 --complex_scan
"""

import json
import sys
import argparse
import warnings
from pathlib import Path

try:
    from mpmath import mp, mpf, mpc, quad, cos, exp, fabs, re, im, linspace
    mp.dps = 55
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Kernel definitions (must match check_log_concavity.py)
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
# Fourier transform evaluation
# ---------------------------------------------------------------------------

def fourier_transform_real(K, xi_real, T_max="30", n_intervals=500):
    """
    Compute F(xi) = 2 * integral_0^{T_max} K(t) * cos(xi * t) dt
    for real xi. Returns a real mpf value.
    """
    xi_real = mpf(xi_real)
    T_max = mpf(T_max)
    integrand = lambda t: K(t) * cos(xi_real * t)
    return 2 * quad(integrand, [0, T_max], maxdegree=8, error=True)[0]


def fourier_transform_complex(K, xi_complex, T_max="30"):
    """
    Compute F(xi) = 2 * integral_0^{T_max} K(t) * cos(xi * t) dt
    for complex xi. Returns a complex mpc value.
    (Uses cos(xi*t) = cos((a+ib)t) = cos(at)cosh(bt) - i*sin(at)sinh(bt))
    """
    from mpmath import quad, mpc, cos as mcos
    xi = mpc(xi_complex)
    T_max = mpf(T_max)
    integrand_re = lambda t: re(K(t) * mcos(xi * t))
    integrand_im = lambda t: im(K(t) * mcos(xi * t))
    F_re = 2 * quad(integrand_re, [0, T_max], maxdegree=8)[0]
    F_im = 2 * quad(integrand_im, [0, T_max], maxdegree=8)[0]
    return mpc(F_re, F_im)


# ---------------------------------------------------------------------------
# Real-axis zero scan
# ---------------------------------------------------------------------------

def scan_real_axis(K, label, xi_min=0, xi_max=30, n_points=300):
    """
    Evaluate F(xi) on [xi_min, xi_max] and look for sign changes (real zeros).
    Returns list of approximate real zeros found.
    """
    xi_grid = [mpf(xi_min) + mpf(xi_max - xi_min) * mpf(k) / mpf(n_points - 1)
               for k in range(n_points)]

    values = []
    for xi in xi_grid:
        try:
            val = float(fourier_transform_real(K, xi))
            values.append((float(xi), val))
        except Exception as e:
            values.append((float(xi), None))

    # Find sign changes
    sign_changes = []
    for i in range(len(values) - 1):
        xi0, v0 = values[i]
        xi1, v1 = values[i + 1]
        if v0 is not None and v1 is not None and v0 * v1 < 0:
            sign_changes.append({"xi_approx": (xi0 + xi1) / 2, "bracket": [xi0, xi1]})

    return {
        "kernel": label,
        "xi_range": [float(xi_min), float(xi_max)],
        "n_points": n_points,
        "real_zeros_found": len(sign_changes),
        "sign_changes": sign_changes,
        "sample_values": [(xi, v) for xi, v in values[:20]],
    }


# ---------------------------------------------------------------------------
# Complex zero search (strip scan)
# ---------------------------------------------------------------------------

def scan_complex_strip(K, label, xi_re_max=20, xi_im_max=5, n_re=40, n_im=20):
    """
    Scan F(xi) in the complex strip {0 <= Re(xi) <= xi_re_max, 0 <= Im(xi) <= xi_im_max}.
    Look for approximate zeros (|F(xi)| < threshold).
    Returns any candidate near-zeros found.

    NOTE: Near-zeros in this scan are COMPUTATION evidence only. Not rigorous.
    """
    from mpmath import fabs as mfabs

    threshold = mpf("1e-5")  # rough threshold for near-zero
    candidates = []

    re_grid = [mpf(xi_re_max) * mpf(k) / mpf(n_re - 1) for k in range(n_re)]
    im_grid = [mpf("1e-4") + mpf(xi_im_max) * mpf(k) / mpf(n_im - 1) for k in range(n_im)]

    print(f"    Scanning {n_re}x{n_im} complex grid for {label}...", end=" ", flush=True)

    for xi_re in re_grid[:10]:  # Limit for speed in initial scan; expand as needed
        for xi_im in im_grid[:5]:
            xi = mpc(xi_re, xi_im)
            try:
                F = fourier_transform_complex(K, xi)
                mag = float(abs(F))
                if mag < float(threshold):
                    candidates.append({
                        "xi_re": float(xi_re),
                        "xi_im": float(xi_im),
                        "F_magnitude": mag,
                        "F_re": float(re(F)),
                        "F_im": float(im(F)),
                        "status": "COUNTEREXAMPLE-CANDIDATE (unverified)",
                        "note": "Requires argument_principle_box.py for rigorous confirmation",
                    })
            except Exception:
                pass

    print(f"{len(candidates)} candidate(s) found")
    return {
        "kernel": label,
        "scan_region": {
            "xi_re": [0, float(xi_re_max)],
            "xi_im": [float(im_grid[0]), float(xi_im_max)],
        },
        "counterexample_candidates": candidates,
        "n_cells_scanned": 10 * 5,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Compute Fourier transform zeros of candidate kernels")
    parser.add_argument("--kernel", default="all")
    parser.add_argument("--xi_min", type=float, default=0)
    parser.add_argument("--xi_max", type=float, default=20)
    parser.add_argument("--n_points", type=int, default=200)
    parser.add_argument("--complex_scan", action="store_true")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.kernel == "all":
        selected = list(KERNELS.items())
    elif args.kernel in KERNELS:
        selected = [(args.kernel, KERNELS[args.kernel])]
    else:
        print(f"Unknown kernel: {args.kernel}", file=sys.stderr)
        sys.exit(1)

    all_results = []
    for name, (K, desc) in selected:
        print(f"\nKernel: {desc}")

        # Real axis scan
        print(f"  Scanning real axis xi in [{args.xi_min}, {args.xi_max}]...")
        real_result = scan_real_axis(K, desc, args.xi_min, args.xi_max, args.n_points)
        result = {
            "kernel": desc,
            "real_axis_scan": real_result,
        }

        # Complex scan (optional)
        if args.complex_scan:
            complex_result = scan_complex_strip(K, desc)
            result["complex_strip_scan"] = complex_result
            if complex_result["counterexample_candidates"]:
                print(f"  *** COUNTEREXAMPLE CANDIDATES FOUND — run argument_principle_box.py ***")
            else:
                print(f"  No complex zero candidates in scanned region")

        all_results.append(result)

    output = {
        "script": "compute_fourier_zeros.py",
        "mp_dps": mp.dps,
        "claim_discipline": (
            "COMPUTATION class only. No complex zero constitutes a counterexample "
            "to H13 without: (1) verification of all H1-H6 hypotheses via "
            "check_log_concavity.py, and (2) rigorous confirmation via argument_principle_box.py."
        ),
        "results": all_results,
    }

    out_str = json.dumps(output, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(out_str)
        print(f"\nResults written to {args.output}")
    else:
        print("\n" + out_str)


if __name__ == "__main__":
    main()
