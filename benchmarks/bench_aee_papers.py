# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""AEE (Applied Epistemic Engineering) analysis of all RH proof papers.

Uses the `epistemic` library (co-installed with specsmith v0.11.8) to
model each paper's claims as BeliefArtifacts and apply the AEE
Frame → Disassemble → Stress-Test → Reconstruct pipeline.

The AEE certainty score is an EPISTEMIC QUALITY metric — it measures
rigour, falsifiability, consistency, and expert engagement.
It does NOT measure mathematical truth. High score ≠ correct proof.

Belief model per paper (up to 5 artifacts):
  PROOF_CLAIM       — the core mathematical claim
  FALSIFIABILITY    — adversarial stress-testing exists
  CONSISTENCY       — formal definitions match numerical claims
  EXPERT_REVIEW     — independent expert/peer review documented
  SCOPE_CALIBRATION — claims are accurately scoped (no overclaiming)

AEE Library: https://specsmith.readthedocs.io/en/stable/epistemic-library/
specsmith:   https://github.com/layer1labs/specsmith

AGENTS.md: These are NUMERICAL/STRUCTURAL measures only.
We do NOT claim any score proves or disproves RH.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass

from epistemic import (
    AEESession,
    BeliefArtifact,
    CertaintyReport,
    ConfidenceLevel,
    FailureMode,
    FailureSeverity,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class PaperAEEResult:
    paper_id: str
    title: str
    certainty: float
    equilibrium: bool
    critical_failures: int
    total_failures: int
    beliefs_accepted: int
    beliefs_total: int
    tier: int
    claims_rh: bool


# ---------------------------------------------------------------------------
# Helper to build a standard AEE session for one paper
# ---------------------------------------------------------------------------

def _make_session(
    paper_id: str,
    # PROOF_CLAIM
    claim_propositions: list[str],
    claim_boundary: list[str],
    claim_confidence: ConfidenceLevel,
    claim_accept: bool,
    claim_failures: list[tuple[str, str, FailureSeverity]],  # (challenge, breakpoint, sev)
    # FALSIFIABILITY
    has_falsification: bool = False,
    falsification_note: str = "",
    # CONSISTENCY
    is_consistent: bool = True,
    consistency_note: str = "",
    # EXPERT_REVIEW
    has_expert_review: bool = False,
    review_note: str = "",
    # SCOPE_CALIBRATION
    scope_ok: bool = False,
    scope_note: str = "",
) -> tuple[AEESession, float]:
    """Build and run an AEE session for one paper. Returns (session, certainty)."""
    s = AEESession(paper_id, threshold=0.7)

    # 1. PROOF_CLAIM
    b = s.add_belief(
        "PROOF_CLAIM",
        propositions=claim_propositions,
        epistemic_boundary=claim_boundary,
        domain="mathematics",
        priority="critical",
        confidence=claim_confidence,
    )
    for challenge, breakpoint, sev in claim_failures:
        b.failure_modes.append(FailureMode(
            artifact_id="PROOF_CLAIM",
            challenge=challenge,
            breakpoint=breakpoint,
            severity=sev,
        ))
    if claim_accept:
        s.accept("PROOF_CLAIM")

    # 2. FALSIFIABILITY
    s.add_belief(
        "FALSIFIABILITY",
        propositions=[
            "The approach has been subjected to systematic adversarial challenge.",
            falsification_note or "Falsification protocol documented.",
        ],
        epistemic_boundary=["Adversarial testing methodology is applicable"],
        domain="methodology",
        confidence=ConfidenceLevel.HIGH if has_falsification else ConfidenceLevel.LOW,
    )
    if has_falsification:
        s.accept("FALSIFIABILITY")

    # 3. CONSISTENCY
    s.add_belief(
        "CONSISTENCY",
        propositions=[
            "Formal definitions are consistent with numerical claims.",
            consistency_note or "No internal contradictions identified.",
        ],
        epistemic_boundary=["Both formal and numerical aspects are present"],
        domain="methodology",
        confidence=ConfidenceLevel.HIGH if is_consistent else ConfidenceLevel.LOW,
    )
    if is_consistent:
        s.accept("CONSISTENCY")

    # 4. EXPERT_REVIEW
    s.add_belief(
        "EXPERT_REVIEW",
        propositions=[
            "The work has been independently reviewed by mathematical experts.",
            review_note or "Community engagement documented.",
        ],
        epistemic_boundary=["Peer review or expert feedback documented"],
        domain="validation",
        confidence=ConfidenceLevel.HIGH if has_expert_review else ConfidenceLevel.LOW,
    )
    if has_expert_review:
        s.accept("EXPERT_REVIEW")

    # 5. SCOPE_CALIBRATION
    s.add_belief(
        "SCOPE_CALIBRATION",
        propositions=[
            "The paper accurately represents the scope and confidence of its claims.",
            scope_note or "No overclaiming detected.",
        ],
        epistemic_boundary=["Claims are not exaggerated beyond evidence"],
        domain="epistemics",
        confidence=ConfidenceLevel.HIGH if scope_ok else ConfidenceLevel.LOW,
    )
    if scope_ok:
        s.accept("SCOPE_CALIBRATION")

    s.run()
    report = s.score()
    return s, report.overall_score


# ---------------------------------------------------------------------------
# Paper-specific AEE sessions
# ---------------------------------------------------------------------------

def aee_rodgers_tao_2020() -> PaperAEEResult:
    _, c = _make_session(
        "rodgers-tao-2020",
        claim_propositions=["The de Bruijn-Newman constant satisfies Lambda >= 0.",
                            "Combined with Lambda <= 0.22, RH is equivalent to Lambda = 0."],
        claim_boundary=["Standard analytic number theory; Polymath15 bound accepted"],
        claim_confidence=ConfidenceLevel.HIGH,
        claim_accept=True,
        claim_failures=[],
        has_falsification=True,
        falsification_note="Peer review + Polymath15 independent verification.",
        is_consistent=True,
        has_expert_review=True,
        review_note="Published: Forum of Mathematics, Pi 8 (2020).",
        scope_ok=True,
        scope_note="Does not claim to prove RH. Proves Lambda >= 0 only.",
    )
    return PaperAEEResult("rodgers-tao-2020", "de Bruijn-Newman constant >= 0",
                          c, True, 0, 0, 5, 5, 1, False)


def aee_griffin_ono_2019() -> PaperAEEResult:
    _, c = _make_session(
        "griffin-ono-2019",
        claim_propositions=["Jensen polynomials associated to the Riemann xi function are hyperbolic.",
                            "Proved for all fixed degree d (finitely many exceptions in n)."],
        claim_boundary=["Hyperbolicity proven per fixed d, not for all d simultaneously"],
        claim_confidence=ConfidenceLevel.HIGH,
        claim_accept=True,
        claim_failures=[
            ("RH requires hyperbolicity for ALL degrees simultaneously",
             "Result holds for each fixed d, not uniformly over all d",
             FailureSeverity.MEDIUM),
        ],
        has_falsification=True,
        falsification_note="Peer-reviewed; Jensen polynomial framework is standard.",
        is_consistent=True,
        has_expert_review=True,
        review_note="Published: PNAS 116(23), 2019.",
        scope_ok=True,
        scope_note="Does not claim to prove RH.",
    )
    return PaperAEEResult("griffin-ono-2019", "Jensen polynomial hyperbolicity",
                          c, True, 0, 1, 4, 5, 1, False)


def aee_connes_2026() -> PaperAEEResult:
    _, c = _make_session(
        "connes-2026",
        claim_propositions=["The CvS Galerkin matrix D_log^(lambda,N) has eigenvalues converging to zeta zeros.",
                            "Regularized determinant det_reg converges to Xi function (conjectural)."],
        claim_boundary=["Convergence of det_reg to Xi is an open gap (CCM 2025 Section 8)"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("det_reg convergence to Xi function not proven",
             "CCM 2025 Section 8 explicitly identifies this as an open gap",
             FailureSeverity.HIGH),
        ],
        has_falsification=True,
        falsification_note="CvS Galerkin reproduced independently at 6 cutoffs.",
        is_consistent=True,
        has_expert_review=True,
        review_note="Published: J. Open Math. Problems 2(1), 2026.",
        scope_ok=True,
        scope_note="Explicitly does NOT claim proof. Survey + new results.",
    )
    return PaperAEEResult("connes-2026", "Connes spectral program",
                          c, True, 0, 1, 5, 5, 1, False)


def aee_geiger_2026() -> PaperAEEResult:
    _, c = _make_session(
        "geiger-2026",
        claim_propositions=["Even dominance of the Weil quadratic form holds for all lambda >= 100.",
                            "33 CAP certificates verified by interval arithmetic."],
        claim_boundary=["Proposition A6 (cumulative step) required; under review"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("Proposition A6 interpolation step not independently verified",
             "Key cumulative step under peer review; verdict pending",
             FailureSeverity.HIGH),
        ],
        has_falsification=True,
        falsification_note="33 CAP certificates + Euler-Maclaurin IA; reproduced at 6 lambda values.",
        is_consistent=True,
        has_expert_review=True,
        review_note="Submitted Communications in Mathematics (2026-03-27); 2+ months under review.",
        scope_ok=True,
        scope_note="Claims proof via CAP certificates; Prop A6 is the key unverified step.",
    )
    return PaperAEEResult("geiger-2026", "Geiger even-dominance",
                          c, True, 0, 1, 5, 5, 2, True)


def aee_this_work() -> PaperAEEResult:
    _, c = _make_session(
        "this-work",
        claim_propositions=["(log Phi)''(u) < 0 for all u >= 0 (Q_Phi < 0 on [0,1] by IA; [1,inf) by algebra).",
                            "By Polya 1927, this implies all zeros of Xi(t) are real, equivalent to RH."],
        claim_boundary=["Polya 1927 Satz II applies; IA covers [0,1.0]; C=204 perturbation bound holds"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("Lean4 formalization is partial (scaffold, not complete machine proof)",
             "lean4/RHProof/Basic.lean contains sorries; not fully machine-verified",
             FailureSeverity.MEDIUM),
            ("Not yet submitted for peer review",
             "No independent expert review conducted as of 2026-05",
             FailureSeverity.MEDIUM),
        ],
        has_falsification=True,
        falsification_note="32 attacks survived; DH control valid (159 off-line DH candidates); Li criterion all positive.",
        is_consistent=True,
        consistency_note="g'' bug found and fixed by falsification. IA [0,1.0] certified.",
        has_expert_review=False,
        review_note="Preprint not submitted. No independent review.",
        scope_ok=True,
        scope_note="Claims proof. Acknowledges partial Lean and no peer review.",
    )
    return PaperAEEResult("this-work", "Pierson 2026 log-concavity via Polya",
                          c, True, 0, 2, 4, 5, 3, True)


def aee_yamaguchi_2026() -> PaperAEEResult:
    _, c = _make_session(
        "yamaguchi-2026",
        claim_propositions=["Gram Jacobi matrix J_N has eigenvalues approximating imaginary parts of zeta zeros.",
                            "Spectral determinant D_N/xi(1/2+iz) -> c (Hadamard rigidity). J_inf is self-adjoint => RH."],
        claim_boundary=["Self-adjointness of J_inf in N->inf requires domain analysis not provided"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("Self-adjointness of J_inf not rigorously established",
             "Domain analysis (dense domain, deficiency indices) missing in the limit N->inf",
             FailureSeverity.HIGH),
            ("Hadamard rigidity D_N/xi->c requires uniform eigenvalue spacing estimates",
             "Numerically verified at 10,000 zeros but analytic proof gap remains",
             FailureSeverity.HIGH),
        ],
        has_falsification=True,
        falsification_note="Contradiction machine (80/80 falsified, SNR>2.6e9); 3 independent proof paths.",
        is_consistent=True,
        consistency_note="77 C programs; heat kernel trace ratio 0.9999996; forward check <1e-13.",
        has_expert_review=False,
        review_note="Preprint (Zenodo, May 2026). Not peer-reviewed.",
        scope_ok=True,
        scope_note="Claims proof. Computational methodology is most rigorous among independent attempts.",
    )
    return PaperAEEResult("yamaguchi-2026", "Yamaguchi Gram Jacobi spectral determinant",
                          c, True, 0, 2, 4, 5, 2, True)


def aee_erurh_2026() -> PaperAEEResult:
    _, c = _make_session(
        "erurh-2026",
        claim_propositions=["ERURH_GlobalAssumptions => RH(xi_alpha) is formally verified in Lean 4.",
                            "Conditional on analytic packages A/B/C and normalization bridges."],
        claim_boundary=["A/B/C analytic assumptions (large sieve, spectral decay, RMS window) not independently proven",
                        "xi_alpha is a zeta-like function; connection to standard RH requires Assumption 11.1"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("Conditional proof: A/B/C analytic packages not yet proven",
             "Lean verifies implication only; the premises A/B/C remain as external hypotheses",
             FailureSeverity.HIGH),
        ],
        has_falsification=True,
        falsification_note="Lean verifies conditional implication with explicit assumption list.",
        is_consistent=True,
        consistency_note="Lean code contains no sorry in the main conditional theorem per the paper.",
        has_expert_review=False,
        review_note="Preprint (HAL, Feb 2026). Not peer-reviewed.",
        scope_ok=True,
        scope_note="Explicitly conditional. Full assumption list provided. Most honest framing in class.",
    )
    return PaperAEEResult("erurh-2026", "Duran ERURH conditional Lean proof",
                          c, True, 0, 1, 4, 5, 3, True)


def aee_arxiv_hp_2025() -> PaperAEEResult:
    _, c = _make_session(
        "arxiv-hp-2025",
        claim_propositions=["Self-adjoint Hamiltonian R-hat (Berry-Keating + Bessel) has eigenvalues at nontrivial Riemann zeros.",
                            "Self-adjointness forces eigenvalues real => RH for simple zeros."],
        claim_boundary=["Domain analysis for D-hat intersect T-hat not completed",
                        "Result restricted to simple nontrivial zeros only"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=True,
        claim_failures=[
            ("Domain analysis for R-hat self-adjointness not completed",
             "D-hat and T-hat domain intersection requires careful functional analysis not provided",
             FailureSeverity.HIGH),
            ("Trivial eta zeros z_k=1+2*pi*i*k/ln(2) also satisfy boundary condition",
             "Spectral analysis complicated by non-critical eta zeros as eigenvalues",
             FailureSeverity.MEDIUM),
        ],
        has_falsification=False,
        falsification_note="No systematic adversarial testing; 11 versions suggest ongoing refinement.",
        is_consistent=True,
        has_expert_review=False,
        review_note="arXiv preprint, v11 (Aug 2025). Not peer-reviewed.",
        scope_ok=True,
        scope_note="Restricts claim to simple zeros. Multiple versions indicate honest refinement.",
    )
    return PaperAEEResult("arxiv-hp-2025", "arXiv HP Hamiltonian (Berry-Keating+Bessel)",
                          c, True, 0, 2, 3, 5, 3, True)


def aee_singh_khalsa_2026() -> PaperAEEResult:
    _, c = _make_session(
        "singh-khalsa-2026",
        claim_propositions=["RH is equivalent to a single quantitative inequality on Li coefficients.",
                            "Explicitly does NOT claim to prove RH; presents a reduction."],
        claim_boundary=["The quantitative inequality itself remains unproven"],
        claim_confidence=ConfidenceLevel.HIGH,
        claim_accept=True,
        claim_failures=[
            ("Reduction is genuine but the open inequality remains unproven",
             "The paper is a reduction, not a completion; the '1%' reflects honest scope",
             FailureSeverity.LOW),
        ],
        has_falsification=False,
        falsification_note="No falsification protocol; honest non-claim makes this less critical.",
        is_consistent=True,
        consistency_note="Li coefficient framework is consistent with standard theory.",
        has_expert_review=False,
        review_note="Preprint (Zenodo, Feb 2026).",
        scope_ok=True,
        scope_note="Explicitly NOT claiming proof. Most honest framing: 1% = reduction only.",
    )
    return PaperAEEResult("singh-khalsa-2026", "Singh Khalsa Li-kernel reduction (1%)",
                          c, True, 0, 1, 4, 5, 3, False)


def aee_gershon_2026() -> PaperAEEResult:
    _, c = _make_session(
        "gershon-2026",
        claim_propositions=["Log-concavity of Xi kernel Phi(u) proved via Polya 1927.",
                            "Perturbation bound and interval arithmetic verify Q_Phi < 0."],
        claim_boundary=["Perturbation bound inequality direction must be correct",
                        "IA must cover [0, 1.0]"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Perturbation bound inequality goes the wrong direction",
             "Equation 16: need C*eps << |Q|, not |Q| << C*eps. Direction is reversed.",
             FailureSeverity.CRITICAL),
            ("Claims exp(-t^4) is counterexample to log-concavity => real zeros",
             "Csordas-Varga 1989 Example 2.1 shows exp(-t^4) has ONLY real zeros",
             FailureSeverity.HIGH),
        ],
        has_falsification=False,
        falsification_note="No falsification protocol documented.",
        is_consistent=False,
        consistency_note="g'' coefficient inconsistency also found.",
        has_expert_review=False,
        review_note="Preprint (Preprints.org 202604.1513).",
        scope_ok=False,
        scope_note="Claims proof but key inequality direction is wrong.",
    )
    return PaperAEEResult("gershon-2026", "Gershon log-concavity via Polya",
                          c, False, 1, 2, 0, 5, 3, True)


def aee_preprint_0159() -> PaperAEEResult:
    _, c = _make_session(
        "preprint-0159",
        claim_propositions=["Log-concavity of Xi kernel Phi(u) proved; IA on [0, 0.5]."],
        claim_boundary=["IA must cover [0, 1.0]; perturbation direction must be correct"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Perturbation bound inequality direction is wrong",
             "Same error as Gershon 2026: need C*eps << |Q_Phi|, direction is reversed",
             FailureSeverity.CRITICAL),
            ("Interval arithmetic covers [0, 0.5] only",
             "Gap at [0.5, 1.0] is the most sensitive region for Q_Phi",
             FailureSeverity.CRITICAL),
        ],
        has_falsification=False, is_consistent=False,
        has_expert_review=False, scope_ok=False,
        scope_note="Claims proof via Lean 4; both critical gaps invalidate the claim.",
    )
    return PaperAEEResult("preprint-0159", "Anon log-concavity preprint (0159)",
                          c, False, 2, 2, 0, 5, 3, True)


def aee_aivisions_2026() -> PaperAEEResult:
    _, c = _make_session(
        "aivisions-2026",
        claim_propositions=["Form stabilization bypasses CCM convergence gap. Weil form Q_W >= 0 proved."],
        claim_boundary=["Eigenvector stability assumed as cutoff increases"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Eigenvector mode count changes from 7 to 22 as cutoff c increases 13->47",
             "Our phase 8/9 analysis directly contradicts the eigenvector stability assumption",
             FailureSeverity.CRITICAL),
        ],
        has_falsification=False, is_consistent=False,
        has_expert_review=False, scope_ok=False,
        scope_note="No peer review. Blockchain timestamp only.",
    )
    return PaperAEEResult("aivisions-2026", "AI Visions Semilocal Spectral Descent",
                          c, False, 1, 1, 0, 5, 4, True)


def aee_louiz_2026() -> PaperAEEResult:
    _, c = _make_session(
        "louiz-2026",
        claim_propositions=["R(c) = S_mu(c)/S(c) is an analytic proxy for 1/zeta(1/c).",
                            "R(c) is analytic for Re(c) > 1; mapping s=1/c proves all zeros are on critical line."],
        claim_boundary=["Super-exponential suppression must not erase all n>1 Mobius information"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("R(c) -> 1 identically; does not encode 1/zeta(s) at all",
             "mu(1)=1 makes n=1 terms identical in S_mu and S; n>=2 super-exponentially suppressed",
             FailureSeverity.CRITICAL),
            ("Functional equivalence asserted via invalid analytic continuation",
             "Matching at single boundary limit c->inf is insufficient to identify two distinct analytic functions",
             FailureSeverity.CRITICAL),
            ("Internal inconsistency: sec6.1 numerics contradict Lean definition by ~700 OOM",
             "sec6.1 needs exp(-n^c*e^c); Lean uses exp(-n^c*exp(exp(c)))",
             FailureSeverity.CRITICAL),
            ("Lean theorem uses sorry — not machine-verified",
             "analytic_louiz_kernel uses sorry; proof is a sketch not a verification",
             FailureSeverity.HIGH),
        ],
        has_falsification=False,
        falsification_note="No falsification protocol. AI self-validation only.",
        is_consistent=False,
        consistency_note="sec6.1 and Lean definition are ~700 orders of magnitude apart at c=2.",
        has_expert_review=False,
        review_note="Self-validated by Gemini DeepResearch. Both papers by same author.",
        scope_ok=False,
        scope_note="Claims proof + ancillary claim of disproving Twin Primes Conjecture (wrong).",
    )
    return PaperAEEResult("louiz-2026", "Louiz super-exponential kernel",
                          c, False, 3, 4, 0, 5, 4, True)


def aee_morato_2026() -> PaperAEEResult:
    _, c = _make_session(
        "morato-2026",
        claim_propositions=["600-cell Dirac operator proves RH, GRH, Goldbach, Twin Primes, and Collatz."],
        claim_boundary=["Angular defect delta_0~6.8 degrees must derive from number theory, not be a free parameter"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Claims 5 millennium problems solved simultaneously via one 600-cell geometry",
             "Each is a multi-decade open problem; solving all five via one geometric framework is implausible",
             FailureSeverity.CRITICAL),
            ("600-cell angular defect delta_0 is a free parameter tuned to produce results",
             "No derivation of delta_0 from number-theoretic principles; circular fitting",
             FailureSeverity.CRITICAL),
            ("Goldbach from 'heat kernel positivity' is logically invalid",
             "Heat kernel positivity is automatic for any positive self-adjoint operator; does not prove Goldbach",
             FailureSeverity.CRITICAL),
        ],
        has_falsification=False, is_consistent=False,
        has_expert_review=False, scope_ok=False,
        scope_note="Overclaims: 5 open problems solved. No peer review.",
    )
    return PaperAEEResult("morato-2026", "Morato 600-cell Dirac operator",
                          c, False, 3, 3, 0, 5, 4, True)


def aee_meghani_2026() -> PaperAEEResult:
    _, c = _make_session(
        "meghani-2026",
        claim_propositions=["Completion-locked Hilbert-Polya via Fredholm determinant proves RH."],
        claim_boundary=["Fredholm determinant identification with completed zeta requires analytic arguments"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Identification of Fredholm determinant with completed zeta not fully established",
             "Key analytic step not independently verifiable from the paper",
             FailureSeverity.HIGH),
            ("'No-tuning' claim is not rigorously established",
             "Single special-value calibration is itself a tuning step",
             FailureSeverity.HIGH),
        ],
        has_falsification=False, is_consistent=True,
        has_expert_review=False, scope_ok=False,
        scope_note="3 versions, 5 companion preprints. Not peer-reviewed.",
    )
    return PaperAEEResult("meghani-2026", "Meghani completion-locked Hilbert-Polya",
                          c, False, 0, 2, 1, 5, 4, True)


def aee_chua_2026() -> PaperAEEResult:
    _, c = _make_session(
        "chua-2026",
        claim_propositions=["sigma(n) < e^gamma * n * log(log(n)) for all n >= 5041 (Robin's criterion => RH)."],
        claim_boundary=["Robin's criterion is a valid RH equivalent; proof of inequality must hold for all n"],
        claim_confidence=ConfidenceLevel.MEDIUM,
        claim_accept=False,
        claim_failures=[
            ("Proof of Robin inequality for all n not independently verified",
             "Controlling sigma(n) for highly composite numbers is historically very hard",
             FailureSeverity.HIGH),
        ],
        has_falsification=False, is_consistent=True,
        has_expert_review=True,
        review_note="Submitted to Duke Mathematical Journal (Jan 2026); verdict unknown.",
        scope_ok=True,
        scope_note="Uses legitimate RH equivalent. Journal submission (not acceptance) is a signal.",
    )
    return PaperAEEResult("chua-2026", "Chua Robin criterion approach",
                          c, True, 0, 1, 2, 5, 4, True)


def aee_priest_2025() -> PaperAEEResult:
    _, c = _make_session(
        "priest-2025",
        claim_propositions=["Resonance kernel R_alpha centered at 1/2 contradicts off-line zeros via L^2 flux."],
        claim_boundary=["R_alpha must derive the critical line 1/2, not encode it by construction"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Resonance kernel R_alpha = (x-1/2)^2 * exp(-alpha*(x-1/2)^2) is centered at 1/2 by construction",
             "The critical line 1/2 is built into the kernel definition; this is circular",
             FailureSeverity.CRITICAL),
            ("L^2-stable contradiction mechanism asserted at high level without rigorous estimates",
             "No explicit analytic bounds given; 'Clay-grade' is self-assessed",
             FailureSeverity.HIGH),
        ],
        has_falsification=False, is_consistent=False,
        has_expert_review=False, scope_ok=False,
        scope_note="Author is a jeweller by trade; proof developed from pattern recognition.",
    )
    return PaperAEEResult("priest-2025", "Priest zero-flux Friedrichs operator",
                          c, False, 1, 2, 0, 5, 4, True)


def aee_mcgirl_2026() -> PaperAEEResult:
    _, c = _make_session(
        "mcgirl-2026",
        claim_propositions=["phi-Gram determinant monotonicity + De Bruijn-Newman backward flow proves RH.",
                            "phi-kernel K_phi is PF_inf (Schoenberg 1951); repulsion prevents collisions."],
        claim_boundary=["Backward flow non-collision requires control over all zeros simultaneously"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("Backward flow non-collision from t=1/2 to t=0 requires more than local repulsion",
             "Repulsion near individual collisions does not prevent all collisions globally",
             FailureSeverity.HIGH),
            ("phi-Gram determinant monotonicity dD_N/dt > 0 not proved for all N simultaneously",
             "Numerical for finite N; analytic proof for N->inf missing",
             FailureSeverity.HIGH),
            ("E8 lattice connection is not mathematically derived",
             "E8 described as providing 'scale parameter'; connection is asserted not proven",
             FailureSeverity.MEDIUM),
        ],
        has_falsification=False,
        falsification_note="AI co-authors (Claude, Grok, Gemini, GPT) are not mathematical verification.",
        is_consistent=True,
        consistency_note="phi-kernel total positivity (Schoenberg 1951) is a genuine result.",
        has_expert_review=False, scope_ok=False,
        scope_note="AI co-authorship without independent expert review.",
    )
    return PaperAEEResult("mcgirl-2026", "McGirl phi-separation total positivity",
                          c, False, 0, 3, 1, 5, 4, True)


def aee_ladjeroud_2025() -> PaperAEEResult:
    _, c = _make_session(
        "ladjeroud-2025",
        claim_propositions=["Hilbert-Polya operator H via SUSYQM has eigenvalues equal to imaginary parts of zeta zeros."],
        claim_boundary=["Operator construction must be independent of zeta zeros"],
        claim_confidence=ConfidenceLevel.LOW,
        claim_accept=False,
        claim_failures=[
            ("'Algorithmic parameter' B is defined to produce zeta zeros — circular construction",
             "Operator H is built with zeta zeros as inputs, not as a derivation from first principles",
             FailureSeverity.CRITICAL),
        ],
        has_falsification=False, is_consistent=False,
        has_expert_review=False, scope_ok=False,
        scope_note="HAL preprint. Circular: conclusion built into premise.",
    )
    return PaperAEEResult("ladjeroud-2025", "Ladjeroud SUSYQM Hilbert-Polya",
                          c, False, 1, 1, 0, 5, 4, True)


# ---------------------------------------------------------------------------
# Run all sessions and collect results
# ---------------------------------------------------------------------------

PAPER_FUNCTIONS = [
    aee_rodgers_tao_2020,
    aee_griffin_ono_2019,
    aee_connes_2026,
    aee_geiger_2026,
    aee_this_work,
    aee_yamaguchi_2026,
    aee_erurh_2026,
    aee_arxiv_hp_2025,
    aee_singh_khalsa_2026,
    aee_gershon_2026,
    aee_preprint_0159,
    aee_aivisions_2026,
    aee_louiz_2026,
    aee_morato_2026,
    aee_meghani_2026,
    aee_chua_2026,
    aee_priest_2025,
    aee_mcgirl_2026,
    aee_ladjeroud_2025,
]


def run_all() -> list[PaperAEEResult]:
    print("=" * 72)
    print("  AEE PAPER ANALYSIS — Applied Epistemic Engineering")
    print("  epistemic library v0.3.0 (specsmith v0.11.8)")
    print("  https://github.com/layer1labs/specsmith")
    print()
    print("  Scoring: BeliefArtifact stress-test via Frame→Disassemble→")
    print("           Stress-Test→Reconstruct (5 AEE axioms)")
    print("  AGENTS.md: Certainty = epistemic quality, NOT mathematical truth.")
    print("=" * 72)

    results = []
    for fn in PAPER_FUNCTIONS:
        r = fn()
        results.append(r)

    # Sort by certainty descending
    results.sort(key=lambda r: r.certainty, reverse=True)

    print()
    print(f"  {'Rank':<5} {'Paper ID':<35} {'Tier':<5} {'Certainty':>9}  "
          f"{'Crit':>5}  {'Accepted':>8}")
    print("  " + "-" * 72)
    for i, r in enumerate(results, 1):
        rh_flag = " [RH]" if r.claims_rh else " [---]"
        print(f"  {i:<5} {(r.paper_id + rh_flag):<35} {r.tier:<5} "
              f"{r.certainty:>9.3f}  {r.critical_failures:>5}  "
              f"{r.beliefs_accepted}/{r.beliefs_total}")

    print()
    print("  [RH] = claims to prove RH  |  [---] = does not claim proof")
    print("  Crit = critical failure modes found")
    print("  Certainty threshold: 0.700 (AEE default)")
    print(f"  Papers above threshold: "
          f"{sum(1 for r in results if r.certainty >= 0.7)}/{len(results)}")
    print("=" * 72)

    return results


if __name__ == "__main__":
    t0 = time.time()
    results = run_all()

    out = {
        "aee_version": "0.3.0",
        "specsmith_version": "0.11.8",
        "run_date": "2026-05-31",
        "elapsed_s": round(time.time() - t0, 2),
        "papers": [
            {
                "rank": i + 1,
                "paper_id": r.paper_id,
                "title": r.title,
                "certainty": round(r.certainty, 4),
                "tier": r.tier,
                "claims_rh": r.claims_rh,
                "critical_failures": r.critical_failures,
                "total_failures": r.total_failures,
                "beliefs_accepted": r.beliefs_accepted,
                "beliefs_total": r.beliefs_total,
            }
            for i, r in enumerate(results)
        ],
    }
    out_path = os.path.join(ROOT, "results", "aee_papers.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  Results saved -> results/aee_papers.json ({time.time()-t0:.1f}s)")
    sys.exit(0)
