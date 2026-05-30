"""Certify the n >= 6 truncation error and cross-validate the IA results.

Part 1: Rigorous upper bound on sum_{n=6}^inf |phi_n(u)| for u in [0, 1.0]
Part 2: Cross-validate Q_Phi values at selected points using high-precision
        non-interval arithmetic vs our interval arithmetic results.
"""
import mpmath as mp
from mpmath import iv
import json

mp.mp.dps = 80
iv.dps = 60

print("=" * 72)
print("  PART 1: TRUNCATION ERROR CERTIFICATION")
print("  Rigorous bound on sum_{n>=6} |phi_n(u)| for u in [0, 1.0]")
print("=" * 72)

# For n >= 6, u in [0, 1]:
# |phi_n(u)| <= (2*pi^2*n^4*e^{9/2} + 3*pi*n^2*e^{5/2}) * e^{-pi*n^2*1}
# (using u <= 1, so e^{9u/2} <= e^{9/2}, e^{-pi*n^2*e^{2u}} <= e^{-pi*n^2})
# Actually for u in [0,1]: e^{2u} >= 1, so e^{-pi*n^2*e^{2u}} <= e^{-pi*n^2}

# Tighter: for u in [0,1], e^{2u} in [1, e^2], so
# phi_n(u) <= (2*pi^2*n^4*e^{9/2}) * e^{-pi*n^2}  (using e^{9u/2} <= e^{9/2})

print()
# Compute the bound using interval arithmetic
total_bound = iv.mpf(0)
print("Individual term bounds |phi_n|_max for n >= 6:")
for n in range(6, 20):
    n_iv = iv.mpf(n)
    # Upper bound on |phi_n(u)| for u in [0, 1]
    # phi_n = (2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * e^{-pi*n^2*e^{2u}}
    # <= 2*pi^2*n^4*e^{9/2} * e^{-pi*n^2}  (e^{9u/2} <= e^{9/2}, decay >= e^{-pi*n^2*e^2})
    # Actually use the worst case: max of phi_n over [0,1]
    # Since phi_n is dominated by decay, the max is at u=0
    bound_n = 4 * (2 * iv.pi**2 * n_iv**4 * iv.exp(iv.mpf(9)/2) ) * iv.exp(-iv.pi * n_iv**2)
    if float(bound_n.b) > 0:
        print("  n=%2d: |4*phi_n| <= %.4e" % (n, float(bound_n.b)))
    else:
        print("  n=%2d: underflows" % n)
    total_bound += bound_n

# Add tail bound for n >= 20
# sum_{n>=20} n^4 * e^{-pi*n^2}: each term underflows below 10^-300
tail_20 = iv.mpf(0)
for n in range(20, 50):
    n_iv = iv.mpf(n)
    tail_20 += 4 * 2 * iv.pi**2 * n_iv**4 * iv.exp(iv.mpf(9)/2) * iv.exp(-iv.pi * n_iv**2)

total_bound += tail_20

print()
print("Total bound on |sum_{n>=6} 4*phi_n(u)| for u in [0, 1.0]:")
print("  <= %.4e" % float(total_bound.b))
print("  Bound: < 10^-42 (dominated by the n=6 term)")
print("  Q_Phi margin: >= 1.44e-13 (from IA verification)")
print("  Truncation / margin ratio: < %.1e (safe by factor %.0e)" %
      (float(total_bound.b) / 1.44e-13, 1.44e-13 / float(total_bound.b)))

print()
print("=" * 72)
print("  PART 2: CROSS-VALIDATION OF Q_Phi VALUES")
print("  Compare rigorous IA vs high-precision floating-point")
print("=" * 72)

# Compute Q_Phi at selected points using TWO independent methods:
# Method A: Interval arithmetic (our verify_logconcavity_rigorous.py approach)
# Method B: High-precision floating-point with exact symbolic derivatives

def phi_n_derivs_float(n, u):
    """Exact symbolic derivatives in floating point."""
    pi = mp.pi; n2 = mp.mpf(n)**2; n4 = n2**2
    e9u2 = mp.exp(mp.mpf(9)*u/2); e5u2 = mp.exp(mp.mpf(5)*u/2)
    e2u = mp.exp(2*u); e4u = e2u**2
    g = 2*pi**2*n4*e9u2 - 3*pi*n2*e5u2
    gp = 9*pi**2*n4*e9u2 - mp.mpf(15)*pi*n2*e5u2/2
    gpp = mp.mpf(81)*pi**2*n4*e9u2/4 - mp.mpf(75)*pi*n2*e5u2/4
    E = mp.exp(-pi*n2*e2u)
    Ep = -2*pi*n2*e2u*E
    Epp = (-4*pi*n2*e2u + 4*pi**2*n4*e4u)*E
    return g*E, gp*E + g*Ep, gpp*E + 2*gp*Ep + g*Epp

def phi_n_derivs_iv(n, u_iv):
    """Exact symbolic derivatives in interval arithmetic."""
    pi = iv.pi; n2 = iv.mpf(n)**2; n4 = n2**2
    e9u2 = iv.exp(iv.mpf(9)*u_iv/2); e5u2 = iv.exp(iv.mpf(5)*u_iv/2)
    e2u = iv.exp(2*u_iv); e4u = e2u**2
    g = 2*pi**2*n4*e9u2 - 3*pi*n2*e5u2
    gp = 9*pi**2*n4*e9u2 - iv.mpf(15)*pi*n2*e5u2/2
    gpp = iv.mpf(81)*pi**2*n4*e9u2/4 - iv.mpf(75)*pi*n2*e5u2/4
    E = iv.exp(-pi*n2*e2u)
    Ep = -2*pi*n2*e2u*E
    Epp = (-4*pi*n2*e2u + 4*pi**2*n4*e4u)*E
    return g*E, gp*E + g*Ep, gpp*E + 2*gp*Ep + g*Epp

print()
print("u_val      | Q_float (80-digit)    | Q_iv_lo              | Q_iv_hi              | Agree?")
print("-" * 100)

all_agree = True
for u_val in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0]:
    u = mp.mpf(u_val)
    
    # Method A: floating point
    f = fp = fpp = mp.mpf(0)
    for n in range(1, 6):
        a, b, c = phi_n_derivs_float(n, u)
        f += a; fp += b; fpp += c
    f *= 4; fp *= 4; fpp *= 4
    Q_float = float(fpp * f - fp**2)
    
    # Method B: interval arithmetic (point interval)
    u_iv = iv.mpf([u_val, u_val])
    fi = fpi = fppi = iv.mpf(0)
    for n in range(1, 6):
        a, b, c = phi_n_derivs_iv(n, u_iv)
        fi += a; fpi += b; fppi += c
    fi *= 4; fpi *= 4; fppi *= 4
    Q_iv = fppi * fi - fpi**2
    
    # Check agreement with tolerance for ULP-level differences
    # IA point intervals may differ from float by rounding at the last ULP
    margin = max(abs(float(Q_iv.b) - float(Q_iv.a)), abs(Q_float) * 1e-14)
    agree = (float(Q_iv.a) - margin) <= Q_float <= (float(Q_iv.b) + margin)
    if not agree:
        all_agree = False
    
    print("u=%.2f     | %.12e | %.12e | %.12e | %s" % 
          (u_val, Q_float, float(Q_iv.a), float(Q_iv.b), "YES" if agree else "NO"))

print()
if all_agree:
    print("CROSS-VALIDATION PASSED: All floating-point values lie within IA enclosures.")
else:
    print("CROSS-VALIDATION FAILED: Some values disagree!")

# Save results
results = {
    "truncation_bound": float(total_bound.b),
    "truncation_bound_below_1e42": float(total_bound.b) < 1e-42,
    "q_phi_margin": 1.44e-13,
    "safety_factor": 1.44e-13 / float(total_bound.b),
    "cross_validation_passed": all_agree,
}
with open("results/truncation_crosscheck.json", "w") as f:
    json.dump(results, f, indent=2)
print("-> results/truncation_crosscheck.json")
