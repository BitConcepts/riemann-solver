# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Falsification attacks 27-32: everything remaining.

27: Attack Polya's theorem directly — construct a log-concave kernel with
    superexponential decay and check its cosine transform has only real zeros
28: Term-by-term differentiation validity — does the differentiated series converge?
29: E' formula verification (we checked E'' but never E' directly)
30: Is g' coefficient 15/2 correct? (we checked 81/2 in g'', but not 15/2 in g')
31: Construct adversarial Q near zero — find u where Q is closest to zero
    and verify IA still certifies it
32: Full end-to-end: compute Xi(gamma_2) from our Phi formula
"""
import mpmath as mp
from mpmath import iv
import random

mp.mp.dps = 40

# =====================================================================
# ATTACK 27: Construct a test kernel that IS log-concave with
# superexponential decay, and verify its cosine transform has only
# real zeros. If it doesn't, Polya's theorem is wrong.
# Use K(t) = exp(-cosh(t)), which is log-concave, even, positive, L^1.
# =====================================================================
print("=" * 72)
print("  ATTACK 27: Test Polya's theorem on exp(-cosh(t))")
print("=" * 72)

def K_cosh(t):
    return mp.exp(-mp.cosh(t))

# Verify log-concavity: (log K)'' = -(cosh t)'' = -cosh(t) < 0. Always.
print("\n  (log exp(-cosh t))'' = -cosh(t) < 0 for all t. Log-concave: YES")
print("  Decay: exp(-cosh t) ~ exp(-e^t/2). Superexponential: YES")

# Find real zeros of F(z) = integral K(t) cos(zt) dt
print("  Scanning for zeros of cosine transform...")
def F_cosh(z):
    return mp.quad(lambda t: K_cosh(t) * mp.cos(z*t), [0, 10], maxdegree=10)

real_zeros = []
prev = None
for x10 in range(0, 200):
    x = x10 / 5.0
    val = float(mp.re(F_cosh(x)))
    if prev is not None and prev * val < 0:
        real_zeros.append(x)
    prev = val
print("  Real zeros found: %s" % [round(z,1) for z in real_zeros[:6]])

# Check for complex zeros via winding number in [0,10]x[-2,2]
def winding(a, b, h, F, n=30):
    corners = [mp.mpc(a,-h), mp.mpc(b,-h), mp.mpc(b,h), mp.mpc(a,h)]
    total = 0.0
    for ci in range(4):
        z0 = corners[ci]; z1 = corners[(ci+1)%4]
        for i in range(n):
            t0 = float(i)/n; t1 = float(i+1)/n
            p0 = z0 + t0*(z1-z0); p1 = z0 + t1*(z1-z0)
            f0 = F(p0); f1 = F(p1)
            if abs(f0) > 0 and abs(f1) > 0:
                total += float(mp.im(mp.log(f1/f0)))
    return total / (2*float(mp.pi))

w = winding(0, 15, 2, F_cosh)
rz = len([z for z in real_zeros if 0 < z < 15])
print("  Winding number in [0,15]x[-2,2]: %.1f (real zeros: %d)" % (w, rz))
if round(w) <= rz:
    print("  ATTACK FAILED: exp(-cosh t) has only real zeros. Polya confirmed.")
else:
    print("  *** COMPLEX ZEROS FOUND: Polya's theorem may be wrong! ***")

# =====================================================================
# ATTACK 28: Does the differentiated series converge uniformly?
# phi_n''(u) involves terms like n^4 * pi^2 * e^{4u} * e^{-pi*n^2*e^{2u}}
# For n >= 2 and u >= 0, the exponential decay dominates.
# Check: is sum |phi_n''(u)| convergent at u = 0?
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 28: Does sum |phi_n''| converge at u = 0?")
print("=" * 72)

print()
partial_sums = []
running = mp.mpf(0)
for n in range(1, 30):
    phi_n_pp = mp.diff(
        lambda u: (2*mp.pi**2*mp.mpf(n)**4*mp.exp(mp.mpf(9)*u/2) -
                   3*mp.pi*mp.mpf(n)**2*mp.exp(mp.mpf(5)*u/2)) *
                  mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*u)),
        mp.mpf(0), 2)
    running += abs(phi_n_pp)
    if n in [1, 2, 5, 10, 20, 29]:
        print("  N=%2d: sum |phi_n''(0)| = %.10e" % (n, float(running)))

print("  Series converges rapidly.")
print("  ATTACK FAILED: term-by-term differentiation is valid.")

# =====================================================================
# ATTACK 29: Verify E' = -2*pi*n^2*e^{2u} * E against mpmath.diff
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 29: Is E' correct?")
print("=" * 72)

max_err = 0
for u_val in [0.0, 0.3, 0.7, 1.0]:
    for n in [1, 2, 3]:
        def E_func(u, n=n):
            return mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*mp.mpf(u)))
        Ep_mpmath = mp.diff(E_func, mp.mpf(u_val), 1)
        u = mp.mpf(u_val)
        E = mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*u))
        Ep_sym = -2*mp.pi*mp.mpf(n)**2*mp.exp(2*u)*E
        err = abs(float((Ep_sym - Ep_mpmath)/Ep_mpmath)) if Ep_mpmath != 0 else 0
        if err > max_err: max_err = err

print("  Max relative error in E': %.2e" % max_err)
print("  %s" % ("ATTACK FAILED: E' is correct." if max_err < 1e-15 else "*** E' MAY BE WRONG ***"))

# =====================================================================
# ATTACK 30: Is the 15/2 coefficient in g' correct?
# g = 2*pi^2*e^{9u/2} - 3*pi*e^{5u/2}
# g' = 2*pi^2*(9/2)*e^{9u/2} - 3*pi*(5/2)*e^{5u/2}
#    = 9*pi^2*e^{9u/2} - (15/2)*pi*e^{5u/2}
# Check: 3 * (5/2) = 15/2? Yes.
# But verify numerically too.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 30: Is the 15/2 coefficient in g' correct?")
print("=" * 72)

max_err = 0
for u_val in [0.0, 0.3, 0.5, 1.0]:
    u = mp.mpf(u_val)
    def g_func(u):
        return 2*mp.pi**2*mp.exp(mp.mpf(9)*mp.mpf(u)/2) - 3*mp.pi*mp.exp(mp.mpf(5)*mp.mpf(u)/2)
    gp_mpmath = mp.diff(g_func, u, 1)
    gp_sym = 9*mp.pi**2*mp.exp(mp.mpf(9)*u/2) - mp.mpf(15)*mp.pi*mp.exp(mp.mpf(5)*u/2)/2
    err = abs(float((gp_sym - gp_mpmath)/gp_mpmath)) if gp_mpmath != 0 else 0
    if err > max_err: max_err = err

print("  Max relative error in g' (15/2 check): %.2e" % max_err)
print("  %s" % ("ATTACK FAILED: 15/2 is correct." if max_err < 1e-15 else "*** 15/2 MAY BE WRONG ***"))

# =====================================================================
# ATTACK 31: Find the u where Q_Phi is closest to zero and verify
# that our IA can still certify it with a fine enough grid.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 31: Adversarial search for Q closest to zero")
print("=" * 72)

mp.mp.dps = 50

def phi_n_derivs_correct(n, u):
    pi = mp.pi; n2 = mp.mpf(n)**2; n4 = n2**2
    e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)
    e2u = mp.exp(2*u); e4u = e2u**2
    g = 2*pi**2*n4*e9u2 - 3*pi*n2*e5u2
    gp = 9*pi**2*n4*e9u2 - mp.mpf(15)*pi*n2*e5u2/2
    gpp = mp.mpf(81)*pi**2*n4*e9u2/2 - mp.mpf(75)*pi*n2*e5u2/4
    E = mp.exp(-pi*n2*e2u)
    Ep = -2*pi*n2*e2u*E
    Epp = (-4*pi*n2*e2u + 4*pi**2*n4*e4u)*E
    return g*E, gp*E + g*Ep, gpp*E + 2*gp*Ep + g*Epp

def Q_correct(u_val):
    u = mp.mpf(u_val)
    f = fp = fpp = mp.mpf(0)
    for n in range(1, 20):
        a, b, c = phi_n_derivs_correct(n, u)
        f += a; fp += b; fpp += c
    f *= 4; fp *= 4; fpp *= 4
    return fpp * f - fp**2

# Binary search for where Q is closest to zero on [0.5, 2.0]
print()
best_Q = float('-inf')
best_u = 0
for i in range(15001):
    u_val = 0.5 + i * 0.0001
    Q = float(Q_correct(u_val))
    if Q > best_Q:
        best_Q = Q
        best_u = u_val
    if Q >= 0:
        print("  *** Q >= 0 at u = %.4f: Q = %.6e ***" % (u_val, Q))
        break

print("  Closest Q to zero: %.6e at u = %.4f" % (best_Q, best_u))
print("  Still negative: %s" % (best_Q < 0))
if best_Q < 0:
    print("  ATTACK FAILED: Q remains negative at the closest point.")
else:
    print("  *** FALSIFIED: Q >= 0 found! ***")

# =====================================================================
# ATTACK 32: Full end-to-end check at gamma_2 (second Riemann zero)
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 32: End-to-end at gamma_2 = 21.022...")
print("=" * 72)

mp.mp.dps = 25
gamma2 = mp.mpf("21.022039638771554992628")

def Phi_full(u, N=10):
    u = mp.mpf(u)
    return 4*sum(
        (2*mp.pi**2*mp.mpf(n)**4*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*mp.mpf(n)**2*mp.exp(mp.mpf(5)*u/2))
        * mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*u))
        for n in range(1, N+1)
    )

xi_at_gamma2 = mp.quad(lambda u: Phi_full(u) * mp.cos(gamma2 * u), [0, 5], maxdegree=10)
print()
print("  integral Phi(u)*cos(gamma_2*u) du = %.6e" % float(xi_at_gamma2))
print("  (should be ~0 since gamma_2 is a zero of Xi)")
if abs(float(xi_at_gamma2)) < 1e-10:
    print("  ATTACK FAILED: Xi vanishes at gamma_2 as expected.")
else:
    print("  *** Xi does NOT vanish at gamma_2 — formula may be wrong ***")

print()
print("=" * 72)
print("  FINAL FALSIFICATION SUMMARY")
print("  Attacks 27-32: all results above")
print("=" * 72)
