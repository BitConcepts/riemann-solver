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

### Geiger even-dominance
- **Source**: Zenodo 10.5281/zenodo.19035640, submitted to Communications in Mathematics (2026-03-27)
- **Approach**: Even dominance of Weil QF via CAP certificates + PNT Transfer
- **Status**: Under peer review (2+ months, no verdict)
- **Our verification**: Even-dominance certificates reproduced at 6 lambda values.
  Consistent with claims. Proposition A6 interpolation is the key step.

## Tier 3: Preprints (not peer-reviewed)

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
