# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Falsification attacks 21-26: the deepest structural checks.

These target the things that are easy to get wrong but hard to notice.
"""
import mpmath as mp
mp.mp.dps = 50

def phi_1_raw(u):
    """Compute phi_1(u) directly from the definition, no decomposition."""
    u = mp.mpf(u)
    return (2*mp.pi**2*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*mp.exp(mp.mpf(5)*u/2)) * mp.exp(-mp.pi*mp.exp(2*u))

def Phi_raw(u, N=20):
    """Compute Phi(u) directly."""
    u = mp.mpf(u)
    return 4*sum(
        (2*mp.pi**2*mp.mpf(n)**4*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*mp.mpf(n)**2*mp.exp(mp.mpf(5)*u/2))
        * mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*u))
        for n in range(1, N+1)
    )

# =====================================================================
# ATTACK 21: Verify E'' formula against mpmath.diff
# E(u) = exp(-pi*n^2*e^{2u})
# E' = -2*pi*n^2*e^{2u} * E
# E'' = (-4*pi*n^2*e^{2u} + 4*pi^2*n^4*e^{4u}) * E
# =====================================================================
print("=" * 72)
print("  ATTACK 21: Is E'' correct?")
print("=" * 72)

mp.mp.dps = 40
max_err = 0
for u_val in [0.0, 0.3, 0.7, 1.0]:
    for n in [1, 2, 3]:
        def E_func(u):
            return mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*mp.mpf(u)))

        Epp_mpmath = mp.diff(E_func, mp.mpf(u_val), 2)

        u = mp.mpf(u_val)
        E = mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*u))
        e2u = mp.exp(2*u)
        e4u = e2u**2
        n2 = mp.mpf(n)**2
        n4 = n2**2
        Epp_sym = (-4*mp.pi*n2*e2u + 4*mp.pi**2*n4*e4u) * E

        err = abs(float((Epp_sym - Epp_mpmath)/Epp_mpmath)) if Epp_mpmath != 0 else 0
        if err > max_err:
            max_err = err

print("  Max relative error in E'': %.2e" % max_err)
print("  %s" % ("ATTACK FAILED: E'' is correct." if max_err < 1e-15 else "*** E'' MAY BE WRONG ***"))

# =====================================================================
# ATTACK 22: Verify the FULL product rule assembly phi'' = g''E + 2g'E' + gE''
# Compare against mpmath.diff(phi_1, u, 2)
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 22: Is the product rule assembly correct?")
print("=" * 72)

max_err = 0
for u_val in [0.0, 0.1, 0.3, 0.5, 0.8, 1.0]:
    u = mp.mpf(u_val)
    phi1pp_mpmath = mp.diff(phi_1_raw, u, 2)

    # Our assembly
    pi = mp.pi
    e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)
    e2u = mp.exp(2*u); e4u = e2u**2

    g = 2*pi**2*e9u2 - 3*pi*e5u2
    gp = 9*pi**2*e9u2 - mp.mpf(15)*pi*e5u2/2
    gpp = mp.mpf(81)*pi**2*e9u2/2 - mp.mpf(75)*pi*e5u2/4
    E = mp.exp(-pi*e2u)
    Ep = -2*pi*e2u*E
    Epp = (-4*pi*e2u + 4*pi**2*e4u)*E

    phi1pp_sym = gpp*E + 2*gp*Ep + g*Epp

    err = abs(float((phi1pp_sym - phi1pp_mpmath)/phi1pp_mpmath)) if phi1pp_mpmath != 0 else 0
    if err > max_err:
        max_err = err

print("  Max relative error in phi_1'' (full assembly vs mpmath.diff): %.2e" % max_err)
print("  %s" % ("ATTACK FAILED: assembly is correct." if max_err < 1e-15 else "*** ASSEMBLY MAY BE WRONG ***"))

# =====================================================================
# ATTACK 23: Check Q_Phi at NEGATIVE u
# If Phi is even, Q_Phi(-u) should equal Q_Phi(u)
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 23: Is Q_Phi the same at positive and negative u?")
print("=" * 72)

def Q_Phi_raw(u_val):
    u = mp.mpf(u_val)
    h = mp.mpf("1e-8")
    f0 = Phi_raw(u)
    fp = Phi_raw(u+h)
    fm = Phi_raw(u-h)
    f_prime = (fp - fm)/(2*h)
    f_dblprime = (fp - 2*f0 + fm)/h**2
    return f_dblprime * f0 - f_prime**2

print()
max_asym = 0
for u_val in [0.1, 0.3, 0.5, 0.7]:
    Q_pos = float(Q_Phi_raw(u_val))
    Q_neg = float(Q_Phi_raw(-u_val))
    rel = abs((Q_pos - Q_neg) / Q_pos) if Q_pos != 0 else 0
    if rel > max_asym:
        max_asym = rel
    print("  u=%.1f: Q(+u)=%.6e, Q(-u)=%.6e, rel_diff=%.2e" % (u_val, Q_pos, Q_neg, rel))

print("  %s" % ("ATTACK FAILED: Q is symmetric." if max_asym < 1e-8 else "*** Q IS NOT SYMMETRIC ***"))

# =====================================================================
# ATTACK 24: Verify the integral representation at a NONZERO t
# Check: integral Phi(u)*cos(t*u) du = xi(1/2 + it) at t = 5
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 24: Does integral Phi*cos(tu) du = xi(1/2+it) at t=5?")
print("=" * 72)

mp.mp.dps = 25
t_val = mp.mpf(5)

integral_val = mp.quad(lambda u: Phi_raw(u, 10) * mp.cos(t_val * u), [0, 5], maxdegree=10)

s = mp.mpc(0.5, t_val)
xi_val = mp.mpf(1)/2 * s * (s-1) * mp.power(mp.pi, -s/2) * mp.gamma(s/2) * mp.zeta(s)
xi_real = mp.re(xi_val)

print()
print("  integral Phi(u)*cos(5u) du = %.10f" % float(integral_val))
print("  Re(xi(1/2 + 5i))          = %.10f" % float(xi_real))
ratio = float(integral_val / xi_real) if xi_real != 0 else float('inf')
print("  Ratio: %.6f" % ratio)
print("  %s" % ("ATTACK FAILED: integral matches xi." if abs(ratio - 1.0) < 0.01 else "*** MISMATCH ***"))

# =====================================================================
# ATTACK 25: Does the factor of 4 in Phi = 4*sum(phi_n) affect Q sign?
# Q_{c*f} = c^2 * Q_f, so the factor 4 gives Q_{Phi} = 16 * Q_{sum}
# Sign is preserved. But verify explicitly.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 25: Does the factor of 4 preserve Q sign?")
print("=" * 72)

print()
u = mp.mpf("0.3")
h = mp.mpf("1e-8")

# Q of sum (without factor 4)
def S(u_val):
    return sum(
        (2*mp.pi**2*mp.mpf(n)**4*mp.exp(mp.mpf(9)*mp.mpf(u_val)/2) - 3*mp.pi*mp.mpf(n)**2*mp.exp(mp.mpf(5)*mp.mpf(u_val)/2))
        * mp.exp(-mp.pi*mp.mpf(n)**2*mp.exp(2*mp.mpf(u_val)))
        for n in range(1, 10)
    )

s0 = S(u); sp = S(u+h); sm = S(u-h)
Q_sum = (sp-2*s0+sm)/h**2 * s0 - ((sp-sm)/(2*h))**2

# Q of 4*sum
f0 = 4*s0; fp = 4*sp; fm = 4*sm
Q_4sum = (fp-2*f0+fm)/h**2 * f0 - ((fp-fm)/(2*h))**2

ratio_Q = float(Q_4sum / Q_sum) if Q_sum != 0 else 0
print("  Q(sum) = %.6e" % float(Q_sum))
print("  Q(4*sum) = %.6e" % float(Q_4sum))
print("  Q(4*sum) / Q(sum) = %.1f (should be 16)" % ratio_Q)
print("  Both negative: %s" % (Q_sum < 0 and Q_4sum < 0))
print("  %s" % ("ATTACK FAILED: factor 4 preserves sign." if abs(ratio_Q - 16) < 0.1 else "*** RATIO WRONG ***"))

# =====================================================================
# ATTACK 26: Does IA evaluation on [a,b] actually enclose ALL values?
# Compute Q at 100 random points in [0.5, 0.501] and check they all
# fall within the IA enclosure of that interval.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 26: Does IA enclosure contain all point evaluations?")
print("=" * 72)

from mpmath import iv
import random
random.seed(12345)

iv.dps = 40
mp.mp.dps = 50

def phi_n_derivs_iv(n, u_iv):
    pi = iv.pi; n2 = iv.mpf(n)**2; n4 = n2**2
    e9u2 = iv.exp(iv.mpf(9)*u_iv/2); e5u2 = iv.exp(iv.mpf(5)*u_iv/2)
    e2u = iv.exp(2*u_iv); e4u = e2u**2
    g = 2*pi**2*n4*e9u2 - 3*pi*n2*e5u2
    gp = 9*pi**2*n4*e9u2 - iv.mpf(15)*pi*n2*e5u2/2
    gpp = iv.mpf(81)*pi**2*n4*e9u2/2 - iv.mpf(75)*pi*n2*e5u2/4
    E = iv.exp(-pi*n2*e2u)
    Ep = -2*pi*n2*e2u*E
    Epp = (-4*pi*n2*e2u + 4*pi**2*n4*e4u)*E
    return g*E, gp*E + g*Ep, gpp*E + 2*gp*Ep + g*Epp

# Compute IA enclosure on [0.5, 0.501]
u_interval = iv.mpf([0.5, 0.501])
f=fp=fpp=iv.mpf(0)
for n in range(1, 6):
    a,b,c = phi_n_derivs_iv(n, u_interval)
    f+=a; fp+=b; fpp+=c
f*=4; fp*=4; fpp*=4
Q_iv = fpp*f - fp**2
Q_lo = float(Q_iv.a)
Q_hi = float(Q_iv.b)

# Now check 100 random points
all_contained = True
for _ in range(100):
    u_pt = 0.5 + random.random() * 0.001
    u_iv_pt = iv.mpf([u_pt, u_pt])
    f2=fp2=fpp2=iv.mpf(0)
    for n in range(1, 6):
        a,b,c = phi_n_derivs_iv(n, u_iv_pt)
        f2+=a; fp2+=b; fpp2+=c
    f2*=4; fp2*=4; fpp2*=4
    Q_pt = fpp2*f2 - fp2**2
    Q_pt_val = float((Q_pt.a + Q_pt.b)/2)
    if Q_pt_val < Q_lo or Q_pt_val > Q_hi:
        all_contained = False
        print("  NOT CONTAINED: u=%.6f Q=%.6e not in [%.6e, %.6e]" % (u_pt, Q_pt_val, Q_lo, Q_hi))
        break

print()
print("  IA enclosure [%.6e, %.6e]" % (Q_lo, Q_hi))
print("  100 random points in [0.5, 0.501]: all contained = %s" % all_contained)
print("  %s" % ("ATTACK FAILED: IA correctly encloses all point values." if all_contained else "*** IA ENCLOSURE IS WRONG ***"))

print()
print("=" * 72)
print("  DEEP FALSIFICATION SUMMARY")
print("  Attacks 21-26: results above")
print("=" * 72)
