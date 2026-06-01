"""CvS 8-cutoff sweep at medium precision (Job B)."""
import sys, json, time, math
sys.path.insert(0, '.')
import connes_cvs
import mpmath as mp

cutoffs = [13, 17, 19, 23, 29, 37, 47, 53]
N, dps = 10, 40
results = []
prev_log10 = None

print(f'CvS sweep N={N} dps={dps}')
header = f"{'c':>5}  {'log10|lam_min|':>16}  {'delta':>8}  {'elapsed':>8}"
print(header)

for c in cutoffs:
    t0 = time.time()
    mp.mp.dps = dps
    Q = connes_cvs.build_galerkin_matrix(c=c, N=N, T=100, dps=dps)
    lam, _ = connes_cvs.compute_ground_state(Q)
    el = time.time() - t0
    la = abs(float(mp.nstr(lam, 6)))
    l10 = math.log10(la) if la > 0 else float('-inf')
    delta = abs(l10 - prev_log10) if prev_log10 is not None else None
    delta_str = f"{delta:>8.2f}" if delta is not None else "     ---"
    print(f'{c:>5}  {l10:>16.2f}  {delta_str}  {el:>7.1f}s')
    results.append({'c': c, 'log10_lam': l10, 'delta': delta, 'elapsed': el})
    prev_log10 = l10

import os
os.makedirs('results', exist_ok=True)
with open('results/cvs_sweep_N10.json', 'w') as f:
    json.dump(results, f, indent=2)
print('Saved to results/cvs_sweep_N10.json')

total_elapsed = sum(r['elapsed'] for r in results)
print(f'\nTotal elapsed: {total_elapsed:.1f}s')
