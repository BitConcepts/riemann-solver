# Riemann Hypothesis Solver

**Rigorous proof or disproof of the Riemann Hypothesis, targeting the
Clay Mathematics Institute Millennium Prize ($1,000,000).**

---

## Overview

The Riemann Hypothesis (RH) asserts that all non-trivial zeros of the Riemann
zeta function ζ(s) lie on the critical line Re(s) = 1/2. This project aims
to produce a **rigorous proof or disproof** of the Riemann Hypothesis,
targeting the **Clay Mathematics Institute Millennium Prize ($1,000,000)**.

### Prize Requirements (Clay Millennium)

All work in this project must satisfy the CMI prize criteria:

1. **Rigorous proof or disproof** — computational evidence alone does not qualify
2. **Published in a refereed journal** of worldwide repute
3. **General acceptance** by the mathematics community for **2+ years** after publication
4. **Reviewed and approved** by the CMI Scientific Advisory Board

The computational tools here serve as:
- **Exploration engines** to identify the most promising proof strategy
- **Verification harnesses** to validate proof steps numerically
- **Falsification harnesses** to actively seek counterexamples
- **Benchmark suites** to ensure all results are reproducible and auditable

### Key Principle

> "If you can't find a counterexample, you haven't looked hard enough."

Every verification result is paired with a falsification harness that actively
searches for contradictions. The Davenport-Heilbronn function (where a
generalized RH is known to fail) serves as a control to prove the falsification
methods actually work.

---

## Attack Vectors

| ID | Approach | Status | Key Reference |
|----|----------|--------|---------------|
| LI | Keiper-Li Criterion | scaffold | Li (1997), Coffey (2005) |
| CVS | Connes-van Suijlekom Galerkin | scaffold | Connes-Consani-Moscovici (2025) |
| ZEROS | Zero Verification & Off-Line Search | scaffold | Odlyzko, Gourdon |
| DBN | De Bruijn-Newman Constant | scaffold | Rodgers-Tao (2018) |
| GUE | Random Matrix Theory | scaffold | Montgomery (1973), Odlyzko (1987) |
| SPECTRAL | Spectral Operator Construction | scaffold | Connes (2025) |

---

## Quick Start

```bash
# Create virtual environment
python -m venv .work/env

# Activate (Windows)
.work\env\Scripts\activate

# Install
pip install -e ".[dev]"

# Run tests
pytest

# Compute first 10 Li coefficients
python -m riemann.li_criterion --count 10

# Verify first 100 zeros
python -m riemann.zeros --count 100
```

---

## Project Structure

```
riemann-solver/
├── scaffold.yml          # specsmith config
├── AGENTS.md             # agent governance
├── pyproject.toml        # Python project config
├── docs/
│   ├── APPROACH.md       # mathematical approach
│   ├── REFERENCES.md     # bibliography
│   └── FALSIFICATION.md  # falsification strategy
├── src/riemann/          # core library
│   ├── zeta.py           # zeta function wrappers
│   ├── xi.py             # xi function and derivatives
│   ├── zeros.py          # zero finding/verification
│   ├── li_criterion.py   # Keiper-Li coefficients
│   ├── dbn_constant.py   # de Bruijn-Newman bounds
│   ├── weil_positivity.py # CvS Galerkin matrix
│   ├── spectral.py       # spectral operators
│   └── utils.py          # common utilities
├── benchmarks/           # benchmark suites
├── falsification/        # falsification harnesses
└── tests/                # test suite
```

---

## Requirements

- Python ≥ 3.11
- mpmath ≥ 1.3 (arbitrary-precision arithmetic)
- numpy ≥ 1.24
- scipy ≥ 1.10

Optional: gmpy2, python-flint (for significant speedups)

---

## References

See `docs/REFERENCES.md` for the complete bibliography.

Key papers:
- Riemann (1859) — "Über die Anzahl der Primzahlen unter einer gegebenen Grösse"
- Li (1997) — "The positivity of a sequence of numbers and the Riemann hypothesis"
- Rodgers & Tao (2018) — "The de Bruijn-Newman constant is non-negative"
- Connes, Consani & Moscovici (2025) — "Zeta Spectral Triples"

---

*Research project — Layer1Labs Silicon Inc.*
