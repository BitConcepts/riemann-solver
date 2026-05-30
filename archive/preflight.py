# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Pre-flight check: verify all phases will work before unattended run.

Runs a quick smoke test of each phase with minimal parameters to catch
import errors, API mismatches, and resource issues BEFORE committing
to a multi-hour unattended run.

Usage:
    python preflight.py
"""

import sys
import time
import traceback

sys.path.insert(0, ".")

PASS = "✓"
FAIL = "✗"
results = []


def check(name, func):
    """Run a check, catch any error, record result."""
    try:
        t0 = time.time()
        func()
        elapsed = time.time() - t0
        results.append((name, True, f"{elapsed:.1f}s"))
        print(f"  {PASS} {name} ({elapsed:.1f}s)")
    except Exception as e:
        results.append((name, False, str(e)))
        print(f"  {FAIL} {name}: {e}")
        traceback.print_exc()


def check_imports():
    """Verify all required modules import."""
    import mpmath
    from riemann import zeta, xi, zeros, li_criterion, dbn_constant
    from riemann import weil_positivity, spectral, utils, resources
    from riemann import davenport_heilbronn, even_dominance
    from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros


def check_resources():
    """Verify resource config loads."""
    from riemann.resources import get_config, check_resources, print_summary
    cfg = get_config()
    assert cfg.max_workers >= 1
    assert cfg.total_ram_gb > 0
    assert check_resources("preflight")


def check_pytest():
    """Verify pytest can discover and would run tests."""
    import subprocess
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "tests/"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"pytest collect failed: {r.stderr}"
    lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
    # Last line should say "X tests collected"
    assert "collected" in r.stdout.lower(), f"No tests collected: {r.stdout}"


def check_cvs_quick():
    """Build a tiny CvS matrix (N=5) to verify the API works."""
    import mpmath as mp
    from connes_cvs import build_galerkin_matrix, compute_ground_state
    mp.mp.dps = 30
    Q = build_galerkin_matrix(c=7, N=5, T=50, dps=30)
    lam, _ = compute_ground_state(Q)
    assert lam != 0, "lambda_min is zero"


def check_dh_quick():
    """Quick DH function evaluation."""
    import mpmath as mp
    from riemann.davenport_heilbronn import davenport_heilbronn
    mp.mp.dps = 15
    val = davenport_heilbronn(mp.mpc(0.5, 5.0))
    assert val is not None


def check_even_dominance_quick():
    """Quick even-dominance check at one lambda."""
    from riemann.even_dominance import check_even_dominance
    cert = check_even_dominance(10.0, N=5, dps=15)
    assert cert is not None


def check_weekend_imports():
    """Verify run_weekend.py can be imported without side effects."""
    # This checks that run_weekend.py has proper __name__ guard
    import importlib.util
    spec = importlib.util.spec_from_file_location("run", "run.py")
    mod = importlib.util.module_from_spec(spec)
    # Should NOT execute main() on import — that's the __name__ guard
    spec.loader.exec_module(mod)
    assert hasattr(mod, "main")
    assert hasattr(mod, "phase_6_form_stabilization")
    assert hasattr(mod, "phase_7_eigenvalue_isolation")


def check_results_dir():
    """Verify results directory exists and is writable."""
    import os, json
    os.makedirs("results", exist_ok=True)
    test_path = "results/_preflight_test.json"
    with open(test_path, "w") as f:
        json.dump({"test": True}, f)
    os.remove(test_path)


if __name__ == "__main__":
    print("=" * 60)
    print("  PRE-FLIGHT CHECK")
    print("  Verifying all phases will work before unattended run")
    print("=" * 60)

    t0 = time.time()

    check("Module imports", check_imports)
    check("Resource config", check_resources)
    check("Pytest collection", check_pytest)
    check("CvS API (tiny N=5)", check_cvs_quick)
    check("DH function eval", check_dh_quick)
    check("Even dominance (tiny)", check_even_dominance_quick)
    check("Weekend runner imports", check_weekend_imports)
    check("Results dir writable", check_results_dir)

    elapsed = time.time() - t0
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)

    print(f"\n{'=' * 60}")
    print(f"  {passed}/{len(results)} checks passed, {failed} failed")
    print(f"  Total: {elapsed:.1f}s")

    if failed == 0:
        print(f"\n  ALL CLEAR — safe to run unattended:")
        print(f"    .work\\env\\Scripts\\python.exe run.py")
    else:
        print(f"\n  *** FIX FAILURES BEFORE RUNNING UNATTENDED ***")
        for name, ok, detail in results:
            if not ok:
                print(f"    {FAIL} {name}: {detail}")

    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)
