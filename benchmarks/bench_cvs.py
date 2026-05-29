"""Benchmark: CvS Galerkin eigenvalue convergence across prime cutoffs.

Reference values from Groskin (2026):
    c=13: λ_min ≈ 2.005e-59
    c=17: λ_min ≈ 10^{-76}
"""

from riemann.weil_positivity import run_galerkin
import mpmath as mp


def run_benchmark(cutoffs: list[int] | None = None, N: int = 20, dps: int = 40):
    """Run Galerkin computation at multiple prime cutoffs."""
    if cutoffs is None:
        cutoffs = [7, 11, 13]  # small cutoffs for scaffold testing

    results = []
    for c in cutoffs:
        result = run_galerkin(c, N=N, dps=dps)
        results.append(result)
        print(f"  c={c:2d}: λ_min = {mp.nstr(result.lambda_min, 10)}")

    return results


if __name__ == "__main__":
    print("CvS Galerkin benchmark (scaffold — small N for speed):")
    run_benchmark(N=10, dps=30)
