# Tests

## Unit tests (`tests/`)

Run with: `pytest -v --tb=short`

| Test | File | Description | REQ |
|------|------|-------------|-----|
| test_lambda_1 | test_li.py | Li coefficient λ₁ positive | REQ-006 |
| test_first_few_positive | test_li.py | First Li coefficients all positive | REQ-006 |
| test_growth_check | test_li.py | Li coefficient growth rate | REQ-006 |
| test_first_zero | test_zeros.py | First nontrivial zero ≈ 14.1347 | REQ-001 |
| test_first_few_zeros | test_zeros.py | First 5 zeros on critical line | REQ-001 |
| test_spacing | test_zeros.py | Zero spacing statistics | REQ-001 |
| test_zeta_known_values | test_zeta.py | ζ(2)=π²/6, ζ(3), ζ(4) | REQ-006 |
| test_hardy_z_sign_change | test_zeta.py | Hardy Z sign change in [14,15] | REQ-001 |
| test_gram_point | test_zeta.py | Gram point g₀ ≈ 17.846 | REQ-001 |
| test_stieltjes | test_zeta.py | Stieltjes constant γ₁ | REQ-006 |

**Current status:** 10/10 passing.

---

## Proof verification scripts

Run with: `python verify.py` (full, ~70s) or `python verify.py --quick` (~2s)

| Script | Description | REQ |
|--------|-------------|-----|
| verify_logconcavity_rigorous.py | IA certificate, 52,898 subintervals | REQ-001 |
| verify_logconcavity_arb.py | Independent Arb/FLINT IA, 55,892 intervals | REQ-002 |
| verify_algebraic_core.py | Algebraic core + C=204 tail bound | REQ-003 |
| verify_truncation_and_crosscheck.py | Truncation error + cross-validation | REQ-001 |

---

## Falsification suite

Run with: `python falsify.py` (full) or `python falsify.py --quick`

| Script | Description | REQ |
|--------|-------------|-----|
| run_all.py | 32 falsification attacks | REQ-004 |
| audit_external.py | External claim audit (4 claims + self) | REQ-005 |

**Current status:** 32/32 attacks survived.

---

## phase-next experiment scripts

Run manually from `phase-next/experiments/scripts/`

| Script | Description | REQ |
|--------|-------------|-----|
| check_log_concavity.py | Verify H1-H6 for candidate kernels | REQ-009 |
| compute_fourier_zeros.py | Scan Fourier transform for complex zeros | REQ-009 |
| argument_principle_box.py | Rigorous zero counting via argument principle | REQ-009 |
| search_counterexamples.py | Master H13 counterexample search pipeline | REQ-009 |
| certify_l2_laguerre.py | IA certification of L₂(u) ≥ 0 for Φ | REQ-010 |
| extended_search.py | Expanded kernel class counterexample search | REQ-009 |

**Current status:** 16 kernels tested, 0 counterexample candidates. L₂ certified.
