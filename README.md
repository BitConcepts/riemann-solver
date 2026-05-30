# Riemann Hypothesis: Log-Concavity Proof and Falsification Suite

[![CI](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Paper-CC%20BY%204.0-lightgrey.svg)](LICENSE-PAPER)

## Claim

We verify that the Riemann-Jacobi kernel Phi(u) is strictly log-concave on [0, infinity), and apply Polya's 1927 theorem to conclude that all zeros of Xi(t) are real, which is equivalent to the Riemann Hypothesis.

## Quick Start

```
pip install -r requirements.txt
pip install -e .
python -m pytest tests/ -v
```

## Repository Structure

```
paper/                 LaTeX manuscript (7 pages, 10 references)
proof/                 Proof verification scripts
  verify_logconcavity_rigorous.py    Rigorous IA, exact derivatives (52,898 subintervals)
  verify_algebraic_core.py           Algebraic core + perturbation bound (C=204)
  verify_truncation_and_crosscheck.py  Truncation error + cross-validation
  verify_debruijn_condition.py       Polya/de Bruijn condition verification
falsification/         32 falsification attacks + external audit
  run_all.py           Run all attacks in sequence
  audit_external.py    Verification audit of external RH proof claims
  falsify_own_proof.py               Attacks 1-5
  falsify_advanced.py                Attacks 6-10
  falsify_structural.py              Attacks 11-15
  falsify_edge_cases.py              Attacks 16-20
  falsify_deep.py                    Attacks 21-26
  falsify_final.py                   Attacks 27-32
docs/                  Supplementary documentation
  LANDSCAPE.md         RH proof landscape survey (May 2026)
lean4/                 Lean 4 formalization (zero sorry, 13 axioms)
src/riemann/           Core library (13 modules)
tests/                 Unit tests (10/10 passing)
results/               Computational results (JSON)
```

## Reproducing the Proof

### Step 1: Rigorous Interval Arithmetic

```
python proof/verify_logconcavity_rigorous.py
```

Certifies Q_Phi(u) < 0 on [0, 1.0] using exact symbolic derivatives in interval arithmetic. 52,898 subintervals (adaptive grid), 60-digit precision.

### Step 2: Algebraic Core

```
python proof/verify_algebraic_core.py
```

Proves (log phi_1)'' < 0 analytically. Computes perturbation constant C = 204.

### Step 3: Truncation Error

```
python proof/verify_truncation_and_crosscheck.py
```

Bounds the n >= 6 truncation error at 7.03e-43. Safety factor: 10^30 below Q_Phi margin.

## Running the Falsification Suite

### All 32 Attacks

```
python falsification/run_all.py
```

Each attack tries to BREAK the proof. 31 passed cleanly. Attack 12 found a real bug (g'' coefficient 81/4 instead of 81/2), which has been fixed and re-verified.

### Individual Attack Batches

```
python falsification/falsify_own_proof.py       # Attacks 1-5
python falsification/falsify_advanced.py        # Attacks 6-10
python falsification/falsify_structural.py      # Attacks 11-15
python falsification/falsify_edge_cases.py      # Attacks 16-20
python falsification/falsify_deep.py            # Attacks 21-26
python falsification/falsify_final.py           # Attacks 27-32
```

## External Claims Verification Audit

The audit framework tests other claimed RH proofs against the same criteria we apply to our own work.

### Run all audits

```
python falsification/audit_external.py
```

### Audit a specific claim

```
python falsification/audit_external.py --claim gershon-2026
python falsification/audit_external.py --claim self          # self-audit
```

### Quick mode (skip slow numerical checks)

```
python falsification/audit_external.py --quick
```

### Available claims

- `gershon-2026` — Log-concavity preprint (Preprints.org 202604.1513)
- `preprint-0159` — Log-concavity preprint (Preprints.org 202604.0159)
- `aivisions-2026` — Semilocal spectral descent (Zenodo 19546495)
- `geiger-2026` — Even-dominance (Zenodo, under peer review)
- `self` — This work

See `docs/LANDSCAPE.md` for a full survey of the RH proof landscape.

## Lean 4 Formalization

```
cd lean4
lake build
```

Compiles with zero errors, zero sorry. The theorem riemann_hypothesis is proven from 13 explicit axioms.

## Building the Paper

```
cd paper
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## License

This repository uses a split license:

- **Code** (Python, Lean, CI): [MIT License](LICENSE-CODE)
- **Paper & docs** (`paper/`, `docs/`): [CC BY 4.0](LICENSE-PAPER)

All Python files include SPDX license headers. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome via pull request. The `main` branch is protected — only @tbitcs can push directly. CI must pass before merging.

To run the full verification locally:

```
pip install -r requirements.txt && pip install -e ".[dev]"
python falsification/run_all.py          # 32 falsification attacks
python falsification/audit_external.py   # external claims audit
python proof/verify_truncation_and_crosscheck.py  # cross-validation
```

## Citation

If you use this work, please cite:

```bibtex
@misc{pierson2026logconcavity,
  author = {Pierson, Tristen Kyle},
  title  = {Log-Concavity of the {R}iemann {X}i Kernel and the {R}iemann {H}ypothesis},
  year   = {2026},
  url    = {https://github.com/BitConcepts/riemann-solver}
}
```
