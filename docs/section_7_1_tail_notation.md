# Deliverable: section_7_1_tail_notation.md
# Proposed §7.1 Tail Notation Subsection

## Problem

The proof uses several related tail-bound quantities:

```
R, δ, ε_old, ε*, λ, C, ΔQ, W_tail, W₁
```

A reviewer reading quickly may lose track of these quantities and their relationships.
A short definitional subsection before Lemma lem:wtail would serve as an anchor.

---

## Proposed Subsection Text (LaTeX)

Insert immediately before Lemma `lem:wtail` as:

```latex
\subsection*{7.1\enspace Tail Notation}
\label{sec:tail_notation}

For clarity, we fix notation for all tail-bound quantities used in this section.

\paragraph{Decomposition of $\Phi$.}
Write
$$
R(u) := \sum_{n \geq 2} \varphi_n(u),
\qquad
\Phi = 4(\varphi_1 + R).
$$

\paragraph{Log-concavity curvatures.}
Define
$$
W(u) := (\log\Phi)''(u),
\quad
W_1(u) := (\log\varphi_1)''(u),
\quad
W_{\mathrm{tail}}(u) := W(u) - W_1(u).
$$
Note that $(\log(4f))'' = (\log f)''$ for any positive $f$, so the factor~$4$
in $\Phi = 4(\varphi_1+R)$ does not appear in $W$.

\paragraph{Perturbation ratio.}
Let $Q_f := f''f - (f')^2$ (log-concavity numerator) and
$$
\lambda(u) := \frac{|\Delta Q(u)|}{|Q_{\varphi_1}(u)|},
\qquad \Delta Q := Q_\Phi - Q_{\varphi_1}.
$$

\paragraph{Tail sums.}
Define
$$
\varepsilon_{\mathrm{old}}(u)
:= \sum_{n=2}^{\infty} n^4\,e^{-\pi(n^2-1)e^{2u}},
\qquad
\varepsilon_*(u) := 2\,\varepsilon_{\mathrm{old}}(u).
$$
The factor $2n^4$ in $\varepsilon_*$ is the tight bound on $B_n(u)$ established in
Proposition~\ref{prop:tail_ratio}.

\paragraph{Perturbation constant.}
$$
C_{\mathrm{old}}
:= \frac{|\Delta Q(1)|}{\varepsilon_{\mathrm{old}}(1)\cdot|Q_{\varphi_1}(1)|}
\approx 204.
$$
Since $\varepsilon_*(1) = 2\varepsilon_{\mathrm{old}}(1)$, using $C=C_{\mathrm{old}}=204$ with
$\varepsilon_*$ is conservative (see~\S\ref{sec:extended}).
```

---

## Rationale

1. **R vs δ**: In Remark rem:truncation, δ denotes the truncation tail
   (n ≥ 6 terms). Here R denotes the full n ≥ 2 tail. The subsection makes this
   distinction visible.

2. **(log(4f))'' = (log f)''**: This identity is obvious but easy to miss; stating it
   prevents any reviewer from asking why the factor-4 disappears.

3. **ε_old vs ε***: Having both defined in one place prevents confusion between the
   old script-computed value and the corrected (×2) value.

4. **C_old vs C***: The factor-of-2 relationship is summarized here and cross-referenced
   to §sec:extended, avoiding duplication.

---

## Acceptance Criterion

Before Lemma lem:wtail, the reader should know:
- What R, W, W₁, W_tail are
- That (log(4f))'' = (log f)''
- What ε_old and ε* are and how they relate
- Why C=204 is conservative when used with ε*

The subsection above provides all four.

**Status: READY FOR INSERTION** (requires paper/main.tex edit only).
