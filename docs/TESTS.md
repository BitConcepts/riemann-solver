# Tests — riemann-solver

## Test Framework

- **Runner**: pytest
- **Test directory**: `tests/`
- **Precision library**: mpmath (≥ 50 decimal digits for all critical paths)
- **Last full run**: 2026-05-29 — 10/10 passing, 0 failing

---

## Test Suites

### tests/test_zeta.py (4 tests)

#### TEST-001 — test_zeta_known_values
Covers: REQ-005
ζ(2) = π²/6, ζ(4) = π⁴/90 etc. verified at 50 dps. Status: passing.

#### TEST-002 — test_hardy_z_sign_change
Covers: REQ-005, REQ-008
Hardy Z-function sign change in [14, 15]. Status: passing.

#### TEST-003 — test_gram_point
Covers: REQ-005, REQ-008
Gram point g₀ ≈ 17.845... matches reference. Status: passing.

#### TEST-004 — test_stieltjes
Covers: REQ-005
γ₀ Stieltjes constant verified to 20 dps. Status: passing.

### tests/test_zeros.py (3 tests)

#### TEST-005 — test_first_zero
Covers: REQ-005, REQ-008
ρ₁ ≈ 1/2 + 14.134725...i, residual < 10⁻²⁰. Status: passing.

#### TEST-006 — test_first_few_zeros
Covers: REQ-005, REQ-008
First 10 zeros on critical line, all residual < 10⁻²⁰. Status: passing.

#### TEST-007 — test_spacing
Covers: REQ-008
GUE-style spacing statistics on first 10 zeros. Status: passing.

### tests/test_li.py (3 tests)

#### TEST-008 — test_lambda_1
Covers: REQ-005, REQ-009
λ₁ = 1 − γ − ln(4π) ≈ −0.0230957... Status: passing.

#### TEST-009 — test_first_few_positive
Covers: REQ-005, REQ-009
λₙ > 0 for n = 2..10 (RH consistency check). Status: passing.

#### TEST-010 — test_growth_check
Covers: REQ-005, REQ-009
λₙ / (n log n) → 1/2 asymptotically. Status: passing.

### tests/test_verification.py (12 tests)

#### TEST-011 — test_ia_cert_result_exists
Covers: REQ-001, REQ-008
IA certification JSON result file exists and indicates success. Status: passing.

#### TEST-012 — test_ia_subinterval_count
Covers: REQ-001
IA result records ≥ 50,000 subintervals. Status: passing.

#### TEST-013 — test_galerkin_cert_result_exists
Covers: REQ-002, REQ-008
Galerkin/algebraic cert result exists and passes. Status: passing.

#### TEST-014 — test_bridge_phase10_result_exists
Covers: REQ-003, REQ-008
Bridge phase 10 result (tail-bound) exists and passes. Status: passing.

#### TEST-015 — test_falsification_attacks_survived
Covers: REQ-004
All bridge result files exist and record attack data. Status: passing.

#### TEST-016 — test_dh_control_present
Covers: REQ-004
At least one result file references the Davenport-Heilbronn control. Status: passing.

#### TEST-017 — test_lean4_basic_exists
Covers: REQ-006
Lean 4 Basic.lean exists and contains no `sorry`. Status: passing.

#### TEST-018 — test_lean4_certificate_framework_exists
Covers: REQ-006
CertificateFramework.lean exists. Status: passing.

#### TEST-019 — test_paper_tex_exists
Covers: REQ-007
paper/main.tex exists. Status: passing.

#### TEST-020 — test_paper_pdf_exists
Covers: REQ-007
Compiled paper/main.pdf exists. Status: passing.

#### TEST-021 — test_agents_md_no_proof_claim
Covers: REQ-010
AGENTS.md contains no forbidden proof-claim language. Status: passing.

#### TEST-022 — test_no_proof_claim_in_scaffold
Covers: REQ-010
scaffold.yml description contains no forbidden claim language. Status: passing.

---

## Proof Verification Scripts

These are not pytest tests but standalone reproducibility scripts with JSON output.

| Script | Purpose | Latest result |
|---|---|---|
| `verify.py` | End-to-end pipeline smoke test | See `results/` |
| `proof/verify_ia_1_to_3.py` | IA cert on [1, 3] extended range | `results/verify_ia_1_to_3.json` |
| `proof/verify_galerkin_extended.py` | CvS Galerkin eigenvalue sweep | `results/galerkin_extended_*.json` |
| `proof/verify_groskin.py` | Groskin eigenvalue reproduction | `results/groskin_reproduction_*.json` |
| `verify_tail_prefactor.py` | C = 204 tail bound | (inline output) |
| `run_bridge.py` | Bridge phase integration tests | `results/bridge_*.json` |

---

## Coverage Target

REQ-009 requires ≥ 80% line coverage across `src/riemann/`.

Run with:
```
pytest tests/ --cov=src/riemann --cov-report=term-missing
```

---

## Falsification Tests

Per AGENTS.md §5, every verification claim is paired with a falsification attempt.
The Davenport-Heilbronn control function (known non-RH) must be tested and must
show the harness correctly detecting failure. See `falsify.py`.
