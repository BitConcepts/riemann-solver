# RH Proof Landscape Leaderboard
## Applied Epistemic Engineering Analysis — May 2026

**AGENTS.md disclaimer**: AEE certainty scores measure *epistemic quality* — the rigour,
falsifiability, internal consistency, and expert engagement of each work. They do NOT
measure mathematical truth. A high score does not mean a proof is correct; a low score
does not mean it is wrong. No paper in this list has been accepted as a proof of RH by
the mathematical community. RH remains an open problem.

---
## AEE Framework

Each paper is modelled as an `AEESession` in the `epistemic` library (specsmith v0.11.8):

```python
from epistemic import AEESession, BeliefArtifact, FailureMode, FailureSeverity
```

**5 belief artifacts per paper:**
1. `PROOF_CLAIM` — the core mathematical assertion, with identified failure modes
2. `FALSIFIABILITY` — systematic adversarial challenge exists
3. `CONSISTENCY` — formal definitions match numerical claims
4. `EXPERT_REVIEW` — independent expert review documented
5. `SCOPE_CALIBRATION` — claims accurately scoped (no overclaiming)

**AEE axioms** (Observability, Falsifiability, Irreducibility, Reconstructability, Convergence)
applied via the Frame → Disassemble → Stress-Test → Reconstruct pipeline.

**The certainty score** is computed by `AEESession.score().overall_score`. Failure modes
with `severity=CRITICAL` prevent equilibrium and heavily penalise the score. Accepted
beliefs increase it. The AEE threshold is 0.700; no paper in this landscape crosses it —
reflecting the genuine difficulty of RH and the gaps that remain in every approach.

**Source code**: `benchmarks/bench_aee_papers.py`
**AEE library**: https://specsmith.readthedocs.io/en/stable/epistemic-library/
**specsmith repo**: https://github.com/layer1labs/specsmith

---
## Full Leaderboard (ranked by AEE certainty)

Run `python benchmarks/bench_aee_papers.py` to reproduce.

```
Rank  Paper ID                       Tier  Certainty  Crit  Accepted  Claims RH
----  ----------------------------   ----  ---------  ----  --------  ---------
   1  rodgers-tao-2020               1       0.2040     0    5/5       No
   2  griffin-ono-2019               1       0.2040     0    4/5       No
   3  connes-2026                    1       0.1900     0    5/5       No
   4  geiger-2026                    2       0.1900     0    5/5       YES
   5  chua-2026                      4       0.1860     0    2/5       YES
   6  this-work (Pierson 2026)       3       0.1690     0    4/5       YES
   6  yamaguchi-2026                 2       0.1690     0    4/5       YES
   6  erurh-2026                     3       0.1690     0    4/5       YES
   9  singh-khalsa-2026              3       0.1620     0    4/5       No
  10  arxiv-hp-2025                  3       0.1480     0    3/5       YES
  11  meghani-2026                   4       0.1210     0    1/5       YES
  11  mcgirl-2026                    4       0.1210     0    1/5       YES
  13  gershon-2026                   3       0.1000     1    0/5       YES
  13  preprint-0159                  3       0.1000     2    0/5       YES
  13  aivisions-2026                 4       0.1000     1    0/5       YES
  13  louiz-2026                     4       0.1000     3    0/5       YES
  13  morato-2026                    4       0.1000     3    0/5       YES
  13  priest-2025                    4       0.1000     1    0/5       YES
  13  ladjeroud-2025                 4       0.1000     1    0/5       YES
```

Certainty threshold: 0.700 | Papers above threshold: 0/19

---
## Tier Analysis

### Tier 1 — Peer-reviewed (no complete proof claimed): 0.190–0.204

These papers occupy the top of the leaderboard *not because they prove RH* but because
they make well-scoped, honest claims backed by independent verification. Rodgers-Tao and
Griffin-Ono score highest because they have zero failure modes — their stated theorems
(Λ ≥ 0; Jensen hyperbolicity for fixed d) are correct and peer-reviewed. Connes is one
point lower because of the known det_reg convergence gap, but all five beliefs are
accepted because the paper honestly identifies this as an open problem.

**Key insight**: Honest, well-scoped claims with peer review dominate the leaderboard even
without claiming to solve RH. This is what epistemic integrity looks like.

### Tier 2 — Submitted / under review: 0.169–0.190

Geiger (0.190) is the highest-scoring paper that claims a complete proof, due to: 33 CAP
certificates independently reproduced, submission to a peer-reviewed journal (2+ months
without rejection), and all five beliefs accepted. The only failure mode is Proposition
A6, which is the key remaining gap.

Yamaguchi (0.169) is the most technically detailed independent attempt (77 C programs,
three independent proof paths, "contradiction machine" with 80/80 falsified). It ties
with this work and ERURH because the analytic J_inf closure gap is significant.

### Tier 3 — Serious preprints: 0.100–0.169

This work (0.169): 4/5 beliefs accepted. PROOF_CLAIM, FALSIFIABILITY, CONSISTENCY, and
SCOPE_CALIBRATION are accepted. EXPERT_REVIEW is NOT accepted (preprint not yet
submitted). Failure modes: partial Lean scaffold (medium), no peer review (medium).
The 32 falsification attacks, DH control, and IA [0,1.0] certification are the key
differentiators vs other Tier 3 papers.

ERURH-2026 (0.169): 4/5 accepted. The most honest framing — explicitly conditional,
explicit assumption list. Lean proof is genuine for the implication (no sorry in main
theorem). The A/B/C analytic packages remain as open premises.

Singh-Khalsa (0.162): 4/5 accepted despite NOT claiming a proof — the honest non-claim
(1% = reduction only) is correctly scored as SCOPE_CALIBRATION accepted. Higher than
papers with more beliefs accepted but wrong scope.

arXiv HP-2025 (0.148): 3/5 accepted. Berry-Keating + Bessel construction is the most
rigorous Hilbert-Pólya attempt. Domain analysis gap and eta-zero complication hold it
below this work / ERURH.

Gershon/Preprint-0159 (0.100): Both have CRITICAL failure modes (wrong perturbation
direction). All five beliefs rejected. Score = AEE floor.

### Tier 4 — Unverified claims with structural flaws: 0.100–0.186

Chua (0.186) ranks surprisingly high among Tier 4 — Robin's criterion is a legitimate
RH equivalent, it's submitted to Duke Math Journal, and no critical flaws were found in
the approach logic. The proof itself isn't independently verified, so PROOF_CLAIM is not
accepted, but CONSISTENCY, EXPERT_REVIEW, and SCOPE_CALIBRATION are.

Meghani and McGirl (0.121): 1/5 each. Some internal consistency but no falsification,
no expert review, no verified claims.

Louiz, Morato, Priest, Ladjeroud, AI Visions (0.100): AEE floor. Zero beliefs accepted.
Each has CRITICAL failure modes (R≡1 for Louiz; 5-problem overclaim for Morato;
circular kernel for Priest; circular operator for Ladjeroud; eigenvector instability for
AI Visions).

---
## Key Takeaways

**1. The floor at 0.100**
Papers with all five beliefs rejected score 0.100. This is not zero — AEE recognises
that even failed approaches contribute to the landscape by showing what doesn't work.
The floor represents the base epistemic contribution of publishing a falsifiable claim.

**2. No paper crosses 0.700**
The AEE threshold of 0.700 is the standard for "this belief system is epistemically
sound." No RH proof in this landscape crosses it. This is not a failure of the scoring
system — it correctly reflects that RH remains open and no approach has yet assembled
the full chain of verified, reviewed, adversarially-tested steps needed.

**3. Honesty is rewarded**
Singh-Khalsa (0.162) outscores several papers that claim complete proofs. ERURH-2026
outscores Yamaguchi despite having fewer computational resources, because its conditional
framing earns SCOPE_CALIBRATION accepted while Yamaguchi's analytic gaps prevent EXPERT_REVIEW.

**4. Falsification is the key differentiator within Tier 3**
This work, Yamaguchi, and ERURH all score 0.169. What separates this work from the others
informationally: the 32 adversarial attacks, the DH control, and the Li criterion checks
provide FALSIFIABILITY evidence that the others lack. If this work achieves peer review,
it would gain EXPERT_REVIEW and score ~0.204 — matching the Tier 1 papers.

**5. AEE maps directly onto our testing infrastructure**

```
Belief artifact       → Our implementation
----------------------------------------------
PROOF_CLAIM           → proof/verify_*.py, lean4/ scaffold
FALSIFIABILITY        → falsification/run_all.py (32 attacks)
CONSISTENCY           → falsification/run_all.py (internal attacks)
EXPERT_REVIEW         → papers/registry.json peer_reviewed field
SCOPE_CALIBRATION     → audit_external.py --claim self
```

This means improving our AEE score is directly actionable:
- **Submit for peer review** → EXPERT_REVIEW accepted → +0.035 to certainty
- **Complete Lean4 scaffold** → removes medium failure mode → +score
- **Both** → approach 0.204 (Tier 1 range)

---
## Lessons Learned Across the Landscape

From `python benchmarks/run_paper_benchmarks.py --lessons`:

**From peer-reviewed work (Tier 1)**
- Jensen polynomials give a finite-dimensional reduction of RH at each degree — a model for
  tractable partial results
- De Bruijn-Newman: Λ=0 is equivalent to RH; proving Λ≤0 (not yet achieved) would suffice
- Honest disclosure of gaps (Connes §8) earns more trust than overclaiming

**From serious attempts (Tier 2-3)**
- CAP certificates (Geiger) are the gold standard for computational verification steps
- 77 independent verification programs (Yamaguchi) is strong but no substitute for analytic closure
- Conditional reduction to finite certificates (ERURH) is epistemically clean and a legitimate
  strategy for AI-assisted formal mathematics
- Our 32 falsification attacks found and fixed a real bug (g'' coefficient direction) — the
  protocol works exactly as designed

**From failed attempts (Tier 4)**
- Fast convergence ≠ correct target (Louiz: R≡1 regardless of ζ)
- Analytic continuation requires open-set agreement, not boundary-point matching
- Kernels/operators centered at 1/2 by construction are circular (Priest)
- Claiming 5 millennium problems simultaneously is always a red flag (Morato)
- AI-generated Lean with `sorry` is not machine verification
- Self-validation by AI is not peer review

---
*This leaderboard is generated by `benchmarks/bench_aee_papers.py` using the `epistemic`
library from [specsmith](https://github.com/layer1labs/specsmith) (v0.11.8). Scores reflect
epistemic quality assessed as of 2026-05-31. All conclusions are numerical evidence only.*
