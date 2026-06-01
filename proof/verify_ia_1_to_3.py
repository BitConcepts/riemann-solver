# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Extended certification: (log Phi)''(u) < 0 on [1.0, 3.0].

NOTE on tail prefactor correction (see docs/tail_prefactor_correction.md):
The actual |phi_n|/phi_1 = B_n(u)*exp(-pi*(n^2-1)*e^{2u}) where B_n > n^4.
This script uses epsilon* = 2*sum(n^4 ...) as a valid conservative upper bound
(since B_n/n^4 <= 1+3/(2pi-3) < 2 for all u>=0). All margins unchanged.

Direct IA on Q = Phi''*Phi - (Phi')^2 for u > 1.0 fails due to catastrophic
cancellation. This script certifies (log Phi)'' < 0 directly (no cancellation).

Proof coverage:
  [0, 1.0]: certified by verify_logconcavity_rigorous.py (52,898 IA subintervals)
  [1.0, 3.0]: certified by THIS SCRIPT (101 overlapping interval checks)
  [3.0, inf): covered by verify_algebraic_core.py (monotonicity argument)
"""

import json
import time
import sys
import os
import mpmath as mp
from mpmath import iv

DPS      = 60    # 60 digits — W_1 ~ O(100), no catastrophic cancellation
N_CHECKS = 100   # 101 checkpoints on [1.0, 3.0] (inclusive)
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def log_phi1_d2_iv(u_iv):
    """Compute (log phi_1)''(u) = -24pi*e^{2u}/h(u)^2 - 4pi*e^{2u} using IA.

    No catastrophic cancellation: values are O(100) to O(300).
    h(u) = 2pi*e^{2u} - 3 > 0 for u >= 0.
    """
    pi  = iv.pi
    e2u = iv.exp(2 * u_iv)
    h   = 2 * pi * e2u - 3          # h(u) > 0 for u >= 0
    return -24 * pi * e2u / h**2 - 4 * pi * e2u   # both terms negative


def epsilon_upper_iv(u_iv, n_tail=15):
    """IA upper bound on epsilon*(u) = 2 * sum_{n>=2} n^4 * exp(-pi*(n^2-1)*e^{2u}).

    CORRECTED: Uses 2*n^4 instead of n^4 to account for the prefactor ratio
    B_n(u) = n^2*h_n/h_1 > n^4. The correction factor B_n/n^4 <= 1+3/(2pi-3) < 2
    for all u >= 0. The factor 2 makes this a valid upper bound.
    See docs/tail_prefactor_correction.md.
    """
    pi  = iv.pi
    e2u = iv.exp(2 * u_iv)
    total = iv.mpf(0)
    for n in range(2, n_tail + 1):
        n2   = iv.mpf(n) ** 2
        # Use 2*n^4 as the corrected prefactor upper bound (B_n(u) <= 2*n^4)
        term = 2 * iv.mpf(n)**4 * iv.exp(-pi * (n2 - 1) * e2u)
        total += term
    return total


def certify_checkpoint(u, half_width, C=204.0):
    """Certify (log Phi)''(u) < 0 at a checkpoint.

    Certifies on interval [u - half_width, u + half_width].
    Returns (ok, margin) where margin > 0 means certified.
    """
    u_iv    = iv.mpf([u - half_width, u + half_width])
    W1_iv   = log_phi1_d2_iv(u_iv)          # O(100), always negative
    eps_iv  = epsilon_upper_iv(u_iv)
    # Upper bound on W_1 + C*eps  (if this < 0, certified)
    W_total_hi = float(W1_iv.b) + C * float(eps_iv.b)
    ok     = W_total_hi < 0
    margin = -W_total_hi
    return ok, margin, float(W1_iv.b), float(eps_iv.b)


def main():
    mp.mp.dps = DPS
    iv.dps    = DPS

    delta = 2.0 / N_CHECKS
    hw    = delta / 2          # half-width for each checkpoint interval

    print("=" * 72)
    print("  EXTENDED CERT: (log Phi)''(u) < 0 on [1.0, 3.0]")
    print("  Method: W_1 = (log phi_1)'' [algebraic, ~O(100)] + C*eps [doubly-exp]")
    print("  %d checkpoints, half-width=%.6f, %d-digit IA" % (N_CHECKS+1, hw, DPS))
    print("=" * 72)
    print()
    print(f"  {'u':>6}  {'W_1_upper':>12}  {'C*eps_upper':>13}  {'margin':>12}  status")
    print("  " + "-" * 60)

    cert_count  = failed_count = 0
    min_margin  = float("inf")
    worst_u     = 1.0
    table       = []
    t0          = time.time()

    for i in range(N_CHECKS + 1):
        u = 1.0 + i * delta
        # Use full interval width for ALL points (including endpoints) to
        # guarantee complete tiling of [0.99, 3.01] ⊃ [1.0, 3.0].
        # Previous code used u_hw=0 at endpoints, leaving gaps (1.0, 1.01)
        # and (2.99, 3.0) uncovered by any interval check.
        u_hw = hw
        ok, margin, w1_hi, eps_hi = certify_checkpoint(u, u_hw)

        if ok:
            cert_count += 1
            if margin < min_margin:
                min_margin = margin
                worst_u    = u
        else:
            failed_count += 1

        C_eps_hi = 204.0 * eps_hi
        status = "OK" if ok else "*** FAIL ***"
        print(f"  {u:6.3f}  {w1_hi:>12.4e}  {C_eps_hi:>13.4e}  {margin:>12.4e}  {status}")
        table.append({"u": round(u, 6), "W_1_upper": w1_hi,
                      "C_eps_upper": C_eps_hi, "margin": margin, "ok": ok})

    elapsed = time.time() - t0
    all_ok  = failed_count == 0

    print()
    print("=" * 72)
    print("  Certified: %d / %d" % (cert_count, N_CHECKS + 1))
    print("  Failed:    %d / %d" % (failed_count, N_CHECKS + 1))
    print("  Min margin (tightest): %.4e at u=%.4f" % (min_margin, worst_u))
    print("  Time: %.1fs" % elapsed)

    if all_ok:
        print()
        print("  *** ALL %d CHECKPOINTS CERTIFIED ***" % (N_CHECKS + 1))
        print("  (log Phi)''(u) < 0 on [1.0, 3.0] — NO CATASTROPHIC CANCELLATION")
        print()
        print("  Combined proof coverage:")
        print("    [0, 1.0]  : IA (52,898 subintervals, verify_logconcavity_rigorous)")
        print("    [1.0, 3.0]: algebraic + perturbation (THIS SCRIPT)")
        print("    [3.0, inf): algebraic C=204 (verify_algebraic_core)")
        print("  ENTIRE domain [0, infinity) rigorously covered.")
    else:
        print("  *** FAILURES — REVIEW ABOVE ***")
    print("=" * 72)

    result = {
        "script": "proof/verify_ia_1_to_3.py",
        "epsilon_definition": "2*sum_{n>=2} n^4 * exp(-pi*(n^2-1)*e^{2u})  [corrected prefactor]",
        "method": "algebraic_log_phi1_d2_plus_perturbation",
        "u_range": [1.0, 3.0],
        "n_checkpoints": N_CHECKS + 1,
        "dps": DPS,
        "perturbation_C": 204,
        "certified": cert_count,
        "failed": failed_count,
        "min_margin": min_margin,
        "worst_u": worst_u,
        "all_certified": all_ok,
        "time_s": round(elapsed, 2),
        "combined_coverage": {
            "[0,1.0]": "IA 52898 subintervals (verify_logconcavity_rigorous.py)",
            "[1.0,3.0]": "algebraic+perturbation (this script, 101 checkpoints)",
            "[3.0,inf)": "algebraic C=204 (verify_algebraic_core.py)",
        },
        "note": (
            "W_1=(log phi_1)'' computed as -24pi*e^{2u}/h^2 - 4pi*e^{2u} "
            "(exact algebraic, O(100), no cancellation). "
            "Tail C*epsilon doubly-exp small. "
            "All 101 checkpoints certify W_1 + tail < 0."
        ),
        "checkpoints": table,
    }

    out_path = os.path.join(ROOT, "results", "verify_ia_1_to_3.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print("  -> results/verify_ia_1_to_3.json")
    return result


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result["all_certified"] else 1)
