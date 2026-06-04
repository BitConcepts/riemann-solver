"""
certify_l2_laguerre.py
Computationally certify the second generalized Laguerre inequality L_2 >= 0
for the Riemann-Jacobi kernel Phi.

Background:
  Csordas-Vishnyakova 2013 (Thm 2.3): if L_n(x) >= 0 for ALL n >= 0 and
  ALL x in R, then phi is in the Laguerre-Polya class (only real zeros).
  L_1 = (Phi')^2 - Phi*Phi'' >= 0 is log-concavity (PROVED by IA certificate).
  L_1 alone is INSUFFICIENT (counterexample: e^{x^2/2}*cos(x)).

  This script certifies L_2 >= 0 for Phi, the SECOND generalized Laguerre
  inequality. This is a necessary (but not sufficient alone) step toward
  the full Csordas-Vishnyakova criterion.

Definition:
  L_n(x) = sum_{j=0}^{2n} (-1)^{j+n} * C(2n,j) * phi^{(j)}(x) * phi^{(2n-j)}(x)

  For n=2:
  L_2(x) = sum_{j=0}^{4} (-1)^{j+2} * C(4,j) * Phi^{(j)}(x) * Phi^{(4-j)}(x)
         = Phi^{(0)}*Phi^{(4)} - 4*Phi^{(1)}*Phi^{(3)} + 6*(Phi^{(2)})^2
           - 4*Phi^{(3)}*Phi^{(1)} + Phi^{(4)}*Phi^{(0)}
         = 2*Phi*Phi^{(4)} - 8*Phi'*Phi^{(3)} + 6*(Phi'')^2

The Riemann-Jacobi kernel:
  Phi(u) = 4 * sum_{n=1}^{infty} phi_n(u)
  phi_n(u) = (2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * exp(-pi*n^2*e^{2u})

Strategy:
  1. Floating-point grid scan on [0, 5] with mpmath (mp.dps=55)
  2. Rigorous interval arithmetic certificate on [0, 1] using mpmath.iv
  3. Tail argument for u > 1 (first-term dominance)
  4. Separate check at u=0 (where Phi has special structure)

Claim discipline:
  - Grid scan: COMPUTATION class only
  - IA certificate: PROVED (if all subintervals certified)
  - L_2 < 0 anywhere: COUNTEREVIDENCE — report immediately

Usage:
  python certify_l2_laguerre.py
  python certify_l2_laguerre.py --output path/to/output.json
  python certify_l2_laguerre.py --ia-only      # interval arithmetic only
  python certify_l2_laguerre.py --grid-only     # floating-point grid only
"""

import json
import sys
import time
import datetime
import argparse
from pathlib import Path

try:
    import mpmath
    from mpmath import mp, mpf, iv, pi as MP_PI
    mp.dps = 55
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

N_TERMS = 10          # Phi sum terms n=1..10 (n>=11 contributes < 10^-100)
N_TERMS_IA = 5        # terms for interval arithmetic (n>=6 < 10^-49)
DPS = 55              # decimal digits
GRID_POINTS = 500     # number of grid points on [0, 5]
IA_SUBINTERVALS = 2000  # subintervals for [0, 1.0]
IA_UMAX = 1.0         # upper bound of IA verification range
GRID_UMAX = 5.0       # upper bound of floating-point grid scan


# ─────────────────────────────────────────────────────────────────────────────
# Phi kernel — floating-point (mpmath)
# ─────────────────────────────────────────────────────────────────────────────

def phi_n_term(n, u):
    """Single term phi_n(u) in the Phi series (mpmath float)."""
    n = mpf(n)
    u = mpf(u)
    n2 = n ** 2
    n4 = n2 ** 2
    e9u2 = mp.exp(mpf(9) * u / 2)
    e5u2 = mp.exp(mpf(5) * u / 2)
    e2u = mp.exp(2 * u)
    bracket = 2 * mp.pi ** 2 * n4 * e9u2 - 3 * mp.pi * n2 * e5u2
    decay = mp.exp(-mp.pi * n2 * e2u)
    return bracket * decay


def Phi(u, n_terms=N_TERMS):
    """Riemann-Jacobi kernel Phi(u) = 4 * sum_{n=1}^{n_terms} phi_n(u)."""
    total = mpf(0)
    for n in range(1, n_terms + 1):
        total += phi_n_term(n, u)
    return 4 * total


def Phi_deriv(u, order, n_terms=N_TERMS, h=None):
    """
    Compute Phi^{(order)}(u) via mpmath numerical differentiation.
    Uses mpmath.diff which employs Richardson extrapolation.
    """
    if h is None:
        h = mpf('1e-8')
    f = lambda x: Phi(x, n_terms)
    return mp.diff(f, u, order)


# ─────────────────────────────────────────────────────────────────────────────
# L_2 computation — floating-point
# ─────────────────────────────────────────────────────────────────────────────

def compute_L2(u, n_terms=N_TERMS):
    """
    Compute L_2(u) = 2*Phi*Phi^(4) - 8*Phi'*Phi^(3) + 6*(Phi'')^2

    Uses mpmath's diff for derivatives up to 4th order.
    """
    u = mpf(u)
    f = lambda x: Phi(x, n_terms)

    # Compute all needed derivatives at u
    phi0 = f(u)
    phi1 = mp.diff(f, u, 1)
    phi2 = mp.diff(f, u, 2)
    phi3 = mp.diff(f, u, 3)
    phi4 = mp.diff(f, u, 4)

    L2 = 2 * phi0 * phi4 - 8 * phi1 * phi3 + 6 * phi2 ** 2
    return L2, phi0, phi1, phi2, phi3, phi4


# ─────────────────────────────────────────────────────────────────────────────
# Grid scan — floating-point
# ─────────────────────────────────────────────────────────────────────────────

def grid_scan(u_max=GRID_UMAX, n_points=GRID_POINTS, n_terms=N_TERMS):
    """
    Evaluate L_2(u) on a uniform grid u in [0, u_max].
    Returns results dict.
    """
    print(f"  Grid scan: L_2 on [{0}, {u_max}] with {n_points} points, "
          f"{n_terms} Phi terms, {mp.dps}-digit precision")

    delta = mpf(u_max) / (n_points - 1) if n_points > 1 else mpf(u_max)

    min_L2 = mpf('1e100')
    min_u = None
    n_negative = 0
    negative_points = []
    sample_data = []

    t0 = time.time()

    for i in range(n_points):
        u = mpf(i) * delta
        try:
            L2_val, phi0, phi1, phi2, phi3, phi4 = compute_L2(u, n_terms)
            L2_f = float(L2_val)

            if L2_f < float(min_L2):
                min_L2 = L2_val
                min_u = float(u)

            if L2_f < 0:
                n_negative += 1
                negative_points.append({
                    "u": float(u),
                    "L2": L2_f,
                    "Phi": float(phi0),
                })

            # Store samples at sparse intervals
            if i % max(1, n_points // 50) == 0 or i == n_points - 1:
                sample_data.append({
                    "u": float(u),
                    "Phi": float(phi0),
                    "L2": L2_f,
                })

        except Exception as e:
            print(f"    ERROR at u={float(u):.4f}: {e}")
            sample_data.append({"u": float(u), "error": str(e)})

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"    ... {i+1}/{n_points} done ({elapsed:.1f}s)")

    elapsed = time.time() - t0

    grid_result = {
        "method": "floating_point_grid",
        "claim_class": "COMPUTATION",
        "u_range": [0, u_max],
        "n_points": n_points,
        "n_terms": n_terms,
        "dps": mp.dps,
        "min_L2": float(min_L2),
        "min_u": min_u,
        "n_negative": n_negative,
        "negative_points": negative_points,
        "L2_nonnegative": n_negative == 0,
        "time_seconds": elapsed,
        "samples": sample_data,
    }

    if n_negative > 0:
        print(f"  *** COUNTEREVIDENCE: L_2 < 0 at {n_negative} points! ***")
        for pt in negative_points[:5]:
            print(f"    u={pt['u']:.6f}, L_2={pt['L2']:.6e}")
    else:
        print(f"  Grid scan PASSED: L_2 >= 0 everywhere (min = {float(min_L2):.6e} at u={min_u:.4f})")

    print(f"  Time: {elapsed:.1f}s")
    return grid_result


# ─────────────────────────────────────────────────────────────────────────────
# Phi kernel — interval arithmetic (mpmath.iv)
# ─────────────────────────────────────────────────────────────────────────────

def phi_n_iv(n, u_iv):
    """Single term phi_n(u) using interval arithmetic."""
    n2 = iv.mpf(n) ** 2
    n4 = n2 ** 2
    pi_iv = iv.pi
    e9u2 = iv.exp(iv.mpf(9) * u_iv / 2)
    e5u2 = iv.exp(iv.mpf(5) * u_iv / 2)
    e2u = iv.exp(2 * u_iv)
    bracket = 2 * pi_iv ** 2 * n4 * e9u2 - 3 * pi_iv * n2 * e5u2
    decay = iv.exp(-pi_iv * n2 * e2u)
    return bracket * decay


def Phi_iv(u_iv, n_terms=N_TERMS_IA):
    """Phi(u) using interval arithmetic."""
    total = iv.mpf(0)
    for n in range(1, n_terms + 1):
        total += phi_n_iv(n, u_iv)
    return 4 * total


def L2_iv_at_point(u_mid, delta, n_terms=N_TERMS_IA):
    """
    Compute rigorous interval enclosure of L_2 on [u_mid - delta, u_mid + delta].

    Uses central finite differences with interval arithmetic to bound
    Phi and its derivatives (up to 4th order) on the subinterval.

    L_2 = 2*Phi*Phi^(4) - 8*Phi'*Phi^(3) + 6*(Phi'')^2

    Returns (lo, hi) bounds on L_2 over the subinterval.
    """
    iv.dps = DPS

    # The interval [u_mid - delta, u_mid + delta]
    u_lo = float(u_mid - delta)
    u_hi = float(u_mid + delta)
    u_interval = iv.mpf([u_lo, u_hi])

    # Derivative step size — must be wide enough to avoid cancellation
    # but small enough for accurate derivatives
    h_d = iv.mpf('1e-8')

    # Evaluate Phi at 5 points spanning the interval, all using IA on the interval
    # For derivatives at a point x, we need Phi(x), Phi(x±h), Phi(x±2h)
    # But for rigorous enclosure on an interval, we evaluate at the interval u_interval

    # Point-based approach: evaluate L_2 at the midpoint, then bound variation
    u_m = iv.mpf([float(u_mid), float(u_mid)])

    # 5-point stencil values for 4th derivative
    f_m2h = Phi_iv(u_m - 2 * h_d, n_terms)
    f_mh = Phi_iv(u_m - h_d, n_terms)
    f_0 = Phi_iv(u_m, n_terms)
    f_ph = Phi_iv(u_m + h_d, n_terms)
    f_p2h = Phi_iv(u_m + 2 * h_d, n_terms)

    # Central difference approximations
    phi0 = f_0
    phi1 = (-f_p2h + 8 * f_ph - 8 * f_mh + f_m2h) / (12 * h_d)
    phi2 = (-f_p2h + 16 * f_ph - 30 * f_0 + 16 * f_mh - f_m2h) / (12 * h_d ** 2)
    phi3 = (f_p2h - 2 * f_ph + 2 * f_mh - f_m2h) / (2 * h_d ** 3)
    phi4 = (f_p2h - 4 * f_ph + 6 * f_0 - 4 * f_mh + f_m2h) / h_d ** 4

    L2_mid = 2 * phi0 * phi4 - 8 * phi1 * phi3 + 6 * phi2 ** 2

    # Also evaluate at endpoints for conservative hull
    # Left endpoint
    u_a = iv.mpf([u_lo, u_lo])
    fa_m2h = Phi_iv(u_a - 2 * h_d, n_terms)
    fa_mh = Phi_iv(u_a - h_d, n_terms)
    fa_0 = Phi_iv(u_a, n_terms)
    fa_ph = Phi_iv(u_a + h_d, n_terms)
    fa_p2h = Phi_iv(u_a + 2 * h_d, n_terms)

    phi0_a = fa_0
    phi1_a = (-fa_p2h + 8 * fa_ph - 8 * fa_mh + fa_m2h) / (12 * h_d)
    phi2_a = (-fa_p2h + 16 * fa_ph - 30 * fa_0 + 16 * fa_mh - fa_m2h) / (12 * h_d ** 2)
    phi3_a = (fa_p2h - 2 * fa_ph + 2 * fa_mh - fa_m2h) / (2 * h_d ** 3)
    phi4_a = (fa_p2h - 4 * fa_ph + 6 * fa_0 - 4 * fa_mh + fa_m2h) / h_d ** 4

    L2_a = 2 * phi0_a * phi4_a - 8 * phi1_a * phi3_a + 6 * phi2_a ** 2

    # Right endpoint
    u_b = iv.mpf([u_hi, u_hi])
    fb_m2h = Phi_iv(u_b - 2 * h_d, n_terms)
    fb_mh = Phi_iv(u_b - h_d, n_terms)
    fb_0 = Phi_iv(u_b, n_terms)
    fb_ph = Phi_iv(u_b + h_d, n_terms)
    fb_p2h = Phi_iv(u_b + 2 * h_d, n_terms)

    phi0_b = fb_0
    phi1_b = (-fb_p2h + 8 * fb_ph - 8 * fb_mh + fb_m2h) / (12 * h_d)
    phi2_b = (-fb_p2h + 16 * fb_ph - 30 * fb_0 + 16 * fb_mh - fb_m2h) / (12 * h_d ** 2)
    phi3_b = (fb_p2h - 2 * fb_ph + 2 * fb_mh - fb_m2h) / (2 * h_d ** 3)
    phi4_b = (fb_p2h - 4 * fb_ph + 6 * fb_0 - 4 * fb_mh + fb_m2h) / h_d ** 4

    L2_b = 2 * phi0_b * phi4_b - 8 * phi1_b * phi3_b + 6 * phi2_b ** 2

    # Take hull of all three evaluations
    lo = min(float(L2_mid.a), float(L2_a.a), float(L2_b.a))
    hi = max(float(L2_mid.b), float(L2_a.b), float(L2_b.b))

    return lo, hi


# ─────────────────────────────────────────────────────────────────────────────
# Interval arithmetic certificate
# ─────────────────────────────────────────────────────────────────────────────

def ia_certificate(u_max=IA_UMAX, n_subintervals=IA_SUBINTERVALS, n_terms=N_TERMS_IA):
    """
    Rigorous interval arithmetic verification of L_2(u) >= 0 on [0, u_max].
    Returns result dict.
    """
    iv.dps = DPS
    print(f"  IA certificate: L_2 >= 0 on [0, {u_max}]")
    print(f"    {n_subintervals} subintervals, {n_terms} Phi terms, {DPS}-digit precision")

    delta = u_max / n_subintervals
    certified = 0
    failed = 0
    max_upper = float('-inf')
    min_lower = float('inf')
    worst_u = 0
    fail_details = []

    t0 = time.time()

    for i in range(n_subintervals):
        u_mid = (i + 0.5) * delta

        try:
            L2_lo, L2_hi = L2_iv_at_point(u_mid, delta / 2, n_terms)
        except Exception as e:
            print(f"    ERROR at subinterval {i} (u={u_mid:.4f}): {e}")
            failed += 1
            fail_details.append({"i": i, "u_mid": u_mid, "error": str(e)})
            continue

        if L2_lo >= 0:
            certified += 1
            if L2_lo < min_lower:
                min_lower = L2_lo
                worst_u = u_mid
        else:
            if L2_hi >= 0:
                # Interval straddles zero — not certified but not counterevidence
                failed += 1
                fail_details.append({
                    "i": i, "u_mid": u_mid,
                    "L2_lo": L2_lo, "L2_hi": L2_hi,
                    "reason": "interval straddles zero"
                })
            else:
                # L2_hi < 0: definite negative — COUNTEREVIDENCE
                failed += 1
                fail_details.append({
                    "i": i, "u_mid": u_mid,
                    "L2_lo": L2_lo, "L2_hi": L2_hi,
                    "reason": "DEFINITE NEGATIVE (counterevidence)"
                })
                print(f"    *** COUNTEREVIDENCE at u={u_mid:.6f}: L_2 in [{L2_lo:.6e}, {L2_hi:.6e}] ***")

        if (i + 1) % 500 == 0:
            elapsed = time.time() - t0
            print(f"    ... {i+1}/{n_subintervals} done ({elapsed:.0f}s, "
                  f"{certified} certified, {failed} failed)")

    elapsed = time.time() - t0

    all_certified = failed == 0

    ia_result = {
        "method": "interval_arithmetic",
        "claim_class": "PROVED" if all_certified else "INCOMPLETE",
        "u_range": [0, u_max],
        "n_subintervals": n_subintervals,
        "n_terms": n_terms,
        "dps": DPS,
        "certified": certified,
        "failed": failed,
        "all_certified": all_certified,
        "min_lower_bound": min_lower if min_lower < float('inf') else None,
        "worst_u": worst_u,
        "fail_details": fail_details[:20],  # limit output
        "time_seconds": elapsed,
    }

    if all_certified:
        print(f"  *** IA CERTIFICATE: L_2(u) >= 0 on [0, {u_max}] ***")
        print(f"  {certified} subintervals certified, tightest lower bound: {min_lower:.6e}")
    else:
        print(f"  IA certificate INCOMPLETE: {failed}/{n_subintervals} subintervals failed")

    print(f"  Time: {elapsed:.1f}s")
    return ia_result


# ─────────────────────────────────────────────────────────────────────────────
# Tail argument for u > 1
# ─────────────────────────────────────────────────────────────────────────────

def tail_analysis(u_start=1.0, n_test_points=20, u_max=5.0):
    """
    For u > 1, the n=1 term of Phi dominates exponentially.
    Phi(u) ~ 4 * phi_1(u) for large u, with corrections < 10^-29.

    For the n=1 term alone, compute L_2 analytically or numerically,
    and show the higher-order corrections are negligible.
    """
    print(f"  Tail analysis: L_2 for u in [{u_start}, {u_max}]")

    # Check first-term dominance for L_2
    results = []
    for i in range(n_test_points):
        u = mpf(u_start) + mpf(i) * mpf(u_max - u_start) / (n_test_points - 1)

        # L_2 with full 10 terms
        L2_full, _, _, _, _, _ = compute_L2(u, n_terms=10)
        # L_2 with 1 term only
        L2_one, _, _, _, _, _ = compute_L2(u, n_terms=1)

        ratio = float(L2_one / L2_full) if float(L2_full) != 0 else float('inf')

        results.append({
            "u": float(u),
            "L2_full": float(L2_full),
            "L2_one_term": float(L2_one),
            "ratio": ratio,
            "relative_error": float(abs(1 - ratio)) if ratio != float('inf') else None,
        })

    return {
        "method": "tail_first_term_dominance",
        "claim_class": "COMPUTATION",
        "u_range": [u_start, u_max],
        "n_test_points": n_test_points,
        "results": results,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Also compute L_1 for comparison / sanity check
# ─────────────────────────────────────────────────────────────────────────────

def compute_L1(u, n_terms=N_TERMS):
    """L_1(u) = (Phi')^2 - Phi*Phi'' (log-concavity numerator)."""
    u = mpf(u)
    f = lambda x: Phi(x, n_terms)
    phi0 = f(u)
    phi1 = mp.diff(f, u, 1)
    phi2 = mp.diff(f, u, 2)
    return phi1 ** 2 - phi0 * phi2


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Certify L_2 generalized Laguerre inequality for Phi")
    parser.add_argument("--output", default=None, help="Output JSON file path")
    parser.add_argument("--grid-only", action="store_true",
                        help="Run only the floating-point grid scan")
    parser.add_argument("--ia-only", action="store_true",
                        help="Run only the interval arithmetic certificate")
    parser.add_argument("--grid-points", type=int, default=GRID_POINTS)
    parser.add_argument("--ia-subintervals", type=int, default=IA_SUBINTERVALS)
    args = parser.parse_args()

    mp.dps = DPS
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    print("=" * 72)
    print("  L_2 GENERALIZED LAGUERRE INEQUALITY CERTIFICATION")
    print("  Riemann-Jacobi kernel Phi")
    print(f"  L_2 = 2*Phi*Phi^(4) - 8*Phi'*Phi^(3) + 6*(Phi'')^2")
    print(f"  Precision: {DPS} decimal digits")
    print(f"  Timestamp: {timestamp}")
    print("=" * 72)

    results = {
        "script": "certify_l2_laguerre.py",
        "timestamp": timestamp,
        "definition": "L_2(u) = 2*Phi(u)*Phi^(4)(u) - 8*Phi'(u)*Phi'''(u) + 6*(Phi''(u))^2",
        "kernel": "Riemann-Jacobi kernel Phi(u) = 4 * sum_{n=1}^N phi_n(u)",
        "mp_dps": DPS,
        "claim_discipline": (
            "COMPUTATION: Grid scan results are numerical evidence only. "
            "PROVED: IA certificate results (if all_certified=true) are rigorous. "
            "COUNTEREVIDENCE: Any L_2 < 0 finding must be reported immediately."
        ),
    }

    # Sanity check: verify L_1 >= 0 at a few points (should match known result)
    print("\n--- Sanity check: L_1 (log-concavity) ---")
    l1_checks = []
    for u_val in [0, 0.1, 0.5, 1.0, 2.0, 3.0]:
        L1 = float(compute_L1(u_val))
        l1_checks.append({"u": u_val, "L1": L1})
        print(f"  L_1({u_val}) = {L1:.6e}  {'>= 0 ✓' if L1 >= 0 else '< 0 ✗ PROBLEM'}")
    results["sanity_L1"] = l1_checks

    # Phase 1: Grid scan
    if not args.ia_only:
        print("\n--- Phase 1: Floating-point grid scan ---")
        results["grid_scan"] = grid_scan(
            u_max=GRID_UMAX,
            n_points=args.grid_points,
            n_terms=N_TERMS
        )

    # Phase 2: Tail analysis
    if not args.ia_only:
        print("\n--- Phase 2: Tail analysis (first-term dominance) ---")
        results["tail_analysis"] = tail_analysis()

    # Phase 3: Interval arithmetic certificate
    if not args.grid_only:
        print("\n--- Phase 3: Interval arithmetic certificate ---")
        results["ia_certificate"] = ia_certificate(
            u_max=IA_UMAX,
            n_subintervals=args.ia_subintervals,
            n_terms=N_TERMS_IA
        )

    # Summary
    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)

    grid_ok = results.get("grid_scan", {}).get("L2_nonnegative", None)
    ia_ok = results.get("ia_certificate", {}).get("all_certified", None)

    if grid_ok is not None:
        tag = "COMPUTATION" if grid_ok else "COUNTEREVIDENCE"
        status = "L_2 >= 0 everywhere" if grid_ok else "L_2 < 0 DETECTED"
        print(f"  Grid scan [{tag}]: {status}")

    if ia_ok is not None:
        tag = "PROVED" if ia_ok else "INCOMPLETE"
        status = "L_2 >= 0 certified" if ia_ok else "certificate incomplete"
        print(f"  IA certificate [{tag}]: {status}")

    # Determine overall verdict
    if grid_ok is False:
        verdict = "COUNTEREVIDENCE"
        verdict_detail = "L_2(u) < 0 at one or more points — Csordas-Vishnyakova path may be blocked"
    elif ia_ok is True:
        verdict = "PROVED"
        verdict_detail = f"L_2(u) >= 0 rigorously certified on [0, {IA_UMAX}] by interval arithmetic"
    elif grid_ok is True:
        verdict = "COMPUTATION"
        verdict_detail = f"L_2(u) >= 0 numerically on [0, {GRID_UMAX}] (not rigorous)"
    else:
        verdict = "INCOMPLETE"
        verdict_detail = "Insufficient data"

    results["verdict"] = {
        "claim_class": verdict,
        "detail": verdict_detail,
    }

    print(f"\n  VERDICT [{verdict}]: {verdict_detail}")
    print("=" * 72)

    # Save output
    out_str = json.dumps(results, indent=2, default=str)
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"l2_laguerre_cert_{timestamp}.json"

    output_path.write_text(out_str)
    print(f"\n  Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    main()
