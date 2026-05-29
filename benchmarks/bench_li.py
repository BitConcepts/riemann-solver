"""Benchmark: Li coefficient growth rate analysis."""

from riemann.li_criterion import li_coefficients, li_growth_check
import mpmath as mp


def run_benchmark(count: int = 20, dps: int = 25):
    """Compute Li coefficients and check growth rate."""
    coeffs = li_coefficients(count, dps)
    diag = li_growth_check(coeffs)
    return coeffs, diag


if __name__ == "__main__":
    mp.mp.dps = 25
    coeffs, diag = run_benchmark(20)
    print("Li coefficient benchmark:")
    for c in coeffs:
        sign = "+" if c.positive else "−"
        print(f"  λ_{c.n:3d} = {mp.nstr(c.value, 15):>25s}  [{sign}]")
    print(f"\nVerdict: {diag['verdict']}")
