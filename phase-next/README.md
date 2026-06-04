# Phase-next: RH Bridge Research Loop

The `phase-next` branch investigates possible theorem bridges from certified log-concavity of the
Riemann–Jacobi kernel to real-rootedness of its Fourier transform. This is exploratory and does
not alter the current manuscript's unconditional claim.

---

## Current status

```
PROVED:      Certified strict log-concavity of Φ on [0, ∞).
OPEN:        Log-concavity-to-real-rootedness bridge (Hypothetical Criterion 13).
CONDITIONAL: RH is a consequence under Hypothetical Criterion 13, if H13 holds.
```

---

## Clay-prize-relevant paths

| Path | Description | Status |
|------|-------------|--------|
| 1 | Prove Hypothetical Criterion 13 | OPEN |
| 2 | Find verified existing theorem supplying the bridge | OPEN |
| 3 | Find alternate route or disprove H13 | OPEN |

---

## Iterative research loop

Each iteration has six steps:

1. **Source scan** — Find or inspect one theorem/source. Extract exact hypotheses and conclusion. Add to `literature/source_index.md`.
2. **Match test** — Compare theorem to H13 and Φ. Update `reports/bridge_status_matrix.md`.
3. **Falsification test** — Try to find a counterexample to the candidate theorem. Log kernel class and result.
4. **Computation** — If a route gives concrete inequalities, write interval/numerical scripts. Store outputs in `experiments/outputs/`.
5. **Formalization planning** — Add any provable sublemma to `formal/theorem_dependencies.md`. Mark what could be Lean-formalized.
6. **Decision** — PROMOTE / HOLD / REJECT.

Each iteration must end with:

```
## Iteration verdict

- Route:
- New evidence:
- Does it advance path 1, 2, or 3?
- Remaining gap:
- Next action:
```

---

## Claim discipline

Every claim must carry one of these tags:

```
PROVED
COMPUTATION
CONJECTURE
SOURCE-CLAIM
COUNTEREXAMPLE-CANDIDATE
REJECTED
OPEN
```

Never promote COMPUTATION to PROVED without a written proof or rigorous interval/formal certificate.
Never promote a SOURCE-CLAIM without exact theorem text and hypothesis matching.
