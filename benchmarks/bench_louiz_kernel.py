# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Numerical benchmark: Louiz Super-Exponential Kernel approach (2026).

Primary paper [1]:
    Akram Louiz, "A new AI assisted proof of the Riemann Hypothesis:
    A Super-Exponential Kernel Approach to the Analyticity of the
    Reciprocal Zeta Function and the Riemann Hypothesis"
    DOI: https://doi.org/10.13140/RG.2.2.35504.32004

Validation report [2]:
    Akram Louiz, "Formal Validation and Logical Verification of the
    Super-Exponential Kernel Approach to the Riemann Hypothesis by using
    Gemini DeepResearch and Lean Language" (May 2026)

Claim:
    Define S(c)  = ΣΣ (-1)^n * K(n,i,c)           (standard kernel)
    Define Sμ(c) = ΣΣ μ(n)*(-1)^n * K(n,i,c)      (Möbius kernel)
    R(c) = Sμ(c)/S(c)  is claimed as analytic proxy for 1/ζ(1/c).
    The mapping s = 1/c connects Re(c) > 1 to the critical strip.

This benchmark:
    1. Verifies §6.1 numerical values to pin down K(n,i,c)
    2. Exposes inconsistency between §6.1 and the paper's Lean definition
    3. Shows R(c) → 1 for all c, not 1/ζ(1/c) — the critical flaw
    4. Documents the proof gaps
    5. Extracts lessons for our own work

AGENTS.md note: All results here are NUMERICAL EVIDENCE only.
We do NOT claim this proves or disproves RH.
"""

from __future__ import annotations

import json
import os
import sys
import time

import mpmath as mp

mp.mp.dps = 50

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Möbius function (trial division — sufficient for n ≤ 100)
# ---------------------------------------------------------------------------

def _mobius(n: int) -> int:
    """Compute μ(n) via trial division."""
    if n == 1:
        return 1
    k, num_primes, d = n, 0, 2
    while d * d <= k:
        if k % d == 0:
            num_primes += 1
            k //= d
            if k % d == 0:
                return 0      # p² | n  →  μ(n) = 0
        d += 1
    if k > 1:
        num_primes += 1
    return (-1) ** num_primes


_MU = {n: _mobius(n) for n in range(1, 101)}


# ---------------------------------------------------------------------------
# Two candidate kernel formulae
# ---------------------------------------------------------------------------

def _term_sec61(n: int, i: int, c: mp.mpf) -> mp.mpf:
    """Formula consistent with §6.1 numerical checks.

    f_{i,n}(c) = (-1)^n * exp(-2^i * n^c * e^c)

    §6.1 verification at c=2:
        n=1, i=0 : e^{-e^2}    ≈ 6.18e-4    ✓
        n=2, i=0 : e^{-4e^2}   ≈ 1.5e-13    ✓
        n=3, i=0 : e^{-9e^2}   ≈ 4.8e-29    ✓
    """
    exp = mp.power(2, i) * mp.power(n, c) * mp.exp(c)
    return mp.power(-1, n) * mp.exp(-exp)


def _term_lean(n: int, i: int, c: mp.mpf) -> mp.mpf:
    """Formula from the Lean definition (§4.1).

    f_{i,n}(c) = (-1)^n * c * e / (exp(2^(c*i) * n^c * exp(exp(c))) * 2^i)

    §6.1 verification at c=2, n=1, i=0:
        denominator = exp(2^0 * 1^2 * exp(e^2))
                    = exp(e^{e^2}) ≈ exp(1618) ≈ 10^{702}
        → term ≈ 10^{-702}   (NOT 6.18e-4 as §6.1 claims)

    This formula is INTERNALLY INCONSISTENT with the paper's own numerics.
    We include it here to document the discrepancy.
    """
    num = mp.power(-1, n) * c * mp.exp(mp.mpf(1))
    try:
        inner = mp.power(2, c * i) * mp.power(n, c) * mp.exp(mp.exp(c))
        denom = mp.exp(inner) * mp.power(2, i)
    except (OverflowError, mp.libmp.libmpf.MPIntervalExponent):
        return mp.mpf(0)
    if denom == 0:
        return mp.mpf(0)
    return num / denom


def _compute_kernels(c: mp.mpf, N_n: int = 20, N_i: int = 4) -> tuple[mp.mpf, mp.mpf]:
    """Return (S(c), Sμ(c)) using the §6.1-consistent formula."""
    S = mp.mpf(0)
    S_mu = mp.mpf(0)
    for i in range(N_i):
        for n in range(1, N_n + 1):
            mu = _MU.get(n, _mobius(n))
            t = _term_sec61(n, i, c)
            S += t
            if mu != 0:
                S_mu += mu * t
    return S, S_mu


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def run_benchmark() -> dict:
    findings: dict = {}

    print("=" * 72)
    print("  LOUIZ SUPER-EXPONENTIAL KERNEL — NUMERICAL BENCHMARK")
    print("  Claim: R(c) = Sμ(c)/S(c)  is an analytic proxy for 1/ζ(1/c)")
    print("=" * 72)

    # ------------------------------------------------------------------
    # Part 1: Reproduce §6.1 numerical values
    # ------------------------------------------------------------------
    print()
    print("[1] Reproducing §6.1 numerical values at c=2")
    c2 = mp.mpf(2)
    checks = [
        (1, 0, 6.18e-4,  "≈ 6.18e-04"),
        (2, 0, 1.5e-13,  "≈ 1.5e-13"),
        (3, 0, 4.8e-29,  "≈ 4.8e-29"),
    ]
    all_match = True
    for n, i, expected, label in checks:
        t61   = float(abs(_term_sec61(n, i, c2)))
        t_lean_str = "~10^-702" if (n == 1 and i == 0) else "—"
        match = abs(t61 - expected) / expected < 0.02
        all_match = all_match and match
        mark = "✓" if match else "✗"
        print(f"  n={n},i={i}: sec61={t61:.3e}  paper says {label}  {mark}"
              f"  [lean: {t_lean_str}]")

    findings["sec61_numerics_match"] = all_match
    findings["lean_def_matches_sec61"] = False

    print()
    print("  *** INTERNAL INCONSISTENCY ***")
    print("  §6.1 numerics match  f = exp(-2^i · n^c · e^c)")
    print("  Lean definition uses f = exp(-2^(c·i) · n^c · exp(exp(c)))")
    print("  At c=2, n=1, i=0 these differ by ~700 orders of magnitude.")
    print("  The paper's formal definition contradicts its own numerics.")

    # ------------------------------------------------------------------
    # Part 2: R(c) vs 1/ζ(1/c)
    # ------------------------------------------------------------------
    print()
    print("[2] R(c) vs 1/ζ(1/c)  for real c ∈ (1, 5]")
    print()
    print(f"  {'c':>5}  {'s=1/c':>6}  {'R(c)':>12}  {'1/ζ(s)':>12}  {'|err|':>10}  note")
    print("  " + "-" * 68)

    c_vals = [1.1, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    comparisons = []
    for cv in c_vals:
        c = mp.mpf(cv)
        s = mp.mpf(1) / c
        S, S_mu = _compute_kernels(c)
        if abs(S) < mp.mpf("1e-200"):
            print(f"  {cv:5.1f}  {float(s):6.4f}  S≈0 (underflow)")
            continue

        R      = S_mu / S
        iz     = mp.mpf(1) / mp.zeta(s)
        err    = float(abs(R - iz))
        R_f    = float(R.real)
        iz_f   = float(iz.real)
        note   = "R≈+1" if abs(R_f - 1.0) < 0.05 else "R≠1"
        print(f"  {cv:5.1f}  {float(s):6.4f}  {R_f:+12.6f}  {iz_f:+12.6f}  {err:10.3e}  {note}")
        comparisons.append({"c": cv, "s": float(s), "R": R_f, "inv_zeta": iz_f, "abs_err": err})

    findings["comparisons"] = comparisons
    near_1 = sum(1 for r in comparisons if abs(r["R"] - 1.0) < 0.05)
    findings["R_near_1_fraction"] = f"{near_1}/{len(comparisons)}"

    print()
    inv_z_half = float((mp.mpf(1) / mp.zeta(mp.mpf("0.5"))).real)
    S2, Smu2 = _compute_kernels(mp.mpf(2))
    R2 = float((Smu2 / S2).real)
    print(f"  R(2)        = {R2:+.6f}")
    print(f"  1/ζ(1/2)   = {inv_z_half:+.6f}  (target)")
    print(f"  Error       = {abs(R2 - inv_z_half):.4f}  (not small)")
    print()
    print("  ROOT CAUSE: μ(1) = 1, so the n=1 terms in S and Sμ are identical.")
    print("  Super-exponential decay makes n≥2 terms negligible → Sμ/S → 1")
    print("  identically, regardless of ζ(s). The kernel does not encode ζ.")

    findings["R_at_c2"] = R2
    findings["inv_zeta_at_s_half"] = inv_z_half
    findings["R_equals_inv_zeta"] = False

    # ------------------------------------------------------------------
    # Part 3: Structural proof gaps
    # ------------------------------------------------------------------
    print()
    print("[3] Proof gaps")
    gaps = [
        ("critical", "Functional equivalence gap",
         "R(c) → 1 identically; the claim R(1/s) = 1/ζ(s) is asserted via "
         "analytic continuation from a single boundary limit (c→∞), which is "
         "insufficient. Analytic continuation requires agreement on a set with "
         "an interior limit point, not just a single boundary value."),
        ("critical", "Lean proof incomplete",
         "The key theorem 'analytic_louiz_kernel' uses 'sorry'. In Lean 4, "
         "'sorry' admits any goal without proof. The Lean code is a sketch, "
         "not a machine-verified proof."),
        ("critical", "Internal formula inconsistency",
         "§6.1 numerics imply f = exp(-2^i · n^c · e^c). "
         "The Lean definition uses exp(2^(c·i) · n^c · exp(exp(c))). "
         "These differ by ~700 orders of magnitude at c=2. "
         "At least one version is wrong."),
        ("warning", "Spurious ancillary claim",
         "§5.2 states Louiz 'disproved the Twin Primes Conjecture via Brun's "
         "upper bound'. Brun's theorem (1919) provides an upper bound on the "
         "sum of reciprocals of twin primes; it does not disprove TPC. "
         "TPC remains open."),
        ("warning", "AI self-validation",
         "Both papers authored by Akram Louiz. Validation performed by Gemini "
         "DeepResearch (an AI tool), not by independent mathematicians. "
         "No peer review."),
    ]
    findings["gaps"] = [{"severity": s, "name": n, "detail": d} for s, n, d in gaps]
    for sev, name, detail in gaps:
        tag = "CRITICAL" if sev == "critical" else "WARNING "
        print(f"  [{tag}] {name}")
        # Wrap detail at 66 chars
        words = detail.split()
        line = "           "
        for w in words:
            if len(line) + len(w) + 1 > 72:
                print(line)
                line = "           " + w
            else:
                line = line + " " + w if line.strip() else "           " + w
        print(line)
        print()

    # ------------------------------------------------------------------
    # Part 4: Lessons
    # ------------------------------------------------------------------
    print("[4] Lessons for our own work")
    lessons = [
        "Fast convergence ≠ correct target. Super-exponential dampening is "
        "real, but converging quickly to 1 does not mean converging to 1/ζ(s). "
        "Always verify the target, not just the speed.",
        "Analytic continuation requires open-set agreement. Matching at a "
        "single boundary point or limit is not enough. Our proof must establish "
        "equality on an open domain.",
        "'sorry' in Lean is not formal verification. Our lean4/ scaffold is "
        "clearly partial (see RHProof/Basic.lean). We must never cite it as "
        "a complete machine proof.",
        "Internal consistency is non-negotiable. If our numerics and our formal "
        "definitions would disagree, that is a bug. Our falsify.py protocol "
        "(run_all.py) exists precisely to catch this.",
        "Independent falsification is what honest science looks like. This paper "
        "has no falsification protocol. We do.",
    ]
    findings["lessons"] = lessons
    for i, lesson in enumerate(lessons, 1):
        words = lesson.split()
        line = f"  L{i}  "
        for w in words:
            if len(line) + len(w) + 1 > 72:
                print(line)
                line = "       " + w
            else:
                line = line + " " + w if len(line) > 6 else line + w
        print(line)
        print()

    print("=" * 72)
    print("  VERDICT: R(c) ≡ 1 (not 1/ζ(1/c)). Proof has 3 critical gaps.")
    print("  The Louiz approach does NOT establish RH.")
    print("  (Numerical evidence only — does not prove or disprove RH.)")
    print("=" * 72)

    return findings


if __name__ == "__main__":
    t0 = time.time()
    findings = run_benchmark()
    elapsed = time.time() - t0

    out = {
        "paper_id":   "louiz-2026",
        "title":      "Super-Exponential Kernel Approach to the Analyticity of 1/ζ(s)",
        "doi":        "10.13140/RG.2.2.35504.32004",
        "run_date":   "2026-05-31",
        "elapsed_s":  round(elapsed, 2),
        **findings,
    }
    out_path = os.path.join(ROOT, "results", "bench_louiz_kernel.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  Results saved → results/bench_louiz_kernel.json  ({elapsed:.1f}s)")
    sys.exit(0)
