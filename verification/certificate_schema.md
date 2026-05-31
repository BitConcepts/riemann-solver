# IA Certificate Schema (v1.0.0)

Machine-checkable interval-arithmetic certificate for the log-concavity
verification of the Riemann–Jacobi kernel Φ(u).

## Purpose

The certificate records the output of a full interval-arithmetic sweep of
Q_Φ(u) = Φ″(u)·Φ(u) − (Φ′(u))² on [0, 1].  If every subinterval's
rigorous upper bound on Q_Φ is strictly negative, log-concavity of Φ is
established on [0, 1].

The certificate is *not* a proof artifact by itself.  It must be paired with:
- A verifier (`verify_certificate.py`) that recomputes selected intervals.
- The algebraic core argument covering u > 1.
- The truncation error bound certifying that N=5 terms suffice.

## Top-level fields

- **schema_version** (string) — Semantic version of this schema.  Currently `"1.0.0"`.
- **description** (string) — Human-readable description.
- **metadata** (object) — Provenance and computation parameters.
- **data** (object) — The certified results.
- **data_sha256** (string) — SHA-256 hex digest of `json.dumps(data, sort_keys=True, separators=(",",":"))`.

## metadata

- **library** (string) — IA library used, e.g. `"python-flint (Arb/FLINT)"`.
- **library_version** (string) — Library version, e.g. `"0.8.0"`.
- **precision_bits** (int) — Arb working precision in bits (200 = ~60 decimal digits).
- **n_terms** (int) — Number of terms in the truncated kernel sum (N=5).
- **kernel** (string) — Formula for the kernel.
- **quantity_certified** (string) — The mathematical quantity whose negativity is certified.
- **date_utc** (string) — ISO 8601 UTC timestamp of generation.
- **git_commit** (string) — Full SHA-1 of the repository HEAD at generation time.
- **generator** (string) — Relative path to the generator script.
- **computation_time_s** (float) — Wall-clock time in seconds.

## data.grid

Deterministic grid parameters — sufficient to reconstruct every subinterval.

- **u_max** (float) — Right endpoint of the certified domain (1.0).
- **u_split** (float) — Boundary between coarse and fine regions.
- **n_coarse** (int) — Number of coarse subintervals on [0, u_split].
- **n_fine** (int) — Number of fine subintervals on [u_split, u_max].
- **total_subintervals** (int) — Must equal n_coarse + n_fine.
- **coarse_delta** (float) — Width of each coarse subinterval = u_split / n_coarse.
- **fine_delta** (float) — Width of each fine subinterval = (u_max − u_split) / n_fine.

### Interval reconstruction

For subinterval index `i` (0-based):
- If `i < n_coarse`: `[i * coarse_delta, (i+1) * coarse_delta]`
- If `i >= n_coarse`: let `j = i - n_coarse`, then `[u_split + j * fine_delta, u_split + (j+1) * fine_delta]`

## data.summary

- **certified** (int) — Number of subintervals where Q_Φ upper bound < 0.
- **failed** (int) — Number of subintervals that could not be certified.
- **all_certified** (bool) — True iff failed == 0.
- **global_max_Q_upper** (float) — Worst (closest to zero) upper bound across all intervals.
- **global_min_Q_upper** (float) — Best (most negative) upper bound.
- **global_mean_Q_upper** (float) — Mean upper bound.

## data.batch_bounds

Array of objects, one per batch of 100 consecutive subintervals.
Each batch records the worst-case (highest upper bound) interval in that batch.

- **batch_index** (int) — 0-based batch number.
- **interval_range** (array[int, int]) — [first_index, last_index] of intervals in this batch.
- **u_range** (array[float, float]) — [u_lo of first interval, u_hi of last interval].
- **n_intervals** (int) — Number of intervals in this batch (100, or fewer for the last batch).
- **n_certified** (int) — How many intervals in this batch were certified.
- **n_failed** (int) — How many failed.
- **worst_upper_bound** (float | null) — Highest Q upper bound in the batch (null if all failed).
- **worst_interval_index** (int | null) — Index of the worst interval.
- **worst_interval** (array[float, float] | null) — [u_lo, u_hi] of the worst interval.

## data.worst_intervals

Array of the 1000 intervals with highest (closest to zero) Q upper bounds,
sorted from worst to best.

- **index** (int) — Global subinterval index.
- **u_lo** (float) — Left endpoint.
- **u_hi** (float) — Right endpoint.
- **Q_upper_bound** (float) — Rigorous upper bound on Q_Φ over this interval (must be < 0).

## Verification procedure

1. Parse `certificate.json`.
2. Recompute `data_sha256` from the `data` field and compare.
3. Check metadata consistency (total = n_coarse + n_fine, certified + failed = total).
4. For each entry in `worst_intervals`, reconstruct [u_lo, u_hi] from grid parameters,
   recompute Q_Φ using Arb at the stated precision, and verify the upper bound is < 0.
5. For each entry in `batch_bounds`, recompute Q_Φ on the batch's worst interval
   and verify the upper bound is < 0.
6. Any single failure → overall FAIL.

## Limitations

- The certificate covers only [0, 1].  The domain [1, ∞) is handled by the
  algebraic core + perturbation bound argument (see `proof/verify_algebraic_core.py`).
- The certificate uses N=5 terms.  The truncation error from omitting n ≥ 6
  is bounded separately (see `proof/verify_truncation_and_crosscheck.py`):
  < 7.03×10⁻⁴³, which is negligible compared to the Q_Φ margin of ~3.36×10⁻¹².
- Verification depends on the correctness of the Arb/FLINT library.
  The mpmath.iv cross-check (52,898 intervals, independent library) provides
  defense-in-depth against single-library bugs.
