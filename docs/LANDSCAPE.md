# RH Proof Landscape: Verification Survey (May 2026)

This document surveys publicly available claimed proofs or proof-relevant
results for the Riemann Hypothesis as of May 2026. Each entry notes the
approach, publication status, and any verification we were able to perform.

This is a factual survey, not a critique. We include our own work for
completeness and apply the same criteria to all entries.

## Tier 1: Peer-reviewed programs (no complete proof claimed)

### Connes spectral program
- **Paper**: Connes (2026), J. Open Math. Problems 2(1), 1-52
- **Status**: Survey + new results. Explicitly does NOT claim proof.
- **Gap**: Convergence of det_reg to Xi function (CCM 2025, Section 8)
- **Our verification**: CvS Galerkin reproduced at 6 cutoffs (c=13..47).
  Eigenvalue plateau confirmed. Sliwinski bound verified.

### Griffin-Ono-Rolen-Zagier Jensen polynomials
- **Paper**: PNAS 116(23), 2019
- **Status**: Proves Jensen polynomial hyperbolicity for each degree d
  (with finitely many exceptions in n). Does NOT prove RH.
- **Verification**: Well-established, peer-reviewed.

### Rodgers-Tao (de Bruijn-Newman constant)
- **Paper**: Forum of Mathematics, Pi 8, 2020
- **Status**: Proves Lambda >= 0. Combined with Lambda <= 0.22 (Polymath15).
  RH is equivalent to Lambda = 0.
- **Verification**: Published, peer-reviewed, widely accepted.

## Tier 2: Submitted or under review

### Yamaguchi "Gram Jacobi / Spectral Determinant" (May 2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.20357668; GitHub danalec/riemann
- **Approach**: Gram Jacobi matrix J_N whose eigenvalues approximate imaginary
  parts of zeta zeros. Spectral determinant D_N/xi(1/2+iz) → c via Hadamard
  rigidity. Self-adjoint J_inf ⇒ real eigenvalues ⇒ RH.
- **Status**: Not peer-reviewed. Most technically detailed independent attempt.
  77 C proof programs, 3 independent proof paths (A/B/C), Bitcoin-timestamped.
- **Gaps**: Self-adjointness of J_inf in N→∞ limit requires domain analysis not
  provided. Hadamard convergence D_N/xi→c needs uniform eigenvalue spacing.
- **Our verification**: `audit_yamaguchi_2026` in `audit_external.py`.
  Heat kernel ratio (0.9999996) is computable; analytic closure not verified.

### Geiger even-dominance
- **Source**: Zenodo 10.5281/zenodo.19035640, submitted to Communications in Mathematics (2026-03-27)
- **Approach**: Even dominance of Weil QF via CAP certificates + PNT Transfer
- **Status**: Under peer review (2+ months, no verdict)
- **Our verification**: Even-dominance certificates reproduced at 6 lambda values.
  Consistent with claims. Proposition A6 interpolation is the key step.

## Tier 3: Preprints (not peer-reviewed)

### arXiv 2408.15135 — Hilbert-Polya Hamiltonian (Aug 2025 v11)
- **Source**: arXiv:2408.15135 (v11, Aug 2025)
- **Approach**: Self-adjoint Hamiltonian R-hat = -D-hat - i*T-hat/(1+exp(-T-hat))
  built from Berry-Keating and Bessel operators. Boundary condition Ψ_s(0)=0
  requires η(s)=0 (Dirichlet eta zeros). Self-adjointness ⇒ real eigenvalues
  ⇒ RH for SIMPLE zeros. Restricts claim to simple nontrivial zeros.
- **Status**: arXiv preprint, 11 versions. Not peer-reviewed.
- **Gaps**: Domain analysis for D-hat ∩ T-hat not completed. Eta zeros at
  z_k = 1+2πik/ln(2) also satisfy boundary condition; spectral complications.
- **Our assessment**: More rigorous construction than most. Multiple versions
  suggest ongoing refinement. Domain gap is the key missing step.

### ERURH — Robert Duran conditional proof (Feb 2026)
- **Source**: HAL hal-05501445; Zenodo 10.5281/zenodo.18010407
- **Approach**: Energy-inertia framework. Reduces RH for xi_alpha to finite
  numerical certificates + classical analytic assumptions A/B/C. Full Lean 4
  formalization of conditional implication ERURH_GlobalAssumptions ⇒ RH(xi_alpha).
- **Status**: Preprint (HAL). Lean proof genuine but explicitly conditional.
- **Gaps**: Requires external proofs of A (large sieve), B (spectral decay),
  C (RMS window hypotheses). xi_alpha is zeta-like but connection to standard
  Riemann zeta requires Assumption 11.1.
- **Our assessment**: Most honest framing in the class. Conditional reduction
  with explicit assumption list is the gold standard for this style of work.

### Singh Khalsa "1% Proof" Li-kernel reduction (Feb 2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.18726797; IIT Bhubaneswar/Mandi/Delhi
- **Approach**: Does NOT claim to prove RH. Reduces RH to a single quantitative
  inequality: any off-line zero produces exponentially growing Li coefficient
  contribution. Uses Laguerre-weighted explicit formula.
- **Status**: Preprint (Zenodo). Explicitly a reduction, not a completion.
- **Our assessment**: One of the most honest papers in this landscape. The
  Li coefficient framework is consistent with our own `li_criterion.py`.
  `audit_singh_khalsa_2026` in `audit_external.py` verifies the framing.

### Ladjeroud — Hilbert-Polya via SUSYQM (Nov 2025)
- **Source**: HAL hal-05342267; Centre Universitaire de Mila, Algeria
- **Approach**: Constructs Hilbert-Polya operator H using supersymmetric quantum
  mechanics (SUSYQM) with shape invariance potentials. 'Algorithmic parameters'
  B are defined to produce the zeta zeros as eigenvalues.
- **Status**: Preprint (HAL). Not peer-reviewed.
- **Critical issue**: Circular construction — zeta zeros are inputs to the
  operator definition, not outputs. Self-adjointness of such an operator does
  not imply the zeros are on the critical line.

### Gershon log-concavity (April 2026)
- **Source**: Preprints.org 202604.1513
- **Approach**: Same log-concavity approach as this work
- **Status**: Not peer-reviewed. Lean 4 partial formalization.
- **Issues identified**: Perturbation bound inequality (equation 16) goes
  the wrong direction. Claims exp(-t^4) is a counterexample to log-concavity
  implying real zeros; this is incorrect per Csordas-Varga 1989 Example 2.1.

### Log-concavity preprint (April 2026)
- **Source**: Preprints.org 202604.0159
- **Approach**: Same log-concavity approach
- **Status**: Not peer-reviewed. Claims Lean 4 formalization.
- **Issues identified**: Same perturbation bound issue as Gershon.
  Interval arithmetic verification covers [0, 0.5] only (vs our [0, 1.0]).

### This work
- **Source**: BitConcepts/riemann-solver
- **Approach**: Log-concavity of Xi kernel via Polya 1927
- **Status**: Not peer-reviewed. Paper available. Lean 4 scaffold.
- **Self-falsification**: 32 attacks, 1 bug found and fixed (g'' coefficient).
  52,898 IA subintervals certified with corrected formula.

## Tier 4: Unverified claims

### Meghani "Completion-Locked Hilbert-Polya" (Jan-Apr 2026, v3)
- **Source**: Zenodo DOI: 10.5281/zenodo.19487972; claims UPenn affiliation
- **Approach**: No-tuning Hilbert-Polya via Archimedean completion as rigid
  boundary condition and zeta-regularized Fredholm determinant.
- **Status**: 3 versions Jan-Apr 2026; 5 companion Zenodo records. Not peer-reviewed.
- **Assessment**: Key identification of Fredholm determinant with completed zeta
  not independently verifiable. Volume of companion papers does not substitute
  for a single complete proof.

### Morato de Dalmases "600-cell proof" (Mar 2026, v5)
- **Source**: Zenodo DOI: 10.5281/zenodo.19112358; CronNet Holo Initiative
- **Approach**: Dirac operator from 600-cell {3,3,5} geometry.
- **Status**: Not peer-reviewed. 11 companion PDFs.
- **Critical issues** (3 critical, per `audit_morato_2026`):
  1. Claims RH + GRH + Goldbach + Twin Primes + Collatz simultaneously.
  2. 600-cell angular defect δ₀~6.8° is a free parameter, not derived.
  3. Goldbach from heat kernel positivity is logically invalid.

### Chua — Robin criterion (Jan 2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.18323203; submitted to Duke Math Journal
- **Approach**: Robin's criterion: σ(n) < e^γ n log log n ∀ n≥5041 ⟺ RH.
- **Status**: Submitted to Duke Mathematical Journal; no verdict published.
- **Assessment**: Legitimate equivalence (Robin 1984). Proof steps for the
  inequality not independently verified.

### Priest — Zero-flux Friedrichs operator (Sep 2025)
- **Source**: Zenodo DOI: 10.5281/zenodo.17228441; author is "jeweller by trade"
- **Approach**: Resonance kernel R_α(x) = (x-1/2)²e^{-α(x-1/2)²}. L²-stable
  contradiction mechanism: off-line zero forces L² divergence.
- **Status**: Not peer-reviewed.
- **Critical issue**: Kernel is centered at 1/2 by construction, encoding the
  critical line as an assumption rather than deriving it.

### McGirl — phi-separation via total positivity (Jan-Mar 2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.18226408; GitHub grapheneaffiliate;
  AI collaborators: Claude, Grok, Gemini, GPT
- **Approach**: phi-kernel K_phi(x) = phi^{-|x|/δ} is PF_∞ (Schoenberg 1951).
  De Bruijn-Newman backward flow from t=1/2 via phi-Gram determinant monotonicity.
  Repulsive zero dynamics prevents collisions backward to t=0.
- **Status**: Preprint (Zenodo); Lean partial; AI co-authored. Not peer-reviewed.
- **Gaps**: Backward flow non-collision requires more than local repulsion.
  E8 lattice connection is not mathematically derived.

### A.I. Visions LTD "Semilocal Spectral Descent" (April 2026)
- **Source**: Zenodo 19546495
- **Approach**: Claims form stabilization bypasses CCM convergence gap
- **Status**: Not peer-reviewed. Blockchain timestamped.
- **Assessment**: Our eigenvector mode analysis shows the eigenvector
  restructures significantly (7-22 modes) as cutoff increases, contradicting
  the paper's implicit assumption of eigenvector stability.

### Bhattacharjee "Liouville-Collar Closure" (April 2026)
- **Source**: IJRST Vol 16, Issue 2
- **Approach**: Liouville function square identity -> spectral large sieve -> RH
- **Status**: Published in non-specialist journal.
- **Assessment**: Not independently verified.

### Louiz "Super-Exponential Kernel" (May 2026)
- **Source**: DOI: 10.13140/RG.2.2.35504.32004 (ResearchGate); validation report May 2026
- **Approach**: Super-exponential Möbius kernel R(c) = Sμ(c)/S(c) as analytic proxy
  for 1/ζ(1/c). Mapping s = 1/c connects Re(c) > 1 to critical strip.
- **Status**: ResearchGate preprint. Self-validated by Gemini DeepResearch (AI).
  No peer review. Primary and validation papers both authored by Louiz.
- **Critical issues found**:
  1. R(c) → 1 identically for all c. Super-exponential suppression erases
     all n≥2 Möbius information because μ(1)=1 makes the n=1 terms identical
     in S and Sμ. The kernel does not encode ζ(s).
  2. Functional equivalence R(1/s)=1/ζ(s) asserted via invalid analytic
     continuation argument (matching at single boundary limit c→∞ is not
     sufficient to identify two distinct analytic functions).
  3. Internal inconsistency: §6.1 numerics are consistent with
     f = exp(-n^c·e^c), but the paper's Lean definition uses
     f = exp(-n^c·exp(exp(c))). These differ by ~700 orders of magnitude
     at c=2. The paper contradicts itself.
  4. Lean theorem uses 'sorry' — not machine-verified.
  5. §5.2 claims Louiz 'disproved the Twin Primes Conjecture via Brun's
     upper bound'. Brun's theorem does not disprove TPC; TPC is open.
- **Our verification**: `bench_louiz_kernel.py` (numerical); `audit_louiz_2026`
  in `audit_external.py`. 3 critical + 2 warning issues documented.
- **Lessons**: Fast convergence ≠ correct target; analytic continuation requires
  open-set agreement; AI-generated Lean with sorry is not formal proof;
  internal consistency checks are mandatory.

### Various Zenodo/viXra claims
- Multiple claimed proofs posted on Zenodo and viXra (Meghani, Singh Khalsa,
  Morato de Dalmases, Duran, Wang-Fu, etc.)
- None peer-reviewed. Most have obvious gaps or circular reasoning.
- Not individually assessed.

## Notes

This survey is maintained in the repository and updated as new information
becomes available. Corrections are welcome via pull request.

The falsification framework in `falsification/` can be applied to any
claimed proof that uses the log-concavity approach.
