# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Run all 32 falsification attacks against the log-concavity proof of RH.

Usage:
    python falsification/run_all.py
"""
import subprocess
import sys
import os

SCRIPTS = [
    ("falsify_own_proof.py", "Attacks 1-5: kernel properties, decay, Polya counterexample"),
    ("falsify_advanced.py", "Attacks 6-10: convention, perturbation C, smoothness, circularity, IA"),
    ("falsify_structural.py", "Attacks 11-15: Polya citation, derivatives, L-functions, equivalence"),
    ("falsify_edge_cases.py", "Attacks 16-20: evenness, exp accuracy, IA tracking, Q formula, g'"),
    ("falsify_deep.py", "Attacks 21-26: E'', product rule, negative u, integral, scaling, IA enclosure"),
    ("falsify_final.py", "Attacks 27-32: Polya on exp(-cosh), convergence, E', 15/2, adversarial Q, gamma_2"),
]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    total_pass = 0
    results = []

    print("=" * 72)
    print("  RUNNING ALL 32 FALSIFICATION ATTACKS")
    print("=" * 72)

    for script, desc in SCRIPTS:
        path = os.path.join(script_dir, script)
        print("\n--- %s ---" % desc)
        print("    Running %s..." % script)

        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=600
        )

        output = result.stdout + result.stderr
        n_wrong = output.count("WRONG")

        if n_wrong > 0:
            print("    *** ISSUES FOUND ***")
            results.append((script, "ISSUES"))
        else:
            passed = output.count("ATTACK FAILED") + output.count("FAILED:")
            print("    %d checks passed" % passed)
            total_pass += 1
            results.append((script, "PASSED"))

    print("\n" + "=" * 72)
    print("  RESULTS: %d/%d script batches passed" % (total_pass, len(SCRIPTS)))
    for script, status in results:
        print("    %-30s %s" % (script, status))
    print("=" * 72)


if __name__ == "__main__":
    main()
