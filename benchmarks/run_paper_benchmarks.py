# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Run numerical benchmarks for external RH proof papers.

Reads papers/registry.json to discover which papers have benchmark scripts,
then runs each in turn and prints a summary.

Usage:
    python benchmarks/run_paper_benchmarks.py                  # all papers with benchmarks
    python benchmarks/run_paper_benchmarks.py --paper louiz-2026  # single paper
    python benchmarks/run_paper_benchmarks.py --list           # list available papers
    python benchmarks/run_paper_benchmarks.py --lessons        # print all lessons learned

Adding a new paper:
    1. Add an entry to papers/registry.json with a "benchmark_script" path.
    2. Create that script; it must accept no arguments and exit 0 on completion.
    3. The script should save JSON results to results/bench_<id>.json.
    4. Optionally add an audit_<id>() function to falsification/audit_external.py.
    5. Run this script to verify integration.

AGENTS.md: Benchmarks produce NUMERICAL EVIDENCE only.
No result here proves or disproves RH.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "papers", "registry.json")


def load_registry() -> list[dict]:
    with open(REGISTRY) as f:
        return json.load(f)


def papers_with_benchmarks(registry: list[dict]) -> list[dict]:
    return [p for p in registry if p.get("benchmark_script")]


def run_benchmark(paper: dict, verbose: bool = True) -> dict:
    """Run the benchmark script for one paper. Returns a result dict."""
    script = os.path.join(ROOT, paper["benchmark_script"])
    pid    = paper["id"]

    if not os.path.exists(script):
        return {"paper_id": pid, "status": "MISSING", "script": script, "elapsed_s": 0}

    if verbose:
        print(f"\n{'=' * 72}")
        print(f"  Paper: {pid}")
        print(f"  {paper['title'][:65]}")
        print(f"  {paper['source'][:65]}")
        print(f"{'=' * 72}")

    # Force UTF-8 for subprocess stdout/stderr (needed on Windows with cp1252)
    import os as _os
    _env = _os.environ.copy()
    _env["PYTHONIOENCODING"] = "utf-8"
    _env["PYTHONUTF8"] = "1"

    t0 = time.time()
    result = subprocess.run(
        [sys.executable, script],
        capture_output=not verbose,
        text=True,
        timeout=300,
        cwd=ROOT,
        env=_env,
    )
    elapsed = time.time() - t0

    if result.returncode == 0:
        status = "OK"
    else:
        status = f"FAILED (exit {result.returncode})"
        if not verbose and result.stderr:
            print(f"  STDERR: {result.stderr[-300:]}")

    return {
        "paper_id": pid,
        "title":    paper["title"],
        "status":   status,
        "elapsed_s": round(elapsed, 2),
        "script":   paper["benchmark_script"],
    }


def print_lessons(registry: list[dict]) -> None:
    """Print all lessons learned across all papers."""
    print("=" * 72)
    print("  LESSONS LEARNED ACROSS ALL BENCHMARKED PAPERS")
    print("=" * 72)
    for paper in registry:
        lessons = paper.get("lessons", [])
        if not lessons:
            continue
        tier = paper.get("tier", "?")
        print(f"\n[Tier {tier}] {paper['id']} — {paper['author']} ({paper['year']})")
        for i, lesson in enumerate(lessons, 1):
            # Word-wrap at 68 chars
            words = lesson.split()
            line  = f"  {i}. "
            for w in words:
                if len(line) + len(w) + 1 > 72:
                    print(line)
                    line = "     " + w
                else:
                    line = line + " " + w if len(line) > 5 else line + w
            print(line)
    print()


def print_summary(results: list[dict], registry: list[dict]) -> None:
    """Print overall summary table."""
    print("\n" + "=" * 72)
    print("  PAPER BENCHMARK SUMMARY")
    print("=" * 72)
    print(f"  {'Paper ID':<22}  {'Status':<12}  {'Time':>6}  Script")
    print("  " + "-" * 65)
    for r in results:
        print(f"  {r['paper_id']:<22}  {r['status']:<12}  {r['elapsed_s']:>5.1f}s  {r['script']}")

    ok  = sum(1 for r in results if r["status"] == "OK")
    bad = len(results) - ok
    print(f"\n  {ok}/{len(results)} benchmarks completed successfully.")
    if bad:
        print(f"  {bad} failed — check output above.")
    print("=" * 72)

    # Print accumulated critical gaps
    ids_run = {r["paper_id"] for r in results}
    gaps_by_paper = {p["id"]: p.get("critical_gaps", []) for p in registry if p["id"] in ids_run}
    if any(gaps_by_paper.values()):
        print("\n  Critical gaps found in benchmarked papers:")
        for pid, gaps in gaps_by_paper.items():
            for g in gaps[:2]:   # show first 2 per paper
                print(f"    [{pid}] {g[:68]}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RH paper benchmarks")
    parser.add_argument("--paper", type=str, default=None,
                        help="Run benchmark for a specific paper ID")
    parser.add_argument("--list",    action="store_true", help="List papers with benchmarks")
    parser.add_argument("--lessons", action="store_true", help="Print all lessons learned")
    parser.add_argument("--quiet",   action="store_true", help="Suppress benchmark output")
    args = parser.parse_args()

    registry = load_registry()

    if args.lessons:
        print_lessons(registry)
        return

    if args.list:
        print("Papers with benchmark scripts:")
        for p in papers_with_benchmarks(registry):
            print(f"  {p['id']:<22}  Tier {p['tier']}  {p['benchmark_script']}")
        papers_no_bench = [p for p in registry if not p.get("benchmark_script") and p["id"] != "this-work"]
        if papers_no_bench:
            print("\nPapers without benchmarks yet (add benchmark_script to registry.json):")
            for p in papers_no_bench:
                print(f"  {p['id']:<22}  Tier {p['tier']}  {p['approach'][:45]}")
        return

    # Select papers to run
    if args.paper:
        targets = [p for p in registry if p["id"] == args.paper]
        if not targets:
            print(f"Error: paper '{args.paper}' not in registry. Run --list to see options.")
            sys.exit(1)
        targets = [p for p in targets if p.get("benchmark_script")]
        if not targets:
            print(f"Paper '{args.paper}' has no benchmark_script. Add one to papers/registry.json.")
            sys.exit(1)
    else:
        targets = papers_with_benchmarks(registry)

    if not targets:
        print("No papers with benchmark scripts found. Add benchmark_script entries to papers/registry.json.")
        sys.exit(0)

    print("=" * 72)
    print(f"  RH PAPER BENCHMARKS — {len(targets)} paper(s)")
    print("=" * 72)

    results = []
    for paper in targets:
        res = run_benchmark(paper, verbose=not args.quiet)
        results.append(res)

    print_summary(results, registry)

    all_ok = all(r["status"] == "OK" for r in results)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
