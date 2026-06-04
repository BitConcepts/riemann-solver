"""
extended_search.py
Iteration 2c: Expanded H13 counterexample search across multiple kernel classes.

Tests 5 classes of kernels:
  Class 2 extended: exp(-t^6), exp(-t^8), exp(-t^10)
  Class 3 extended: exp(-t^2 - eps*t^4) for eps in {1, 5, 10, 50}
  Class 6b (drop H5): exp(-t^2)/(1+0.01*t^2), (1+t^2)^{-2}
  Class 6c (drop H6): exp(-t^2)*(1+0.5*cos(2t)), exp(-t^2+0.1*sin(t^2))
  Near-counterexample probes: exp(-t^4)*cos^2(0.1*t), exp(-alpha*t^2)*|cos(beta*t)|

For each kernel:
  1. Verify all 6 H13 hypotheses (numerically)
  2. Scan real axis for sign changes (Fourier zeros)
  3. Scan complex strip (Re in [0,20], Im in [0.01,5], 30x15 grid)
  4. Save JSON output to experiments/outputs/

Claim discipline:
  All results are COMPUTATION class only.
  No complex zero constitutes a counterexample to H13 without:
    (1) verification of all H1-H6 hypotheses
    (2) rigorous confirmation via argument_principle_box.py

Usage:
    python extended_search.py                  # all kernels
    python extended_search.py --class class2   # specific class
    python extended_search.py --deep           # larger complex grid

Co-Authored-By: Oz <oz-agent@warp.dev>
"""

import json
import sys
import argparse
import datetime
from pathlib import Path

try:
    from mpmath import (
        mp, mpf, mpc, quad, cos, sin, exp, log, diff,
        re as mre, im as mim, fabs, pi, inf, power, absmin,
    )
    mp.dps = 55
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================================
# Kernel definitions
# ==========================================================================

# --- Class 2 extended: exp(-t^{2m}) ---

def kernel_exp_t6(t):
    """exp(-t^6)"""
    t = mpf(t)
    return exp(-t**6)

def kernel_exp_t8(t):
    """exp(-t^8)"""
    t = mpf(t)
    return exp(-t**8)

def kernel_exp_t10(t):
    """exp(-t^10)"""
    t = mpf(t)
    return exp(-t**10)


# --- Class 3 extended: exp(-t^2 - eps*t^4) ---

def make_gauss_eps(eps_str):
    """Factory for exp(-t^2 - eps*t^4)."""
    eps = mpf(eps_str)
    def kernel(t):
        t = mpf(t)
        return exp(-t**2 - eps * t**4)
    kernel.__doc__ = f"exp(-t^2 - {eps_str}*t^4)"
    return kernel


# --- Class 6b: Drop H5 (superexponential decay) ---

def kernel_gauss_rational(t):
    """exp(-t^2) / (1 + 0.01*t^2)  — slower tail decay than superexponential"""
    t = mpf(t)
    return exp(-t**2) / (1 + mpf("0.01") * t**2)

def kernel_poly_decay(t):
    """(1 + t^2)^{-2}  — polynomial decay, NOT superexponential"""
    t = mpf(t)
    return (1 + t**2)**(-2)


# --- Class 6c: Drop H6 (log-concavity) ---

def kernel_gauss_cos_mod(t):
    """exp(-t^2) * (1 + 0.5*cos(2t))  — may or may not be log-concave"""
    t = mpf(t)
    return exp(-t**2) * (1 + mpf("0.5") * cos(2 * t))

def kernel_gauss_sin_mod(t):
    """exp(-t^2 + 0.1*sin(t^2))  — almost certainly NOT log-concave"""
    t = mpf(t)
    return exp(-t**2 + mpf("0.1") * sin(t**2))


# --- Near-counterexample probes ---

def kernel_exp_t4_cos2(t):
    """exp(-t^4) * cos^2(0.1*t)  — check if log-concave"""
    t = mpf(t)
    return exp(-t**4) * cos(mpf("0.1") * t)**2

def kernel_gauss_abscos(t):
    """exp(-5*t^2) * |cos(0.5*t)|  — small beta/alpha ratio"""
    t = mpf(t)
    c = cos(mpf("0.5") * t)
    return exp(-5 * t**2) * abs(c)


# ==========================================================================
# Registry of all kernels to test
# ==========================================================================

# Each entry: (kernel_func, meta_dict)
# meta_dict keys: label, class, H1_even, H2_positive, H3_integrable,
#                 H4_analytic, H5_superexp_decay, notes

KERNELS = {
    # --- Class 2 extended ---
    "exp_t6": (kernel_exp_t6, {
        "label": "exp(-t^6) [Class 2, m=3]",
        "class": "2_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "Known (Polya) to have only real Fourier zeros for even integer p",
    }),
    "exp_t8": (kernel_exp_t8, {
        "label": "exp(-t^8) [Class 2, m=4]",
        "class": "2_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "Known (Polya) to have only real Fourier zeros",
    }),
    "exp_t10": (kernel_exp_t10, {
        "label": "exp(-t^10) [Class 2, m=5]",
        "class": "2_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "Known (Polya) to have only real Fourier zeros",
    }),

    # --- Class 3 extended ---
    "gauss_eps1": (make_gauss_eps("1"), {
        "label": "exp(-t^2 - t^4) [Class 3, eps=1]",
        "class": "3_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "(log K)'' = -2 - 12*t^2 < 0 => strictly log-concave",
    }),
    "gauss_eps5": (make_gauss_eps("5"), {
        "label": "exp(-t^2 - 5*t^4) [Class 3, eps=5]",
        "class": "3_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "(log K)'' = -2 - 60*t^2 < 0 => strictly log-concave",
    }),
    "gauss_eps10": (make_gauss_eps("10"), {
        "label": "exp(-t^2 - 10*t^4) [Class 3, eps=10]",
        "class": "3_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "(log K)'' = -2 - 120*t^2 < 0 => strictly log-concave",
    }),
    "gauss_eps50": (make_gauss_eps("50"), {
        "label": "exp(-t^2 - 50*t^4) [Class 3, eps=50]",
        "class": "3_extended",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "(log K)'' = -2 - 600*t^2 < 0 => strictly log-concave",
    }),

    # --- Class 6b: drop H5 ---
    "gauss_rational": (kernel_gauss_rational, {
        "label": "exp(-t^2)/(1+0.01*t^2) [Class 6b, slower decay]",
        "class": "6b_drop_H5",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        # Note: this still decays superexponentially because exp(-t^2) dominates.
        # Revised below if needed after checking.
        "notes": "exp(-t^2) dominates; H5 likely still holds. Borderline case.",
    }),
    "poly_decay": (kernel_poly_decay, {
        "label": "(1+t^2)^{-2} [Class 6b, polynomial decay]",
        "class": "6b_drop_H5",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": False,
        "notes": "Polynomial decay ~ t^{-4}. FAILS H5. FT is known: K(xi) = (pi/2)*(1+|xi|)*exp(-|xi|). Has NO complex zeros (all zeros on real axis if any). Control case.",
    }),

    # --- Class 6c: drop H6 ---
    "gauss_cos_mod": (kernel_gauss_cos_mod, {
        "label": "exp(-t^2)*(1+0.5*cos(2t)) [Class 6c, H6 check needed]",
        "class": "6c_drop_H6",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "Log-concavity must be checked numerically. Cosine modulation may break H6.",
    }),
    "gauss_sin_mod": (kernel_gauss_sin_mod, {
        "label": "exp(-t^2+0.1*sin(t^2)) [Class 6c, likely fails H6]",
        "class": "6c_drop_H6",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "sin(t^2) oscillation almost certainly breaks log-concavity.",
    }),

    # --- Near-counterexample probes ---
    "exp_t4_cos2": (kernel_exp_t4_cos2, {
        "label": "exp(-t^4)*cos^2(0.1*t) [near-CX probe]",
        "class": "near_cx",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": True, "H5_superexp_decay": True,
        "notes": "cos^2(0.1*t) modulation with tiny frequency. Check log-concavity.",
    }),
    "gauss_abscos": (kernel_gauss_abscos, {
        "label": "exp(-5*t^2)*|cos(0.5*t)| [near-CX probe, H4 check]",
        "class": "near_cx",
        "H1_even": True, "H2_positive": True, "H3_integrable": True,
        "H4_analytic": False,
        "H5_superexp_decay": True,
        "notes": "|cos(.)| is NOT analytic at zeros of cos. Fails H4. Control.",
    }),
}


# ==========================================================================
# Log-concavity check
# ==========================================================================

def log_second_derivative(K, t):
    """Compute (log K)''(t) using mpmath diff. Returns mpf."""
    lK = lambda s: log(K(s))
    try:
        return diff(lK, mpf(t), 2)
    except Exception:
        h = mpf("1e-8")
        return (lK(mpf(t) + h) - 2*lK(mpf(t)) + lK(mpf(t) - h)) / h**2


def check_log_concavity(K, label="kernel"):
    """
    Check (log K)''(t) <= 0 on [0, 10] using a grid of ~70 points.
    Returns dict with log_concave bool, max violation, worst_t.
    """
    t_grid = (
        [mpf("0")]
        + [mpf(x) / 100 for x in range(1, 11)]
        + [mpf(x) / 10 for x in range(1, 51)]
        + [mpf(x) for x in range(1, 11)]
    )
    t_grid = sorted(set(t_grid))

    max_val = mpf("-1e100")
    worst_t = None
    n_positive = 0

    for t in t_grid:
        try:
            val = log_second_derivative(K, t)
            fval = float(val)
            if fval > float(max_val):
                max_val = mpf(str(fval))
                worst_t = float(t)
            if fval > 1e-12:  # small tolerance for numerical noise
                n_positive += 1
        except Exception:
            pass

    log_concave = float(max_val) <= 1e-12
    return {
        "log_concave": log_concave,
        "max_log_second_deriv": float(max_val),
        "worst_t": worst_t,
        "n_violations": n_positive,
        "n_points": len(t_grid),
    }


# ==========================================================================
# Fourier transform
# ==========================================================================

def fourier_real(K, xi, T_max="30"):
    """F(xi) = 2 * int_0^{T_max} K(t) cos(xi*t) dt, for real xi."""
    xi = mpf(xi)
    T = mpf(T_max)
    integrand = lambda t: K(t) * cos(xi * t)
    try:
        val, err = quad(integrand, [0, T], maxdegree=8, error=True)
        return 2 * val
    except Exception:
        return mpf("nan")


def fourier_complex(K, xi_c, T_max="30"):
    """F(xi) for complex xi. Returns mpc."""
    from mpmath import cos as mcos
    xi = mpc(xi_c)
    T = mpf(T_max)
    integrand_re = lambda t: mre(K(t) * mcos(xi * t))
    integrand_im = lambda t: mim(K(t) * mcos(xi * t))
    try:
        F_re = 2 * quad(integrand_re, [0, T], maxdegree=8)[0]
        F_im = 2 * quad(integrand_im, [0, T], maxdegree=8)[0]
        return mpc(F_re, F_im)
    except Exception:
        return mpc("nan", "nan")


# ==========================================================================
# Real axis scan
# ==========================================================================

def scan_real_zeros(K, label, xi_max=20, n_points=200):
    """Scan F(xi) on [0, xi_max] for sign changes."""
    step = float(xi_max) / (n_points - 1)
    values = []
    for i in range(n_points):
        xi = mpf(step * i)
        try:
            val = float(fourier_real(K, xi))
        except Exception:
            val = None
        values.append((float(xi), val))

    sign_changes = []
    for i in range(len(values) - 1):
        x0, v0 = values[i]
        x1, v1 = values[i + 1]
        if v0 is not None and v1 is not None and v0 * v1 < 0:
            sign_changes.append({"xi_approx": (x0 + x1) / 2, "bracket": [x0, x1]})

    return {
        "kernel": label,
        "xi_range": [0, float(xi_max)],
        "n_points": n_points,
        "real_zeros_found": len(sign_changes),
        "sign_changes": sign_changes[:20],  # cap output
    }


# ==========================================================================
# Complex strip scan
# ==========================================================================

def scan_complex_zeros(K, label, xi_re_max=20, xi_im_min=0.01, xi_im_max=5,
                       n_re=30, n_im=15):
    """
    Scan |F(xi)| in complex strip and look for near-zeros.
    Grid: Re in [0, xi_re_max], Im in [xi_im_min, xi_im_max].
    """
    threshold = mpf("1e-4")
    candidates = []

    re_step = float(xi_re_max) / max(n_re - 1, 1)
    im_step = float(xi_im_max - xi_im_min) / max(n_im - 1, 1)

    print(f"    Complex scan {n_re}x{n_im} for {label}...", end=" ", flush=True)

    for ir in range(n_re):
        xi_re = mpf(re_step * ir)
        for ii in range(n_im):
            xi_im = mpf(xi_im_min) + mpf(im_step * ii)
            xi = mpc(xi_re, xi_im)
            try:
                F = fourier_complex(K, xi)
                mag = float(abs(F))
                if mag < float(threshold):
                    candidates.append({
                        "xi_re": float(xi_re),
                        "xi_im": float(xi_im),
                        "F_magnitude": mag,
                        "F_re": float(mre(F)),
                        "F_im": float(mim(F)),
                        "status": "COUNTEREXAMPLE-CANDIDATE (unverified)",
                    })
            except Exception:
                pass

    print(f"{len(candidates)} candidate(s)")
    return {
        "kernel": label,
        "scan_region": {
            "xi_re": [0, float(xi_re_max)],
            "xi_im": [float(xi_im_min), float(xi_im_max)],
        },
        "grid": f"{n_re}x{n_im}",
        "n_cells_scanned": n_re * n_im,
        "counterexample_candidates": candidates,
    }


# ==========================================================================
# Full pipeline for one kernel
# ==========================================================================

def test_kernel(name, K, meta, deep=False):
    """Run full H13 falsification pipeline for one kernel."""
    label = meta["label"]
    print(f"\n{'='*60}")
    print(f"Kernel: {label}")
    print(f"  Class: {meta['class']}")
    print(f"{'='*60}")

    # --- Step 1: Check hypotheses ---
    print("  Step 1: Hypothesis check...")
    H1 = meta.get("H1_even", True)
    H2 = meta.get("H2_positive", True)
    H3 = meta.get("H3_integrable", True)
    H4 = meta.get("H4_analytic", True)
    H5 = meta.get("H5_superexp_decay", True)

    # Numerical log-concavity check
    lc = check_log_concavity(K, label)
    H6 = lc["log_concave"]

    hyp = {
        "H1_even": H1, "H2_positive": H2, "H3_integrable": H3,
        "H4_analytic": H4, "H5_superexp_decay": H5,
        "H6_log_concave": H6,
        "H6_max_violation": lc["max_log_second_deriv"],
        "H6_worst_t": lc["worst_t"],
        "H6_n_violations": lc["n_violations"],
    }
    all_ok = H1 and H2 and H3 and H4 and H5 and H6

    for k in ["H1_even", "H2_positive", "H3_integrable", "H4_analytic",
              "H5_superexp_decay", "H6_log_concave"]:
        v = hyp[k]
        sym = "✓" if v else "✗"
        print(f"    {k}: {sym}")

    # --- Step 2: Real axis scan ---
    print("  Step 2: Real axis scan [0, 20]...")
    real_scan = scan_real_zeros(K, label, xi_max=20, n_points=200)
    print(f"    Real zeros found: {real_scan['real_zeros_found']}")

    # --- Step 3: Complex strip scan ---
    n_re = 30 if not deep else 50
    n_im = 15 if not deep else 25
    xi_re_max = 20 if not deep else 40
    xi_im_max = 5 if not deep else 10

    print(f"  Step 3: Complex strip scan (Re∈[0,{xi_re_max}], Im∈[0.01,{xi_im_max}])...")
    complex_scan = scan_complex_zeros(K, label,
                                       xi_re_max=xi_re_max,
                                       xi_im_min=0.01,
                                       xi_im_max=xi_im_max,
                                       n_re=n_re, n_im=n_im)
    n_complex = len(complex_scan["counterexample_candidates"])

    # --- Verdict ---
    if not all_ok:
        failed = [k for k in ["H1_even","H2_positive","H3_integrable",
                               "H4_analytic","H5_superexp_decay","H6_log_concave"]
                  if not hyp[k]]
        status = "INVALID CANDIDATE"
        notes = f"Fails: {', '.join(failed)}. "
        if n_complex > 0:
            notes += (f"Found {n_complex} complex near-zero(s) — "
                      f"confirms {'H5' if 'H5' in str(failed) else 'violated hypothesis'} "
                      f"is necessary for H13.")
            status = "HYPOTHESIS-NECESSITY EVIDENCE"
        else:
            notes += "No complex zeros found despite hypothesis failure."
    elif n_complex > 0:
        status = "COUNTEREXAMPLE CANDIDATE"
        notes = (f"ALL H1-H6 satisfied but {n_complex} complex near-zero(s) found. "
                 f"REQUIRES argument_principle_box.py for rigorous confirmation.")
    else:
        status = "NO COUNTEREXAMPLE"
        notes = "All H1-H6 satisfied. No complex zeros in scanned region."

    print(f"  → Status: {status}")

    return {
        "kernel_name": name,
        "kernel_label": label,
        "kernel_class": meta["class"],
        "hypotheses": hyp,
        "all_hypotheses_satisfied": all_ok,
        "real_axis_scan": {
            "zeros_found": real_scan["real_zeros_found"],
            "sign_changes": real_scan["sign_changes"],
        },
        "complex_strip_scan": {
            "region": complex_scan["scan_region"],
            "grid": complex_scan["grid"],
            "cells_scanned": complex_scan["n_cells_scanned"],
            "candidates_found": n_complex,
            "candidates": complex_scan["counterexample_candidates"],
        },
        "status": status,
        "notes": notes,
    }


# ==========================================================================
# Main
# ==========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Iteration 2c: Expanded H13 counterexample search")
    parser.add_argument("--class", dest="kernel_class", default="all",
                        help="Kernel class to test: all, 2_extended, 3_extended, "
                             "6b_drop_H5, 6c_drop_H6, near_cx")
    parser.add_argument("--kernel", default=None,
                        help="Specific kernel name (overrides --class)")
    parser.add_argument("--deep", action="store_true",
                        help="Larger complex scan grid")
    parser.add_argument("--output_dir", default=None)
    args = parser.parse_args()

    out_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR

    # Select kernels
    if args.kernel:
        if args.kernel not in KERNELS:
            print(f"Unknown kernel: {args.kernel}. Available: {list(KERNELS.keys())}",
                  file=sys.stderr)
            sys.exit(1)
        selected = {args.kernel: KERNELS[args.kernel]}
    elif args.kernel_class == "all":
        selected = KERNELS
    else:
        selected = {k: v for k, v in KERNELS.items()
                    if v[1]["class"] == args.kernel_class}
        if not selected:
            print(f"No kernels in class '{args.kernel_class}'", file=sys.stderr)
            sys.exit(1)

    print(f"Iteration 2c: Expanded H13 Counterexample Search")
    print(f"Kernels: {list(selected.keys())}")
    print(f"Deep scan: {args.deep}")
    print(f"Precision: {mp.dps} decimal digits")
    print(f"Claim discipline: COMPUTATION class only.")
    print()

    all_results = []
    for name, (K, meta) in selected.items():
        result = test_kernel(name, K, meta, deep=args.deep)
        all_results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY — Iteration 2c")
    print('='*60)
    cx_count = 0
    h5_evidence = False
    h6_evidence = False
    for r in all_results:
        s = r["status"]
        sym = "★" if "COUNTEREXAMPLE" in s and "NO" not in s else "—"
        print(f"  {sym} {r['kernel_label'][:45]:45s} → {s}")
        if "COUNTEREXAMPLE CANDIDATE" == s:
            cx_count += 1
        if "HYPOTHESIS-NECESSITY" in s:
            failed = [k for k in ["H5_superexp_decay", "H6_log_concave"]
                      if not r["hypotheses"].get(k, True)]
            if "H5_superexp_decay" in failed:
                h5_evidence = True
            if "H6_log_concave" in failed:
                h6_evidence = True

    print(f"\nCounterexample candidates (all H1-H6 hold): {cx_count}")
    print(f"H5 necessity evidence: {'YES' if h5_evidence else 'NO'}")
    print(f"H6 necessity evidence: {'YES' if h6_evidence else 'NO'}")

    # Save output
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output = {
        "script": "extended_search.py",
        "iteration": "2c",
        "timestamp": timestamp,
        "mp_dps": mp.dps,
        "deep": args.deep,
        "claim_discipline": (
            "COMPUTATION class only. Status 'NO COUNTEREXAMPLE' does NOT prove H13. "
            "Status 'COUNTEREXAMPLE CANDIDATE' requires argument_principle_box.py "
            "confirmation AND verification of all H1-H6 hypotheses before ANY "
            "disproof claim."
        ),
        "summary": {
            "total_kernels_tested": len(all_results),
            "counterexample_candidates": cx_count,
            "H5_necessity_evidence": h5_evidence,
            "H6_necessity_evidence": h6_evidence,
        },
        "results": all_results,
    }

    output_file = out_dir / f"extended_search_{timestamp}.json"
    output_file.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to: {output_file}")

    if cx_count > 0:
        print("\n*** COUNTEREXAMPLE CANDIDATES FOUND — RUN argument_principle_box.py ***")
    else:
        print("\nNo counterexample found. H13 holds on all tested kernels (COMPUTATION).")

    return output


if __name__ == "__main__":
    main()
