# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Common math utilities for the Riemann solver."""

from __future__ import annotations

import mpmath as mp


def primes_up_to(n: int) -> list[int]:
    """Sieve of Eratosthenes returning all primes ≤ n."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def von_mangoldt(n: int) -> mp.mpf:
    """The von Mangoldt function Λ(n).

    Λ(n) = log(p) if n = p^k for some prime p and k ≥ 1, else 0.
    """
    if n < 2:
        return mp.mpf(0)
    for p in range(2, n + 1):
        if n % p == 0:
            # p is the smallest prime factor
            m = n
            while m % p == 0:
                m //= p
            if m == 1:
                return mp.log(mp.mpf(p))
            return mp.mpf(0)
    return mp.mpf(0)


def chebyshev_psi(x: int) -> mp.mpf:
    """The Chebyshev function ψ(x) = Σ_{n≤x} Λ(n).

    By the Prime Number Theorem, ψ(x) ~ x.
    Under RH: ψ(x) = x + O(√x log²x).
    """
    return sum(von_mangoldt(n) for n in range(1, x + 1))


def prime_counting(x: int) -> int:
    """π(x) — the number of primes ≤ x."""
    return len(primes_up_to(x))


def li(x: float | mp.mpf) -> mp.mpf:
    """The logarithmic integral Li(x) = ∫₂ˣ dt/ln(t).

    This is the main term in the prime-counting approximation:
        π(x) ≈ Li(x)
    """
    return mp.li(x)
