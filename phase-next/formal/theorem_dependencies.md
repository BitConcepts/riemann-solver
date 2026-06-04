# Theorem Dependency Graph

Tracks logical dependencies between statements in the proof chain from certified log-concavity
to the Riemann Hypothesis. Updated as new lemmas are identified.

---

## Current proof chain

```
T1: Φ(u) > 0 for all u ∈ ℝ                               [PROVED — standard]
T2: Φ(-u) = Φ(u)                                          [PROVED — standard]
T3: Φ ∈ L^1(ℝ)                                            [PROVED — standard]
T4: Φ is real analytic                                     [PROVED — standard]
T5: Φ decays superexponentially                            [PROVED — standard]
T6: (log Φ)''(u) < 0 for all u ≥ 0 (strict log-concavity) [PROVED — IA certificate]
  └── Certificate: Q_Φ < 0 on [0,1] (52,898 subintervals)
  └── Algebraic core: (log φ₁)'' < 0 for u ≥ 0
  └── Tail bound: C = 204, u > 1

T7: Xi(z/2) = (1/2) ∫ Φ(u) e^{iuz} du                   [PROVED — standard]
T8: RH ⟺ ∀ z: Ξ(z) = 0 → Im(z) = 0                     [PROVED — standard]

OPEN BRIDGE:
T9: T1 + T2 + T3 + T4 + T5 + T6 → ∀ z: ∫Φ(u)e^{iuz}du = 0 → Im(z) = 0
                                                           [OPEN — Hypothetical Criterion 13]

CONDITIONAL:
T10: T9 + T6 → T8 (RH)                                   [CONDITIONAL on T9]
```

---

## Dependency diagram

```
T1  T2  T3  T4  T5  T6
 \   \   |   |  /  /
  \   \  |   | /  /
   ╔═══════════════╗
   ║   H13 Bridge  ║  ← T9 (OPEN)
   ╚═══════════════╝
           |
          T7
           |
          T8 (RH)  ← CONDITIONAL on T9
```

---

## Sublemmas added from research iterations

*(None yet — updated as iterations run.)*

---

## Notes

- T6 is the strongest proved statement in this project.
- T9 is the single missing step.
- No additional lemmas between T6 and T9 have been identified yet.
- Any new lemma that reduces T9 to a known theorem should be added here immediately.
