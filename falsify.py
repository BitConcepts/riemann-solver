# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Run the falsification suite against the RH proof.

This script runs:
  1. All 32 falsification attacks (6 script batches)
  2. External claims verification audit

Each attack tries to BREAK the proof. Passing means the proof survived.

Usage:
    python falsify.py            # Full suite + external audit
    python falsify.py --quick    # External audit only (skip 32 attacks)
    python falsify.py --attacks  # 32 attacks only (skip external audit)
"""
import argparse
import subprocess
import sys
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
FALSIFICATION_DIR = os.path.join(ROOT, "falsification")
RESULTS_DIR = os.path.join(ROOT, "results")


def run_attacks():
    """Run all 32 falsification attacks via run_all.py."""
    script = os.path.join(FALSIFICATION_DIR, "run_all.py")
    print("[1] Running 32 falsification attacks...")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=600, cwd=ROOT,
    )
    output = result.stdout + result.stderr

    # Parse results
    n_passed = output.count("PASSED")
    n_issues = output.count("ISSUES")

    # Print summary lines
    for line in output.strip().split("\n"):
        if "RESULTS:" in line or "PASSED" in line or "ISSUES" in line:
            print("  " + line.strip())

    return n_issues == 0


def run_audit(quick=True):
    """Run external claims verification audit."""
    script = os.path.join(FALSIFICATION_DIR, "audit_external.py")
    args = [sys.executable, script]
    if quick:
        args.append("--quick")

    print("\n[2] Running external claims audit%s..." % (" (quick)" if quick else ""))
    result = subprocess.run(
        args, capture_output=True, text=True, timeout=600, cwd=ROOT,
    )

    # Print audit output
    for line in result.stdout.strip().split("\n"):
        print("  " + line)

    # Check self-audit
    audit_path = os.path.join(RESULTS_DIR, "audit_external.json")
    if os.path.exists(audit_path):
        with open(audit_path) as f:
            data = json.load(f)
        self_audit = next((d for d in data if d["claim_id"] == "self"), None)
        if self_audit and self_audit["n_failed"] > 0:
            return False
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run falsification suite")
    parser.add_argument("--quick", action="store_true",
                        help="Run external audit only (skip 32 attacks)")
    parser.add_argument("--attacks", action="store_true",
                        help="Run 32 attacks only (skip external audit)")
    args = parser.parse_args()

    print("=" * 72)
    print("  RH PROOF FALSIFICATION SUITE")
    print("=" * 72)

    attacks_ok = True
    audit_ok = True

    if not args.quick:
        attacks_ok = run_attacks()

    if not args.attacks:
        audit_ok = run_audit(quick=True)

    print("\n" + "=" * 72)
    if not args.quick:
        print("  32 attacks: %s" % ("PASSED" if attacks_ok else "ISSUES FOUND"))
    if not args.attacks:
        print("  Self-audit: %s" % ("PASSED" if audit_ok else "FAILED"))
    print("=" * 72)

    sys.exit(0 if (attacks_ok and audit_ok) else 1)


if __name__ == "__main__":
    main()
