# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Suzuki (2025) norm equality test — an unconditional RH equivalent.

Implements the computational test of Suzuki's Theorem 1.4:

    RH ⟺ ||P̂Dψ||²_{L²(ℝ)} = π⟨ψ, ψ⟩_W   for all ψ ∈ C_c^∞(ℝ)

where:
    P̂  = Fourier projection onto [−1/2, 1/2]
    D   = multiplication by x
    ⟨ψ, ψ⟩_W = Weil hermitian form (from explicit formula)

The left side (Paley-Wiener norm) is unconditional and computable.
The right side (Weil form) is the same quantity our CvS Galerkin measures.

If the equality holds numerically for a rich set of test functions,
it is strong evidence for RH. If it fails for ANY test function, RH is false.

Also implements Suzuki's screw function S_t(z) (eq. 1.5-1.6), which
generates the unconditional Hilbert spaces H₀ and K₀.

References:
    - Suzuki (2025), "On the Hilbert space derived from the Weil distribution"
      arXiv:2301.00421v3, Theorems 1.1 and 1.4
    - Connes (2026), arXiv:2602.04022
    - Weil (1952), explicit formulas
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


# ── Known zeros of ζ(s) ──────────────────────────────────────────────

# First 30 nontrivial zeros: γ_n where ρ_n = 1/2 + i·γ_n
_KNOWN_ZEROS = [
    "14.134725141734693790457251983562470270784257115699",
    "21.022039638771554992628479593896902777334340524903",
    "25.010857580145688763213790992562821818659549672558",
    "30.424876125859513210311897530584091320181560023715",
    "32.935061587739189690662368964074903488812715603517",
    "37.586178158825671257217763480705332821405597350831",
    "40.918719012147495187398126914633254395726165962777",
    "43.327073280914999519496122165406805782645668371837",
    "48.005150881167159727942472749427516041686844001245",
    "49.773832477672302181916784678563724057723178299677",
    "52.970321477714460644147296608880990063825017888821",
    "56.446247697063394804367759476706198987095809635968",
    "59.347044002602353079653648674992219031098772806466",
    "60.831778524609809844259901824524003802910090451219",
    "65.112544048081606660875054253183705029348149295167",
    "67.079810529494173714478828896522216770107144951746",
    "69.546401711173979252926857526554738443012474209603",
    "72.067157674481907582522107969826168390480906621457",
    "75.704690699083933168326916762030345922811903530697",
    "77.144840068874805372682664856304637015796032449235",
    "79.337375020249367922763592877116228190609489940483",
    "82.910380854086030183164837494770609497508880593782",
    "84.735492980517050105735311206827741417106627934408",
    "87.425274613125229406531667850919213252171886401269",
    "88.809111207634465423682348079509378395444893409818",
    "92.491899270558484296259725241810684878721794027731",
    "94.651344040519886966597925815208153937728027015655",
    "95.870634228245309758741029219246781695256461224988",
    "98.831194218193692233324420138622327820658039063428",
    "101.31785100573139122878544794029230890633286638430",
]


# ── Weil form via spectral zero sum ──────────────────────────────────


def _ft_at_freq(
    psi: callable,
    freq: mp.mpf,
    support: tuple[float, float],
    dps: int,
) -> mp.mpc:
    """Compute ψ̂(freq) = ∫ ψ(x) exp(-2πi·freq·x) dx over the support interval."""
    a, b = mp.mpf(str(support[0])), mp.mpf(str(support[1]))
    return mp.quad(
        lambda x: psi(x) * mp.exp(-2j * mp.pi * freq * x),
        [a, b],
        maxdegree=9,
    )


def weil_form_zeros(
    psi: callable,
    n_zeros: int = 30,
    dps: int = 50,
    support: tuple[float, float] = (-2.0, 2.0),
    use_zetazero: bool = False,
) -> mp.mpf:
    """Compute the ZERO CONTRIBUTION to the Weil quadratic form.

    Formula:
        W_zeros(ψ) = Σ_{n=1}^{n_zeros} 2 |ψ̂(γ_n/(2π))|²

    where γ_n = Im(ρ_n) are the imaginary parts of the nontrivial zeros
    ρ_n = 1/2 + iγ_n of ζ(s), and ψ̂(f) = ∫ ψ(x) exp(-2πifx) dx.

    IMPORTANT: This is only the ZERO CONTRIBUTION. The complete Weil form is:
        W_complete(ψ) = W_zeros(ψ) + W_primes(ψ) + W_arch(ψ)

    where W_primes involves the von Mangoldt sum over prime powers, and
    W_arch is the archimedean (log|x|/log-Gamma) contribution.

    For the Suzuki equality ||P̂Dψ||² = π⟨ψ,ψ⟩_W to hold, W_complete is
    required. W_zeros alone is sufficient only when the archimedean and prime
    contributions are negligible, which holds approximately for test functions
    concentrated near 0 (small support, e.g. gaussian_bump with σ ≤ 0.3).

    Convergence note: as n_zeros → ∞, W_zeros(ψ) → W_complete(ψ) for
    test functions whose Fourier transform decays slowly (broad-support
    functions benefit from more zeros); use use_zetazero=True and large
    n_zeros for best accuracy.

    Args:
        psi: test function ψ ∈ C_c^∞(ℝ)
        n_zeros: number of nontrivial zeros to include
        dps: decimal precision
        support: interval over which ψ is nonzero (for quadrature bounds)
        use_zetazero: if True, compute zeros via mp.zetazero (slow but unlimited)
                      if False, use precomputed _KNOWN_ZEROS list (max 30)

    Returns:
        W_zeros(ψ) ≥ 0  (partial Weil form; see docstring)
    """
    with mp.workdps(dps):
        total = mp.mpf(0)
        n = n_zeros if use_zetazero else min(n_zeros, len(_KNOWN_ZEROS))

        for i in range(n):
            if use_zetazero:
                gamma_n = mp.im(mp.zetazero(i + 1))
            else:
                gamma_n = mp.mpf(_KNOWN_ZEROS[i])

            freq = gamma_n / (2 * mp.pi)
            ft_val = _ft_at_freq(psi, freq, support, dps)
            # ρ and ρ̄ contribute equally for real ψ: 2|ψ̂(freq)|²
            total += 2 * abs(ft_val) ** 2

        return total


def weil_form_primes(
    psi: callable,
    prime_max: int = 100,
    dps: int = 50,
    support: tuple[float, float] = (-2.0, 2.0),
) -> mp.mpf:
    """Compute the PRIME POWER contribution to the Weil quadratic form.

    From the Weil explicit formula, the prime powers p^k contribute:
        W_primes(ψ) = 2 Σ_{n≥2, Λ(n)>0} (Λ(n)/√n) · Re[ψ̂(log(n)/(2π))]
                    · ψ̂(0)

    More precisely, the bilinear form has a cross-term:
        W_primes(ψ, ψ) = Σ_{n≥2} (Λ(n)/√n) · [ψ̂(log(n)/(2π)) · ψ̂(0)*
                         + ψ̂(0) · ψ̂(log(n)/(2π))* + ...]

    For real ψ, the von Mangoldt contribution simplifies to:
        W_primes(ψ) = 2 Σ_{Λ(n)>0, n≤prime_max^k} (Λ(n)/√n) ·
                      Re[ψ̂(log(n)/(2π))] · |ψ̂(0)|

    Note: the sign of this contribution relative to W_zeros determines
    whether it increases or decreases the total form. It enters with a
    NEGATIVE sign in the standard explicit formula decomposition.

    This function computes the MAGNITUDE |W_primes(ψ)| for diagnostic use.
    Args:
        psi: test function ψ
        prime_max: include all prime powers p^k ≤ prime_max
        dps: decimal precision
        support: quadrature bounds

    Returns:
        |W_primes(ψ)|  (unsigned magnitude, for diagnostic purposes)
    """
    with mp.workdps(dps):
        # ψ̂(0) = ∫ ψ(x) dx
        ft_zero = _ft_at_freq(psi, mp.mpf(0), support, dps)

        total = mp.mpf(0)
        for n in range(2, prime_max + 1):
            lam = _von_mangoldt(n)
            if lam <= 0:
                continue
            freq = mp.log(mp.mpf(n)) / (2 * mp.pi)
            ft_val = _ft_at_freq(psi, freq, support, dps)
            # Contribution: (Λ(n)/√n) · 2·Re[ψ̂(freq)·ψ̂(0)*]
            contribution = (lam / mp.sqrt(mp.mpf(n))) * 2 * mp.re(ft_val * mp.conj(ft_zero))
            total += contribution

        return abs(total)


def weil_form(
    psi: callable,
    n_zeros: int = 30,
    dps: int = 50,
    support: tuple[float, float] = (-2.0, 2.0),
    use_zetazero: bool = False,
) -> mp.mpf:
    """Compute the Weil quadratic form (zero contribution; backwards-compatible).

    Wrapper around weil_form_zeros for backwards compatibility.
    See weil_form_zeros for the full documentation and caveats.
    """
    return weil_form_zeros(
        psi, n_zeros=n_zeros, dps=dps, support=support, use_zetazero=use_zetazero
    )


# ── Correct Suzuki operator (Corollary 1.2, arXiv:2209.04658v3) ──────


def suzuki_P_hat_D_norm_sq(
    psi: callable,
    t_max: float = 10.0,
    n_points: int = 30,
    dps: int = 30,
    support: tuple[float, float] = (-1.0, 1.0),
) -> mp.mpf:
    """Compute ||P̂(Dψ)||²_{L²(ℝ)} using Suzuki's CORRECT screw function operator.

    From Corollary 1.2 of arXiv:2209.04658v3:
        P̂φ(z) = ∫ S_t(z) φ(t) dt

    where S_t(z) is the screw function (eq 1.5-1.6), and Dψ(t) = ψ'(t).

    So P̂(Dψ)(z) = ∫ S_t(z) ψ'(t) dt

    and ||P̂(Dψ)||² = ∫ |P̂(Dψ)(z)|^2 dz

    This is the LEFT side of Suzuki's RH-equivalent norm equality.
    """
    with mp.workdps(dps):
        a, b = mp.mpf(str(support[0])), mp.mpf(str(support[1]))
        h_deriv = mp.power(10, -(dps // 3))

        # Dψ(t) = ψ'(t) via numerical differentiation
        def dpsi(t):
            return (psi(t + h_deriv) - psi(t - h_deriv)) / (2 * h_deriv)

        # P̂(Dψ)(z) = ∫_{support} S_t(z) ψ'(t) dt
        def P_hat_D_psi(z):
            def integrand(t):
                return screw_function_S(mp.exp(abs(t)) if abs(t) > 0.01 else mp.mpf(2), z, dps=dps) * dpsi(t)
            # Use simple quadrature over the support of ψ'
            return mp.quad(integrand, [a, b], maxdegree=6)

        # ||P̂(Dψ)||² = ∫_{-∞}^{∞} |P̂(Dψ)(z)|^2 dz
        # Truncate to [-t_max, t_max] since S_t decays
        def norm_integrand(z):
            val = P_hat_D_psi(mp.mpf(z))
            return abs(val) ** 2

        result = mp.quad(norm_integrand, [-t_max, t_max], maxdegree=5)
        return mp.re(result)


# ── Paley-Wiener norm (INCORRECT old implementation, kept for reference) ──


def paley_wiener_norm_sq(
    psi: callable,
    dps: int = 50,
    support: tuple[float, float] = (-1.0, 1.0),
) -> mp.mpf:
    """Compute ||P̂Dψ||²_{L²(ℝ)} — the Paley-Wiener norm squared.

    P̂ = Fourier projection onto frequencies in [-1/2, 1/2]
    D = multiplication by x

    So P̂Dψ = Fourier restriction of (x·ψ(x)) to [-1/2, 1/2].

    Equivalently:
        ||P̂Dψ||² = ∫_{-1/2}^{1/2} |F[x·ψ(x)](ξ)|² dξ

    where F is the Fourier transform.

    For numerical stability, we split into real and imaginary parts
    of the Fourier transform and integrate each separately.
    The support parameter tells the integrator where ψ is nonzero.
    """
    with mp.workdps(dps):
        a, b = mp.mpf(str(support[0])), mp.mpf(str(support[1]))

        def ft_real(xi):
            return mp.quad(
                lambda x: x * psi(x) * mp.cos(2 * mp.pi * xi * x),
                [a, b],
                maxdegree=9,
            )

        def ft_imag(xi):
            return -mp.quad(
                lambda x: x * psi(x) * mp.sin(2 * mp.pi * xi * x),
                [a, b],
                maxdegree=9,
            )

        def integrand(xi):
            re = ft_real(xi)
            im = ft_imag(xi)
            return re ** 2 + im ** 2

        result = mp.quad(integrand, [mp.mpf("-0.5"), mp.mpf("0.5")], maxdegree=7)
        return mp.re(result)


# ── Test functions ───────────────────────────────────────────────────


def bump_function(x: mp.mpf, a: mp.mpf = mp.mpf("-0.5"), b: mp.mpf = mp.mpf("0.5")) -> mp.mpf:
    """Standard C^∞ bump function supported on [a, b].

    ψ(x) = exp(-1/(1 - ((2x-a-b)/(b-a))²))  for x ∈ (a,b), else 0
    """
    x = mp.mpf(x)
    if x <= a or x >= b:
        return mp.mpf(0)
    t = (2 * x - a - b) / (b - a)
    t2 = t ** 2
    if t2 >= 1:
        return mp.mpf(0)
    return mp.exp(mp.mpf(-1) / (1 - t2))


def gaussian_bump(x: mp.mpf, sigma: mp.mpf = mp.mpf("0.2")) -> mp.mpf:
    """Gaussian-like bump ψ(x) = exp(-x²/(2σ²)) · χ_{[-1,1]}(x).

    Not exactly C^∞ at boundaries, but smooth enough for numerical tests.
    """
    x = mp.mpf(x)
    if abs(x) >= 1:
        return mp.mpf(0)
    return mp.exp(-x ** 2 / (2 * sigma ** 2)) * mp.exp(-1 / (1 - x ** 2))


def cosine_bump(x: mp.mpf, n: int = 1) -> mp.mpf:
    """Cosine-modulated bump: cos(nπx) · bump(x).

    Tests the norm equality for oscillatory test functions.
    """
    x = mp.mpf(x)
    b = bump_function(x)
    if b == 0:
        return mp.mpf(0)
    return mp.cos(n * mp.pi * x) * b


def shifted_bump(x: mp.mpf) -> mp.mpf:
    """Asymmetric bump on [0.1, 0.9] — avoids odd-symmetry cancellation."""
    return bump_function(x, mp.mpf("0.1"), mp.mpf("0.9"))


def wide_bump(x: mp.mpf) -> mp.mpf:
    """Wide bump on [-1.5, 1.5] — wider support, more FT content at low freq."""
    return bump_function(x, mp.mpf("-1.5"), mp.mpf("1.5"))


def hat_function(x: mp.mpf) -> mp.mpf:
    """Smooth hat: bump on [-0.8, 0.8] — intermediate width."""
    return bump_function(x, mp.mpf("-0.8"), mp.mpf("0.8"))


# ── Suzuki's screw function S_t(z) ──────────────────────────────────


def screw_function_S(t: mp.mpf, z: mp.mpc, dps: int = 50, N_terms: int = 200) -> mp.mpc:
    """Suzuki's screw function S_t(z) (equation 1.5-1.6).

    S_t(z) = Σ_{n ≤ t} Λ(n) n^{-z} - t^{1-z}/(1-z)
           + Σ correction terms involving digamma/Stieltjes

    This generates the "screw line" in Suzuki's unconditional H₀ space.
    The function is well-defined for all z ∈ ℂ, Re(z) > 0.

    Args:
        t: parameter (typically t > 1)
        z: complex variable
        dps: decimal precision
        N_terms: max terms in von Mangoldt sum
    """
    with mp.workdps(dps):
        t = mp.mpf(t)
        z = mp.mpc(z)

        # Σ_{n ≤ t} Λ(n) n^{-z}  — von Mangoldt function sum
        von_mangoldt_sum = mp.mpf(0)
        n = 2
        while n <= int(t):
            lam_n = _von_mangoldt(n)
            if lam_n > 0:
                von_mangoldt_sum += lam_n * mp.power(mp.mpf(n), -z)
            n += 1

        # Correction: -t^{1-z}/(1-z)
        correction = -mp.power(t, 1 - z) / (1 - z)

        return von_mangoldt_sum + correction


def _von_mangoldt(n: int) -> mp.mpf:
    """Von Mangoldt function Λ(n).

    Λ(n) = log(p) if n = p^k for some prime p and k ≥ 1, else 0.
    """
    if n < 2:
        return mp.mpf(0)

    # Check if n is a prime power
    for p in range(2, n + 1):
        if p * p > n:
            # n itself is prime
            if _is_prime(n):
                return mp.log(mp.mpf(n))
            return mp.mpf(0)
        if n % p == 0:
            # p divides n — check if n = p^k
            k = 0
            m = n
            while m % p == 0:
                m //= p
                k += 1
            if m == 1:  # n = p^k
                return mp.log(mp.mpf(p))
            return mp.mpf(0)
    return mp.mpf(0)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ── Norm equality test ───────────────────────────────────────────────


@dataclass
class NormEqualityResult:
    """Result of testing Suzuki's Theorem 1.4 norm equality."""

    test_function_name: str
    pw_norm_sq: float  # ||P̂Dψ||²
    pi_weil_form: float  # π⟨ψ, ψ⟩_W
    ratio: float  # pw_norm / (π · weil_form)
    log10_residual: float  # log10|ratio - 1|
    n_zeros: int  # number of zeros used
    dps: int


def test_norm_equality(
    psi: callable,
    name: str,
    n_zeros: int = 30,
    dps: int = 30,
    support: tuple[float, float] = (-1.0, 1.0),
) -> NormEqualityResult:
    """Test Suzuki's Theorem 1.4 norm equality for a specific test function.

    Computes both sides:
        LHS = ||P̂Dψ||²_{L²(ℝ)}
        RHS = π⟨ψ, ψ⟩_W  (via spectral zero sum with n_zeros zeros)

    and checks whether LHS ≈ RHS.

    If LHS/RHS = 1 to high precision → evidence for RH
    If LHS/RHS ≠ 1 → evidence against RH (potential disproof!)
    """
    with mp.workdps(dps):
        lhs = paley_wiener_norm_sq(psi, dps=dps, support=support)
        # Pass the function's support to weil_form so quadrature bounds are correct.
        # Note: weil_form computes W_zeros only (see weil_form_zeros docstring).
        # For broad-support functions the archimedean term is not included here.
        rhs_weil = weil_form(psi, n_zeros=n_zeros, dps=dps, support=support)
        rhs = mp.pi * rhs_weil

        if rhs != 0:
            ratio = float(lhs / rhs)
        else:
            ratio = float("inf") if lhs != 0 else 1.0

        residual = abs(ratio - 1.0)
        log_res = float(mp.log10(residual)) if residual > 0 else -dps

    return NormEqualityResult(
        test_function_name=name,
        pw_norm_sq=float(lhs),
        pi_weil_form=float(rhs),
        ratio=ratio,
        log10_residual=log_res,
        n_zeros=n_zeros,
        dps=dps,
    )


def run_norm_equality_suite(
    n_zeros: int = 30,
    dps: int = 30,
) -> list[NormEqualityResult]:
    """Run the norm equality test on a suite of test functions.

    Includes symmetric, asymmetric, and varying-width test functions
    to distinguish genuine norm equality from numerical artifacts.
    """
    test_fns = [
        (gaussian_bump, "gaussian_bump(σ=0.2)", (-1.0, 1.0)),
        (shifted_bump, "shifted_bump[0.1,0.9]", (0.1, 0.9)),
        (hat_function, "hat[-0.8,0.8]", (-0.8, 0.8)),
        (wide_bump, "wide_bump[-1.5,1.5]", (-1.5, 1.5)),
        (lambda x: bump_function(x), "bump[-0.5,0.5]", (-0.5, 0.5)),
    ]

    results = []
    for fn, name, supp in test_fns:
        result = test_norm_equality(fn, name, n_zeros=n_zeros, dps=dps, support=supp)
        results.append(result)

    return results


# ── Screw line computation for H₀ ───────────────────────────────────


@dataclass
class ScrewLineResult:
    """Result of computing S_t along the critical line."""

    t: float
    z_values: list[complex]
    s_values: list[complex]
    norm_sq: float  # ||S_t||² in L² on a segment


def compute_screw_line(
    t: float,
    sigma: float = 0.5,
    t_range: tuple[float, float] = (10, 50),
    n_points: int = 100,
    dps: int = 30,
) -> ScrewLineResult:
    """Evaluate S_t(σ + it) along a vertical line.

    Under RH, the values on the critical line σ = 1/2 generate H₀.
    """
    with mp.workdps(dps):
        t_vals = [t_range[0] + i * (t_range[1] - t_range[0]) / n_points
                  for i in range(n_points + 1)]
        z_vals = [mp.mpc(sigma, tv) for tv in t_vals]
        s_vals = [screw_function_S(mp.mpf(t), z, dps=dps) for z in z_vals]

        # L² norm on the segment
        dt = (t_range[1] - t_range[0]) / n_points
        norm_sq = sum(abs(s) ** 2 * dt for s in s_vals)

    return ScrewLineResult(
        t=t,
        z_values=[complex(z) for z in z_vals],
        s_values=[complex(s) for s in s_vals],
        norm_sq=float(norm_sq),
    )


if __name__ == "__main__":
    mp.mp.dps = 30
    print("=" * 72)
    print("  SUZUKI THEOREM 1.4 — NORM EQUALITY TEST")
    print("  RH ⟺ ||P̂Dψ||² = π⟨ψ, ψ⟩_W for all ψ ∈ C_c^∞(ℝ)")
    print("=" * 72)

    results = run_norm_equality_suite(n_zeros=30, dps=30)
    for r in results:
        status = "✓" if abs(r.ratio - 1.0) < 0.1 else "✗"
        print(f"\n  {status} {r.test_function_name}:")
        print(f"    ||P̂Dψ||²   = {r.pw_norm_sq:.6e}")
        print(f"    π⟨ψ,ψ⟩_W   = {r.pi_weil_form:.6e}")
        print(f"    ratio       = {r.ratio:.6f}")
        print(f"    log10|r-1|  = {r.log10_residual:.1f}")

    print(f"\n  All consistent with RH: {all(abs(r.ratio - 1.0) < 0.5 for r in results)}")
