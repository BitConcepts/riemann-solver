"""
search_counterexamples.py
Master counterexample search for H13.

Runs a pipeline for each candidate kernel:
1. Check all H13 hypotheses (H1-H6) via check_log_concavity.py logic.
2. Scan real axis for sign changes (real zeros location).
3. Scan complex strip for near-zeros (COMPUTATION class only).
4. Save result to experiments/outputs/ as JSON.

This script is the primary entry point for the falsification-first approach to H13.

Usage:
    python search_counterexamples.py                  # all kernels
    python search_counterexamples.py --kernel exp_t4  # single kernel
    python search_counterexamples.py --deep           # deeper complex scan

Outputs: JSON files in ../../outputs/counterexample_search_<kernel>_<timestamp>.json
"""

import json
import sys
import argparse
import datetime
from pathlib import Path

try:
    from mpmath import mp, mpf, mpc, quad, cos, exp, log, diff, re, im, fabs
    mp.dps = 55
except ImportError:
    print("ERROR: mpmath is required. Run: pip install mpmath", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Import sub-scripts (as modules)
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from check_log_concavity import (
    KERNELS as LC_KERNELS,
    check_all_hypotheses,
)
from compute_fourier_zeros import (
    KERNELS as FZ_KERNELS,
    scan_real_axis,
    scan_complex_strip,
)


# ---------------------------------------------------------------------------
# Result format (per AGENTS.md spec)
# ---------------------------------------------------------------------------

def make_result(kernel_name, kernel_desc, hypotheses, fourier_test, status, notes):
    return {
        "kernel": kernel_desc,
        "parameters": {"name": kernel_name},
        "hypotheses_checked": {
            "even": hypotheses.get("H1_even", True),
            "positive": hypotheses.get("H2_positive", True),
            "integrable": hypotheses.get("H3_integrable", True),
            "analytic_origin": hypotheses.get("H4_analytic", False),
            "superexponential_decay": hypotheses.get("H5_superexp_decay", True),
            "log_concave_halfline": hypotheses.get("H6_log_concave", False),
        },
        "fourier_zero_test": fourier_test,
        "status": status,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Main search loop
# ---------------------------------------------------------------------------

def search_kernel(name, deep=False):
    """Run the full H13 falsification pipeline for one kernel."""
    if name not in LC_KERNELS:
        print(f"  ERROR: {name} not in KERNELS", file=sys.stderr)
        return None

    K_lc, analytic, desc = LC_KERNELS[name]
    K_fz, _ = FZ_KERNELS[name]

    print(f"\n{'='*60}")
    print(f"Kernel: {desc}")
    print('='*60)

    # Step 1: Check hypotheses
    print("  Step 1: Checking hypotheses H1-H6...")
    hyp = check_all_hypotheses(K_lc, label=desc, analytic=analytic)
    for k, v in hyp.items():
        if k.startswith("H"):
            status_str = "✓" if v else "✗"
            print(f"    {k}: {status_str} ({v})")

    all_hyp_ok = hyp["all_hypotheses_satisfied"]
    if not all_hyp_ok:
        print(f"  → One or more hypotheses FAILED. Classifying as INVALID CANDIDATE.")
        fourier_test = {"box": "skipped", "complex_zeros_found": 0}
        return make_result(name, desc, hyp, fourier_test,
                           "invalid candidate",
                           f"H4={hyp['H4_analytic']}, H6={hyp['H6_log_concave']} — "
                           f"kernel fails H13 hypotheses")

    # Step 2: Scan real axis
    print("  Step 2: Scanning real axis [0, 20] for Fourier zeros...")
    real_scan = scan_real_axis(K_fz, desc, xi_min=0, xi_max=20, n_points=100)
    n_real = real_scan["real_zeros_found"]
    print(f"    Real zeros found: {n_real}")

    # Step 3: Complex scan
    xi_re_max = 20 if not deep else 40
    xi_im_max = 5 if not deep else 10
    n_re = 20 if not deep else 40
    n_im = 10 if not deep else 20

    print(f"  Step 3: Complex strip scan (Re ∈ [0,{xi_re_max}], Im ∈ [1e-4, {xi_im_max}])...")
    complex_scan = scan_complex_strip(K_fz, desc,
                                     xi_re_max=xi_re_max, xi_im_max=xi_im_max,
                                     n_re=n_re, n_im=n_im)

    n_complex = len(complex_scan.get("counterexample_candidates", []))
    fourier_test = {
        "real_axis": {"zeros_found": n_real, "scan_range": [0, 20]},
        "complex_strip": {
            "box": f"Re ∈ [0,{xi_re_max}], Im ∈ [1e-4,{xi_im_max}]",
            "complex_zeros_found": n_complex,
            "candidates": complex_scan.get("counterexample_candidates", []),
        },
    }

    if n_complex > 0:
        status = "counterexample candidate"
        notes = (f"Found {n_complex} near-zero(s) in complex strip. "
                 f"REQUIRES argument_principle_box.py for rigorous confirmation. "
                 f"NOT a disproof of H13 until confirmed.")
        print(f"  *** {n_complex} CANDIDATE(S) FOUND — NOT YET A DISPROOF ***")
    else:
        status = "no counterexample"
        notes = (f"No complex zeros found in scanned region. "
                 f"Does NOT prove H13; only rules out zeros in the tested box.")
        print(f"  → No counterexample found in scanned region.")

    return make_result(name, desc, hyp, fourier_test, status, notes)


def main():
    parser = argparse.ArgumentParser(description="Master H13 counterexample search")
    parser.add_argument("--kernel", default="all")
    parser.add_argument("--deep", action="store_true", help="Larger complex scan grid")
    parser.add_argument("--output_dir", default=None,
                        help="Directory for output JSON (default: ../../outputs/)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else \
                 SCRIPT_DIR.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    kernels_to_run = list(LC_KERNELS.keys()) if args.kernel == "all" else [args.kernel]

    print(f"H13 Counterexample Search")
    print(f"Kernels: {kernels_to_run}")
    print(f"Deep scan: {args.deep}")
    print(f"Precision: {mp.dps} decimal digits")

    all_results = []
    for name in kernels_to_run:
        result = search_kernel(name, deep=args.deep)
        if result:
            all_results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for r in all_results:
        print(f"  {r['kernel'][:40]:40s} → {r['status']}")

    # Save output
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    kernel_tag = args.kernel.replace(" ", "_")
    output_file = output_dir / f"counterexample_search_{kernel_tag}_{timestamp}.json"

    output = {
        "script": "search_counterexamples.py",
        "timestamp": timestamp,
        "mp_dps": mp.dps,
        "deep": args.deep,
        "claim_discipline": (
            "COMPUTATION class only. Status 'no counterexample' does NOT prove H13. "
            "Status 'counterexample candidate' requires argument_principle_box.py confirmation "
            "AND verification of all H1-H6 hypotheses before ANY disproof claim."
        ),
        "results": all_results,
    }

    output_file.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to: {output_file}")

    # Alarm if any counterexample candidate found
    candidates = [r for r in all_results if r["status"] == "counterexample candidate"]
    if candidates:
        print("\n*** COUNTEREXAMPLE CANDIDATES FOUND — RUN argument_principle_box.py ***")
        for c in candidates:
            print(f"  {c['kernel']}")
    else:
        print("\nNo counterexample candidates found. H13 holds on all tested kernels.")

    return output


if __name__ == "__main__":
    main()
