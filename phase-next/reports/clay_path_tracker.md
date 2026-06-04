# Clay Prize Path Tracker

## Current status

The current paper does **not** prove RH. It proves certified strict log-concavity of Φ.

```
PROVED:      Certified strict log-concavity of the Riemann–Jacobi kernel Φ on [0, ∞).
OPEN:        Log-concavity-to-real-rootedness bridge (Hypothetical Criterion 13).
CONDITIONAL: RH is a consequence of certified log-concavity under H13, IF H13 holds.
```

---

## Clay-relevant paths

### Path 1 — Prove H13

**Status:** OPEN

**Requirements:**
- Complete proof of Hypothetical Criterion 13 from the six hypotheses (even, positive, integrable, analytic, superexp decay, log-concave on [0,∞)).
- Verification that ALL six hypotheses hold for Φ (T1–T5 standard; T6 proved).
- Derivation that Fourier transform of Φ has only real zeros.
- Connection: real zeros of Fourier transform of Φ ⟺ Ξ has only real zeros ⟺ RH.

**Current blockers:**
- H13 is unsourced and unproved.
- No published theorem with matching hypotheses has been identified.

### Path 2 — Find verified existing theorem

**Status:** OPEN

**Requirements:**
- Primary-source theorem with exact hypotheses matching or implying H13.
- No circular prior-real-rootedness assumption.
- Theorem applies to Φ (all hypotheses verified for Φ).
- Accepted citation trail (not secondary paraphrase).

**Candidates under investigation:**
- Cardon (2002) — first iteration target
- Csordas (2015) — first iteration target
- Pólya Hilfssatz II — first iteration target

### Path 3 — Different proof route

**Status:** OPEN

**Requirements:**
- New theorem or method deriving real-rootedness of Ξ from some combination of properties of Φ.
- Uses certified log-concavity as one ingredient (or bypasses it and uses another proved property).
- Produces independent proof that Ξ has only real zeros.

**Routes under investigation:**
- Route A: Total positivity / PF∞
- Route B: LP closure / approximants
- Route D: Mellin zeros
- Route E: Series structure + heat flow (de Bruijn–Newman)

---

## Clay procedural requirements

Even if RH is proved on this branch:

1. **Journal submission:** Submit manuscript to a refereed mathematics journal of worldwide repute (Annals of Mathematics, Inventiones Mathematicae, JAMS, Acta Mathematica, or equivalent).
2. **Peer review:** Must survive full peer review, including scrutiny of the bridge theorem.
3. **Community acceptance:** Clay Institute rules require 2+ years of broad acceptance after publication.
4. **Reproducibility:** All computational artifacts (IA certificates, scripts, benchmarks) must be publicly auditable.
5. **No premature claim:** The Clay submission cannot be made until the bridge is proved, peer-reviewed, and accepted.

---

## What the current paper CAN claim

The paper may claim:
- "We certify strict log-concavity of Φ."
- "RH is equivalent to H13 holding for Φ, where H13 is the hypothetical criterion that log-concavity of Φ (under conditions T1–T6) implies real-rootedness of its Fourier transform."
- "H13 is open; we provide the first certified computation establishing all known verifiable hypotheses."

The paper CANNOT claim:
- "We prove RH."
- "Pólya's theorem proves RH."
- "Log-concavity implies real-rootedness."
- "This work solves the Clay Millennium Problem."

---

## Next milestone

First iteration of phase-next research loop (Cardon 2002, Csordas 2015, counterexample search).
