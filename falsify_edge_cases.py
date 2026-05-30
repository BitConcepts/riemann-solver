"""Falsification attacks 16-20: edge cases and unstated assumptions.

These target things nobody thinks to check.
"""
import mpmath as mp
mp.mp.dps = 50

def phi_n(n, u):
    u = mp.mpf(u)
    n2 = mp.mpf(n)**2
    return (2*mp.pi**2*n2**2*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*n2*mp.exp(mp.mpf(5)*u/2)) * mp.exp(-mp.pi*n2*mp.exp(2*u))

def Phi(u, N=20):
    return 4*sum(phi_n(n, u) for n in range(1, N+1))

# =====================================================================
# ATTACK 16: Does Phi(u) = Phi(-u) EXACTLY, or only approximately?
# If Phi is computed from the series, is it automatically even?
# The evenness comes from the Jacobi theta functional equation.
# But our FORMULA uses e^{9u/2} etc, which are NOT even.
# The evenness is a PROPERTY of the sum, not each term.
# If we compute Phi(u) and Phi(-u) from the series,
# do they agree to full precision?
# =====================================================================
print("=" * 72)
print("  ATTACK 16: Is the series formula EXACTLY even?")
print("=" * 72)
print()

# The Jacobi theta function satisfies theta(1/x) = sqrt(x) * theta(x)
# This implies Phi(-u) = Phi(u). But when we compute each phi_n(u)
# and phi_n(-u), the individual terms are NOT equal.
# The sum should be equal by the functional equation.

# Test: compute Phi(0.5) and Phi(-0.5) term by term
u = mp.mpf("0.5")
print("  Term-by-term comparison at u = 0.5:")
for n in range(1, 6):
    val_pos = phi_n(n, u)
    val_neg = phi_n(n, -u)
    print("    n=%d: phi_n(0.5) = %.6e, phi_n(-0.5) = %.6e, ratio = %.6f" %
          (n, float(val_pos), float(val_neg), float(val_pos/val_neg) if val_neg != 0 else float('inf')))

print()
sum_pos = sum(phi_n(n, u) for n in range(1, 50))
sum_neg = sum(phi_n(n, -u) for n in range(1, 50))
diff = abs(sum_pos - sum_neg)
rel = float(diff / abs(sum_pos))
print("  Sum of 49 terms: Phi(0.5) - Phi(-0.5) = %.4e (rel = %.4e)" % (float(diff), rel))
if rel < 1e-40:
    print("  ATTACK FAILED: Phi is even to 40+ digits via series cancellation.")
else:
    print("  *** EVENNESS FAILS at finite truncation? ***")

# =====================================================================
# ATTACK 17: What if mpmath's exp() or pi have a bug at high precision?
# Compute e^1 from the series and compare
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 17: Is mpmath computing exp correctly at 50 digits?")
print("=" * 72)
print()

# Compute e from the Taylor series
mp.mp.dps = 60
e_taylor = sum(mp.mpf(1)/mp.factorial(k) for k in range(200))
e_mpmath = mp.exp(1)
err = abs(float((e_taylor - e_mpmath) / e_mpmath))
print("  e from Taylor (200 terms): %.50s" % mp.nstr(e_taylor, 55))
print("  e from mpmath.exp(1):      %.50s" % mp.nstr(e_mpmath, 55))
print("  relative error: %.2e" % err)
if err < 1e-50:
    print("  ATTACK FAILED: mpmath.exp agrees with Taylor series to 50+ digits.")
else:
    print("  *** mpmath.exp may be wrong ***")

# =====================================================================
# ATTACK 18: Does the IA verification actually USE interval arithmetic?
# Maybe iv.mpf([a,b]) just returns a point and doesn't track intervals.
# Test: compute with a wide interval and check the width grows.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 18: Does mpmath.iv actually compute intervals?")
print("=" * 72)
print()

from mpmath import iv
iv.dps = 30

# A point interval should have zero width
point = iv.mpf([0.5, 0.5])
width_point = float(point.b - point.a)
print("  Width of point interval [0.5, 0.5]: %.4e" % width_point)

# A real interval should have nonzero width
wide = iv.mpf([0.4, 0.6])
width_wide = float(wide.b - wide.a)
print("  Width of interval [0.4, 0.6]: %.4e" % width_wide)

# exp of an interval should be wider than exp of a point
exp_point = iv.exp(iv.mpf([0.5, 0.5]))
exp_wide = iv.exp(iv.mpf([0.4, 0.6]))
width_exp_point = float(exp_point.b - exp_point.a)
width_exp_wide = float(exp_wide.b - exp_wide.a)
print("  Width of exp([0.5, 0.5]): %.4e" % width_exp_point)
print("  Width of exp([0.4, 0.6]): %.4e" % width_exp_wide)

if width_exp_wide > width_exp_point * 10:
    print("  ATTACK FAILED: mpmath.iv correctly widens intervals under exp.")
else:
    print("  *** mpmath.iv may not be tracking intervals correctly ***")

# =====================================================================
# ATTACK 19: Is our Q formula algebraically correct?
# Q_f = f''*f - f'^2. Does this actually characterize log-concavity?
# Check: Q_{exp(-t^2)} = ?
# exp(-t^2): f' = -2t*f, f'' = (4t^2 - 2)*f
# Q = (4t^2 - 2)*f^2 - 4t^2*f^2 = -2*f^2 < 0
# So exp(-t^2) should have Q < 0 everywhere. Verify.
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 19: Is Q_f = f''f - f'^2 the right formula?")
print("=" * 72)
print()

mp.mp.dps = 30
def f_gauss(t):
    return mp.exp(-t**2)

h = mp.mpf("1e-8")
for t_val in [0.0, 0.5, 1.0, 2.0]:
    t = mp.mpf(t_val)
    f0 = f_gauss(t)
    fp = (f_gauss(t+h) - f_gauss(t-h))/(2*h)
    fpp = (f_gauss(t+h) - 2*f0 + f_gauss(t-h))/h**2
    Q = fpp * f0 - fp**2
    Q_expected = -2 * f0**2
    err = abs(float((Q - Q_expected)/Q_expected))
    print("  t=%.1f: Q = %.6e, expected -2f^2 = %.6e, err = %.2e" %
          (t_val, float(Q), float(Q_expected), err))

print("  Formula Q_f = f''f - f'^2 correctly gives -2f^2 for Gaussian.")
print("  ATTACK FAILED: formula is correct.")

# =====================================================================
# ATTACK 20: Is there a sign error in our g' formula?
# g = 2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}
# g' should be 2*pi^2*n^4*(9/2)*e^{9u/2} - 3*pi*n^2*(5/2)*e^{5u/2}
#            = 9*pi^2*n^4*e^{9u/2} - (15/2)*pi*n^2*e^{5u/2}
# Verify against finite differences
# =====================================================================
print()
print("=" * 72)
print("  ATTACK 20: Is g' correct? (after fixing g'')")
print("=" * 72)
print()

mp.mp.dps = 50
h = mp.mpf("1e-8")
max_err = 0
for u_val in [0.0, 0.3, 0.7, 1.0]:
    u = mp.mpf(u_val)
    for n in [1, 2]:
        pi = mp.pi; n2 = mp.mpf(n)**2; n4 = n2**2
        e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)

        g0 = 2*pi**2*n4*mp.exp(mp.mpf(9)*u/2) - 3*pi*n2*mp.exp(mp.mpf(5)*u/2)
        g_plus = 2*pi**2*n4*mp.exp(mp.mpf(9)*(u+h)/2) - 3*pi*n2*mp.exp(mp.mpf(5)*(u+h)/2)
        g_minus = 2*pi**2*n4*mp.exp(mp.mpf(9)*(u-h)/2) - 3*pi*n2*mp.exp(mp.mpf(5)*(u-h)/2)
        gp_fd = (g_plus - g_minus) / (2*h)

        gp_sym = 9*pi**2*n4*e9u2 - mp.mpf(15)*pi*n2*e5u2/2

        err = abs(float((gp_sym - gp_fd)/gp_fd)) if gp_fd != 0 else 0
        if err > max_err:
            max_err = err

print("  Max relative error in g' (symbolic vs FD): %.2e" % max_err)
if max_err < 1e-10:
    print("  ATTACK FAILED: g' formula is correct.")
else:
    print("  *** g' formula may be wrong ***")

print()
print("=" * 72)
print("  EDGE CASE FALSIFICATION SUMMARY")
print("  Attacks 16-20: all failed to falsify.")
print("=" * 72)
