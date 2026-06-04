# Requirements

## REQ-001 — Rigorous log-concavity certificate

**Status:** implemented
**Description:** Certify that Q_Φ(u) = Φ(u)Φ''(u) − [Φ'(u)]² < 0 for all u ≥ 0
using interval arithmetic with at least 50 decimal digits of precision.
**Acceptance:** IA certificate covers [0,1]; algebraic/tail argument covers (1,∞).
**Test:** `proof/verify_logconcavity_rigorous.py`, `verification/verify_certificate.py`

---

## REQ-002 — Independent IA verification

**Status:** implemented
**Description:** Independent interval arithmetic verification using a different library
(Arb/FLINT) to rule out shared software bugs.
**Acceptance:** ≥ 50,000 subintervals, ≥ 100-bit precision.
**Test:** `proof/verify_logconcavity_arb.py`

---

## REQ-003 — Algebraic core proof

**Status:** implemented
**Description:** Prove (log φ₁)'' < 0 for all u ≥ 0 algebraically (first theta term dominance).
Prove perturbation bound C = 204 for the tail u > 1.
**Acceptance:** Symbolic computation with explicit constants.
**Test:** `proof/verify_algebraic_core.py`

---

## REQ-004 — Falsification harness

**Status:** implemented
**Description:** 32 falsification attacks on the proof. The Davenport-Heilbronn control
must correctly return a generalized RH failure.
**Acceptance:** 32/32 attacks survived; Davenport-Heilbronn correctly fails.
**Test:** `falsification/run_all.py`

---

## REQ-005 — External claim audit

**Status:** implemented
**Description:** Audit pipeline for external RH claims (self-audit + 4 external claims).
**Acceptance:** Self-audit passes; external claims classified correctly.
**Test:** `falsification/audit_external.py`

---

## REQ-006 — Precision requirements

**Status:** implemented
**Description:** All zeta evaluations ≥ 50 decimal digits; Li coefficients ≥ 30 digits;
zero residuals \|ζ(ρ)\| < 10⁻²⁰; grid resolution δ ≤ 10⁻⁶.
**Test:** Enforced throughout `src/riemann/` and proof scripts.

---

## REQ-007 — Claim language discipline

**Status:** implemented
**Description:** No claim of RH proved. All RH conclusions marked conditional on H13.
Paper and codebase must maintain: PROVED / OPEN / CONDITIONAL distinction.
**Acceptance:** AGENTS.md prohibitions respected; manuscript reviewed.
**Test:** Manual review; AGENTS.md governance.

---

## REQ-008 — Reproducibility

**Status:** implemented
**Description:** All computational results reproducible from source. Bootstrap scripts
for clean environments on Linux, macOS, Windows.
**Acceptance:** `bootstrap.sh` / `bootstrap.ps1` produce passing test run.
**Test:** CI matrix (3 OS × 2 Python versions).

---

## REQ-009 — H13 bridge investigation (phase-next)

**Status:** partial
**Description:** Systematically investigate whether a theorem bridge from certified
log-concavity of Φ to real-rootedness of its Fourier transform exists or can be proved.
Three paths: prove H13, find existing theorem, find counterexample/alternate route.
**Acceptance:** Bridge found and verified, or H13 disproved, or all known routes exhausted.
**Test:** `phase-next/experiments/scripts/`, `phase-next/reports/bridge_status_matrix.md`

---

## REQ-010 — Generalized Laguerre certifications (phase-next)

**Status:** partial
**Description:** Certify L_n(u) ≥ 0 for the Riemann–Jacobi kernel Φ for increasing orders n.
L_1 and L_2 are proved. L_3, L_4, … remain open.
**Acceptance:** Rigorous IA certificates for all certified orders.
**Test:** `phase-next/experiments/scripts/certify_l2_laguerre.py`
