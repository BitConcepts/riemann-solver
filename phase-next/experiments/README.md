# Experiments — Phase-next

All experiments in this directory are falsification-first: we try to disprove H13 before
attempting to prove it.

---

## Structure

```
experiments/
  kernels/           — Candidate kernel descriptions
  scripts/           — Computation scripts
  outputs/           — JSON result logs (one file per experiment run)
```

---

## Output format

Every script must produce a JSON output of this form:

```json
{
  "kernel": "...",
  "parameters": {},
  "hypotheses_checked": {
    "even": true,
    "positive": true,
    "integrable": true,
    "analytic_origin": true,
    "superexponential_decay": true,
    "log_concave_halfline": true
  },
  "fourier_zero_test": {
    "box": "...",
    "complex_zeros_found": 0
  },
  "status": "no counterexample / counterexample candidate / invalid candidate",
  "notes": "..."
}
```

---

## Claim discipline for experiment outputs

- `no counterexample`: No complex zero found in the tested box. Does NOT prove H13.
- `counterexample candidate`: A potential complex zero was found. Requires rigorous verification before any disproof claim.
- `invalid candidate`: One or more H13 hypotheses failed for this kernel.

**Never report `counterexample candidate` as a disproof without:**
1. Rigorous (argument-principle or interval arithmetic) verification of all six H13 hypotheses.
2. Rigorous verification that the candidate zero is complex (not a numerical artifact).

---

## Precision requirements

- All Fourier transform evaluations: minimum 50 decimal digits (mpmath with mp.dps=55).
- Argument principle contour integrals: at least 1000 quadrature points per side.
- Log-concavity checks: verify $(\log K)'' < 0$ to at least $10^{-30}$ precision.
