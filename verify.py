# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Run the complete proof verification pipeline.

This script executes the five verification steps of the RH proof:
  1. Rigorous IA: Q_Phi < 0 on [0, 1.0] (52,898 subintervals, 60-digit)
  2. Algebraic core + perturbation bound (C=204) for u > 1.5
  3. Truncation error certification + cross-validation
  4. Polya/de Bruijn condition check
  5. Extended cert: (log Phi)'' < 0 on [1.0, 1.5] (algebraic, 51 checkpoints)

Usage:
    python verify.py           # Full pipeline (~70s)
    python verify.py --quick   # Skip the slow IA step, run steps 2-5 only (~2s)
"""
import argparse
import subprocess
import sys
import os
import json

PROOF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proof")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

STEPS = [
    ("verify_logconcavity_rigorous.py", "Rigorous IA: 52,898 subintervals on [0, 1.0]"),
    ("verify_algebraic_core.py",        "Algebraic core + perturbation bound (C=204)"),
    ("verify_truncation_and_crosscheck.py", "Truncation error + cross-validation"),
    ("verify_debruijn_condition.py",    "Polya/de Bruijn condition check"),
    ("verify_ia_1_to_1_5.py",           "Extended cert: (log Phi)'' < 0 on [1.0, 1.5] (51 algebraic checkpoints)"),
]


def run_step(script, desc, quiet=False):
    path = os.path.join(PROOF_DIR, script)
    if not os.path.exists(path):
        print("  SKIP: %s not found" % script)
        return False

    result = subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True, timeout=600,
        cwd=os.path.dirname(PROOF_DIR),
    )

    if result.returncode != 0:
        print("  FAIL (exit code %d)" % result.returncode)
        if result.stderr:
            print(result.stderr[-500:])
        return False

    if not quiet:
        # Print last few meaningful lines
        lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
        for line in lines[-6:]:
            print("  " + line)

    return True


def main():
    parser = argparse.ArgumentParser(description="Run RH proof verification pipeline")
    parser.add_argument("--quick", action="store_true",
                        help="Skip the slow rigorous IA step (~70s)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress step output")
    args = parser.parse_args()

    steps = STEPS[1:] if args.quick else STEPS

    print("=" * 72)
    print("  RH PROOF VERIFICATION PIPELINE")
    print("  %d steps%s" % (len(steps), " (quick mode — skipping IA)" if args.quick else ""))
    print("=" * 72)

    passed = 0
    for i, (script, desc) in enumerate(steps, 1):
        print("\n[%d/%d] %s" % (i, len(steps), desc))
        if run_step(script, desc, quiet=args.quiet):
            passed += 1

    # Check cross-validation result
    xv_path = os.path.join(RESULTS_DIR, "truncation_crosscheck.json")
    xv_ok = False
    if os.path.exists(xv_path):
        with open(xv_path) as f:
            xv = json.load(f)
        xv_ok = xv.get("cross_validation_passed", False)

    print("\n" + "=" * 72)
    print("  RESULTS: %d/%d steps passed" % (passed, len(steps)))
    print("  Cross-validation: %s" % ("PASSED" if xv_ok else "NOT RUN or FAILED"))

    if not args.quick:
        ia_path = os.path.join(RESULTS_DIR, "verify_logconcavity_rigorous.json")
        if os.path.exists(ia_path):
            with open(ia_path) as f:
                ia = json.load(f)
            print("  IA certified: %d/%d subintervals" % (ia["certified"], ia["n_subintervals"]))

    print("=" * 72)
    sys.exit(0 if passed == len(steps) else 1)


if __name__ == "__main__":
    main()
