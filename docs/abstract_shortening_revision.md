# Deliverable: abstract_shortening_revision.md
# Task 6 — Shorten Abstract to 180-250 Words

## Replacement Abstract (205 words)

We verify that the Riemann--Jacobi kernel $\Phi(u)$, appearing in the cosine
transform representation $\Xi(t) = \int_0^\infty \Phi(u)\cos(tu)\,du$ of the
Riemann Xi function, is strictly log-concave on $[0,\infty)$.
Subject to the cited form of Pólya's 1927 theorem, this implies that all zeros
of $\Xi(t)$ are real, equivalently the Riemann Hypothesis.

The proof has four components: an elementary algebraic core for the dominant term
$\varphi_1$; rigorous interval arithmetic certifying $Q_\Phi < 0$ on $[0,1]$
across 52,898 subintervals at 60-digit precision (independently verified by
Arb/FLINT); a no-cancellation algebraic approach certifying $(\log\Phi)'' < 0$
on $[1.0, 3.0]$ across 101 overlapping interval checks; and an explicit
monotonicity-based tail bound covering $[3.0,\infty)$.

All computational claims are accompanied by reproducible Python scripts,
certificate JSON files with SHA256 hashes, and a corrected tail prefactor
(using $2n^4$ in place of the invalid $n^4$ bound). A Lean 4 formalization
verifies the algebraic core and records external dependencies as explicit
axioms with zero \texttt{sorry} declarations. All proof-critical dependencies
are identified in a separate table; the remaining non-formalized inputs are
Pólya's theorem, the Fourier representation of $\Xi$, and the computational
certificates, which have not yet been derived inside Lean.

## Removed from abstract
- Detailed Lean build information (moved to Section 12)
- CvS spectral paragraph (moved to Appendix A)
- Code identifier list (moved to Section 12)
- Falsification-suite details (kept in Section 11)
