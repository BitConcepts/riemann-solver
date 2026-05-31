import Lake
open Lake DSL

package RHProof where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]
  moreLeanArgs := #["-DautoImplicit=false"]

-- Mathlib provides: Real.pi_gt_three, Real.exp_pos, Real.exp_le_exp,
--   Real.pi_pos, nlinarith, div_neg_of_neg_of_pos, pow_pos, and the
--   Analysis.SpecialFunctions.{Exp,Trigonometric.Basic} imports.
-- Run `lake update && lake build` after cloning to fetch Mathlib.
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.16.0"

@[default_target]
lean_lib RHProof
