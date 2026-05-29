"""Quick CvS Galerkin run at c=17."""
from connes_cvs import build_galerkin_matrix, compute_ground_state, extract_zeros
import mpmath as mp
import math, time

mp.mp.dps = 80
print("CvS Galerkin c=17, N=50, T=400, dps=80")
t0 = time.time()
Q = build_galerkin_matrix(c=17, N=50, T=400, dps=80)
lam_min, eigvec = compute_ground_state(Q)
zeros = extract_zeros(eigvec, L=math.log(17), n_zeros=3, dps=80)
t1 = time.time()
print(f"  lambda_min = {mp.nstr(lam_min, 12)}")
log_val = float(mp.log10(abs(lam_min)))
print(f"  log10|lambda_min| = {log_val:.1f}")
for z in zeros:
    g = z["gamma_detected"]
    e = z["error"]
    k = z["k"]
    if g is not None and e is not None and e != 0:
        d = -float(mp.log10(abs(e)))
        print(f"  gamma_{k}: {mp.nstr(g, 25)}, {d:.0f} matching digits")
    else:
        print(f"  gamma_{k}: not detected")
print(f"  Time: {t1-t0:.0f}s")
