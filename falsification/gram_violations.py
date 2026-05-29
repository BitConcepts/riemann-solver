"""Falsification: Gram's law violation analysis.

Gram's law states (-1)^n Z(g_n) > 0 at Gram points g_n.
Violations are well-studied; anomalous patterns could signal issues.
"""

import mpmath as mp
from riemann.zeta import gram_point, hardy_z


def find_gram_violations(n_max: int = 200) -> list[dict]:
    """Find violations of Gram's law up to index n_max."""
    violations = []
    for n in range(n_max):
        g = gram_point(n)
        z = hardy_z(g)
        if (-1) ** n * z < 0:
            violations.append({
                "index": n,
                "gram_point": float(g),
                "z_value": float(z),
            })
    return violations


if __name__ == "__main__":
    mp.mp.dps = 15
    violations = find_gram_violations(200)
    print(f"Gram violations (n < 200): {len(violations)} found")
    # First violation is at n=126
    for v in violations[:10]:
        print(f"  n={v['index']:4d}: g={v['gram_point']:.6f}, Z={v['z_value']:.8f}")
