# Hypothetical Criterion 13

## Target theorem

Let $K:\mathbb{R}\to\mathbb{R}$ be even, positive, integrable, real analytic near the origin,
superexponentially decaying, and log-concave on $[0,\infty)$. Does it follow that

$$F(z)=\int_{-\infty}^{\infty}K(t)e^{izt}\,dt$$

has only real zeros?

## Known status

**OPEN** / unsourced in current manuscript.

## Current evidence

| Source | Claim | Verdict |
|--------|-------|---------|
| Pólya Satz I (1927) | Preservation of real zeros under LP multipliers | PRESERVATION, not sufficient |
| Pólya Satz II (1927) | Mellin transform with negative real zeros → Fourier real zeros | MELLIN CONDITION, not log-concavity |
| Csordas–Varga Thm 2.2 (1989) | Restates Pólya Satz II | MELLIN CONDITION ONLY |
| de Bruijn–Ilieff theorem | LP condition on derivative → Fourier real zeros | LP CONDITION, different from ordinary log-concavity |
| Csordas (2015) | Generalized Laguerre inequalities enter real-zero criterion | PARTIAL — first inequality may coincide with log-concavity |

## Paths to resolution

- **A. Prove H13.** Construct a direct proof from the six hypotheses to real-rootedness of $F$.
- **B. Find existing theorem equivalent to H13.** Primary-source theorem with matching hypotheses, no circular prior-real-rootedness assumption.
- **C. Disprove H13 by counterexample.** Find $K$ satisfying all six hypotheses whose Fourier transform $F$ has a complex zero.
- **D. Prove a narrower Φ-specific version.** Use the special Riemann–Jacobi series structure to derive real-rootedness of $2\Xi$ without requiring H13 in full generality.

## Connection to RH

The Riemann xi function satisfies:

$$\Xi(t/2) = \frac{1}{2}\int_{-\infty}^{\infty} \Phi(u) e^{iut}\,du$$

where $\Phi(u)$ is the Riemann–Jacobi kernel. RH is equivalent to $\Xi$ having only real zeros,
which is equivalent to the Fourier transform of $\Phi$ having only real zeros.

The current paper proves: $\Phi$ is strictly log-concave on $[0,\infty)$ (PROVED).
The missing bridge: log-concavity of $\Phi$ implies real zeros of its Fourier transform (OPEN).

## What is NOT sufficient

- Numerical evidence of real zeros of $\Xi$ (does not constitute proof)
- Pólya Satz I alone (requires prior real-rootedness — circular)
- Log-concavity of $\Xi$ itself (not the same as log-concavity of $\Phi$)
- Partial verification of generalized Laguerre inequalities
