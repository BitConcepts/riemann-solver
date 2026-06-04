# Verification Standards

## Precision requirements

| Computation | Minimum |
|-------------|---------|
| Zeta evaluations | 50 decimal digits |
| Li coefficients | 30 decimal digits |
| Zero residuals \|ζ(ρ)\| | < 10⁻²⁰ |
| Grid resolution δ | ≤ 10⁻⁶ |

## Falsification protocol

Every verification claim MUST have a corresponding falsification attempt.
The Davenport-Heilbronn control MUST be used to validate falsification harnesses.

Run: `python falsify.py` (32 attacks) and `python verify.py` (4-step pipeline).

## Paper build rule

After every LaTeX compilation of `paper/main.tex`, ALWAYS copy the output PDF:

```
cp paper/main.pdf paper/Pierson_LogConcavity_RiemannJacobi_2026.pdf
```

This is the submission-ready filename. Never leave only `main.pdf`.

## Phase-next bridge research

Current gap: H13 (log-concavity → real zeros of Fourier transform) is OPEN.
See `phase-next/reports/bridge_status_matrix.md` for current status.
See `phase-next/reports/clay_path_tracker.md` for Clay Prize path status.
