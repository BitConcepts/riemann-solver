"""Run the real Connes-van Suijlekom Galerkin computation."""

import math
import time

import mpmath as mp
from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros

SEP = "=" * 72

print(SEP)
print("  CONNES-VAN SUIJLEKOM GALERKIN — REAL IMPLEMENTATION")
print("  Using connes-cvs package (Groskin 2026)")
print("  This is the closest existing infrastructure to a proof of RH.")
print(SEP)

c = 13
N = 50
T = 400
dps = 80

print(f"\nBuilding Q(c={c}), N={N}, T={T}, dps={dps}...")
t0 = time.time()
Q = build_galerkin_matrix(c=c, N=N, T=T, dps=dps)
t1 = time.time()
print(f"  Matrix built in {t1 - t0:.1f}s (dim={Q.rows}x{Q.cols})")

print("Diagonalizing...")
lam_min, eigvec = compute_ground_state(Q)
t2 = time.time()
print(f"  Diagonalized in {t2 - t1:.1f}s")
print(f"  lambda_min(c={c}) = {mp.nstr(lam_min, 15)}")
log_val = float(mp.log10(abs(lam_min)))
print(f"  log10|lambda_min| = {log_val:.1f}")

print("Extracting zeros from eigenvector...")
zeros = extract_zeros(eigvec, L=math.log(c), n_zeros=3)
t3 = time.time()

for z in zeros:
    gamma = z["gamma_detected"]
    err = z["error"]
    if err != 0:
        digits = -float(mp.log10(abs(err)))
    else:
        digits = float("inf")
    idx = z["index"]
    print(f"  gamma_{idx} = {mp.nstr(gamma, 30)}")
    print(f"    |error| = {mp.nstr(err, 6)} ({digits:.0f} matching digits)")

total = t3 - t0
print(f"\n  Total time: {total:.1f}s")
print(f"\n  SIGNIFICANCE: The zeros extracted from this operator are")
print(f"  PROVABLY on the critical line (Theorem 1.1(iii) of CCM 2025).")
print(f"  If their convergence to the actual Riemann zeros is proven,")
print(f"  the Riemann Hypothesis follows by Hurwitz's theorem.")
