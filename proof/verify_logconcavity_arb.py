# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""INDEPENDENT log-concavity verification using Arb (FLINT).

This script reproduces the rigorous IA certification from
verify_logconcavity_rigorous.py using a COMPLETELY DIFFERENT interval
arithmetic library: Arb (via python-flint) instead of mpmath.iv.

If both libraries certify all subintervals, the result is independent
of any single IA implementation — addressing the strongest referee
objection against computer-assisted proofs.

Requires: pip install python-flint

Usage:
    python proof/verify_logconcavity_arb.py           # Full run (~70s)
    python proof/verify_logconcavity_arb.py --quick    # First 100 + last 100 subintervals
"""
import argparse
import json
import os
import time

from flint import arb, ctx

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

# Match the mpmath verification — Arb needs slightly earlier split
# (Arb ball widths are marginally wider than mpmath.iv near the boundary)
N_TERMS = 5
U_MAX = 1.0
U_SPLIT = 0.946
N_COARSE = 1892   # delta = 0.0005
N_FINE = 54000    # delta ~ 1e-6

# Arb precision in bits (200 bits ≈ 60 decimal digits, matching mpmath dps=60)
PREC = 200


def phi_n_and_derivs_arb(n, u):
    """Compute phi_n(u), phi_n'(u), phi_n''(u) using Arb interval arithmetic.

    Exact same formulas as verify_logconcavity_rigorous.py, but using
    Arb balls instead of mpmath intervals.
    """
    pi = arb.pi()
    n2 = arb(n) ** 2
    n4 = n2 ** 2

    e9u2 = (arb(9) * u / 2).exp()
    e5u2 = (arb(5) * u / 2).exp()
    e2u = (2 * u).exp()
    e4u = e2u ** 2

    # g and derivatives
    g = 2 * pi**2 * n4 * e9u2 - 3 * pi * n2 * e5u2
    gp = 9 * pi**2 * n4 * e9u2 - arb(15) * pi * n2 * e5u2 / 2
    gpp = arb(81) * pi**2 * n4 * e9u2 / 2 - arb(75) * pi * n2 * e5u2 / 4

    # E and derivatives
    E = (-pi * n2 * e2u).exp()
    Ep = -2 * pi * n2 * e2u * E
    Epp = (-4 * pi * n2 * e2u + 4 * pi**2 * n4 * e4u) * E

    # Product rule
    f = g * E
    fp = gp * E + g * Ep
    fpp = gpp * E + 2 * gp * Ep + g * Epp

    return f, fp, fpp


def Q_Phi_arb(u):
    """Compute Q_Phi = Phi'' * Phi - (Phi')^2 using Arb."""
    f_total = arb(0)
    fp_total = arb(0)
    fpp_total = arb(0)

    for n in range(1, N_TERMS + 1):
        f, fp, fpp = phi_n_and_derivs_arb(n, u)
        f_total += f
        fp_total += fp
        fpp_total += fpp

    Phi = 4 * f_total
    Phi_p = 4 * fp_total
    Phi_pp = 4 * fpp_total

    return Phi_pp * Phi - Phi_p ** 2


def make_interval(lo, hi):
    """Create an Arb ball containing [lo, hi]."""
    mid = (lo + hi) / 2
    rad = (hi - lo) / 2
    return arb("[%s +/- %s]" % (mid, rad + 1e-20))


def main():
    parser = argparse.ArgumentParser(
        description="Independent IA verification using Arb/FLINT"
    )
    parser.add_argument("--quick", action="store_true",
                        help="Test first 100 + last 100 subintervals only")
    args = parser.parse_args()

    ctx.prec = PREC

    # Build subinterval list (identical to mpmath version)
    subintervals = []
    dc = U_SPLIT / N_COARSE
    for i in range(N_COARSE):
        subintervals.append((i * dc, (i + 1) * dc))
    df = (U_MAX - U_SPLIT) / N_FINE
    for i in range(N_FINE):
        subintervals.append((U_SPLIT + i * df, U_SPLIT + (i + 1) * df))

    n_total = len(subintervals)

    if args.quick:
        # Test boundary subintervals (most likely to fail)
        indices = list(range(100)) + list(range(n_total - 100, n_total))
        test_intervals = [(i, subintervals[i]) for i in indices]
        label = "quick (%d subintervals)" % len(test_intervals)
    else:
        test_intervals = list(enumerate(subintervals))
        label = "full (%d subintervals)" % n_total

    print("=" * 72)
    print("  INDEPENDENT LOG-CONCAVITY VERIFICATION (Arb/FLINT)")
    print("  Library: python-flint (Arb ball arithmetic)")
    print("  Precision: %d bits (≈%d decimal digits)" % (PREC, PREC * 3 // 10))
    print("  Mode: %s" % label)
    print("=" * 72)

    certified = 0
    failed = 0
    max_upper = float("-inf")
    worst_u = 0

    t0 = time.time()

    for count, (idx, (u_lo, u_hi)) in enumerate(test_intervals):
        try:
            u_interval = make_interval(u_lo, u_hi)
            Q = Q_Phi_arb(u_interval)

            # Arb: Q < 0 returns True iff the entire ball is strictly negative
            if Q < 0:
                certified += 1
                mid = float(Q.mid())
                rad = float(Q.rad())
                upper = mid + rad
                if upper > max_upper:
                    max_upper = upper
                    worst_u = (u_lo + u_hi) / 2
            else:
                print("  FAIL at subinterval %d (u=[%.6f,%.6f]): Q = %s" %
                      (idx, u_lo, u_hi, Q))
                failed += 1

        except Exception as e:
            print("  ERROR at subinterval %d (u=[%.6f,%.6f]): %s" %
                  (idx, u_lo, u_hi, e))
            failed += 1

        if (count + 1) % 5000 == 0 or (count + 1) == len(test_intervals):
            elapsed = time.time() - t0
            print("  ... %d/%d done (%.0fs, %d certified, %d failed)" %
                  (count + 1, len(test_intervals), elapsed, certified, failed))

    elapsed = time.time() - t0

    print()
    print("=" * 72)
    print("  RESULTS (Arb/FLINT)")
    print("  Certified: %d/%d" % (certified, len(test_intervals)))
    print("  Failed:    %d/%d" % (failed, len(test_intervals)))
    print("  Max upper bound on Q: %.6e at u=%.6f" % (max_upper, worst_u))
    print("  Time: %.0fs" % elapsed)

    if failed == 0:
        print()
        print("  *** ALL %d SUBINTERVALS CERTIFIED (Arb/FLINT) ***" % len(test_intervals))
        print("  This is an INDEPENDENT confirmation using a different IA library.")
        print("  Combined with mpmath.iv verification, the result is robust")
        print("  against implementation bugs in either library.")
    else:
        print()
        print("  *** %d SUBINTERVALS NOT CERTIFIED ***" % failed)

    print("=" * 72)

    result = {
        "method": "arb_flint_independent",
        "library": "python-flint (Arb)",
        "library_version": "0.8.0",
        "precision_bits": PREC,
        "n_subintervals_tested": len(test_intervals),
        "n_subintervals_total": n_total,
        "n_terms": N_TERMS,
        "u_range": [0, U_MAX],
        "u_split": U_SPLIT,
        "certified": certified,
        "failed": failed,
        "max_Q_upper": max_upper,
        "worst_u": worst_u,
        "time_s": elapsed,
        "all_certified": failed == 0,
        "quick_mode": args.quick,
        "note": "Independent verification using Arb (FLINT), NOT mpmath.iv",
    }
    out_path = os.path.join(ROOT_DIR, "results", "verify_logconcavity_arb.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print("  -> %s" % out_path)


if __name__ == "__main__":
    main()
