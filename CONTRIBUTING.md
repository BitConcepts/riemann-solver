# Contributing

## Standards

This project targets the Clay Mathematics Institute Millennium Prize.
All contributions must meet the standards in `AGENTS.md`:

1. **Distinguish evidence from proof** — numerical results are not proofs
2. **Cite sources** — every non-trivial mathematical claim needs a reference
3. **Precision requirements** — see AGENTS.md §4
4. **Falsification** — every verification must be paired with a falsification attempt

## Development

```bash
# Setup
python -m venv .work/env
.work\env\Scripts\activate  # Windows
pip install -e ".[dev,cvs]"

# Test
pytest -v

# Lint
ruff check src/ tests/

# GPU detection
python -m riemann.gpu
```

## PR Process

1. Branch from `develop`
2. Ensure all tests pass
3. Ensure lint is clean
4. Fill out the PR template completely
5. Request review from @tpierson
