# Architecture

## Project type

Research mathematics — computational verification targeting the Riemann Hypothesis
(Clay Millennium Prize). The project uses Python for all computations and LaTeX for
the manuscript. This is not a software product; it is a research artifact.

Note: `pyproject.toml` uses library-python conventions (setuptools, pytest) as a
pragmatic choice for reproducible dependency management and test running, not because
this is a software library.

---

## Verification pipeline

```
Riemann-Jacobi kernel Φ(u)
         │
         ▼
┌─────────────────────────────┐
│  Step 1: Rigorous IA         │  proof/verify_logconcavity_rigorous.py
│  52,898 subintervals         │  mpmath.iv interval arithmetic
│  Q_Φ < 0 on [0,1] certified  │  60-digit precision
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Step 2: Independent IA      │  proof/verify_logconcavity_arb.py
│  55,892 subintervals         │  Arb/FLINT 200-bit precision
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Step 3: Algebraic core      │  proof/verify_algebraic_core.py
│  (log φ₁)'' < 0 for u ≥ 0   │  C = 204 tail bound
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Step 4: Truncation/cross    │  proof/verify_truncation_and_crosscheck.py
│  Error bounds + validation   │
└─────────────┬───────────────┘
              │
              ▼
         PROVED: Φ strictly log-concave on [0,∞)
```

---

## Falsification harness

```
falsification/
  run_all.py          ← 32 attack scripts
  audit_external.py   ← External RH claim auditor
```

Every verification claim is accompanied by a falsification attempt.
The Davenport-Heilbronn control (a function where generalized RH fails)
validates that the harness actually works.

---

## Bridge research (phase-next branch)

```
phase-next/
  hypotheses/         ← H13 statement, bridge candidates, counterexample candidates
  literature/         ← Source index, theorem extraction notes
  experiments/        ← Computation scripts (H1-H6 check, Fourier zeros, arg principle)
  formal/             ← Lean proof planning, theorem dependency graph
  reports/            ← Bridge status matrix, Clay path tracker
```

---

## Source layout

```
src/riemann/          ← Core library (zeta, xi, Phi, Li coefficients)
tests/                ← Unit tests (pytest, 10 tests)
proof/                ← Proof verification scripts
falsification/        ← Falsification scripts (32 attacks)
verification/         ← Audit documents and certificates
paper/                ← LaTeX manuscript
docs/                 ← Documentation
lean4/                ← Lean 4 formal proofs
```

---

## Precision requirements (from AGENTS.md)

| Computation | Minimum precision |
|-------------|-------------------|
| Zeta evaluations | 50 decimal digits |
| Li coefficients | 30 decimal digits |
| Zero verification residual | \|ζ(ρ)\| < 10⁻²⁰ |
| Off-line search grid | δ ≤ 10⁻⁶ |

---

## CI

GitHub Actions (`.github/workflows/ci.yml`):
- Matrix: Python 3.11, 3.12 × Ubuntu, Windows, macOS
- Steps: lint (ruff), unit tests (pytest), quick proof verify, quick falsification audit
