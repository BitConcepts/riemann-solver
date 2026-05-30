import Lake
open Lake DSL

package RHProof where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]  
  moreLeanArgs := #["-DautoImplicit=false"]

@[default_target]
lean_lib RHProof
