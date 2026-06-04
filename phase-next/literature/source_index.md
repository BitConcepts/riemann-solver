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

---

## Source: Cardon 2005 — Fourier transforms having only real zeros — ACQUIRED

- **Citation:** D.A. Cardon, "Fourier transforms having only real zeros,"
  Proc. Amer. Math. Soc. 133 (2005), no. 5, 1349–1356.
- **URL / DOI:** https://doi.org/10.1090/s0002-9939-04-07677-4
- **Full text:** https://www.ams.org/journals/proc/2005-133-05/S0002-9939-04-07677-4/
- **Full text acquired?** Yes — AMS PDF retrieved and read.
- **Theorem numbers inspected:** Theorem 1 (main), Theorem 3, Proposition 1 (Pólya quoted)
- **Does it mention log-concavity?** No.
- **Does it mention Laguerre–Pólya?** Yes — LP* class (LP of order < 2) is central.
- **Does it mention Fourier transforms with only real zeros?** Yes — central topic.
- **Does it require prior real-rootedness?** YES — Theorem 1 requires G ∈ LP*,
  i.e., G must already be a real entire function of order < 2 with only real zeros.
- **Does it require a Mellin transform with negative real zeros?** No.
- **Does it apply to Φ?** No — to use this theorem for Φ, one would need to decompose
  the Fourier integral as H(z) = ∫G(it)e^{izt}dF(t) where G already has only real zeros.
  This is a preservation/construction theorem, not a bridge from log-concavity.
- **Verdict:** PRESERVATION ONLY — REJECT as bridge.
- **Key finding (Theorem 1, verbatim):**
  > "Suppose G is an entire function of order < 2 that is real on the real axis and
  > has only real zeros. Let {a_k} be a nonincreasing sequence of positive real numbers,
  > let {X_k} be the sequence of independent random variables such that X_k takes
  > values ±1 with equal probability, and let F_n be the distribution function of the
  > normalized sum Y_n = (a_1 X_1 + ... + a_n X_n)/s_n where s²_n = a²_1 + ... + a²_n.
  > The functions F_n converge pointwise to a continuous distribution F. Let H be the
  > Fourier transform of G(it) with respect to the measure dF. [...] If H is not
  > identically zero, then H has only real zeros."
- **Key finding (Theorem 3):** If G ∈ LP* with only real zeros, and K is integrable with
  K(t) = O(e^{-|t|^{2+ε}}), and L(t) = ∫cosh(ts)dF(s), then H(z) = ∫K(t)L(t)e^{izt}dt
  has only real zeros. Requires G already real-rooted.
- **Applicability assessment:** All theorems require the input function G to already
  have only real zeros. For RH this is circular: applying to Ξ requires Ξ to already
  have real zeros.
- **Follow-up needed:** None — verdict is clear.

---

## Source: Cardon 2009 — Extended Laguerre inequalities and a criterion for real zeros

- **Citation:** D.A. Cardon, "Extended Laguerre inequalities and a criterion for
  real zeros," in *Progress in Analysis and its Applications*, Proceedings of the
  7th International ISAAC Congress (London, July 13–18, 2009), World Scientific,
  Hackensack, 2010, pp. 143–149.
- **URL / DOI:** Zbl 1262.30004
- **Full text acquired?** No — conference proceedings; content reconstructed from
  Csordas-Vishnyakova 2013 citations and Cardon's BYU publications page.
- **Theorem numbers inspected:** Main theorem (criterion for real zeros)
- **Does it mention log-concavity?** Indirectly — L_1 ≥ 0 is log-concavity.
- **Does it mention Laguerre–Pólya?** Yes — criterion for LP class membership.
- **Does it mention Fourier transforms with only real zeros?** No — about entire
  functions directly (LP class membership).
- **Does it require prior real-rootedness?** No — this is a CRITERION (sufficient
  conditions for real zeros).
- **Does it require a Mellin transform with negative real zeros?** No.
- **Does it apply to Φ?** PARTIAL — see verdict.
- **Verdict:** PARTIAL MATCH — extends the Laguerre inequality framework.
- **Key content (from Csordas-Vishnyakova 2013 reference):**
  Cardon extends the generalized Laguerre operators L_n to a broader framework.
  The Csordas-Vishnyakova 2013 paper's Conjecture 3.3 is described as "based on
  Cardon's recent, ingenious extension of the Laguerre-type inequalities."
  The criterion remains: ALL L_n ≥ 0 (not just L_1) implies LP class membership.
  Log-concavity alone (L_1 ≥ 0) is insufficient.
- **Key insight:** Cardon's extension does NOT weaken the requirement from
  "all L_n ≥ 0" to "L_1 ≥ 0 alone." The gap between L_1 and all L_n remains.
- **Follow-up needed:** (1) Acquire full text to verify exact theorem statement.
  (2) Computationally certify L_2 ≥ 0 for Φ (would narrow the gap).

---

## Source: Brandén–Chasse 2016 — Classification theorems for operators preserving zeros in a strip — ACQUIRED

- **Citation:** P. Brandén, M. Chasse, "Classification theorems for operators
  preserving zeros in a strip," J. Anal. Math. (2017). arXiv:1402.2795v2 (2016).
- **URL / DOI:** https://arxiv.org/abs/1402.2795
- **Full text acquired?** Yes — arXiv PDF retrieved and read.
- **Theorem numbers inspected:** Theorems 1.1, 1.2, 4.5, 4.7, Section 5 (Fourier
  transforms with only real zeros)
- **Does it mention log-concavity?** No — not a hypothesis in any theorem.
- **Does it mention Laguerre–Pólya?** Yes — LP class and strip-preserving operators.
- **Does it mention Fourier transforms with only real zeros?** Yes — Section 5
  extends de Bruijn and de Bruijn–Ilieff theorems.
- **Does it require prior real-rootedness?** For strip-preservation results (Thm 1.1,
  1.2): requires input to have zeros in a strip. For Section 5 (Fourier real zeros):
  extends de Bruijn's theorem which requires h'(t) ∈ LP (derivative in LP class).
- **Does it apply to Φ?** Indirectly — the de Bruijn–Ilieff extension (Section 5)
  gives sufficient conditions for K(t) = exp(-h(t)) to have a Fourier transform
  with only real zeros, but requires h'(t) to be a uniform limit of polynomials
  with purely imaginary zeros. This is the LP condition on the derivative.
- **Verdict:** LP CONDITION ON DERIVATIVE — not a direct bridge from log-concavity.
- **Key finding (Section 5, extending de Bruijn Theorem 1):**
  > De Bruijn (1950): Let h(t) be entire such that h'(t) is the uniform limit,
  > on compact subsets of C, of polynomials all of whose zeros lie on the imaginary
  > axis. If h(t) is non-constant with h(t) = h(-t), and h(t) ≥ 0 (t ∈ R), then
  > F(z) = ∫exp(-h(t))e^{izt}dt has only real zeros.
  Brandén–Chasse extend this with new classes of differential operators that
  contract zeros toward the real axis (property (I) of strong universal factors,
  Theorems 4.5, 4.7). They also prove new sufficient conditions via elementary
  methods.
- **Key finding (strip contraction):** Theorems 4.5 and 4.7 give sharp sufficient
  conditions for differential operators to have property (I) of strong universal
  factors. But property (II) remains open for these new operators.
- **Applicability to H13:** The de Bruijn–Ilieff condition requires h'(t) ∈ LP
  (or analogous). For Φ(u) = exp(-h(u)), we would need h(u) = -log Φ(u)
  and h'(u) to have only purely imaginary zeros. This is a DIFFERENT condition
  from log-concavity of Φ. The bridge from log-concavity to h' ∈ LP is unknown.
- **Follow-up needed:** (1) Investigate whether log-concavity of Φ implies h'(-log Φ)'
  has imaginary zeros. (2) Check if new strip-contracting operators apply to Ξ.
