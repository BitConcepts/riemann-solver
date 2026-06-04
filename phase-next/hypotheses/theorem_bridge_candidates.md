# Theorem Bridge Candidates

Each route is investigated to determine whether it can connect certified log-concavity of Φ
to real-rootedness of its Fourier transform. Status updated each iteration.

---

## Route A — Total positivity / Pólya frequency

**Question:** Does log-concavity plus analyticity plus superexponential decay imply a PF∞ or
variation-diminishing property?

**Current assessment:** Unknown. Likely no in full generality; Φ-specific answer undetermined.

**Tasks:**
- Search Schoenberg PF∞ theory (1951, 1988).
- Check whether Φ or a transformed version can be shown to be PF∞.
- Determine whether PF∞ implies real-rooted Fourier transform.
- Record gaps.

**Status:** OPEN

---

## Route B — Laguerre–Pólya membership

**Question:** Can the Fourier transform of Φ be shown to belong to the Laguerre–Pólya class by
verifying closure properties?

**Tasks:**
- Express Ξ as a locally uniform limit of real-rooted entire functions.
- Identify candidate approximants (truncated Euler product, de Bruijn heat-flow deformations).
- Prove approximants are real-rooted.
- Check Hurwitz / LP closure conditions.

**Status:** OPEN

---

## Route C — Csordas generalized Laguerre inequalities

**Question:** Can Csordas (2015) criteria be verified directly for Φ?

**Tasks:**
- Extract exact Csordas (2015) Theorems 3.5–3.7.
- Translate criteria into computable inequalities for Φ.
- Determine whether log-concavity of Φ gives the first-order condition only or more.
- Attempt interval certificates for higher-order generalized Laguerre inequalities.

**Status:** POSSIBLE — requires full theorem extraction

---

## Route D — Mellin condition from Pólya Satz II

**Question:** Can the Mellin transform

$$H(z)=\int_0^\infty u^{z-1}\Phi(u)\,du$$

be shown to have only real negative zeros?

**Tasks:**
- Define exact Mellin transform for Φ or related kernel $f$.
- Determine whether Pólya Satz II applies to Φ or a transformed kernel.
- Numerically locate zeros of $H(z)$.
- Search for known Mellin transform identities for the Riemann–Jacobi kernel.
- If $H$ has complex zeros, reject this route.

**Status:** PARTIAL — Mellin connection to Riemann zeta known but zero structure not verified

---

## Route E — Direct Ξ proof using certified structure

**Question:** Can strict log-concavity plus the special Riemann–Jacobi series structure imply
real-rootedness of Ξ without requiring H13?

**Tasks:**
- Use the explicit theta/Jacobi series $\Phi(u) = \sum_{n=1}^\infty (2\pi^2 n^4 e^{9u/2} - 3\pi n^2 e^{5u/2}) e^{-\pi n^2 e^{2u}}$.
- Explore heat-flow / de Bruijn–Newman deformation.
- Check whether log-concavity constrains zero movement under deformation.
- Look for additional sign/variation/convexity properties of Φ.

**Status:** OPEN

---

## Summary table

| Route | Method | Gap | Status |
|-------|--------|-----|--------|
| A | PF∞ / total positivity | Whether log-concavity implies PF∞ | OPEN |
| B | LP closure / approximants | Construction of real-rooted approximants | OPEN |
| C | Csordas generalized Laguerre | Higher-order inequalities for Φ unverified | POSSIBLE |
| D | Mellin zeros of H(z) | Complex zeros of Mellin transform not ruled out | PARTIAL |
| E | Series structure + heat flow | Connection between log-concavity and zero movement | OPEN |
