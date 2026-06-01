# Requirements — riemann-solver

## Project Goal

Produce a rigorous, reproducible, journal-submission-ready proof that the
Riemann Hypothesis is true (or false) via log-concavity of the Riemann-Jacobi
kernel Φ(u), targeting the Clay Millennium Prize.

---

## REQ-001 — Interval Arithmetic Certification

**Priority**: MUST  
**Status**: implemented-verified

Q_Phi(u) < 0 must be certified on [0, 1] by rigorous interval arithmetic
using ≥ 50,000 subintervals with two independent IA libraries.
Current: 52,898 subintervals (primary) + 55,892 (cross-check).

---

## REQ-002 — Algebraic Log-Concavity Certificate

**Priority**: MUST  
**Status**: implemented-verified

(log φ₁)'' < 0 must be verified for all u ≥ 0 via an algebraic certificate
covering ≥ 50 checkpoints. Current: 51 checkpoints.

---

## REQ-003 — Perturbation Tail Bound

**Priority**: MUST  
**Status**: implemented-verified

The constant C = 204 must be computed and verified such that the tail
contribution cannot flip the sign of Q_Phi for u > 1. Result must be
reproducible via `python verify_tail_prefactor.py`.

---

## REQ-004 — Falsification Battery

**Priority**: MUST  
**Status**: implemented-verified

A minimum of 32 distinct falsification attacks must be attempted against the
proof. All must be survived. Attacks must include:

- Off-critical-line zero search (REQ-004a)
- Li coefficient sign monitoring — any λₙ < 0 disproves RH (REQ-004b)
- Davenport-Heilbronn control — falsification harness must correctly detect
  failure on a known non-RH function (REQ-004c)
- Gram violation analysis (REQ-004d)
- Lehmer pair escalation (REQ-004e)

Current: 36 attacks across 7 batches, all survived.

---

## REQ-005 — Numerical Precision

**Priority**: MUST  
**Status**: implemented-verified

All critical computations must meet minimum precision thresholds (per AGENTS.md §4):

| Computation | Minimum precision |
|---|---|
| Zeta function evaluation | 50 decimal digits |
| Li coefficient computation | 30 decimal digits |
| Zero verification residual | \|ζ(ρ)\| < 10⁻²⁰ |
| Off-line zero search grid | δ ≤ 10⁻⁶ |

---

## REQ-006 — Lean 4 Formal Verification

**Priority**: SHOULD  
**Status**: in-progress

The proof core must be encoded in Lean 4 with:

- ≥ 10 axioms (current: 12)
- ≥ 4 proved theorems with no `sorry` (current: 4 proved, 0 sorry)
- A `CertificateFramework` for linking IA results to formal statements

---

## REQ-007 — Manuscript Quality

**Priority**: MUST  
**Status**: in-progress

The LaTeX manuscript must be:

- Compilable without errors via `pdflatex` + `bibtex`
- ≤ 250 words in abstract
- All theorems, lemmas, and corollaries numbered consistently
- All references traceable to peer-reviewed sources
- All computational identifiers cited with DOI or arXiv ID

---

## REQ-008 — Reproducibility

**Priority**: MUST  
**Status**: implemented-verified

Any result in `results/*.json` must be reproducible by running the
corresponding `proof/verify_*.py` script from a clean environment.
Reference benchmarks (Odlyzko, Maślanka, Groskin, GUE correlation) must
produce matching values within stated precision.

---

## REQ-009 — Test Coverage

**Priority**: SHOULD  
**Status**: partial

Pytest suite must achieve ≥ 80% line coverage across `src/riemann/`.
Current passing: 10/10 tests across 3 suites (zeta, zeros, Li).

---

## REQ-010 — Claim Language Integrity

**Priority**: MUST  
**Status**: implemented-verified

No agent, script, or document may claim to have "proved" or "disproved" the
Riemann Hypothesis (per AGENTS.md §3). All outputs must distinguish:

- Numerical evidence (supports but does not prove)
- Heuristic arguments (suggestive but not rigorous)
- Rigorous proof steps (logically complete, no gaps)
