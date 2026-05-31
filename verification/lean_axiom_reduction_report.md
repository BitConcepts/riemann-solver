# Lean 4 Axiom Reduction Report

## File Analyzed

`lean4/RHProof/Basic.lean` — 59 lines, namespace `RHProof`.

## Summary

The file declares **16 axiom statements** (counting `axiom` keywords), but the file header says "12 total" and groups them as 5 published + 5 algebraic + 2 computational. The discrepancy is because several axioms are `Prop` declarations (type-level) rather than implication axioms, and the header counts functional groupings.

I count **16 `axiom` declarations** total. The theorem `riemann_hypothesis` is proved from 6 hypotheses using 2 intermediate lemma axioms (`log_concavity_from_components` and `polya_debruijn`).

The file compiles with zero `sorry`. All unproved content is explicit `axiom`.

---

## Complete Axiom Inventory

### Axiom 1: `RiemannHypothesis : Prop`
- **Classification**: avoidable-placeholder
- **What it does**: Declares the type of the Riemann Hypothesis as a proposition.
- **Can it be proved in Lean?** Not as-is. This is a pure declaration, not a statement. It could be replaced with a concrete definition (e.g., `def RiemannHypothesis := ∀ s, zeta s = 0 → s.re = 1/2 ∨ ...`) if Lean had a zeta function library.
- **Reducible?** Only with a formalized zeta function, which does not exist in Mathlib as of 2026.

### Axiom 2: `XiHasOnlyRealZeros : Prop`
- **Classification**: avoidable-placeholder
- **What it does**: Declares the type of "Ξ has only real zeros" as a proposition.
- **Can it be proved in Lean?** Same issue — needs a formalized Xi function.
- **Reducible?** Only with extensive Mathlib infrastructure.

### Axiom 3: `rh_iff_xi_real : RiemannHypothesis ↔ XiHasOnlyRealZeros`
- **Classification**: external-theorem
- **What it does**: States the classical equivalence between RH and Ξ having only real zeros.
- **Source**: Titchmarsh §2.10; standard in analytic number theory.
- **Can it be proved in Lean?** In principle, with a formalized zeta function and Xi function. Not currently feasible.
- **Reducible?** No — requires deep Mathlib development.

### Axiom 4: `phi_positive : Prop`
- **Classification**: classical-property
- **What it does**: Declares "Φ > 0" as a proposition type.
- **Can it be proved in Lean?** The statement itself is just a type declaration. The *proof* of Φ > 0 could be formalized: each φ_n(u) > 0 for u ≥ 0 because 2πn²e^{2u} - 3 > 0 for n ≥ 1, u ≥ 0. This is elementary algebra.
- **Reducible?** Yes, with moderate effort — requires formalizing the series and elementary inequalities.

### Axiom 5: `phi_even : Prop`
- **Classification**: classical-property
- **What it does**: Declares "Φ is even" as a proposition type.
- **Can it be proved in Lean?** Requires formalizing the Jacobi theta functional equation. This is a nontrivial but known result.
- **Reducible?** With significant effort. The theta functional equation is not in Mathlib as of 2026.

### Axiom 6: `phi_integrable : Prop`
- **Classification**: classical-property
- **What it does**: Declares "Φ ∈ L¹" as a proposition type.
- **Can it be proved in Lean?** Requires formalizing the superexponential decay and Lebesgue integration. Mathlib has L¹ spaces but not the specific series bounds.
- **Reducible?** With moderate effort, given Mathlib's integration infrastructure.

### Axiom 7: `phi_log_concave : Prop`
- **Classification**: computational-certificate
- **What it does**: Declares "Φ is log-concave" as a proposition type.
- **Can it be proved in Lean?** This is the core computational claim. Proving it would require either:
  - Importing the IA certificate into Lean (very difficult — no mature framework for this)
  - Reproducing the entire IA computation in Lean (impractical)
- **Reducible?** Not with current technology. This is the most important axiom.

### Axiom 8: `polya_debruijn`
- **Classification**: external-theorem
- **What it does**: States: phi_positive → phi_even → phi_integrable → phi_log_concave → XiHasOnlyRealZeros
- **Source**: Pólya 1927, de Bruijn 1950
- **Can it be proved in Lean?** Requires formalizing the theory of entire functions of finite order, Laguerre-Pólya class, and Laplace transform theory. This is a deep result.
- **Reducible?** No — this would be a major formalization project in its own right.

### Axiom 9: `h_pos_for_nonneg : Prop`
- **Classification**: algebraic-identity
- **What it does**: Declares h(u) = 2πe^{2u} - 3 > 0 for u ≥ 0.
- **Can it be proved in Lean?** Yes. This is: 2π ≈ 6.28 > 3, and e^{2u} ≥ 1 for u ≥ 0, so 2πe^{2u} ≥ 2π > 3.
- **Reducible?** Yes, easily — requires only `Real.pi_pos` and `Real.exp_pos` from Mathlib.

### Axiom 10: `log_h_d2_neg : Prop`
- **Classification**: algebraic-identity
- **What it does**: Declares (log h)'' < 0.
- **Can it be proved in Lean?** Yes. (log h)'' = -24πe^{2u}/h² < 0 since all factors are positive.
- **Reducible?** Yes, with moderate effort — requires differentiation of composed functions.

### Axiom 11: `log_phi1_d2_neg : Prop`
- **Classification**: algebraic-identity
- **What it does**: Declares (log φ₁)'' < 0 for u ≥ 0.
- **Can it be proved in Lean?** Yes. (log φ₁)'' = (log h)'' - 4πe^{2u}, both terms negative.
- **Reducible?** Yes — follows from axioms 9, 10, and the chain rule.

### Axiom 12: `tail_decay : Prop`
- **Classification**: algebraic-identity
- **What it does**: Declares the tail decay bound (e^{-πn²e^{2u}} ≤ e^{-3π}·e^{-πe^{2u}} for n ≥ 2).
- **Can it be proved in Lean?** Yes. Equivalent to (n²-1)e^{2u} ≥ 3, which holds since n²-1 ≥ 3 and e^{2u} ≥ 1.
- **Reducible?** Yes, easily.

### Axiom 13: `exp_neg_3pi_bound : Prop`
- **Classification**: algebraic-identity
- **What it does**: Related bound on e^{-3π}.
- **Can it be proved in Lean?** Yes — this is a numerical inequality.
- **Reducible?** Yes — Lean's `norm_num` or `native_decide` could handle this with appropriate setup.

### Axiom 14: `ia_verification_0_to_1 : Prop`
- **Classification**: computational-certificate
- **What it does**: Declares that Q_Φ < 0 on [0,1] has been verified by IA.
- **Can it be proved in Lean?** Not practically. This encodes the result of 52,898 interval arithmetic evaluations. One could in principle:
  - Generate a Lean proof term from the IA computation (certificate translation)
  - Use Lean's `native_decide` with a verified IA kernel
  Neither approach is mature.
- **Reducible?** Not with current technology. This is the second most important axiom.

### Axiom 15: `perturbation_bound_above_1 : Prop`
- **Classification**: computational-certificate
- **What it does**: Declares that the perturbation bound holds for u > 1.
- **Can it be proved in Lean?** Partially. The algebraic core part (axiom 11) could be formalized. The explicit constant C=204 computation could be translated. The "monotonicity for u > 1" part would need work.
- **Reducible?** Partially — the algebraic part is feasible, the numerical constant computation is harder.

### Axiom 16: `log_concavity_from_components`
- **Classification**: algebraic-identity
- **What it does**: States: ia_verification_0_to_1 → log_phi1_d2_neg → perturbation_bound_above_1 → phi_log_concave
- **Can it be proved in Lean?** In principle, yes — this is the logical assembly of the three components covering [0,1] and (1,∞). The proof would need to show that these two regions cover [0,∞) and that the conditions imply Q_Φ < 0 everywhere.
- **Reducible?** Yes, with moderate effort — this is a structural lemma, not a deep result.

---

## Reduction Priority

### Tier 1: Immediately reducible (could be done now with Mathlib)
1. `h_pos_for_nonneg` (axiom 9) — simple inequality 2π > 3
2. `tail_decay` (axiom 12) — simple inequality (n²-1)e^{2u} ≥ 3
3. `exp_neg_3pi_bound` (axiom 13) — numerical bound
4. `log_concavity_from_components` (axiom 16) — structural assembly

### Tier 2: Reducible with moderate Mathlib work
5. `log_h_d2_neg` (axiom 10) — differentiation + sign analysis
6. `log_phi1_d2_neg` (axiom 11) — follows from 10 + chain rule
7. `phi_positive` (axiom 4) — elementary series positivity
8. `phi_integrable` (axiom 6) — L¹ from dominated convergence

### Tier 3: Reducible but requires significant formalization
9. `phi_even` (axiom 5) — needs Jacobi theta functional equation
10. `perturbation_bound_above_1` (axiom 15) — partial: algebra is feasible, constant computation is hard

### Tier 4: Not reducible with current technology
11. `rh_iff_xi_real` (axiom 3) — needs formalized zeta/xi functions
12. `polya_debruijn` (axiom 8) — needs entire function theory
13. `phi_log_concave` (axiom 7) — encodes computational certificate
14. `ia_verification_0_to_1` (axiom 14) — encodes 52,898 IA evaluations
15. `RiemannHypothesis` (axiom 1) — type declaration, needs zeta
16. `XiHasOnlyRealZeros` (axiom 2) — type declaration, needs xi

---

## Assessment

The Lean formalization serves as a **proof structure checker**, not a proof verifier. It confirms that IF all 16 axioms hold, THEN the proof logically follows. This is valuable for catching structural errors (e.g., using the wrong hypothesis in the wrong place), but it does not independently verify any computational claim.

### What a reviewer will note

1. **Zero `sorry` is good** — it means the proof structure is complete with no holes disguised as `sorry`.
2. **But 16 axioms is a lot.** The formalization essentially axiomatizes the entire mathematical content and only proves the trivial top-level implication.
3. **The most important axioms (7, 8, 14) cannot currently be reduced.** These are the computational certificate, Pólya's theorem, and the IA verification — exactly the claims that carry the proof's weight.
4. **Tier 1 axioms should be proved.** There is no reason to axiomatize 2π > 3. Proving these would reduce the axiom count from 16 to 12 and signal good faith.
5. **The `Prop` declarations (axioms 1, 2, 4–7) are structurally necessary** but could be replaced with concrete definitions if Mathlib had the infrastructure. They are not "cheating" — they are honest declarations of what the formalization does not yet formalize.

### Recommendation

Reduce axiom count from 16 to ≤10 by proving Tier 1 items (axioms 9, 12, 13, 16). This is straightforward Lean 4 work and would meaningfully strengthen the formalization. Tier 2 items would bring the count to ~6, which is a strong position for a computer-assisted proof paper.
