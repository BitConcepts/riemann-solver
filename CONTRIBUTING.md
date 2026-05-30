# Contributing

## Standards

This project targets the Clay Mathematics Institute Millennium Prize.
All contributions must meet the standards in `AGENTS.md`:

1. **Distinguish evidence from proof** — numerical results are not proofs
2. **Cite sources** — every non-trivial mathematical claim needs a reference
3. **Precision** — interval arithmetic at 60+ digits for all critical computations
4. **Falsification** — every verification must be paired with a falsification attempt
5. **SPDX headers** — all Python files must include `# SPDX-License-Identifier: MIT`

## Development

Requires Python 3.11+. Works on Linux, macOS, and Windows.

```bash
# Setup
pip install -r requirements.txt
pip install -e ".[dev]"

# Test
pytest -v

# Lint
ruff check src/ tests/ --select E,F,W --ignore E501

# Proof verification (quick)
python verify.py --quick

# Falsification suite (quick)
python falsify.py --quick
```

## PR Process

1. Branch from `main`
2. Ensure `python verify.py --quick` passes
3. Ensure `python falsify.py --quick` passes (self-audit 6/6)
4. Ensure lint and tests pass
5. CI must pass on all platforms (ubuntu, windows, macos)
6. Request review from @tbitcs
