# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tristen Kyle Pierson / BitConcepts Research
"""Use argument principle to count zeros of F(z) = int exp(-t^4) cos(zt) dt
in rectangles of the form [a,b] x [-h,h].

The argument principle: (1/2pi) * contour_integral F'/F dz = N_zeros - N_poles
Since F is entire (no poles), this gives the exact zero count.

If the count in [a,b] x [-h,h] exceeds the number of real zeros in [a,b],
then there must be complex zeros.
"""
import mpmath as mp
mp.mp.dps = 20

def F(z):
    z = mp.mpc(z)
    return mp.quad(lambda t: mp.exp(-t**4) * mp.cos(z * t), [0, 8], maxdegree=10)

def dF(z):
    """Numerical derivative of F."""
    h = mp.mpf("1e-8")
    return (F(z + h) - F(z - h)) / (2 * h)

def winding_number(a, b, h, n_pts=100):
    """Compute winding number of F around rectangle [a,b] x [-h,h].
    
    = number of zeros of F inside the rectangle (since F is entire).
    """
    # Parameterize the rectangle: bottom, right, top, left
    total_arg = mp.mpf(0)
    
    def arg_change_segment(z0, z1, n):
        """Compute total argument change of F along segment z0 -> z1."""
        total = mp.mpf(0)
        for i in range(n):
            t0 = mp.mpf(i) / n
            t1 = mp.mpf(i + 1) / n
            p0 = z0 + t0 * (z1 - z0)
            p1 = z0 + t1 * (z1 - z0)
            f0 = F(p0)
            f1 = F(p1)
            if abs(f0) > 0 and abs(f1) > 0:
                darg = float(mp.im(mp.log(f1 / f0)))
                total += darg
        return total
    
    # Four sides
    corners = [
        mp.mpc(a, -h), mp.mpc(b, -h),  # bottom
        mp.mpc(b, -h), mp.mpc(b, h),    # right
        mp.mpc(b, h), mp.mpc(a, h),     # top
        mp.mpc(a, h), mp.mpc(a, -h),    # left
    ]
    
    total = 0
    for i in range(0, 8, 2):
        total += arg_change_segment(corners[i], corners[i+1], n_pts)
    
    return total / (2 * mp.pi)

print("=== ARGUMENT PRINCIPLE: Counting zeros in rectangles ===\n")

# Count real zeros in several intervals
# We know real zeros at approximately: 3.45, 6.78, 9.64, 12.23, 14.65, 16.94, 19.14
# Test rectangles around pairs of real zeros

tests = [
    # (a, b, h, expected_real_zeros, description)
    (2, 5, 0.5, 1, "contains z~3.45"),
    (5, 8, 0.5, 1, "contains z~6.78"),
    (2, 8, 0.5, 2, "contains z~3.45, 6.78"),
    (17, 21, 0.5, 2, "contains z~19.14 + maybe complex?"),
    (17, 21, 2.0, 2, "wider: contains z~19.14 + complex?"),
    (0, 5, 3.0, 1, "wide rectangle near origin"),
]

for a, b, h, expected, desc in tests:
    print("Rectangle [%d,%d] x [%.1f,%.1f]: %s" % (a, b, -h, h, desc))
    try:
        w = winding_number(a, b, h, n_pts=80)
        w_rounded = round(float(w))
        print("  Winding number = %.4f (rounded: %d, expected real: %d)" % 
              (float(w), w_rounded, expected))
        if w_rounded > expected:
            print("  *** COMPLEX ZEROS DETECTED: %d total - %d real = %d complex ***" % 
                  (w_rounded, expected, w_rounded - expected))
        elif w_rounded == expected:
            print("  Consistent with real zeros only.")
        else:
            print("  Fewer than expected? Check boundaries.")
    except Exception as e:
        print("  ERROR: %s" % e)
    print()

print("=== CONCLUSION ===")
print("If any rectangle has winding number > expected real zeros,")
print("then exp(-t^4) has complex zeros in its cosine transform,")
print("and the Polya log-concavity approach to RH fails.")
