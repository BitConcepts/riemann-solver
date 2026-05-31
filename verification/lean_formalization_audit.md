# Lean Formalization Audit

**Auditor:** Oz (automated verification agent)
**Date:** 2026-05-31
**File:** `lean4/RHProof/Basic.lean` (95 lines, Lean 4 v4.16.0)
**Build status:** Compiles, zero `sorry`, `autoImplicit=false`

---

## 1. Axiom Inventory

16 `axiom` declarations + 1 `theorem`. All mathematical content is axiomatized; only the top-level implication chain is proved.

### Tier 1 — Irreducible External Propositions (6)

| # | Name | Type | What it encodes |
|---|------|------|-----------------|
| 1 | `RiemannHypothesis` | `Prop` | Placeholder type for RH |
| 2 | `XiHasOnlyRealZeros` | `Prop` | Placeholder type for Ξ having real zeros only |
| 3 | `rh_iff_xi_real` | `RH ↔ XiReal` | Classical equivalence (Titchmarsh §2.10) |
| 4 | `phi_positive` | `Prop` | Φ(u) > 0 for all u |
| 5 | `phi_even` | `Prop` | Φ(-u) = Φ(u) |
| 6 | `phi_integrable` | `Prop` | Φ ∈ L¹(ℝ) |

**Assessment:** Axioms 1–2 are type declarations, not mathematical claims. Axiom 3 is a deep classical result requiring a formalized zeta function (not in Mathlib). Axioms 4–6 are classical properties provable in principle but requiring substantial Mathlib infrastructure.

### Tier 2 — Pólya's Theorem (3)

| # | Name | Type | What it encodes |
|---|------|------|-----------------|
| 7 | `phi_superexp_decay` | `Prop` | Φ = O(exp(−πe^{2u})), satisfies condition (iv) |
| 8 | `phi_log_concave` | `Prop` | (log Φ)'' ≤ 0 for u ≥ 0 |
| 9 | `polya_theorem` | implication | pos → even → L¹ → log-concave → decay → XiReal |

**Assessment:** Axiom 9 (`polya_theorem`) is the central analytic bridge. It now correctly takes `phi_superexp_decay` as a hypothesis, which was previously missing.

### Tier 3 — Algebraic Identities (4)

| # | Name | Type | What it encodes |
|---|------|------|-----------------|
| 10 | `h_pos_for_nonneg` | `Prop` | h(u) = 2πe^{2u} − 3 > 0 for u ≥ 0 |
| 11 | `log_h_d2_neg` | `Prop` | (log h)'' < 0 |
| 12 | `log_phi1_d2_neg` | `Prop` | (log φ₁)'' < 0 for u ≥ 0 |
| 13 | `tail_decay` | `Prop` | |R|/φ₁ < 1/50 for u ≥ 0 |

**Assessment:** All four are provable in Lean with Mathlib. Axioms 10 and 13 are elementary inequalities (2π > 3; geometric series bound). Axioms 11–12 require differentiation of composed functions but are straightforward. These SHOULD be proved to reduce axiom count.

### Tier 4 — Computational Certificates (2)

| # | Name | Type | What it encodes |
|---|------|------|-----------------|
| 14 | `ia_verification_0_to_1` | `Prop` | Q_Φ < 0 on [0,1] certified by IA |
| 15 | `perturbation_bound_above_1` | `Prop` | Q_Φ < 0 for u > 1 via C=204 |

**Assessment:** These are computational certificates. Neither is provable in Lean with current technology. Axiom 14 encodes 52,898 IA evaluations; axiom 15 encodes the perturbation argument. Axiomatization is the correct approach.

### Tier 5 — Structural Implication (2)

| # | Name | Type | What it encodes |
|---|------|------|-----------------|
| 15 | `log_concavity_from_components` | implication | IA + algebraic + perturbation → log-concave |
| 16 | `phi_log_concave` | `Prop` | The conclusion: Φ is log-concave |

**Assessment:** `log_concavity_from_components` is a structural lemma that could be proved in Lean (it just assembles the [0,1] and (1,∞) regions). `phi_log_concave` is the intermediate `Prop` fed to Pólya.

---

## 2. Theorem Structure

The theorem `riemann_hypothesis` takes 7 hypotheses and proves `RiemannHypothesis`:

```
theorem riemann_hypothesis
    (h1 : phi_positive)       -- Tier 1
    (h2 : phi_even)            -- Tier 1
    (h3 : phi_integrable)      -- Tier 1
    (h4 : phi_superexp_decay)  -- Tier 2
    (h5 : ia_verification_0_to_1)        -- Tier 4
    (h6 : log_phi1_d2_neg)               -- Tier 3
    (h7 : perturbation_bound_above_1)    -- Tier 4
    : RiemannHypothesis
```

**Proof:** Two `have` steps + `exact`:
1. `log_concavity_from_components h5 h6 h7` → `phi_log_concave`
2. `polya_theorem h1 h2 h3 lc h4` → `XiHasOnlyRealZeros`
3. `rh_iff_xi_real.mpr xi_real` → `RiemannHypothesis`

The proof structure is logically correct. The dependency chain is: IA + algebraic + perturbation → log-concavity → Pólya → Ξ real → RH.

---

## 3. What the Formalization DOES Prove

The Lean formalization proves that the **dependency graph is a valid deduction**:
- Given the 7 hypotheses, the conclusion follows by the axiomatized intermediate lemmas.
- There is no structural error (e.g., wrong hypothesis used in wrong place, missing premise).
- The zero-sorry guarantee means no holes are hidden.

This is genuinely valuable: it eliminates an entire class of errors (structural logic mistakes in the proof chain).

---

## 4. What the Formalization Does NOT Prove

The formalization does NOT verify any mathematical content. Specifically:

1. **No mathematical objects are defined.** `RiemannHypothesis`, `XiHasOnlyRealZeros`, `phi_positive`, etc. are bare `Prop` types with no internal structure. The formalization cannot distinguish "Φ is positive" from any other proposition.

2. **No computation is verified.** The IA certificate (52,898 intervals) is a single `Prop` axiom. Lean does not check that any computation was performed.

3. **No external theorem is verified.** Pólya's theorem is an axiom. Lean trusts it without checking.

4. **The `Prop` declarations are semantically empty.** `phi_positive : Prop` is equivalent to declaring `P : Prop` — it carries no mathematical meaning within Lean's type system.

---

## 5. CRITICAL GAP: Condition (v) Missing from Lean

**The paper's Theorem 1 now includes condition (v): K must be real analytic near the origin.**

The Lean axiom `polya_theorem` does NOT include this condition:

```
axiom polya_theorem :
  phi_positive → phi_even → phi_integrable →
  phi_log_concave → phi_superexp_decay → XiHasOnlyRealZeros
```

There is no `phi_real_analytic : Prop` axiom and no hypothesis for it in `polya_theorem`.

**Impact:** The Lean proof would be valid even for a kernel that is NOT real analytic (e.g., e^{-|t|³}), for which Pólya's theorem does not apply. The formalization is WEAKER than the paper's stated theorem.

**Fix required:** Add:
```
axiom phi_real_analytic : Prop  -- Φ is real analytic on ℝ
```
And modify `polya_theorem` to:
```
axiom polya_theorem :
  phi_positive → phi_even → phi_integrable →
  phi_log_concave → phi_superexp_decay → phi_real_analytic → XiHasOnlyRealZeros
```
And add `(h8 : phi_real_analytic)` to the theorem hypotheses.

**Severity:** MODERATE. The paper correctly includes condition (v), and Φ trivially satisfies it (convergent series of analytic functions). But the Lean formalization does not reflect the paper's own theorem statement.

---

## 6. Axiom Count Discrepancy

The file header comment says:
- Tier 1: 6 axioms
- Tier 2: 3 axioms ("phi_superexp_decay, phi_log_concave, polya_theorem")
- Tier 3: 5 axioms ("phi_superexp_decay, h_pos_for_nonneg, log_h_d2_neg, log_phi1_d2_neg, tail_decay")
- Tier 4: 2 axioms
- Tier 5: 2 axioms

`phi_superexp_decay` appears in BOTH Tier 2 and Tier 3 in the header comment. The header lists Tier 3 as having 5 axioms, but the code only has 4 axioms in the Tier 3 section (h_pos_for_nonneg, log_h_d2_neg, log_phi1_d2_neg, tail_decay). The total 6+3+5+2+2 = 18 ≠ 16.

The actual code places `phi_superexp_decay` in the Tier 2 section. The correct count is:
- Tier 1: 6 (RiemannHypothesis, XiHasOnlyRealZeros, rh_iff_xi_real, phi_positive, phi_even, phi_integrable)
- Tier 2: 3 (phi_superexp_decay, phi_log_concave, polya_theorem)
- Tier 3: 4 (h_pos_for_nonneg, log_h_d2_neg, log_phi1_d2_neg, tail_decay)
- Tier 4: 2 (ia_verification_0_to_1, perturbation_bound_above_1)
- Tier 5: 1 (log_concavity_from_components)

Total: 6+3+4+2+1 = 16. ✓ Matches `grep ^axiom` count.

The header comment double-counts `phi_superexp_decay` and says Tier 5 has 2 when only `log_concavity_from_components` is in that section (`phi_log_concave` is listed in the header as Tier 5 but placed in code under Tier 2). **Minor comment error; no logical impact.**

---

## 7. Axiom Reducibility Assessment

### Immediately provable (Tier 1 reduction targets):
- `h_pos_for_nonneg` — 2π > 3 ∧ e^{2u} ≥ 1. Trivial in Mathlib.
- `tail_decay` — geometric series with e^{-3π} < 1/50. Needs `norm_num`.
- `log_concavity_from_components` — structural assembly of two regions.

### Provable with moderate effort:
- `log_h_d2_neg` — needs `Real.deriv` and sign analysis.
- `log_phi1_d2_neg` — follows from `log_h_d2_neg` + chain rule.
- `phi_positive` — elementary: each φ_n > 0 since 2πn²e^{2u} > 3.
- `phi_integrable` — dominated convergence with super-exponential decay.

### Not provable with current Mathlib:
- `rh_iff_xi_real` — no zeta function in Mathlib.
- `polya_theorem` — deep entire function theory.
- `ia_verification_0_to_1` — 52,898 IA evaluations.
- `perturbation_bound_above_1` — partial: algebra feasible, C=204 computation hard.

**Recommendation:** Prove at least the 3 Tier-1 targets to bring axiom count from 16 to 13. Proving the 4 moderate-effort items would bring it to 9, which is a much stronger position.

---

## 8. Verdict

**LEAN FORMALIZATION: STRUCTURAL ONLY**

The Lean formalization correctly proves that the dependency graph is valid: given 7 hypotheses (encoding positivity, evenness, integrability, decay, IA certificate, algebraic core, and perturbation bound), the Riemann Hypothesis follows via Pólya's theorem. Zero sorry, all unproven content is explicit axiom.

**Strengths:**
- Zero sorry — no hidden holes
- Clear tiered axiom classification
- The proof structure matches the paper's logic exactly
- `autoImplicit=false` prevents accidental implicit assumptions

**Weaknesses:**
- 16 axioms is high; at least 3–7 are immediately provable
- Condition (v) (real analyticity) is NOT encoded — **gap**
- All `Prop` types are semantically empty — Lean cannot distinguish meaningful mathematical statements from arbitrary propositions
- No computational verification is embedded

**The formalization is a structural proof checker, not a mathematical proof verifier.** It should be presented as such in the paper.
