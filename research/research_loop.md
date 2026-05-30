# Research Integration Loop

A repeatable process for monitoring the RH proof landscape and integrating
new results. Run periodically or before major computation runs.

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

### Step 3: Assess proof claims
For any PROOF_CLAIM:
1. Is it published in a peer-reviewed journal?
2. Does it address a known equivalent formulation?
3. Can we reproduce the key computational step?
4. What is the community reception? (MathOverflow, MathSciNet reviews)
5. Run the falsification audit: `python falsify.py --quick`

### Step 4: Integrate findings
- Update `docs/LANDSCAPE.md` with new entries
- Add new claims to `falsification/audit_external.py` if applicable
- Implement new computational checks if relevant
- Update `scaffold.yml` if the proof landscape has changed

### Step 5: Log the integration
Append to `research/research_log.jsonl`:
```json
{"date": "YYYY-MM-DD", "query": "...", "findings": N, "integrated": M, "notes": "..."}
```

## Key Monitors

### Log-concavity approaches (direct competitors)
- New preprints using the same Polya 1927 log-concavity approach?
- Has anyone identified a gap in the perturbation bound argument?
- Independent interval arithmetic reproductions?

### Connes spectral program
- Has the spectral convergence gap (CCM 2025, Section 8) been closed?
- New CvS Galerkin cutoffs verified?

### Geiger even-dominance
- Has the Communications in Mathematics review concluded?
- Community response on MathOverflow?

### De Bruijn-Newman constant
- New upper bounds on Lambda tighter than 0.22?
- New Lehmer pairs at very large height?

### Falsification
- Any claimed counterexamples to RH?
- New zeros computed at unprecedented height?
- Any Dirichlet L-function where GRH fails unexpectedly?
