# Research Integration Loop

A repeatable process for harvesting new results and integrating them.
Run this periodically (weekly or before major computation runs).

## Protocol

### Step 1: Search for new papers
Query these sources for new RH-related results:
- arXiv: `cat:math.NT riemann hypothesis` (last 30 days)
- arXiv: `cat:math.NT connes weil positivity` (last 90 days)
- Zenodo: `riemann hypothesis proof` (last 90 days)
- Google Scholar: `"riemann hypothesis" proof OR disproof` (last year)

### Step 2: Classify findings
For each new result, classify as:
- **PROOF_CLAIM**: Claims to prove RH (assess rigor)
- **DISPROOF_CLAIM**: Claims counterexample (verify computationally)
- **PROOF_PROGRESS**: Advances toward proof without claiming it
- **COMPUTATIONAL**: New computational data (zeros, Li coefficients, etc.)
- **FRAMEWORK**: New mathematical framework applicable to RH
- **TOOL**: New computational tool relevant to our work

### Step 3: Assess proof claims
For any PROOF_CLAIM:
1. Is it published in a peer-reviewed journal? (if not, skepticism warranted)
2. Does it address a known equivalent formulation? (Li, Weil, DBN, etc.)
3. Can we reproduce the key computational step?
4. What is the community reception? (MathOverflow, MathSciNet reviews)
5. Does it have a gap we can identify?

### Step 4: Integrate findings
- Update `docs/REFERENCES.md` with new citations
- Update `docs/PROOF_STRATEGY.md` if the proof gap has narrowed
- Implement new computational checks if applicable
- Update `scaffold.yml` attack vector status if warranted

### Step 5: Log the integration
Append to `research_log.jsonl`:
```json
{"date": "2026-05-29", "query": "...", "findings": N, "integrated": M, "notes": "..."}
```

## Key Monitors

### Connes Program (highest priority)
- Has Connes published a follow-up to arXiv:2602.04022?
- Has the spectral convergence gap (CCM §8) been closed?
- New connes-cvs releases? New cutoffs verified?

### Geiger Even-Dominance (submitted proof)
- Has the Communications in Mathematics review concluded?
- Community response on MathOverflow?
- Any identified gaps?

### De Bruijn-Newman
- New upper bounds on Λ tighter than 0.22?
- New Lehmer pairs at very large height?

### Falsification Attempts
- Any claimed counterexamples to RH?
- New zeros computed at unprecedented height?
- Any Dirichlet L-function where GRH fails unexpectedly?

## Trigger: Run This Before Any Major Computation
Before starting the weekend runner or any deep computation,
run the research loop first — there may be new results that
change what computation is most valuable.
