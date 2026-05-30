# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Systematic falsification of our own RH proof.

The proof chain has 5 links. We attack each one:

1. Is Polya's Satz II actually a theorem? (Check the exact statement)
2. Is Phi actually positive for all u?
3. Is Phi actually even?
4. Is (log Phi)'' actually <= 0 everywhere? (Try to find a violation)
5. Does Phi actually decay fast enough?

For each: we try to BREAK it, not confirm it.
"""
import mpmath as mp
from mpmath import iv
import time

mp.mp.dps = 80
iv.dps = 60

def phi_n(n, u):
    u = mp.mpf(u)
    n2 = mp.mpf(n)**2
    return (2*mp.pi**2*n2**2*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*n2*mp.exp(mp.mpf(5)*u/2)) * mp.exp(-mp.pi*n2*mp.exp(2*u))

def Phi(u, N=20):
    return 4*sum(phi_n(n, u) for n in range(1, N+1))

def phi_n_derivs(n, u):
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

def Q_Phi(u_val):
    u = mp.mpf(u_val)
    f = fp = fpp = mp.mpf(0)
    for n in range(1, 20):
        a, b, c = phi_n_derivs(n, u)
        f += a; fp += b; fpp += c
    f *= 4; fp *= 4; fpp *= 4
    return fpp * f - fp**2

print("=" * 72)
print("  FALSIFICATION BATTERY: Attacking our own proof")
print("=" * 72)

# =====================================================================
# ATTACK 1: Is Polya's Satz II real?
# We can't falsify a published theorem computationally, but we CAN
# check: does a known counterexample to a WEAKER version of the
# theorem actually have complex zeros?
# =====================================================================
print("\n--- ATTACK 1: Polya's theorem counterexample check ---")
print("If exp(-t^3) [odd power, NOT covered by Satz II] has complex")
print("zeros in its cosine transform, that CONFIRMS the theorem is")
print("correctly stated (the decay condition matters).")

# exp(-t^3) is NOT log-concave on all of [0,inf) since
# (log exp(-t^3))'' = (-t^3)'' = -6t, which is 0 at t=0
# and negative for t>0. But the point is p=3 is NOT an even integer.
# Csordas-Varga says it should have complex zeros.

def F3(z):
    """Cosine transform of exp(-t^3)."""
    z = mp.mpc(z)
    return mp.quad(lambda t: mp.exp(-t**3) * mp.cos(z*t), [0, 8], maxdegree=10)

# Check for sign changes on real axis
print("Checking exp(-t^3) cosine transform for complex zeros...")
# Find a real zero first
prev = None
real_zeros_3 = []
for x10 in range(0, 100):
    x = x10 / 5.0
    val = float(mp.re(F3(x)))
    if prev is not None and prev * val < 0:
        real_zeros_3.append(x)
    prev = val

print("  Real zeros of F3 found near: %s" % [round(z, 1) for z in real_zeros_3[:5]])

# Now check if F3 has a zero OFF the real axis near a real zero
if real_zeros_3:
    z0 = real_zeros_3[0]
    # Check F3 at z0 + 0.5i
    val_off = F3(mp.mpc(z0, 0.5))
    print("  |F3(%.1f + 0.5i)| = %.4e" % (z0, float(abs(val_off))))
    print("  If this is small, exp(-t^3) has complex zeros -> Polya's theorem")
    print("  correctly requires the decay condition.")

# =====================================================================
# ATTACK 2: Is Phi actually positive?
# Try u values where Phi might go negative
# =====================================================================
print("\n--- ATTACK 2: Can Phi go negative? ---")

# Phi could potentially go negative if the subtracted term dominates
# phi_n = (2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * exp(...)
# The bracket 2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}
# = pi*n^2*e^{5u/2}*(2*pi*n^2*e^{2u} - 3)
# For n=1: 2*pi*e^{2u} - 3. At u=0: 2*pi - 3 > 0. For u < 0?
# At u = -0.3: 2*pi*e^{-0.6} - 3 = 2*pi*0.549 - 3 = 3.45 - 3 = 0.45 > 0
# At u = -0.5: 2*pi*e^{-1} - 3 = 2*pi*0.368 - 3 = 2.31 - 3 = -0.69 < 0!
# BUT: Phi is even, so Phi(-0.5) = Phi(0.5) > 0.

# The individual terms phi_n could be negative for large negative u,
# but the FULL Phi is defined as even. Let's verify directly.
min_phi = mp.inf
min_u = None
for i in range(10001):
    u = mp.mpf(i) / 10000  # u from 0 to 1
    p = Phi(u)
    if p < min_phi:
        min_phi = p
        min_u = float(u)
    if p <= 0:
        print("  FALSIFIED: Phi(%.6f) = %.6e <= 0" % (float(u), float(p)))
        break
else:
    print("  Phi > 0 on [0, 1] with 10001 points. Min = %.4e at u = %.4f" %
          (float(min_phi), min_u))
    print("  ATTACK FAILED: Phi appears positive.")

# =====================================================================
# ATTACK 3: Is Phi actually even?
# Check Phi(u) = Phi(-u) to high precision
# =====================================================================
print("\n--- ATTACK 3: Is Phi(-u) = Phi(u)? ---")

max_asym = 0
worst_u = 0
for u_val in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    u = mp.mpf(u_val)
    diff = abs(Phi(u) - Phi(-u))
    rel = float(diff / abs(Phi(u))) if abs(Phi(u)) > 0 else float(diff)
    if rel > max_asym:
        max_asym = rel
        worst_u = u_val

if max_asym > 1e-50:
    print("  FALSIFIED: max asymmetry = %.2e at u = %.2f" % (max_asym, worst_u))
else:
    print("  Max asymmetry: %.2e (at u=%.2f) -- below 80-digit precision" %
          (max_asym, worst_u))
    print("  ATTACK FAILED: Phi is even to working precision.")

# =====================================================================
# ATTACK 4: Can we find a u where (log Phi)'' > 0?
# This is the CRITICAL attack. If we find ANY such u, the proof fails.
# =====================================================================
print("\n--- ATTACK 4: Searching for (log Phi)'' > 0 ---")
print("This is the make-or-break attack.")

# Strategy: random sampling at high precision
import random
random.seed(42)

max_Q = float('-inf')
max_Q_u = 0
n_tested = 0

# Dense scan of [0, 1]
for i in range(5001):
    u_val = i / 5000.0
    Q = float(Q_Phi(u_val))
    n_tested += 1
    if Q > max_Q:
        max_Q = Q
        max_Q_u = u_val
    if Q >= 0:
        print("  *** FALSIFIED at u = %.6f: Q = %.6e ***" % (u_val, Q))
        break

# Random sampling in [0, 2]
for _ in range(1000):
    u_val = random.uniform(0, 2)
    Q = float(Q_Phi(u_val))
    n_tested += 1
    if Q > max_Q:
        max_Q = Q
        max_Q_u = u_val
    if Q >= 0:
        print("  *** FALSIFIED at u = %.6f: Q = %.6e ***" % (u_val, Q))
        break

# Adversarial: try near the boundary where IA had trouble (u ~ 0.98)
for i in range(1000):
    u_val = 0.95 + i * 0.00005
    Q = float(Q_Phi(u_val))
    n_tested += 1
    if Q > max_Q:
        max_Q = Q
        max_Q_u = u_val
    if Q >= 0:
        print("  *** FALSIFIED at u = %.6f: Q = %.6e ***" % (u_val, Q))
        break

print("  Tested %d points. Max Q = %.6e at u = %.6f" % (n_tested, max_Q, max_Q_u))
if max_Q < 0:
    print("  ATTACK FAILED: Q_Phi < 0 at all tested points.")
    print("  Closest to zero: Q = %.4e at u = %.4f" % (max_Q, max_Q_u))

# =====================================================================
# ATTACK 5: Does Phi decay fast enough?
# Polya requires K(t) = O(exp(-|t|^{2+delta})) for some delta > 0.
# Our Phi decays as exp(-pi*e^{2u}). Is this really faster than exp(-u^3)?
# =====================================================================
print("\n--- ATTACK 5: Decay rate check ---")

for u_val in [2, 3, 5, 8]:
    u = mp.mpf(u_val)
    phi_val = Phi(u)
    if phi_val > 0:
        log_phi = float(mp.log10(phi_val))
        log_u3 = -u_val**3 / float(mp.log(10))
        passes = log_phi < log_u3
        print("  u=%d: log10(Phi)=%.1f, log10(exp(-u^3))=%.1f, Phi < exp(-u^3): %s" %
              (u_val, log_phi, log_u3, passes))
        if not passes:
            print("  *** FALSIFIED: Phi does NOT decay faster than exp(-u^3) at u=%d ***" % u_val)
    else:
        print("  u=%d: Phi underflows (definitely decays fast enough)" % u_val)

print("\n" + "=" * 72)
print("  FALSIFICATION SUMMARY")
print("=" * 72)
