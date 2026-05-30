# Riemann Hypothesis: Log-Concavity Proof and Falsification Suite

[![CI](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20465036-blue)](https://doi.org/10.5281/zenodo.20465036)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Paper-CC%20BY%204.0-lightgrey.svg)](LICENSE-PAPER)

**Paper**: [Pierson (2026) — Log-Concavity of the Riemann Xi Kernel and the Riemann Hypothesis](https://doi.org/10.5281/zenodo.20465036)

## Claim

We verify that the Riemann-Jacobi kernel Phi(u) is strictly log-concave on [0, infinity), and apply Polya's 1927 theorem to conclude that all zeros of Xi(t) are real, which is equivalent to the Riemann Hypothesis.

## Quick Start

Requires Python 3.11+. Works on Linux, macOS, and Windows.

```
pip install -r requirements.txt
pip install -e .
python verify.py --quick    # proof verification (fast, ~2s)
python falsify.py --quick   # falsification audit (fast, ~1s)
```

Or use the bootstrap script:

```
bash bootstrap.sh          # Linux / macOS
.\bootstrap.ps1            # Windows PowerShell
```

## Repository Structure

```
verify.py              Run the proof verification pipeline
falsify.py             Run the falsification suite + external audit
proof/                 Proof verification scripts
  verify_logconcavity_rigorous.py    Rigorous IA (52,898 subintervals)
  verify_algebraic_core.py           Algebraic core + perturbation (C=204)
  verify_truncation_and_crosscheck.py  Truncation error + cross-validation
  verify_debruijn_condition.py       Polya condition verification
falsification/         32 falsification attacks + external audit
  run_all.py           Run all 32 attacks
  audit_external.py    Verification audit of external RH claims
  falsify_*.py         Individual attack batches (1-5, 6-10, ..., 27-32)
paper/                 LaTeX manuscript (7 pages, 10 references)
docs/                  Supplementary documentation
  LANDSCAPE.md         RH proof landscape survey (May 2026)
lean4/                 Lean 4 formalization (zero sorry, 13 axioms)
src/riemann/           Core library
tests/                 Unit tests
results/               Computational results (JSON)
research/              Research loop workflow and logs
```

## Reproducing the Proof

### Full pipeline (~70s)

```
python verify.py
```

Runs all 4 verification steps: rigorous IA (52,898 subintervals, 60-digit precision), algebraic core, truncation error, Polya conditions.

### Quick check (~2s)

```
python verify.py --quick
```

Skips the slow IA step; runs algebraic core, truncation/cross-validation, and Polya conditions.

## Running the Falsification Suite

### Full suite (32 attacks + external audit)

```
python falsify.py
```

Each attack tries to BREAK the proof. 32/32 pass. Attack 12 historically found a real bug (g'' coefficient 81/4 instead of 81/2), which has been fixed.

### Quick audit only

```
python falsify.py --quick
```

### Individual scripts

```
python falsification/run_all.py                # 32 attacks
python falsification/audit_external.py --quick  # external claims audit
python falsification/audit_external.py --claim self  # self-audit only
```

### Auditable claims

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
python verify.py     # full proof pipeline
python falsify.py    # 32 attacks + external audit
```

## Citation

If you use this work, please cite:

```bibtex
@misc{pierson2026logconcavity,
  author = {Pierson, Tristen Kyle},
  title  = {Log-Concavity of the {R}iemann {X}i Kernel and the {R}iemann {H}ypothesis},
  year   = {2026},
  doi    = {10.5281/zenodo.20465036},
  url    = {https://github.com/BitConcepts/riemann-solver}
}
```
