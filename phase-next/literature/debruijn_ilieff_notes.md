# de Bruijn (1950) and Ilieff (1955) Notes

---

## de Bruijn 1950 — The roots of trigonometric integrals

**Citation:** N.G. de Bruijn, "The roots of trigonometric integrals," Duke Math. J. 17 (1950), 197–226.
DOI: https://doi.org/10.1215/S0012-7094-50-01720-0

### Main theorem (paraphrase)

If $f \in L^1(\mathbb{R})$ is real-valued, even, and the function $h$ defined by $f(t) = h(e^t)$
satisfies certain conditions — particularly that $h$ or a related derivative belongs to the
Laguerre–Pólya class — then the Fourier transform $F(\lambda) = \int f(t) e^{i\lambda t} dt$
has only real zeros.

**Key condition:** The LP-class condition is on the derivative $f'$ or a related kernel,
NOT on log-concavity of $f$ directly.

**Exact theorem:** Not yet extracted from primary text. Requires full text.

**Status:** LP CONDITION ONLY

**Gap for Φ:** The LP class condition on the derivative of Φ is not known to follow from
log-concavity of Φ. These are different conditions. LP class membership requires:
- The function is a uniform limit on compact sets of polynomials with only real zeros.
- Or equivalently: an entire function of genus 0 or 1 with only real zeros.

Log-concavity of Φ does NOT imply Φ' ∈ LP class without additional argument.

---

## Ilieff 1955

**Citation:** L. Ilieff, "Sur les fonctions entières," C. R. Acad. Sci. Paris 240 (1955), 269–270.
(Tentative — verify exact citation)

**Status:** Not extracted. Short note extending de Bruijn's result.

**Role:** Cited alongside de Bruijn in the literature on Fourier transforms with real zeros.
Typically considered a strengthening or clarification of de Bruijn's LP condition.

---

## de Bruijn–Newman constant

**Note:** Separately from the 1950 paper, de Bruijn (1950) and Newman (1976) introduced
the de Bruijn–Newman constant $\Lambda$ via heat-flow deformation of Ξ. This is a different
result from the 1950 trigonometric integral theorem.

RH ⟺ Λ ≤ 0. It has now been proved (Rodgers–Tao, 2018) that Λ ≥ 0, so RH ⟺ Λ = 0.

**Relation to phase-next:** The heat-flow deformation may connect to Route E in
theorem_bridge_candidates.md. The question is whether log-concavity of Φ constrains
the de Bruijn–Newman deformation in a way that pins Λ = 0.

**Status of Route E connection:** OPEN — speculative, needs investigation.

---

## Follow-up

- [ ] Acquire de Bruijn 1950 full text (Duke Math. J. via library access).
- [ ] Extract exact hypotheses for the main theorem (especially the LP condition on $f'$).
- [ ] Determine whether LP condition on $f'$ is strictly stronger than log-concavity of $f$.
- [ ] Acquire Ilieff 1955.
- [ ] Investigate whether log-concavity of Φ constrains Λ = 0 in the de Bruijn–Newman framework.
