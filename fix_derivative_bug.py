"""Fix the g'' coefficient bug found by Attack 12.

g(u) = 2*pi^2*e^{9u/2} - 3*pi*e^{5u/2}
g'(u) = 9*pi^2*e^{9u/2} - (15/2)*pi*e^{5u/2}
g''(u) = 9*pi^2*(9/2)*e^{9u/2} - (15/2)*pi*(5/2)*e^{5u/2}
       = (81/2)*pi^2*e^{9u/2} - (75/4)*pi*e^{5u/2}

OUR CODE HAD: (81/4) instead of (81/2) for the first coefficient.
This is a factor-of-2 error in g''.
"""
import mpmath as mp
mp.mp.dps = 40

def phi_1(u):
    u = mp.mpf(u)
    return (2*mp.pi**2*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*mp.exp(mp.mpf(5)*u/2)) * mp.exp(-mp.pi*mp.exp(2*u))

print("=== DERIVATIVE BUG FIX VERIFICATION ===")
print()
print("Bug: g'' had coefficient 81/4 instead of 81/2")
print("     9 * (9/2) = 81/2, NOT 81/4")
print()

for u_val in [0.0, 0.1, 0.3, 0.5, 1.0]:
    u = mp.mpf(u_val)
    pi = mp.pi
    e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)
    e2u = mp.exp(2*u); e4u = e2u**2

    g = 2*pi**2*e9u2 - 3*pi*e5u2
    gp = 9*pi**2*e9u2 - mp.mpf(15)*pi*e5u2/2

    # WRONG:
    gpp_wrong = mp.mpf(81)/4*pi**2*e9u2 - mp.mpf(75)/4*pi*e5u2
    # CORRECT:
    gpp_right = mp.mpf(81)/2*pi**2*e9u2 - mp.mpf(75)/4*pi*e5u2

    E = mp.exp(-pi*e2u)
    Ep = -2*pi*e2u*E
    Epp = (-4*pi*e2u + 4*pi**2*e4u)*E

    fpp_wrong = gpp_wrong*E + 2*gp*Ep + g*Epp
    fpp_right = gpp_right*E + 2*gp*Ep + g*Epp
    fpp_mpmath = mp.diff(phi_1, u, 2)

    err_wrong = abs(float((fpp_wrong - fpp_mpmath) / fpp_mpmath)) if fpp_mpmath != 0 else 0
    err_right = abs(float((fpp_right - fpp_mpmath) / fpp_mpmath)) if fpp_mpmath != 0 else 0

    print("u=%.1f: wrong=%.6e right=%.6e mpmath=%.6e  err_wrong=%.2e err_right=%.2e" %
          (u_val, float(fpp_wrong), float(fpp_right), float(fpp_mpmath), err_wrong, err_right))

print()
print("NOW CHECK: Does Q_Phi still come out negative with the CORRECT formula?")
print()

def Q_Phi_fixed(u_val):
    u = mp.mpf(u_val)
    f = fp = fpp = mp.mpf(0)
    for n in range(1, 20):
        pi = mp.pi; n2 = mp.mpf(n)**2; n4 = n2**2
        e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)
        e2u = mp.exp(2*u); e4u = e2u**2
        g = 2*pi**2*n4*e9u2 - 3*pi*n2*e5u2
        gp = 9*pi**2*n4*e9u2 - mp.mpf(15)*pi*n2*e5u2/2
        # FIXED: 81/2 not 81/4
        gpp = mp.mpf(81)/2*pi**2*n4*e9u2 - mp.mpf(75)/4*pi*n2*e5u2
        E = mp.exp(-pi*n2*e2u)
        Ep = -2*pi*n2*e2u*E
        Epp = (-4*pi*n2*e2u + 4*pi**2*n4*e4u)*E
        f += g*E; fp += gp*E + g*Ep; fpp += gpp*E + 2*gp*Ep + g*Epp
    f *= 4; fp *= 4; fpp *= 4
    return fpp * f - fp**2

for u_val in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
    Q = float(Q_Phi_fixed(u_val))
    print("  u=%.1f: Q_Phi = %.6e  negative: %s" % (u_val, Q, Q < 0))
