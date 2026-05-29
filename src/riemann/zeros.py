"""Non-trivial zero finding, verification, and analysis.

Provides tools for:
- Computing specific zeros via mpmath.zetazero
- Batch zero computation
- Zero verification (residual checking)
- Off-critical-line search
- Spacing statistics

References:
    - Odlyzko (1987), spacing statistics
    - Arias de Reyna, mpmath zetazero implementation
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


@dataclass
class ZetaZero:
    """A verified non-trivial zero of the Riemann zeta function."""

    index: int
    t: mp.mpf  # imaginary part (rho = 1/2 + i*t)
    residual: mp.mpf  # |zeta(1/2 + i*t)|
    verified: bool  # residual < threshold

    @property
    def rho(self) -> mp.mpc:
        """The zero as a complex number ρ = 1/2 + it."""
        return mp.mpc(0.5, self.t)


def compute_zero(n: int, dps: int = 50) -> ZetaZero:
    """Compute the n-th non-trivial zero of ζ(s) to `dps` digits.

    Returns a ZetaZero with the imaginary part, residual, and
    verification status.
    """
    with mp.workdps(dps):
        rho = mp.zetazero(n)
        t = mp.im(rho)
        residual = abs(mp.zeta(rho))
        threshold = mp.power(10, -(dps // 2))
        return ZetaZero(
            index=n,
            t=t,
            residual=residual,
            verified=(residual < threshold),
        )


def compute_zeros(start: int, count: int, dps: int = 50) -> list[ZetaZero]:
    """Compute zeros from index `start` to `start + count - 1`."""
    return [compute_zero(n, dps) for n in range(start, start + count)]


def verify_zero(t: float | mp.mpf, dps: int = 50) -> tuple[mp.mpf, bool]:
    """Verify that ζ(1/2 + it) ≈ 0 to the given precision.

    Returns (residual, is_verified).
    """
    with mp.workdps(dps):
        s = mp.mpc(0.5, t)
        residual = abs(mp.zeta(s))
        threshold = mp.power(10, -(dps // 2))
        return residual, residual < threshold


def zero_spacing(zeros: list[ZetaZero]) -> list[mp.mpf]:
    """Compute consecutive spacings between zeros.

    Returns δ_n = t_{n+1} - t_n for n = 0, ..., len(zeros)-2.
    """
    return [zeros[i + 1].t - zeros[i].t for i in range(len(zeros) - 1)]


def normalized_spacing(zeros: list[ZetaZero]) -> list[mp.mpf]:
    """Compute normalized spacings δ_n / <δ> where <δ> is the mean spacing.

    Under RH + GUE hypothesis, these follow the GUE spacing distribution.
    """
    spacings = zero_spacing(zeros)
    if not spacings:
        return []
    mean_spacing = sum(spacings) / len(spacings)
    return [s / mean_spacing for s in spacings]


def off_line_search(
    sigma: float,
    t_start: float,
    t_end: float,
    t_step: float = 0.1,
    dps: int = 60,
    threshold: float = 1e-10,
) -> list[tuple[mp.mpf, mp.mpf, mp.mpf]]:
    """Search for near-zeros of ζ(σ + it) with σ ≠ 1/2.

    This is a falsification harness: any result with |ζ| < threshold
    at σ ≠ 1/2 would be evidence against RH.

    Returns list of (sigma, t, |ζ(s)|) for candidate points.
    """
    candidates = []
    with mp.workdps(dps):
        t = mp.mpf(t_start)
        while t <= t_end:
            s = mp.mpc(sigma, t)
            val = abs(mp.zeta(s))
            if val < threshold:
                candidates.append((mp.mpf(sigma), t, val))
            t += t_step
    return candidates


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute and verify zeta zeros")
    parser.add_argument("--count", type=int, default=10, help="Number of zeros to compute")
    parser.add_argument("--dps", type=int, default=50, help="Decimal precision")
    args = parser.parse_args()

    print(f"Computing first {args.count} non-trivial zeros at {args.dps} dps:")
    for z in compute_zeros(1, args.count, args.dps):
        status = "✓" if z.verified else "✗"
        print(f"  ρ_{z.index} = 1/2 + {mp.nstr(z.t, 30)}i  |ζ|={mp.nstr(z.residual, 5)}  {status}")
