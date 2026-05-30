# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Does the cosine transform of exp(-t^4) have only real zeros?

This is the CRITICAL test. The log-concavity preprint claims:
  'exp(-t^4) is log-concave but its cosine transform has complex zeros'

If TRUE: log-concavity is NOT sufficient for RH, and the Polya approach fails.
If FALSE: the counterexample is wrong, and the Polya approach may work.

F(z) = integral_0^inf exp(-t^4) cos(zt) dt
"""
import mpmath as mp
mp.mp.dps = 30

def F(z):
    """Cosine transform of exp(-t^4) at complex z."""
    z = mp.mpc(z)
    return mp.quad(lambda t: mp.exp(-t**4) * mp.cos(z * t), [0, 10], maxdegree=12)

# First: find real zeros by sign changes
print("=== REAL ZEROS of F(z) = int exp(-t^4) cos(zt) dt ===\n")
print("Scanning real axis for sign changes:")
prev_val = None
real_zeros = []
for x_10 in range(0, 300):
    x = x_10 / 10.0
    val = float(mp.re(F(x)))
    if prev_val is not None and prev_val * val < 0:
        # Sign change - find zero by bisection
        a, b = x - 0.1, x
        for _ in range(50):
            mid = (a + b) / 2
            if float(mp.re(F(mid))) * float(mp.re(F(a))) < 0:
                b = mid
            else:
                a = mid
        real_zeros.append((a + b) / 2)
        print("  zero at z = %.6f" % ((a + b) / 2))
    prev_val = val

print("\nFound %d real zeros in [0, 30]" % len(real_zeros))

# Now: check for complex zeros near the real axis
print("\n=== CHECKING FOR COMPLEX ZEROS ===")
print("If F(x + iy) = 0 for y != 0, then log-concavity is NOT sufficient.\n")

found_complex = False
for y_val in [0.1, 0.5, 1.0, 2.0, 3.0]:
    for x_10 in range(0, 200, 5):
        x = x_10 / 10.0
        z = mp.mpc(x, y_val)
        val = F(z)
        mag = abs(val)
        if mag < 1e-6:
            print("  NEAR ZERO at z = %.1f + %.1fi: |F| = %.2e" % (x, y_val, float(mag)))
            found_complex = True

if not found_complex:
    print("  No complex zeros found with |y| in {0.1, 0.5, 1, 2, 3}")
    print("  and x in [0, 20].")

# Direct test: evaluate F at purely imaginary points
print("\n=== F on imaginary axis (should be positive if no complex zeros nearby) ===")
for y in [1, 2, 5, 10]:
    val = F(mp.mpc(0, y))
    print("  F(i*%d) = %.6e" % (y, float(mp.re(val))))

print("\n=== CONCLUSION ===")
if found_complex:
    print("COMPLEX ZEROS FOUND: exp(-t^4) IS a valid counterexample.")
    print("Log-concavity is NOT sufficient. The Polya approach to RH FAILS.")
else:
    print("NO complex zeros found in our search region.")
    print("The counterexample exp(-t^4) may be WRONG.")
    print("If Polya's theorem says log-concavity => real zeros,")
    print("and our Phi passes log-concavity, then RH follows.")
    print("\nCAVEAT: We only searched a finite region.")
    print("A definitive answer requires either a proof or")
    print("a more exhaustive search.")
