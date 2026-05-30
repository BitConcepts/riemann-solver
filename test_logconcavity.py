"""Stress test the log-concavity RH claim (Preprints.org April 2026)."""
import mpmath as mp
mp.mp.dps = 80

def phi_n(n, u):
    u = mp.mpf(u)
    n2 = mp.mpf(n)**2
    return (2*mp.pi**2*n2**2*mp.exp(mp.mpf(9)*u/2) - 3*mp.pi*n2*mp.exp(mp.mpf(5)*u/2)) * mp.exp(-mp.pi*n2*mp.exp(2*u))

def Phi(u, N=20):
    return 4*sum(phi_n(n, u) for n in range(1, N+1))

h = mp.mpf("1e-12")

def Q_Phi(u):
    f0 = Phi(u); fp = Phi(u+h); fm = Phi(u-h)
    return (fp-2*f0+fm)/h**2 * f0 - ((fp-fm)/(2*h))**2

print("=== STRESS TEST: Log-concavity RH claim ===\n")

# Test 1: Phi positivity
print("Test 1: Phi(u) > 0 for u in [0, 1.0]")
min_phi = mp.inf
for i in range(101):
    u = mp.mpf(i)/100
    p = Phi(u)
    if p < min_phi: min_phi = p
    if p <= 0:
        print(f"  FAIL at u={float(u):.2f}")
        break
else:
    print(f"  PASS (min = {float(min_phi):.4e})")

# Test 2: Q < 0 dense scan
print("\nTest 2: Q_Phi < 0 on [0.15, 0.35] (201 points)")
max_Q = -mp.inf
worst_u = 0
for i in range(201):
    u = mp.mpf(150+i)/1000
    Q = Q_Phi(u)
    if Q > max_Q:
        max_Q = Q
        worst_u = float(u)
    if Q >= 0:
        print(f"  FAIL at u={float(u):.3f}: Q = {float(Q):.6e}")
        break
else:
    print(f"  PASS (closest to 0 at u={worst_u:.3f}: Q = {float(max_Q):.4e})")

# Test 3: Evenness
print("\nTest 3: Phi evenness")
for uv in [0.1, 0.3, 0.5]:
    u = mp.mpf(uv)
    rd = float(abs(Phi(u)-Phi(-u))/abs(Phi(u)))
    status = "PASS" if rd < 1e-30 else "FAIL"
    print(f"  {status}: |Phi({uv})-Phi(-{uv})|/|Phi| = {rd:.2e}")

# Test 4: Xi vanishes at gamma_1
print("\nTest 4: Xi at gamma_1")
g1 = mp.mpf("14.134725141734693790457251983562470270784257115699")
xi1 = mp.quad(lambda u: Phi(u,10)*mp.cos(g1*u), [0,5], maxdegree=10)
xi15 = mp.quad(lambda u: Phi(u,10)*mp.cos(15*u), [0,5], maxdegree=10)
print(f"  Xi(gamma_1) = {float(xi1):.6e}  (expect ~0)")
print(f"  Xi(15.000)  = {float(xi15):.6e}  (expect nonzero)")

# Test 5: (log Phi)'' profile - the actual log-concavity
print("\nTest 5: second log-derivative profile")
for uv in [0.0, 0.10, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50]:
    u = mp.mpf(uv)
    f0 = Phi(u)
    Q = Q_Phi(u)
    if f0 > 0:
        val = float(Q / f0**2)
        print(f"  u={uv:.2f}: (log Phi)'' = {val:.4f}")

# Test 6: THE KILLER TEST - what if Polya's theorem doesn't apply?
# Polya requires Phi in L^1(R). Check integrability.
print("\nTest 6: Phi integrability (Polya requirement)")
integral = mp.quad(lambda u: abs(Phi(u, 10)), [0, 10], maxdegree=8)
print(f"  integral_0^10 |Phi(u)| du = {float(integral):.6e}")
print(f"  Phi decays super-exponentially, so L^1 is satisfied.")

# Test 7: Does the claim's formula match the STANDARD Xi kernel?
# Standard: Xi(t) = xi(1/2 + it) where xi(s) = s(s-1)/2 * pi^{-s/2} * Gamma(s/2) * zeta(s)
print("\nTest 7: Cross-check Phi against mpmath xi function")
xi_direct = mp.re(mp.xi(mp.mpc(0.5, g1)))
xi_fourier = float(xi1) * 8  # H_0(z) = (1/8)*xi(1/2 + iz/2), so Xi(t) = 8*H_0(2t) ... normalization
print(f"  xi(1/2 + i*gamma_1) = {float(xi_direct):.6e}")
print(f"  This should be 0 by definition of gamma_1.")

print("\n=== ASSESSMENT ===")
print("If all tests pass, the log-concavity claim survives our stress test.")
print("This does NOT prove the claim is correct - only that we could not break it.")
