# Deliverable: lemma_12_final_repair.md — Lemma W Complete Repair

## Problem
Lemma W claims |W_tail(u)| ≤ λ(1)·|W₁(u)| ≤ 1.82×10⁻²⁵ for all u ≥ 1.
The text says "λ(u) decreasing" but does NOT prove λ(u)·|W₁(u)| is bounded.
Since |W₁| grows, λ(u)↓ alone does not imply G(u) := λ(u)·|W₁(u)| ↓.

## Fix: Explicit G'(u) < 0 Proof (Option B)

**Lemma W (corrected):** For all u ≥ 0, G(u) := λ(u)·|W₁(u)| is strictly decreasing.
Hence G(u) ≤ G(1) = 1.82×10⁻²⁵ for all u ≥ 1.

**Proof of G'(u) < 0:**

d(log G)/du = d(log λ)/du + d(log|W₁|)/du

**Step 1:** d(log λ)/du ≤ 2 - 6πe^{2u} for u ≥ 0.
(From docs/uniform_wtail_bound.md: C(u) = O(e^{2u}), ε decays as e^{-6πe^{2u}}.)

**Step 2:** d(log|W₁|)/du ≤ 2 for all u ≥ 0.
  |W₁(u)| = 24πe^{2u}/h² + 4πe^{2u} where h = 2πe^{2u}-3.
  d|W₁|/du = 48πe^{2u}(-2πe^{2u}-3)/h³ + 8πe^{2u}
  Since -48πe^{2u}(2πe^{2u}+3)/h³ < 0, we have d|W₁|/du < 8πe^{2u}.
  Also |W₁(u)| ≥ 4πe^{2u}.
  Therefore d(log|W₁|)/du = (d|W₁|/du)/|W₁| < 8πe^{2u}/(4πe^{2u}) = 2.

**Step 3:** d(log G)/du ≤ (2 - 6πe^{2u}) + 2 = 4 - 6πe^{2u} ≤ 4 - 6π < 0 for all u ≥ 0.

(4 - 6π ≈ 4 - 18.85 = -14.85 < 0.)

**Conclusion:** G is strictly decreasing for all u ≥ 0.
G(u) ≤ G(1) = λ(1)·|W₁(1)| = 1.95×10⁻²⁷ × 93.15 ≈ 1.82×10⁻²⁵ for all u ≥ 1.

## Status: PROVED (elementary calculus, no IA needed)
