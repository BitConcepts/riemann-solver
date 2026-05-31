# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Generate a machine-checkable IA certificate for the log-concavity verification.

Runs the full Arb/FLINT interval-arithmetic computation of Q_Phi on [0,1]
and produces certificate.json with:
  - metadata (library, precision, date, git commit)
  - grid parameters (sufficient to reconstruct every subinterval)
  - per-batch (100 intervals) worst-case upper bound on Q_Phi
  - the 1000 intervals with highest (closest to zero) Q upper bound
  - SHA-256 hash of the data section for integrity

Requires: pip install python-flint
Usage:   python verification/generate_certificate.py
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

from flint import arb, ctx

# ── Grid parameters (must match proof/verify_logconcavity_arb.py exactly) ────
N_TERMS = 5
U_MAX = 1.0
U_SPLIT = 0.946
N_COARSE = 1892
N_FINE = 54000
PREC = 200          # bits
BATCH_SIZE = 100    # intervals per batch summary

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)


# ── Kernel Q_Phi computation (identical to proof/verify_logconcavity_arb.py) ─
def phi_n_and_derivs_arb(n, u):
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
    mid = (lo + hi) / 2
    rad = (hi - lo) / 2
    return arb("[%s +/- %s]" % (mid, rad + 1e-20))


def git_commit_hash():
    try:
        result = subprocess.run(
            ["git", "-C", ROOT_DIR, "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def build_subintervals():
    subs = []
    dc = U_SPLIT / N_COARSE
    for i in range(N_COARSE):
        subs.append((i * dc, (i + 1) * dc))
    df = (U_MAX - U_SPLIT) / N_FINE
    for i in range(N_FINE):
        subs.append((U_SPLIT + i * df, U_SPLIT + (i + 1) * df))
    return subs


def main():
    ctx.prec = PREC
    subintervals = build_subintervals()
    n_total = len(subintervals)
    assert n_total == N_COARSE + N_FINE

    print("=" * 72)
    print("  CERTIFICATE GENERATOR — Arb/FLINT IA Verification")
    print("  %d subintervals, %d-bit precision" % (n_total, PREC))
    print("=" * 72)

    # ── Run full verification, collecting per-interval upper bounds ───────
    interval_uppers = []       # (index, u_lo, u_hi, upper_bound)
    certified = 0
    failed = 0
    t0 = time.time()

    for idx, (u_lo, u_hi) in enumerate(subintervals):
        try:
            u_iv = make_interval(u_lo, u_hi)
            Q = Q_Phi_arb(u_iv)
            if Q < 0:
                certified += 1
                mid = float(Q.mid())
                rad = float(Q.rad())
                upper = mid + rad
                interval_uppers.append((idx, u_lo, u_hi, upper))
            else:
                print("  FAIL idx=%d [%.8f, %.8f]: Q = %s" % (idx, u_lo, u_hi, Q))
                failed += 1
                interval_uppers.append((idx, u_lo, u_hi, None))
        except Exception as e:
            print("  ERROR idx=%d: %s" % (idx, e))
            failed += 1
            interval_uppers.append((idx, u_lo, u_hi, None))

        if (idx + 1) % 5000 == 0 or (idx + 1) == n_total:
            elapsed = time.time() - t0
            print("  ... %d/%d (%.0fs, %d ok, %d fail)" %
                  (idx + 1, n_total, elapsed, certified, failed))

    elapsed = time.time() - t0
    print("\n  Done: %d/%d certified in %.1fs" % (certified, n_total, elapsed))

    if failed > 0:
        print("  *** %d FAILURES — certificate will record them ***" % failed)

    # ── Build per-batch summaries ────────────────────────────────────────
    n_batches = (n_total + BATCH_SIZE - 1) // BATCH_SIZE
    batch_bounds = []
    for b in range(n_batches):
        start = b * BATCH_SIZE
        end = min(start + BATCH_SIZE, n_total)
        batch_entries = interval_uppers[start:end]
        valid = [e for e in batch_entries if e[3] is not None]
        fails = [e for e in batch_entries if e[3] is None]
        if valid:
            worst = max(valid, key=lambda e: e[3])
            batch_bounds.append({
                "batch_index": b,
                "interval_range": [start, end - 1],
                "u_range": [batch_entries[0][1], batch_entries[-1][2]],
                "n_intervals": end - start,
                "n_certified": len(valid),
                "n_failed": len(fails),
                "worst_upper_bound": worst[3],
                "worst_interval_index": worst[0],
                "worst_interval": [worst[1], worst[2]],
            })
        else:
            batch_bounds.append({
                "batch_index": b,
                "interval_range": [start, end - 1],
                "u_range": [batch_entries[0][1], batch_entries[-1][2]],
                "n_intervals": end - start,
                "n_certified": 0,
                "n_failed": len(fails),
                "worst_upper_bound": None,
                "worst_interval_index": None,
                "worst_interval": None,
            })

    # ── Collect 1000 worst intervals ─────────────────────────────────────
    valid_uppers = [e for e in interval_uppers if e[3] is not None]
    valid_uppers.sort(key=lambda e: e[3], reverse=True)   # highest (closest to 0) first
    worst_1000 = []
    for idx, u_lo, u_hi, upper in valid_uppers[:1000]:
        worst_1000.append({
            "index": idx,
            "u_lo": u_lo,
            "u_hi": u_hi,
            "Q_upper_bound": upper,
        })

    # ── Global stats ─────────────────────────────────────────────────────
    all_uppers = [e[3] for e in interval_uppers if e[3] is not None]
    global_max_upper = max(all_uppers) if all_uppers else None
    global_min_upper = min(all_uppers) if all_uppers else None
    global_mean_upper = sum(all_uppers) / len(all_uppers) if all_uppers else None

    # ── Assemble certificate ─────────────────────────────────────────────
    data_section = {
        "grid": {
            "u_max": U_MAX,
            "u_split": U_SPLIT,
            "n_coarse": N_COARSE,
            "n_fine": N_FINE,
            "total_subintervals": n_total,
            "coarse_delta": U_SPLIT / N_COARSE,
            "fine_delta": (U_MAX - U_SPLIT) / N_FINE,
        },
        "summary": {
            "certified": certified,
            "failed": failed,
            "all_certified": failed == 0,
            "global_max_Q_upper": global_max_upper,
            "global_min_Q_upper": global_min_upper,
            "global_mean_Q_upper": global_mean_upper,
        },
        "batch_bounds": batch_bounds,
        "worst_intervals": worst_1000,
    }

    # Compute hash of the data section
    data_json = json.dumps(data_section, sort_keys=True, separators=(",", ":"))
    data_hash = hashlib.sha256(data_json.encode("utf-8")).hexdigest()

    certificate = {
        "schema_version": "1.0.0",
        "description": "Machine-checkable IA certificate for Q_Phi < 0 on [0, 1]",
        "metadata": {
            "library": "python-flint (Arb/FLINT)",
            "library_version": "0.8.0",
            "precision_bits": PREC,
            "n_terms": N_TERMS,
            "kernel": "Phi(u) = 4 * sum_{n=1}^{N} phi_n(u)",
            "quantity_certified": "Q_Phi(u) = Phi''(u)*Phi(u) - (Phi'(u))^2 < 0",
            "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "git_commit": git_commit_hash(),
            "generator": "verification/generate_certificate.py",
            "computation_time_s": round(elapsed, 2),
        },
        "data": data_section,
        "data_sha256": data_hash,
    }

    out_path = os.path.join(SCRIPT_DIR, "certificate.json")
    with open(out_path, "w") as f:
        json.dump(certificate, f, indent=2)
    print("\n  -> %s  (%d bytes)" % (out_path, os.path.getsize(out_path)))
    print("  SHA-256: %s" % data_hash)

    if failed == 0:
        print("\n  *** CERTIFICATE COMPLETE: ALL %d SUBINTERVALS CERTIFIED ***" % n_total)
    else:
        print("\n  *** CERTIFICATE INCOMPLETE: %d FAILURES ***" % failed)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
