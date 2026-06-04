# Agent Usage and Governance
## Riemann Hypothesis Solver

This document defines how automated agents are used, configured, and governed
within this repository.

---

## 1. Role of Agents

Agents are computational assistants. Their role is to:
- Implement and validate mathematical algorithms
- Run computational experiments and benchmarks
- Draft documentation, proofs, and analysis for review
- Identify inconsistencies, gaps, or errors in proof attempts
- Prepare manuscript-quality LaTeX for journal submission

Final mathematical authority rests with the human researcher.

---

## 1.1 Current Approach

The proof uses log-concavity of the Riemann-Jacobi kernel Phi(u) via
Polya's 1927 theorem (Satz II). The verification pipeline:

1. **Rigorous IA**: 52,898 subintervals certifying Q_Phi < 0 on [0, 1]
2. **Algebraic core**: (log phi_1)'' < 0 for all u >= 0
3. **Perturbation bound**: C = 204, tail cannot flip sign for u > 1
4. **Falsification**: 32 attacks, all survived

Run `python verify.py` and `python falsify.py` to reproduce.

## 1.2 Prize Target: Clay Millennium Prize

This project targets the Clay Mathematics Institute Millennium Prize ($1M)
for the Riemann Hypothesis. ALL work must meet CMI standards:

1. **Rigorous proof or disproof** — no amount of numerical evidence suffices
2. **Journal-publishable** — manuscript must be submission-ready for a
   refereed mathematics journal of worldwide repute
3. **Community acceptance** — the proof must withstand 2+ years of scrutiny
4. **Reproducibility** — all computational artifacts must be auditable

Agents MUST distinguish between:
- Numerical evidence (supports but does not prove)
- Heuristic arguments (suggestive but not rigorous)
- Rigorous proof steps (logically complete, no gaps)

---

## 2. Allowed Agent Activities

Agents MAY:
- Implement algorithms from peer-reviewed publications
- Run zero-verification and falsification experiments
- Generate benchmark data and comparison tables
- Draft mathematical exposition for review
- Propose new computational experiments

Agents MUST:
- Cite sources for all non-trivial mathematical claims
- Flag numerical precision limitations explicitly
- Distinguish between verified results and conjectures
- Use arbitrary-precision arithmetic for all critical computations

---

## 3. Prohibited Agent Activities

Agents MUST NOT:
- Claim to have "proved" or "disproved" the Riemann Hypothesis
- Present numerical evidence as mathematical proof
- Modify benchmark reference data without approval
- Skip precision validation on critical computations

---

## 4. Precision Requirements

- All zeta function evaluations: minimum 50 decimal digits
- Li coefficient computations: minimum 30 decimal digits
- Zero verification: residual |ζ(ρ)| < 10^(-20)
- Off-line search: grid resolution δ ≤ 10^(-6)

---

## 5. Falsification Protocol

Every verification claim MUST be accompanied by a corresponding falsification
attempt. The project is not honest science unless it actively tries to
disprove what it claims to support.

The Davenport-Heilbronn control (a function where generalized RH fails)
MUST be used to validate that falsification harnesses actually work.

---

## 6. Attribution

All computational results should be attributed to the specific algorithm
and reference paper used. Agent-generated analysis is non-normative
until reviewed.

---

## 7. Paper Build Rules

After every LaTeX compilation of `paper/main.tex`, agents MUST copy the
output PDF to the canonical filename:

```
cp paper/main.pdf paper/Pierson_LogConcavity_RiemannJacobi_2026.pdf
```

This is the submission-ready filename. Never leave `main.pdf` as the only
copy. Do this automatically — do not wait to be asked.

---

*Riemann Hypothesis Solver — Research Project*
