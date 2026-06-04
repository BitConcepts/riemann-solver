# Literature Source Index

Each source entry follows the standard template. Updated after every iteration.

**Verdict codes:**
- MATCH — hypotheses and conclusion align with H13; applies to Φ
- PARTIAL MATCH — partial alignment; one or more gaps remain
- PRESERVATION ONLY — theorem preserves real zeros but requires prior real-rootedness
- MELLIN CONDITION ONLY — requires Mellin transform with negative real zeros
- LP CONDITION ONLY — requires Laguerre–Pólya class membership
- COUNTEREVIDENCE — evidence against H13 or against a candidate route
- IRRELEVANT — does not bear on the bridge problem

---

## Source: Pólya 1927 — Über trigonometrische Integrale mit nur reellen Nullstellen

- **Citation:** G. Pólya, "Über trigonometrische Integrale mit nur reellen Nullstellen," J. Reine Angew. Math. 158 (1927), 6–18.
- **URL / DOI:** https://doi.org/10.1515/crll.1927.158.6
- **Full text acquired?** No (paywalled; Göttingen digitization partial)
- **Theorem numbers inspected:** Satz I, Satz II, Hilfssatz I, Hilfssatz II
- **Does it mention log-concavity?** No — log-concavity is not the hypothesis
- **Does it mention Laguerre–Pólya?** Yes — Satz I is a preservation theorem for LP multipliers
- **Does it mention Fourier transforms with only real zeros?** Yes — central topic
- **Does it require prior real-rootedness?** Satz I: yes (circular). Satz II: no, but requires Mellin condition.
- **Does it require a Mellin transform with negative real zeros?** Satz II: yes
- **Does it apply to Φ?** Satz II: conditionally, if Mellin transform of Φ has negative real zeros (unverified)
- **Verdict:** MELLIN CONDITION ONLY (Satz II), PRESERVATION ONLY (Satz I)
- **Key quote (Satz II paraphrase):** If $f$ is real, even, of bounded variation, and if the Mellin transform $M(z) = \int_0^\infty t^{z-1} f(\log t) dt$ has only real negative zeros, then $F(\lambda) = \int_{-\infty}^\infty f(t) e^{i\lambda t} dt$ has only real zeros.
- **Follow-up needed:** Verify whether Mellin transform of Φ has only real negative zeros (Route D).

---

## Source: Csordas–Varga 1989

- **Citation:** G. Csordas, R.S. Varga, "Necessary and sufficient conditions and the Riemann Hypothesis," Adv. Appl. Math. 11 (1989), 328–357.
- **URL / DOI:** https://doi.org/10.1016/0196-8858(89)90026-0
- **Full text acquired?** No
- **Theorem numbers inspected:** Theorem 2.2
- **Does it mention log-concavity?** No
- **Does it mention Laguerre–Pólya?** Yes — LP class central
- **Does it mention Fourier transforms with only real zeros?** Yes
- **Does it require prior real-rootedness?** Theorem 2.2: restates Pólya Satz II; requires Mellin condition
- **Does it require a Mellin transform with negative real zeros?** Yes
- **Does it apply to Φ?** Same gap as Pólya Satz II
- **Verdict:** MELLIN CONDITION ONLY
- **Follow-up needed:** None additional beyond Pólya Satz II Route D.

---

## Source: de Bruijn 1950 — The roots of trigonometric integrals

- **Citation:** N.G. de Bruijn, "The roots of trigonometric integrals," Duke Math. J. 17 (1950), 197–226.
- **URL / DOI:** https://doi.org/10.1215/S0012-7094-50-01720-0
- **Full text acquired?** No
- **Theorem numbers inspected:** Main theorem (Theorem 1)
- **Does it mention log-concavity?** No
- **Does it mention Laguerre–Pólya?** Yes
- **Does it mention Fourier transforms with only real zeros?** Yes
- **Does it require prior real-rootedness?** Requires LP class condition on the kernel's derivative
- **Does it apply to Φ?** Unknown — LP condition on derivative not verified for Φ
- **Verdict:** LP CONDITION ONLY
- **Follow-up needed:** Determine whether Φ' belongs to LP class or analogous condition.

---

## Source: Cardon 2002 ("Convolution operators and zeros of entire functions") — ACQUIRED

- **Citation:** D.A. Cardon, "Convolution operators and zeros of entire functions,"
  Proc. Amer. Math. Soc. 130 (2002), no. 6, 1725–1734.
- **URL / DOI:** https://doi.org/10.1090/S0002-9939-01-06351-1
- **Full text:** https://www.ams.org/journals/proc/2002-130-06/S0002-9939-01-06351-1/S0002-9939-01-06351-1.pdf
- **Full text acquired?** Yes — PDF retrieved and read.
- **Theorem numbers inspected:** Theorem 1 (main), Theorem 2 (Pólya Hilfssatz II quoted), Theorem 3
- **Does it mention log-concavity?** No. Log-concavity not a hypothesis anywhere.
- **Does it mention Laguerre–Pólya?** Yes — LP class is central throughout.
- **Does it mention Fourier transforms with only real zeros?** Yes — Theorem 3.
- **Does it require prior real-rootedness?** YES — Theorem 1 requires $G$ to already have
  only real zeros. Theorem 2 (Hilfssatz II) requires prior real-rootedness.
- **Does it require a Mellin transform with negative real zeros?** No.
- **Does it apply to Φ?** No — all theorems require $G$ to already be in LP class.
- **Verdict:** PRESERVATION ONLY — REJECT as bridge.
- **Key finding:** Pólya Hilfssatz II (exact statement extracted):
  > "Let $a$ be a positive constant and let $G(z)$ be an entire function of genus 0 or 1 that
  > for real $z$ takes real values, has at least one real zero, and has only real zeros. Then
  > the function $G(z + ia) + G(z − ia)$ has only real zeros."
  This requires G to ALREADY have only real zeros. Circular if applied to Ξ.
- **Follow-up needed:** None — verdict is clear.

**NOTE:** There is ALSO a Cardon 2005 paper: "Fourier transforms having only real zeros,"
Proc. Amer. Math. Soc. 133 (2005), 1349–1356. DOI: 10.1090/s0002-9939-04-07677-4.
This is a different paper and has not yet been acquired. Still a candidate.

---

## Source: Csordas & Vishnyakova 2013 — ACQUIRED

- **Citation:** G. Csordas, A. Vishnyakova, "The generalized Laguerre inequalities and
  functions in the Laguerre-Pólya class," *Open Mathematics* 11(9) (2013), 1643–1650.
- **URL / DOI:** https://doi.org/10.2478/s11533-013-0269-x
- **Full text acquired?** Yes — PDF and HTML retrieved.
- **Note:** This is the paper matching "Csordas 2015" in the prompt (year misremembered).
- **Theorem numbers inspected:** Theorem 1.2 (necessary), Theorem 2.3 (sufficient)
- **Does it mention log-concavity?** Yes — $L_1 \geq 0$ is the first Laguerre inequality,
  equivalent to log-concavity.
- **Does it mention Laguerre–Pólya?** Yes — central topic.
- **Does it mention Fourier transforms with only real zeros?** No — about entire functions,
  not their Fourier transforms.
- **Does it require prior real-rootedness?** No.
- **Does it require a Mellin transform with negative real zeros?** No.
- **Does it apply to Φ?** PARTIAL — see verdict.
- **Verdict:** PARTIAL MATCH
- **Key finding:** Theorem 2.3: $L_n(x) \geq 0$ for ALL $n \geq 0$ and all $x$ implies
  $\phi \in L$-$P$ (only real zeros). But log-concavity = only $L_1 \geq 0$. Need ALL orders.
- **Critical negative result:** $\phi = e^{x^2/2}\cos x$ satisfies $L_1 \geq 0$ (log-concave)
  but has non-real zeros. PROVES log-concavity alone is INSUFFICIENT for general entire functions.
- **Conjecture (open):** Section 3 of the paper mentions that if $L_1 \geq 0$ under suitable
  conditions, higher $L_n \geq 0$ might follow — but this is an OPEN CONJECTURE, not a theorem.
- **Follow-up needed:** (1) Verify whether higher $L_n \geq 0$ can be certified for $\Phi$
  computationally. (2) Check Cardon 2009 for related extended Laguerre criteria.

---

## Source: Csordas 2015

- **Citation:** G. Csordas, "Fourier transforms of log-concave functions and the Riemann Hypothesis" (or similar title — verify exact title/venue)
- **URL / DOI:** TBD
- **Full text acquired?** No — first iteration target
- **Theorem numbers inspected:** 3.5, 3.6, 3.7 (targeted)
- **Does it mention log-concavity?** Yes — possibly central
- **Does it mention Laguerre–Pólya?** Likely yes
- **Does it mention Fourier transforms with only real zeros?** Yes
- **Does it require prior real-rootedness?** TBD
- **Does it apply to Φ?** Possibly — first iteration target
- **Verdict:** TBD — first iteration target
- **Follow-up needed:** Acquire exact theorem statements for 3.5–3.7; map to H13 hypotheses.
