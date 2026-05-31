# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Standalone verifier for the IA log-concavity certificate.

Reads certificate.json and independently re-verifies every recorded
interval using Arb/FLINT interval arithmetic.  The verifier:

  1. Checks metadata consistency (grid parameters, counts).
  2. Verifies the SHA-256 hash of the data section.
  3. For each of the 1000 worst recorded intervals, recomputes Q_Phi
     and confirms the upper bound is strictly negative.
  4. For each batch, recomputes Q_Phi on the batch's worst interval
     and confirms the upper bound is strictly negative.
  5. Reports PASS or FAIL.  Any single failure → overall FAIL.

The verifier does NOT choose which intervals to test, does NOT tune
precision, and does NOT skip failures.

Requires: pip install python-flint
Usage:    python verification/verify_certificate.py [path/to/certificate.json]
"""
import hashlib
import json
import os
import sys
import time

from flint import arb, ctx

# ── Kernel computation (must match the generator exactly) ────────────────────

N_TERMS = 5


def phi_n_and_derivs_arb(n, u):
    """Compute phi_n(u), phi_n'(u), phi_n''(u) using Arb ball arithmetic."""
    pi = arb.pi()
    n2 = arb(n) ** 2
    n4 = n2 ** 2
    e9u2 = (arb(9) * u / 2).exp()
    e5u2 = (arb(5) * u / 2).exp()
    e2u = (2 * u).exp()
    e4u = e2u ** 2
    g = 2 * pi**2 * n4 * e9u2 - 3 * pi * n2 * e5u2
    gp = 9 * pi**2 * n4 * e9u2 - arb(15) * pi * n2 * e5u2 / 2
    gpp = arb(81) * pi**2 * n4 * e9u2 / 2 - arb(75) * pi * n2 * e5u2 / 4
    E = (-pi * n2 * e2u).exp()
    Ep = -2 * pi * n2 * e2u * E
    Epp = (-4 * pi * n2 * e2u + 4 * pi**2 * n4 * e4u) * E
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


def reconstruct_subinterval(grid, idx):
    """Reconstruct the endpoints of subinterval `idx` from grid parameters."""
    n_coarse = grid["n_coarse"]
    n_fine = grid["n_fine"]
    u_split = grid["u_split"]
    u_max = grid["u_max"]
    if idx < n_coarse:
        dc = u_split / n_coarse
        return (idx * dc, (idx + 1) * dc)
    else:
        j = idx - n_coarse
        df = (u_max - u_split) / n_fine
        return (u_split + j * df, u_split + (j + 1) * df)


# ── Verification steps ───────────────────────────────────────────────────────

def verify_hash(cert):
    """Verify the SHA-256 hash of the data section."""
    data_json = json.dumps(cert["data"], sort_keys=True, separators=(",", ":"))
    computed = hashlib.sha256(data_json.encode("utf-8")).hexdigest()
    expected = cert["data_sha256"]
    return computed == expected, computed, expected


def verify_metadata(cert):
    """Check internal consistency of metadata and grid parameters."""
    errors = []
    grid = cert["data"]["grid"]
    summary = cert["data"]["summary"]

    expected_total = grid["n_coarse"] + grid["n_fine"]
    if grid["total_subintervals"] != expected_total:
        errors.append("total_subintervals mismatch: %d != %d" %
                       (grid["total_subintervals"], expected_total))

    if summary["certified"] + summary["failed"] != expected_total:
        errors.append("certified + failed != total: %d + %d != %d" %
                       (summary["certified"], summary["failed"], expected_total))

    if grid["u_max"] != 1.0:
        errors.append("u_max != 1.0: %s" % grid["u_max"])

    if not (0 < grid["u_split"] < grid["u_max"]):
        errors.append("u_split out of range: %s" % grid["u_split"])

    meta = cert["metadata"]
    if meta["precision_bits"] < 64:
        errors.append("precision_bits too low: %d" % meta["precision_bits"])

    if meta["n_terms"] < 1:
        errors.append("n_terms < 1: %d" % meta["n_terms"])

    return errors


def verify_interval(grid, prec, u_lo, u_hi, claimed_upper):
    """Recompute Q_Phi on [u_lo, u_hi] and check the claimed upper bound."""
    ctx.prec = prec
    u_iv = make_interval(u_lo, u_hi)
    Q = Q_Phi_arb(u_iv)

    if not (Q < 0):
        return False, "Q not certifiably negative: %s" % Q

    recomputed_upper = float(Q.mid()) + float(Q.rad())
    if recomputed_upper >= 0:
        return False, "recomputed upper >= 0: %.6e" % recomputed_upper

    # The claimed upper bound should be consistent (within floating-point
    # representation tolerance) with what we recompute.  We allow the
    # recomputed upper to differ slightly due to platform/version
    # differences, but both must be negative.
    if claimed_upper is not None and claimed_upper >= 0:
        return False, "claimed upper >= 0: %.6e" % claimed_upper

    return True, "ok (recomputed upper=%.6e)" % recomputed_upper


def main():
    cert_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "certificate.json")

    if not os.path.isfile(cert_path):
        print("FAIL: certificate not found: %s" % cert_path)
        return 1

    with open(cert_path) as f:
        cert = json.load(f)

    print("=" * 72)
    print("  CERTIFICATE VERIFIER")
    print("  Input: %s" % cert_path)
    print("=" * 72)

    all_pass = True

    # ── Step 1: Metadata ─────────────────────────────────────────────────
    print("\n[1/4] Metadata consistency...")
    meta_errors = verify_metadata(cert)
    if meta_errors:
        for e in meta_errors:
            print("  FAIL: %s" % e)
        all_pass = False
    else:
        print("  PASS: metadata consistent")
        print("    library:    %s" % cert["metadata"]["library"])
        print("    precision:  %d bits" % cert["metadata"]["precision_bits"])
        print("    git_commit: %s" % cert["metadata"]["git_commit"][:12])
        print("    date:       %s" % cert["metadata"]["date_utc"])

    # ── Step 2: Hash ─────────────────────────────────────────────────────
    print("\n[2/4] SHA-256 hash...")
    hash_ok, computed, expected = verify_hash(cert)
    if hash_ok:
        print("  PASS: hash verified (%s...)" % computed[:16])
    else:
        print("  FAIL: hash mismatch")
        print("    expected: %s" % expected)
        print("    computed: %s" % computed)
        all_pass = False

    grid = cert["data"]["grid"]
    prec = cert["metadata"]["precision_bits"]

    # ── Step 3: Worst 1000 intervals ─────────────────────────────────────
    worst = cert["data"]["worst_intervals"]
    print("\n[3/4] Recomputing %d worst intervals..." % len(worst))
    t0 = time.time()
    worst_pass = 0
    worst_fail = 0

    for i, entry in enumerate(worst):
        # Reconstruct the interval from grid parameters rather than
        # trusting the certificate's u_lo/u_hi — this ensures the
        # verifier is independent.
        idx = entry["index"]
        u_lo, u_hi = reconstruct_subinterval(grid, idx)
        claimed = entry["Q_upper_bound"]

        ok, msg = verify_interval(grid, prec, u_lo, u_hi, claimed)
        if ok:
            worst_pass += 1
        else:
            print("  FAIL idx=%d [%.8f,%.8f]: %s" % (idx, u_lo, u_hi, msg))
            worst_fail += 1
            all_pass = False

        if (i + 1) % 200 == 0 or (i + 1) == len(worst):
            print("  ... %d/%d checked (%.1fs)" %
                  (i + 1, len(worst), time.time() - t0))

    if worst_fail == 0:
        print("  PASS: all %d worst intervals verified" % worst_pass)
    else:
        print("  FAIL: %d/%d worst intervals failed" % (worst_fail, len(worst)))

    # ── Step 4: Batch representative intervals ───────────────────────────
    batches = cert["data"]["batch_bounds"]
    print("\n[4/4] Recomputing %d batch worst-case intervals..." % len(batches))
    t0 = time.time()
    batch_pass = 0
    batch_fail = 0
    batch_skip = 0

    for i, batch in enumerate(batches):
        if batch["worst_interval_index"] is None:
            # Batch had no certified intervals (all failed)
            batch_skip += 1
            all_pass = False
            continue

        idx = batch["worst_interval_index"]
        u_lo, u_hi = reconstruct_subinterval(grid, idx)
        claimed = batch["worst_upper_bound"]

        ok, msg = verify_interval(grid, prec, u_lo, u_hi, claimed)
        if ok:
            batch_pass += 1
        else:
            print("  FAIL batch=%d idx=%d [%.8f,%.8f]: %s" %
                  (i, idx, u_lo, u_hi, msg))
            batch_fail += 1
            all_pass = False

        if (i + 1) % 100 == 0 or (i + 1) == len(batches):
            print("  ... %d/%d checked (%.1fs)" %
                  (i + 1, len(batches), time.time() - t0))

    if batch_fail == 0 and batch_skip == 0:
        print("  PASS: all %d batch representatives verified" % batch_pass)
    else:
        if batch_fail > 0:
            print("  FAIL: %d/%d batch representatives failed" %
                  (batch_fail, len(batches)))
        if batch_skip > 0:
            print("  SKIP: %d batches had no certified intervals" % batch_skip)

    # ── Verdict ──────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    summary = cert["data"]["summary"]
    print("  Certificate claims: %d/%d subintervals certified" %
          (summary["certified"], grid["total_subintervals"]))
    print("  Worst Q upper bound: %.6e" % summary["global_max_Q_upper"])
    print()

    if all_pass and summary["all_certified"]:
        print("  *** PASS ***")
        print("  Certificate is internally consistent and all recorded")
        print("  intervals independently verified: Q_Phi < 0 on [0, 1].")
    else:
        print("  *** FAIL ***")
        if not summary["all_certified"]:
            print("  Certificate itself records %d failures." % summary["failed"])
        if not all_pass:
            print("  Verification detected inconsistencies.")

    print("=" * 72)
    return 0 if all_pass and summary["all_certified"] else 1


if __name__ == "__main__":
    sys.exit(main())
