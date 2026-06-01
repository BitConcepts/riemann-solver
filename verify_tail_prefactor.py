# Verify tail prefactor bound and compute corrected epsilon values
# Determines whether |phi_n|/phi_1 <= n^4 * exp(-pi*(n^2-1)*e^{2u}) is valid

import mpmath as mp
mp.mp.dps = 50

pi = mp.pi

def phi_n(n, u):
    """phi_n(u) = (2*pi^2*n^4*e^{9u/2} - 3*pi*n^2*e^{5u/2}) * e^{-pi*n^2*e^{2u}}"""
    return (2*pi**2*n**4*mp.exp(9*u/2) - 3*pi*n**2*mp.exp(5*u/2)) * mp.exp(-pi*n**2*mp.exp(2*u))

def B_n(n, u):
    """Actual prefactor ratio |phi_n|/phi_1 / exp(-pi*(n^2-1)*e^{2u})"""
    h_n = 2*pi*n**2*mp.exp(2*u) - 3
    h_1 = 2*pi*mp.exp(2*u) - 3
    return mp.mpf(n)**2 * h_n / h_1

def eps_old(u, N=15):
    """Old epsilon: sum_{n>=2} n^4 * exp(-pi*(n^2-1)*e^{2u})"""
    return sum(mp.mpf(n)**4 * mp.exp(-pi*(n**2-1)*mp.exp(2*u)) for n in range(2, N+1))

def eps_corrected(u, N=15):
    """Corrected epsilon: sum_{n>=2} B_n(u) * exp(-pi*(n^2-1)*e^{2u})"""
    return sum(B_n(n, u) * mp.exp(-pi*(n**2-1)*mp.exp(2*u)) for n in range(2, N+1))

def eps_factor2(u, N=15):
    """Conservative correction: 2 * sum_{n>=2} n^4 * exp(-pi*(n^2-1)*e^{2u})"""
    return 2 * eps_old(u, N)

print("=" * 70)
print("TAIL PREFACTOR AUDIT")
print("=" * 70)

print("\n--- Checking B_n(u) vs n^4 ---")
print(f"{'u':>5}  {'n':>3}  {'B_n(u)':>12}  {'n^4':>6}  {'B_n/n^4':>10}  {'valid?':>8}")
for u_val in [0.0, 1.0, 3.0]:
    for n in [2, 3, 4]:
        u = mp.mpf(u_val)
        b = float(B_n(n, u))
        n4 = n**4
        print(f"  {u_val:3.1f}  {n:3d}  {b:12.4f}  {n4:6d}  {b/n4:10.4f}  {'INVALID' if b > n4 else 'ok':>8}")

print("\n--- Epsilon values ---")
print(f"{'u':>6}  {'eps_old':>15}  {'eps_corrected':>15}  {'eps_factor2':>15}  {'ratio_corrected/old':>20}")
for u_val in [1.0, 1.5, 2.0, 3.0]:
    u = mp.mpf(u_val)
    e_old = float(eps_old(u))
    e_corr = float(eps_corrected(u))
    e_f2 = float(eps_factor2(u))
    print(f"  {u_val:4.1f}  {e_old:15.6e}  {e_corr:15.6e}  {e_f2:15.6e}  {e_corr/e_old:20.6f}")

print("\n--- Maximum B_n/n^4 ratio over all u>=0 ---")
print("B_n(u)/n^4 = 1 + 3(n^2-1) / (n^2 * h1(u))  where h1=2pi*e^{2u}-3")
print("Maximum at u=0: h1(0) = 2pi-3 =", float(2*pi-3))
for n in [2, 3, 4, 5]:
    u = mp.mpf(0)
    ratio = float(B_n(n, u) / mp.mpf(n)**4)
    print(f"  n={n}: B_n(0)/n^4 = {ratio:.6f}, global bound 1+3/(n^2*(2pi-3)) = {1+3/(n**2*float(2*mp.mpf(1)*pi-3)):.6f}")

print("\n--- Conservative global bound: B_n(u)/n^4 <= 1 + 3/(2pi-3) for all u>=0 ---")
global_bound = 1 + 3/float(2*pi-3)
print(f"  1 + 3/(2pi-3) = {global_bound:.6f} < 2  =>  factor-2 bound is valid")

print("\n--- Updated Proposition 5 (corrected |R|/phi_1 bound at u=0) ---")
u = mp.mpf(0)
old_sum = float(sum(mp.mpf(n)**4 * mp.exp(-pi*(n**2-1)*mp.exp(0)) for n in range(2, 20)))
corr_sum = float(sum(B_n(n, u) * mp.exp(-pi*(n**2-1)*mp.exp(0)) for n in range(2, 20)))
f2_sum = 2 * old_sum
print(f"  Old sum (n^4): {old_sum:.6e}")
print(f"  Corrected sum (B_n): {corr_sum:.6e}")
print(f"  Factor-2 sum (2*n^4): {f2_sum:.6e}")
print(f"  1/50 = {1/50:.6e}")
print(f"  Corrected < 1/50: {corr_sum < 1/50}")

print("\n--- C=204 audit under corrected eps ---")
# At u=1: lambda(1) = |DeltaQ| / (eps * |Q_phi1|) = 1.95e-27
# eps_old(1) = 9.59e-30
# eps_corrected(1) = ?
u = mp.mpf(1)
lam1 = mp.mpf('1.95e-27')  # lambda(1) = |DeltaQ|/|Q_phi1| which doesn't depend on eps
eps1_old = eps_old(u)
eps1_corr = eps_corrected(u)
C_old = lam1 / eps1_old
C_new = lam1 / eps1_corr
print(f"  eps_old(1) = {float(eps1_old):.4e}")
print(f"  eps_corrected(1) = {float(eps1_corr):.4e}")
print(f"  C_old = lambda/eps_old = {float(C_old):.2f}")
print(f"  C_new = lambda/eps_corrected = {float(C_new):.2f}")
print(f"  Using C=204 with eps_corrected: 204*eps_corr = {204*float(eps1_corr):.4e}")
print(f"  Still << margin 93.15: {204*float(eps1_corr) < 90}")
