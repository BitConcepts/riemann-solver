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

### RH for Hyperelliptic Curves (Lean 4 formalization, Feb 2026)
- **Source**: GitHub math-inc/RiemannHypothesisCurves; ~4000 lines Lean 4
- **Approach**: Bombieri-Stepanov polynomial method proving |#solutions - q| ≤ 5m√q
  for hyperelliptic curves y²=f(x) over F_q. This is RH for function fields (Weil
  theorem), NOT classical RH.
- **Status**: Complete Lean4 proof. Gold standard for AI-assisted formal verification.

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

### Bhattacharjee "Liouville-Collar Closure" (April 2026)
- **Source**: IJRST Vol 16, Issue 2, DOI:10.37648/ijrst.v16i02.002
- **Approach**: Liouville function L(X), dyadic collar partition, Kuznetsov spectral
  formula, β-large-sieve dispersion bound. RH via Littlewood-Denjoy.
- **Status**: Published in IJRST (broad-scope journal, peer-reviewed). Kuznetsov
  spectral cancellation requires conductor uniformity not established.

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

### Structural Resolution (Anonymous, Jan 2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.18365022
- **Approach**: Second-difference observables + oscillatory probes + β-large-sieve
  contradiction. Off-critical zero exceeds large-sieve dispersion bound.
- **Status**: Unvalidated. 'Globally locked parameter regime' is circular.

### Tensor-Sieve p-adic Framework (ryanncode, April 2026)
- **Source**: GitHub ryanncode/tensor-sieve; based on MeLoCoToN/FTNILO arXiv preprints
- **Approach**: Non-Archimedean F₁ algebraic curve, Krein space, p-adic Bruhat-Tits
  tree shift operator, adelic harmonic analysis. Phase 1 only: GUE-like spacing.
- **Status**: Phase 1 executable only. No unconditional proof claimed.

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

## Tier 5: Pseudoscientific frameworks

### Motanova "Riemann-Adelic" / QCAL (2025-2026)
- **Source**: Zenodo DOI: 10.5281/zenodo.17281699; GitHub motanova84/Riemann-adelic
- **Approach**: S-finite adelic systems wrapped in QCAL (Quantum Coherent Algebraic
  Logic) framework. Claims 'cosmic coherence' at f₀=141.7001 Hz connecting Riemann
  zeros to QCD vacuum modes and consciousness. Claims 5 millennium problems solved.
- **Status**: Pseudoscientific QCAL layer. Lean code uses sorry extensively.
  Mathematical core (adelic/Fredholm) not independently reviewable due to noise.

### Various Zenodo/viXra claims
- Multiple claimed proofs posted on Zenodo and viXra (Meghani, Singh Khalsa,
  Morato de Dalmases, Duran, Wang-Fu, etc.)
- None peer-reviewed. Most have obvious gaps or circular reasoning.
- Not individually assessed.

---

## Research Loop Update (2026-05-31)

### Connes (2026), arXiv:2602.04022 — Major survey + new strategy
- **Source**: arXiv:2602.04022v1, "The Riemann Hypothesis: Past, Present and a
  Letter Through Time", February 2026.
- **Approach**: Comprehensive 165-year survey plus a new "Letter to Riemann"
presenting a strategy using prolate spheroidal wave functions, the Poisson
formula, and the approximation k_λ → k as λ→∞. Proves convergence zeros
lie exactly on the critical line for every finite truncation.
- **Convergence gap status**: **STILL OPEN** (confirmed in §6). Connes
  explicitly frames §6.5 "Convergence of the Fourier transforms" and §6.6
  "Remaining steps" as open problems, not resolved results. The spectral
  convergence gap from CCM 2025 §8 is referenced as open.
- **New connection**: Information theory / prolate wave operator as the
  analytic bridge (§7.6). This is the direction our run_bridge.py Phase 9
  (Shannon analysis) follows.
- **Impact for this project**: §6.5 is exactly the convergence gap we are
  trying to address. No closed proof yet.

### Sliwinski (2026), arXiv:2601.12133 — Inverse-logarithmic lower bound
- **Source**: arXiv:2601.12133, "Spectral Analysis of the D^{λ,N}_log Operators",
  January 2026.
- **Key result**: Proves ε(λ, N) ≥ 1/(4 ln λ) as a *lower bound* on the
  Mean Absolute Error between the CvS/CCM spectrum and the Riemann zeros.
  Convergence is at most inverse-logarithmic; if no faster rate holds,
  convergence to the Riemann zeros is extremely slow.
- **Consequence**: If ε → 0 only as 1/ln λ, the N-sweep used by Groskin
  (fast convergence in c at fixed N) is a finite-N artifact, not the
  continuum limit. This partially explains why nine convergence models
  failed in Groskin (2026).
- **Impact**: Warns against interpreting fast c-convergence as evidence
  for the continuum limit. The proof is Heisenberg-based (uncertainty
  principle on H_λ = L²([λ⁻¹,λ], d*u)).

### Real Sociedad Española de Física (Zenodo March 2026)
- **Source**: Zenodo 10.5281/zenodo.19355650, "Spectral Properties of the
  Truncated Weil Operator & Numerical Verification of Weil Positivity"
- **Unconditional results**: Proves 5 results including resolvent
  convergence rate O(Λ⁻¹/²), J-self-adjointness, Hilbert-Schmidt
  decomposition.
- **Obstruction identified**: Proves norm convergence of truncated operators
  to the prolate projection is **IMPOSSIBLE**, ruling out the most direct
  convergence route. RH reduces to a single analytic statement:
  "asymptotic kernel invisibility" as Λ→∞.
- **Impact**: Removes one candidate proof strategy but narrows the gap
  to a concrete falsifiable condition.

### Michałowski (Feb 2026), arXiv:2602.20313 — De Bruijn-Newman kernel ∉ PF5
- **Source**: arXiv:2602.20313, "On the Pólya Frequency Order of the
  de Bruijn-Newman Kernel"
- **Result**: Proves K(u)=Φ(|u|) is not a Pólya frequency function of
  order 5 (PF5). The 5×5 Toeplitz minor has certified negative determinant
  −1.85×10⁻⁹ (80-digit interval arithmetic).
- **Impact on Lambda bound**: Does not change Λ ≤ 0.2 (Platt-Trudgian 2021).
  Total positivity (PF∞) would imply all zeros real, so PF5 failure means the
  kernel is not totally positive. No new upper/lower bound on Λ.

### Gershon (April 2026, preprints.org) — Claimed Λ = 0
- **Source**: preprints.org 10.20944/preprints202604.1513.v1,
  "The De Bruijn-Newman Constant Is Zero"
- **Claim**: Proves Λ = 0 (which is RH) via strict log-concavity κ ≥ 19.24,
  Jensen polynomial hyperbolicity Kd,n < 0 for d ≤ 22, and a dissipation
  bound on Dr(n).
- **Status**: NOT peer-reviewed. The log-concavity result (Part I) is
  consistent with our proof (it is a strengthening of our IA result).
  The Λ = 0 conclusion in §11 requires the dissipation bound S ≤ 19.41,
  which depends on 10,822-point interval arithmetic. The passage from
  log-concavity to all-zeros-real is non-trivial and requires Pólya TP∞,
  not just TP2. Not independently verified.
- **Impact**: The κ ≥ 19.24 log-concavity lower bound strengthens our IA
  result (we certify Q_Phi < 0; Gershon gives a quantitative bound on the
  curvature). Worth tracking.

### Lambda upper bound status (2026-05-31)
- Best rigorous upper bound: **Λ ≤ 0.2** (Platt-Trudgian 2021; tighter
  than Polymath15's 0.22 from 2019).
- No published improvement in 2025-2026 found by this search.
- Gershon (2026) claims Λ = 0 but not peer-reviewed.

---

## Notes

This survey is maintained in the repository and updated as new information
becomes available. Corrections are welcome via pull request.

The falsification framework in `falsification/` can be applied to any
claimed proof that uses the log-concavity approach.
