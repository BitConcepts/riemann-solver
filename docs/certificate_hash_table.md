# Deliverable: certificate_hash_table.md
# Task 8 — Certificate Hash Table

## SHA256 Hashes of All Certificate Files

Computed 2026-06-01 on committed files in repo.

| Cert | Claim | Script | Output JSON | SHA256 (first 16 hex) |
|------|-------|--------|-------------|----------------------|
| C4 | Q_Φ < 0 on [0,1] | proof/verify_logconcavity_rigorous.py | results/verify_logconcavity_rigorous.json | 0D0841DAB32396D9... |
| C4b | Arb/FLINT reproduction | proof/verify_logconcavity_arb.py | results/verify_logconcavity_arb.json | 974B67CC58B96117... |
| C5 | (log Φ)'' < 0 on [1,3] | proof/verify_ia_1_to_1_5.py | results/verify_ia_1_to_1_5.json | 7D65253C5A8FA397... |
| Main | Full proof chain | verification/verify_certificate.py | verification/proof_certificate_v2.json | 8B538345D589638A... |

### Full SHA256 Hashes

C4  (verify_logconcavity_rigorous.json):
  0D0841DAB32396D99BEF8587D189FD8A18ECA3E3FD357E57F87939A093D67997

C4b (verify_logconcavity_arb.json):
  974B67CC58B96117074E8849ED737A2202A5232C4D31890965631FE9DB68C3B1

C5  (verify_ia_1_to_1_5.json):
  7D65253C5A8FA397FD83684A7A90978A71731552E073E4197DE543A894097F32

Main (proof_certificate_v2.json):
  8B538345D589638A7AB9534470085CF531DACABD57D9143A2BF327C5CB2DC192

## Certificate Summary Data

C4:
  method: exact_symbolic_derivatives
  n_subintervals: 52898 (1898 coarse + 51000 fine)
  certified: 52898 / 52898
  max_Q_upper: -3.356e-12
  dps: 60
  all_certified: true

C4b:
  method: arb_flint_independent
  library: python-flint (Arb) v0.8.0
  precision_bits: 200
  n_subintervals: 55892
  certified: 55892 / 55892
  max_Q_upper: -7.912e-12
  all_certified: true

C5:
  method: algebraic_log_phi1_d2_plus_perturbation
  u_range: [1.0, 3.0]
  n_checkpoints: 101
  perturbation_C: 204
  certified: 101 / 101
  min_margin: 93.149
  dps: 60
  all_certified: true

## Regeneration Instructions

To reproduce and verify hashes:
  python proof/verify_logconcavity_rigorous.py
  # Compare SHA256 of results/verify_logconcavity_rigorous.json with C4 above

  python proof/verify_logconcavity_arb.py
  # Compare SHA256 of results/verify_logconcavity_arb.json with C4b above

  python proof/verify_ia_1_to_1_5.py
  # Compare SHA256 of results/verify_ia_1_to_1_5.json with C5 above

  python verification/verify_certificate.py
  # Validates the proof_certificate_v2.json structure and contents

## Required Paper Change (Appendix B)

Add the full SHA256 hash table above to Appendix B, replacing the current statement
"regenerate by running [script]" with the explicit hash values for auditor reference.
