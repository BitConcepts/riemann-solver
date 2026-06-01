# Architecture — riemann-solver

## Overview

Paper: Pierson (2026) — Log-Concavity of the Riemann Xi Kernel and the Riemann Hypothesis

- **Languages**: python
- **Build system**: pyproject
- **Test framework**: pytest
- **Project type**: research-mathematics (Python tooling auxiliary)
- **Files**: 230

## Modules

### riemann
- **Purpose**: Core numerical library for Riemann zeta / Xi-kernel computations.
  Houses `suzuki.py` (Phi/log-phi evaluation, Q_Phi kernel), zero verification,
  Li coefficient computation, and Davenport-Heilbronn control.

### proof/
- **Purpose**: Standalone verification scripts (`verify_ia_1_to_3.py`,
  `verify_galerkin_extended.py`, `verify_groskin.py`). Each script is a
  self-contained falsifiable experiment with JSON result output.

### lean4/RHProof/
- **Purpose**: Lean 4 formal proof skeleton. `Basic.lean` encodes 12 axioms and
  4 proved theorems. `CertificateFramework.lean` provides the certificate-checking
  infrastructure for the IA results.

### paper/
- **Purpose**: LaTeX manuscript (`main.tex`), compiled PDF, bibliography, and
  build artefacts targeting journal submission.

### results/
- **Purpose**: Immutable JSON result store for all verification/falsification runs.
  Never modified by agents without explicit approval (AGENTS.md §3).

## Data Flow

```
src/riemann/  ──► proof/verify_*.py  ──► results/*.json
                        │
                        ▼
               .specsmith/testcases.json
                        │
                        ▼
              lean4/RHProof/*.lean  (formal certificates)
                        │
                        ▼
              paper/main.tex  (manuscript)
```

All critical numerical paths use `mpmath` at ≥ 50 decimal digits.
Arbitrary-precision cross-checks use `python-flint` (FLINT backend) and `gmpy2`.

## External Dependencies

- `setuptools`
- `mpmath`
- `numpy`
- `scipy`
- `pytest`
- `ruff`
- `gmpy2`
- `python-flint`
- `cupy-cuda12x`
- `torch`
- `connes-cvs`
- `matplotlib`
- `specsmith`

## Language Distribution

- markdown: 91 files
- python: 68 files
- json: 38 files
- yaml: 2 files
- powershell: 1 files
- bash: 1 files
- toml: 1 files
- latex: 1 files
- bibtex: 1 files

