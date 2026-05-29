"""Falsification: monitor Li coefficients for sign changes.

Any λ_n < 0 immediately disproves the Riemann Hypothesis.
"""

from riemann.li_criterion import li_coefficient
import mpmath as mp


def monitor(n_max: int = 50, dps: int = 25) -> dict:
    """Compute λ_n for n = 1..n_max, watching for negatives."""
    results = {"all_positive": True, "max_n": n_max, "violations": []}

    for n in range(1, n_max + 1):
        c = li_coefficient(n, dps)
        if not c.positive:
            results["all_positive"] = False
            results["violations"].append({
                "n": n,
                "value": float(c.value),
            })
            print(f"  *** λ_{n} = {mp.nstr(c.value, 15)} < 0 — RH VIOLATED ***")
        else:
            if n <= 10 or n % 10 == 0:
                print(f"  λ_{n:3d} = {mp.nstr(c.value, 12):>20s}  [+]")

    return results


if __name__ == "__main__":
    mp.mp.dps = 25
    print("Li coefficient sign monitor (falsification):")
    results = monitor(30)
    if results["all_positive"]:
        print(f"\nAll λ_n positive for n ≤ {results['max_n']} (consistent with RH)")
    else:
        print(f"\n*** VIOLATIONS FOUND: {results['violations']} ***")
