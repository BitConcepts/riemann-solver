import Lake
open Lake DSL

package RHProof where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib RHProof where
  srcDir := "RHProof"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "master"
