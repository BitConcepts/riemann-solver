# Governance Ledger

Tamper-evident record of key decisions, milestones, and audit gates for the
riemann-solver project. All entries are append-only.

---

## 2026-05-29 — Project inception

**Type:** milestone
**Decision:** Initiate computational verification of log-concavity of the Riemann–Jacobi
kernel Φ(u) as a candidate approach toward the Riemann Hypothesis.
**Status:** CONFIRMED

---

## 2026-05-30 — Verification pipeline established

**Type:** milestone
**Decision:** Adopt four-step verification pipeline: (1) rigorous IA via mpmath.iv,
(2) independent IA via Arb/FLINT, (3) algebraic core, (4) truncation/crosscheck.
**Status:** CONFIRMED

---

## 2026-05-31 — Falsification harness approved

**Type:** audit-gate
**Decision:** 32 falsification attacks implemented. Davenport-Heilbronn control verified.
All 32 attacks survived. Falsification harness approved as scientifically honest.
**Status:** CONFIRMED

---

## 2026-06-01 — Rigorous IA certificate issued

**Type:** milestone
**Decision:** 52,898 subintervals certify Q_Φ < 0 on [0, 1] with 60-digit precision.
Algebraic core: (log φ₁)'' < 0 for all u ≥ 0. Tail bound: C = 204, u > 1.
Strict log-concavity of Φ on [0, ∞) is PROVED.
**Status:** CONFIRMED

---

## 2026-06-03 — Claim language reviewed

**Type:** decision
**Decision:** Paper claim updated to reflect that Hypothetical Criterion 13 (H13) is open.
Manuscript does NOT claim RH is proved. All conditional language preserved.
**Status:** CONFIRMED

---

## 2026-06-04 — phase-next branch initiated

**Type:** milestone
**Decision:** Open `phase-next` branch for iterative investigation of H13 bridge theorem.
Three Clay-prize paths defined. Falsification-first protocol adopted.
**Status:** CONFIRMED

---

## 2026-06-04 — L₂ generalized Laguerre inequality certified

**Type:** milestone
**Decision:** L₂(u) ≥ 0 for all u ≥ 0 certified via rigorous IA (2000 subintervals,
lower bound 3.14e-8). Combined with existing L₁ proof: two Laguerre orders proved for Φ.
**Status:** CONFIRMED

---

## 2026-06-04 — Route C identified (Brandén-Chasse de Bruijn-Ilieff)

**Type:** decision
**Decision:** Brandén-Chasse (2016) Section 5 extension of de Bruijn-Ilieff identified as
new proof route (Route C). Condition: h'(u) = −Φ'(u)/Φ(u) ∈ LP class.
Investigation scheduled for next iteration.
**Status:** OPEN

---

*All entries above are append-only. Do not modify existing entries.*

## 2026-06-04T14:28 — specsmith migration: 0.11.7 → 0.13.0
- **Author**: specsmith
- **Type**: migration
- **Status**: complete
- **Chain hash**: `667c5548e106dc10...`
