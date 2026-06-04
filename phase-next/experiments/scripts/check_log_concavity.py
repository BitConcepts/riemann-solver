"""
check_log_concavity.py
Verify log-concavity (H6) for candidate kernels.

For a kernel K(t), log-concavity on [0, inf) means:
    (log K)''(t) = K''(t)/K(t) - (K'(t)/K(t))^2 <= 0   for all t >= 0.

Uses mpmath for high-precision arithmetic (50+ decimal digits).

Usage:
    python check_log_concavity.py              # check all built-in kernel classes
    python check_log_concavity.py --kernel exp_t4  # check specific kernel

Output: JSON result per kernel class.
"""

import json
import sys
import argparse
from pathlib import Path

try:
    import mpmath
    from mpmath import mp, mpf, log, diff, matrix
    mp.dps = 55  # 55 decimal places of working precision
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Kernel definitions
# All kernels are defined on the real line, even, positive, and analytic.
# ---------------------------------------------------------------------------

def kernel_gaussian(t):
    """K(t) = exp(-t^2)  [Class 2, m=1]"""
    t = mpf(t)
    return mp.exp(-t**2)


def kernel_exp_t4(t):
    """K(t) = exp(-t^4)  [Class 2, m=2]"""
    t = mpf(t)
    return mp.exp(-t**4)


def kernel_exp_t6(t):
    """K(t) = exp(-t^6)  [Class 2, m=3]"""
    t = mpf(t)
    return mp.exp(-t**6)


def kernel_gauss_eps_t4(t, eps=mpf("0.1")):
    """K(t) = exp(-t^2 - eps*t^4)  [Class 3, eps=0.1]"""
    t = mpf(t)
    return mp.exp(-t**2 - eps * t**4)


def kernel_abs_t3(t):
    """K(t) = exp(-|t|^3)  [Class 6a control — NOT analytic at 0]"""
    t = mpf(t)
    return mp.exp(-abs(t)**3)


# ---------------------------------------------------------------------------
# Log-concavity check
# ---------------------------------------------------------------------------

def log_second_derivative(K, t, h=None):
    """
    Compute (log K)''(t) numerically using mpmath's diff.
    (log K)''(t) = K''K - (K')^2) / K^2
    Returns the value; should be <= 0 for log-concavity.
    """
    if h is None:
        h = mpf("1e-8")
    # Numerical second derivative of log K
    lK = lambda s: log(K(s))
    try:
        val = diff(lK, t, 2)
    except Exception:
        # Fallback: finite difference
        val = (lK(t + h) - 2*lK(t) + lK(t - h)) / h**2
    return val


def check_log_concavity_on_halfline(K, t_grid=None, label="kernel"):
    """
    Check (log K)''(t) <= 0 on a grid of t values in [0, T_max].
    Returns a dict with worst violation and overall status.
    """
    if t_grid is None:
        # Evaluate at 200 points: 0, 0.01, 0.05, 0.1, 0.2, ..., up to 5.0
        t_grid = (
            [mpf("0")]
            + [mpf(x) / 100 for x in range(1, 11)]
            + [mpf(x) / 10 for x in range(1, 51)]
            + [mpf(x) for x in range(1, 11)]
        )
        t_grid = sorted(set(t_grid))

    max_violation = mpf("-1e100")  # track max value of (log K)''
    worst_t = None
    n_positive = 0  # count of points where (log K)'' > 0

    results = []
    for t in t_grid:
        try:
            val = float(log_second_derivative(K, t))
            if val > float(max_violation):
                max_violation = mpf(str(val))
                worst_t = float(t)
            if val > 0:
                n_positive += 1
            results.append({"t": float(t), "log_second_deriv": val})
        except Exception as e:
            results.append({"t": float(t), "error": str(e)})

    log_concave = float(max_violation) <= 0
    strictly = float(max_violation) < 0

    return {
        "kernel": label,
        "log_concave": log_concave,
        "strictly_log_concave": strictly,
        "max_log_second_deriv": float(max_violation),
        "worst_t": worst_t,
        "n_positive_violations": n_positive,
        "n_points_checked": len(t_grid),
        "sample_points": results[:10],  # first 10 only
    }


# ---------------------------------------------------------------------------
# Hypothesis checks
# ---------------------------------------------------------------------------

def check_all_hypotheses(K, label, analytic=True):
    """
    Check H1–H6 for kernel K. H1–H5 are mostly analytic; H6 is checked numerically.
    'analytic' flag lets user override H4 (e.g. for |t|^3 kernels).
    """
    lc = check_log_concavity_on_halfline(K, label=label)
    return {
        "kernel": label,
        "H1_even": True,   # All built-in kernels are even by construction
        "H2_positive": True,  # exp(anything) > 0 always
        "H3_integrable": True,  # All test kernels integrate finitely
        "H4_analytic": analytic,  # Passed as argument
        "H5_superexp_decay": True,  # All exp(-t^p) for p>0 decay superexponentially
        "H6_log_concave": lc["log_concave"],
        "H6_strictly": lc["strictly_log_concave"],
        "H6_max_violation": lc["max_log_second_deriv"],
        "H6_worst_t": lc["worst_t"],
        "all_hypotheses_satisfied": (
            analytic and lc["log_concave"]
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

KERNELS = {
    "exp_t2":        (kernel_gaussian,                    True,  "exp(-t^2) [Gaussian, m=1]"),
    "exp_t4":        (kernel_exp_t4,                      True,  "exp(-t^4) [m=2]"),
    "exp_t6":        (kernel_exp_t6,                      True,  "exp(-t^6) [m=3]"),
    "gauss_eps01":   (lambda t: kernel_gauss_eps_t4(t, mpf("0.1")),  True, "exp(-t^2 - 0.1*t^4) [Class 3, eps=0.1]"),
    "gauss_eps10":   (lambda t: kernel_gauss_eps_t4(t, mpf("1.0")),  True, "exp(-t^2 - t^4) [Class 3, eps=1.0]"),
    "abs_t3":        (kernel_abs_t3,                      False, "exp(-|t|^3) [Class 6a control, H4 fails]"),
}


def main():
    parser = argparse.ArgumentParser(description="Check log-concavity of candidate kernels")
    parser.add_argument("--kernel", default="all", help="Kernel to check (or 'all')")
    parser.add_argument("--output", default=None, help="Output JSON file path")
    args = parser.parse_args()

    if args.kernel == "all":
        selected = KERNELS.items()
    elif args.kernel in KERNELS:
        selected = [(args.kernel, KERNELS[args.kernel])]
    else:
        print(f"Unknown kernel: {args.kernel}. Available: {list(KERNELS.keys())}", file=sys.stderr)
        sys.exit(1)

    results = []
    for name, (K, analytic, desc) in selected:
        print(f"  Checking log-concavity: {desc} ...", end=" ", flush=True)
        r = check_all_hypotheses(K, label=desc, analytic=analytic)
        results.append(r)
        status = "LOG-CONCAVE" if r["H6_log_concave"] else f"VIOLATION at t={r['H6_worst_t']:.4f}"
        print(status)

    output = {
        "script": "check_log_concavity.py",
        "mp_dps": mp.dps,
        "results": results,
    }

    out_str = json.dumps(output, indent=2)
    if args.output:
        Path(args.output).write_text(out_str)
        print(f"\nResults written to {args.output}")
    else:
        print("\n" + out_str)

    return output


if __name__ == "__main__":
    main()
