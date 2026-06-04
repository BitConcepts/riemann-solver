# Pólya 1927 — Auxiliary Lemmas (Hilfssätze)

**Source:** G. Pólya, "Über trigonometrische Integrale mit nur reellen Nullstellen,"
J. Reine Angew. Math. 158 (1927), 6–18.
DOI: https://doi.org/10.1515/crll.1927.158.6

**Status:** Primary source. Full German text required for exact Hilfssatz statements.
Current notes drawn from secondary sources (Csordas–Varga 1989, Cardon 2002 references).

---

## Satz I (Theorem I) — Preservation theorem

**Paraphrase:** If $F(\lambda) = \int_{-\infty}^{\infty} f(t) e^{i\lambda t} dt$ has only real zeros
and $\phi(\lambda)$ is an LP-class entire function, then $\phi(d/d\lambda) F(\lambda)$ preserves
only real zeros.

**Status:** PRESERVATION ONLY — requires prior real-rootedness of $F$.
**Verdict for H13:** REJECT as direct bridge. Circular if applied to Ξ.

---

## Satz II (Theorem II) — Mellin–Fourier theorem

**Paraphrase:** Let $f:\mathbb{R}\to\mathbb{R}$ be real, even, of bounded variation on every
finite interval, absolutely integrable. Write $f(t) = g(e^t)$ for $t>0$. If the Mellin transform

$$M(z) = \int_0^\infty u^{z-1} g(u)\,du$$

has only real negative zeros (and suitable convergence), then

$$F(\lambda) = \int_{-\infty}^\infty f(t) e^{i\lambda t}\,dt$$

has only real zeros.

**Exact hypothesis list (from secondary sources — verify against primary):**
- $f$ real-valued, even
- $f$ of bounded variation on every compact interval
- $f \in L^1(\mathbb{R})$
- The Mellin transform $M(z)$ has only negative real zeros
- Convergence condition on $M$

**Status:** MELLIN CONDITION ONLY
**Gap for Φ:** The Mellin transform of Φ (or the related $g$) must have only negative real zeros.
This has NOT been verified. (Route D in theorem_bridge_candidates.md.)

---

## Hilfssatz I (Lemma I)

**Known from secondary sources:** Deals with factorization or approximation properties
of entire functions with real zeros. Exact statement requires primary text.

**Status:** Unextracted — needs primary source.

---

## Hilfssatz II (Lemma II) — EXACT STATEMENT EXTRACTED

**Source:** Quoted verbatim in Cardon (2002), Proc. Amer. Math. Soc. 130 (2002), p. 1726.
Full PDF: https://www.ams.org/journals/proc/2002-130-06/S0002-9939-01-06351-1/S0002-9939-01-06351-1.pdf

> **Theorem 2 (Pólya [18], Hilfssatz II).** Let $a$ be a positive constant and let $G(z)$ be
> an entire function of genus 0 or 1 that for real $z$ takes real values, has at least one
> real zero, and has only real zeros. Then the function $G(z + ia) + G(z − ia)$ has only
> real zeros.

**Proof sketch (from Cardon 2002, p. 1726):** If $z = x + iy$ is a zero of $G(z+ia)+G(z-ia)$,
then $|G(z+ia)| = |G(z-ia)|$. Writing $G$ as a Weierstrass product, one shows the ratio
$|G(z-ia)/G(z+ia)|^2 < 1$ when $y > 0$ and $> 1$ when $y < 0$. Hence $y = 0$.

**Hypotheses required:**
- $G$ has genus 0 or 1 (bounded genus)
- $G$ is real-valued on the real axis
- $G$ has at least one real zero
- $G$ has ONLY REAL ZEROS (prior real-rootedness assumption)

**Status:** SOURCE-CLAIM — extracted verbatim from primary source (via Cardon 2002).

**Verdict for H13:** PRESERVATION ONLY — REJECT as bridge.
Hilfssatz II requires G to ALREADY have only real zeros. It does not derive real-rootedness
from positivity, log-concavity, or any analytic property of the kernel. Applying it to Φ
would require first proving Ξ has only real zeros — which is exactly what we are trying to
prove. The application is circular.

---

## Notes on the 1927 paper

- The paper is in German.
- GDZ digitization may have partial scans.
- Pólya (1930) follow-up paper discusses related material in more detail.
- English expositions in Csordas–Varga (1989) and Levin's "Distribution of Zeros of Entire Functions."

## Follow-up

- [ ] Acquire German text of Pólya 1927 (GDZ / archive.org / interlibrary loan).
- [ ] Extract exact statements of Hilfssatz I, Hilfssatz II.
- [ ] Verify Satz II hypothesis list against primary text.
- [ ] Check whether any Hilfssatz concerns log-concavity directly.
