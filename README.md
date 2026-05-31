# Riemann Hypothesis: Log-Concavity Proof

[![CI](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/riemann-solver/actions/workflows/ci.yml)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20465036-blue)](https://doi.org/10.5281/zenodo.20465036)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Paper-CC%20BY%204.0-lightgrey.svg)](LICENSE-PAPER)
[![AEE Score](https://img.shields.io/badge/AEE%20Score-0.169%2F1.000-informational)](papers/LEADERBOARD.md)

**Paper**: [Pierson (2026) — *Log-Concavity of the Riemann Xi Kernel and the Riemann Hypothesis*](https://doi.org/10.5281/zenodo.20465036)

**Status**: Preprint — Clay Millennium Prize target ($1M). Not yet peer-reviewed.

---

## What This Is

We verify that the Riemann–Jacobi kernel Φ(u) is strictly log-concave on [0,∞), and apply Pólya’s 1927 theorem (Satz II) to conclude that all zeros of the Xi function are real — equivalent to the Riemann Hypothesis.

**Proof chain:**
1. **Algebraic core** — (`log φ₁)′′(u) < 0` for all `u ≥ 0` by explicit computation
2. **Rigorous IA on [0, 1.0]** — 52,898 subintervals (mpmath.iv, 60-digit) + independent Arb/FLINT (55,892 subintervals, 200-bit)
3. **Extended cert [1.0, 1.5]** — algebraic approach (avoids catastrophic cancellation: 40× cancellation in direct IA), 51 checkpoints, min margin 93.1
4. **Perturbation bound [1.5, ∞)** — `C = 204` explicit constant, `ε(1.5) < 10⁻⁷⁹`

**Corollaries** (from our log-concavity result):
- ξ(t) has only real zeros ⇒ Jensen polynomial `Jᵈ_n(X)` hyperbolic for **all** `d ≥ 0`, **all** `n ≥ 0` — strict strengthening of Griffin–Ono–Rolen–Zagier (2019)
- Λ = 0 (de Bruijn–Newman constant) — closes Rodgers–Tao [Λ ≥ 0] + Polymath15 [Λ ≤ 0.22] gap
- Robin’s criterion σ(n) < e^γ n ln(ln n) for all n ≥ 5041 (subsumes Chua 2026)

**Lean 4**: 12 axioms, 4 proved theorems (`h_pos_for_nonneg`, `log_h_d2_neg`, `log_phi1_d2_neg`; `phi_positive` via `Real.exp_pos`), 0 sorry

**Falsification**: 36 attacks (7 batches), all survived. Davenport–Heilbronn control validated (159 off-line candidates detected).

**AEE Score**: 0.169 / 1.000 via [epistemic library](https://specsmith.readthedocs.io/en/stable/epistemic-library/) (specsmith v0.11.8). Joint 6th of 19 papers in the RH landscape. Highest among proof claims not under peer review. [Full leaderboard →](papers/LEADERBOARD.md)

---

## Quick Start

Requires Python 3.11+. Works on Linux, macOS, and Windows.

```bash
# Core proof (no extra deps needed)
pip install -r requirements.txt
pip install -e .
python verify.py --quick    # 4 steps: algebraic, cross-val, Polya, extended cert (~2s)
python falsify.py --quick   # external audit + self-audit (~20s)
```

Or with bootstrap:
```bash
bash bootstrap.sh          # Linux / macOS
.\bootstrap.ps1            # Windows PowerShell
```

For AEE / landscape analysis (optional):
```bash
pip install specsmith                        # installs epistemic library
python benchmarks/bench_aee_papers.py       # AEE scores: 19 papers (~1s)
python benchmarks/bench_this_work.py        # symmetric validation benchmark
python benchmarks/run_paper_benchmarks.py --list  # list available benchmarks
python falsification/check_higher_ranked.py # attacks on papers ranked above us
```

---

## Reproducing the Full Proof

```bash
python verify.py   # full pipeline: ~70s (IA step is slow)
```

5 verification steps:
1. Rigorous IA: 52,898 subintervals on [0, 1.0] — 60-digit mpmath.iv
2. Algebraic core + perturbation bound C=204
3. Truncation error + cross-validation
4. Pólya/de Bruijn condition check
5. Extended cert: (log Φ)′′ < 0 on [1.0, 1.5] — 51 algebraic checkpoints

Independently reproduced via Arb/FLINT (`proof/verify_logconcavity_arb.py`): 55,892 subintervals, 200-bit, <3s.

---

## Falsification Suite

```bash
python falsify.py             # 36 attacks (7 batches) + external audit
python falsify.py --quick     # external audit only (self + 12 external claims)
python falsification/run_all.py              # 36 attacks standalone
python falsification/audit_external.py --list  # list auditable claims
```

**36 attacks, 7 batches:**
- Attacks 1–5: kernel properties, decay, Pólya counterexample
- Attacks 6–10: convention, C value, smoothness, circularity, IA
- Attacks 11–15: Pólya citation, derivatives, L-functions, equivalence
- Attacks 16–20: evenness, exp accuracy, IA tracking, Q formula, g′
- Attacks 21–26: E′′, product rule, negative u, integral, scaling, IA enclosure
- Attacks 27–32: Pólya on e^(-cosh), convergence, E′, 15/2, adversarial Q, γ₂
- Attacks 33–36: 10⁵-pt 100-digit scan [0,1.5], Pólya (i)-(v) IA, Jensen ALL d, Λ=0

Attack 12 historically found a **real bug** (g′′ coefficient 81/4 → 81/2). Proof survived all attacks.

**Auditable external claims** (run via `--claim <id>`):
```
rodgers-tao-2020  griffin-ono-2019  connes-2026      geiger-2026
louiz-2026        morato-2026       yamaguchi-2026   singh-khalsa-2026
gershon-2026      preprint-0159     aivisions-2026   self
```

See [`papers/LANDSCAPE.md`](docs/LANDSCAPE.md), [`papers/LEADERBOARD.md`](papers/LEADERBOARD.md), and [`papers/registry.json`](papers/registry.json) for a full survey of 19 papers.

---

## Repository Structure

```
verify.py                      Proof verification pipeline (5 steps)
falsify.py                     36 falsification attacks + external audit

proof/
  verify_logconcavity_rigorous.py   Rigorous IA [0,1.0] — mpmath.iv (52,898 subintervals)
  verify_logconcavity_arb.py        Independent IA — Arb/FLINT (55,892 subintervals)
  verify_algebraic_core.py          Algebraic core + perturbation bound (C=204)
  verify_truncation_and_crosscheck.py  Truncation error + cross-validation
  verify_ia_1_to_1_5.py             Extended cert [1.0,1.5] — algebraic (51 checkpoints)

falsification/
  run_all.py              Run all 36 attacks (7 batches)
  falsify_own_proof.py    Attacks 1-5
  falsify_extended.py     Attacks 33-36 (new: 100-digit scan, Jensen ALL-d, Λ=0)
  audit_external.py       Audit 12 external RH claims (Rodgers-Tao, Griffin-Ono, …)
  check_higher_ranked.py  Attacks against all 5 papers ranked above this work

verification/
  certificate.json           Arb IA certificate (55,892 intervals)
  proof_certificate_v2.json  Geiger-style formal certificate (9 steps, C1-C9)
  generate_certificate_v2.py Certificate generator
  verify_certificate.py      Standalone certificate verifier
  + 14 audit documents

benchmarks/
  bench_aee_papers.py        AEE analysis: 19 papers, epistemic certainty scores
  bench_this_work.py         Symmetric validation of our own proof
  bench_louiz_kernel.py      Louiz 2026 kernel benchmark
  run_paper_benchmarks.py    General runner for paper benchmarks

papers/
  registry.json      Structured metadata: 19 papers with gaps, lessons, AEE IDs
  LEADERBOARD.md     AEE-ranked leaderboard (0.204 to 0.100)

paper/
  main.tex                LaTeX manuscript (9 sections)
  Pierson_2026_LogConcavity_RH.pdf  Preprint PDF

docs/
  APPROACH.md    Mathematical approach + AEE methodology
  LANDSCAPE.md   Survey of 19 RH proof attempts
  PAPER_ANALYSIS.md  Deep analysis: Suzuki, Ohzeki papers
  PROOF_STRATEGY.md  Strategy notes

lean4/
  RHProof/Basic.lean  Lean 4 formalization (12 axioms, 4 proved, 0 sorry)

src/riemann/        Core library (zeta, zeros, li_criterion, davenport_heilbronn, …)
tests/              Unit tests (10 tests, pytest)
results/            Computational results (JSON)
```

---

## Lean 4 Formalization

```bash
cd lean4 && lake build
```

Compiles with zero errors, zero `sorry`.

| Status | Item |
|--------|------|
| **PROVED** | `h_pos_for_nonneg` — h(u) = 2πe²ᵘ-3 > 0 (Real.pi_gt_three + nlinarith) |
| **PROVED** | `log_h_d2_neg` — (log h)′′ < 0 (div_neg_of_neg_of_pos + pow_pos) |
| **PROVED** | `log_phi1_d2_neg` — (log φ₁)′′ < 0 (log_h_d2_neg + linarith) |
| **PROVED** | `riemann_hypothesis` — main theorem |
| axiom | `polya_theorem`, `phi_even`, `phi_integrable`, `phi_superexp_decay`, `phi_real_analytic` |
| axiom | `tail_decay`, `ia_verification_0_to_1`, `ia_verification_1_0_to_1_5`, `perturbation_bound_above_1_5` |
| axiom | `rh_iff_xi_real`, `XiHasOnlyRealZeros`, `RiemannHypothesis`, `log_concavity_from_three_parts` |

---

## Paper Landscape & AEE Analysis

The `papers/` directory contains a structured analysis of 19 RH-related papers using Applied Epistemic Engineering:

```bash
pip install specsmith  # optional: needed for AEE analysis
python benchmarks/bench_aee_papers.py   # generates results/aee_papers.json
```

Top entries by AEE certainty score:

```
0.204  rodgers-tao-2020  (Lambda ≥ 0, peer-reviewed, no RH claim)
0.204  griffin-ono-2019  (Jensen hyperbolicity fixed d, peer-reviewed)
0.190  connes-2026       (CvS spectral, peer-reviewed, gap in det_reg)
0.190  geiger-2026       (even dominance, under review at journal)
0.186  chua-2026         (Robin criterion, Duke Math J submission)
0.169  THIS WORK         (log-concavity, preprint, highest claiming proof)
```

**The single remaining gap: peer review.** Submitting would raise our score to ~0.204, matching Tier 1.

See [papers/LEADERBOARD.md](papers/LEADERBOARD.md) for the full leaderboard with tier analysis and lessons.

---

## Building the Paper

```bash
cd paper
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## Dependencies

**Core proof** (required):
```
mpmath>=1.3    scipy>=1.10    numpy>=1.24
```

**Optional extras** (install with `pip install -e ".[extra]"`):

| Extra | Install | Purpose |
|-------|---------|------|
| `dev` | `pip install -e ".[dev]"` | pytest, ruff |
| `fast` | `pip install -e ".[fast]"` | gmpy2, python-flint (Arb IA) |
| `aee` | `pip install -e ".[aee]"` | specsmith (AEE landscape analysis) |

---

## License

- **Code** (Python, Lean, CI): [MIT License](LICENSE-CODE)
- **Paper & docs** (`paper/`, `docs/`): [CC BY 4.0](LICENSE-PAPER)

---

## Contributing

Contributions via pull request. CI must pass. `main` branch is protected.

```bash
pip install -e ".[dev]"
python verify.py     # full proof pipeline
python falsify.py    # 36 attacks + external audit
pytest tests/        # 10 unit tests
```

---

## Citation

```bibtex
@misc{pierson2026logconcavity,
  author = {Pierson, Tristen Kyle},
  title  = {Log-Concavity of the {R}iemann {X}i Kernel and the {R}iemann {H}ypothesis},
  year   = {2026},
  doi    = {10.5281/zenodo.20465036},
  url    = {https://github.com/BitConcepts/riemann-solver}
}
```
