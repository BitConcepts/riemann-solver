#!/usr/bin/env bash
# Bootstrap script for riemann-solver (Linux / macOS)
# Usage: bash bootstrap.sh
set -euo pipefail

echo "=== Riemann Solver Bootstrap ==="

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -e ".[dev]"

echo ""
echo "Running unit tests..."
python -m pytest tests/ -v --tb=short

echo ""
echo "Running proof verification (quick)..."
python verify.py --quick

echo ""
echo "Running falsification audit (quick)..."
python falsify.py --quick

echo ""
echo "=== Bootstrap complete ==="
echo "To run the full rigorous verification:  python verify.py"
echo "To run all 32 falsification attacks:    python falsify.py"
echo "To build the paper:                     cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex"
