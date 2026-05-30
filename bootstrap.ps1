# Bootstrap script for riemann-solver (Windows)
# Usage: .\bootstrap.ps1

Write-Host "=== Riemann Solver Bootstrap ===" -ForegroundColor Cyan

Write-Host "`nInstalling dependencies..."
pip install -r requirements.txt
pip install -e ".[dev]"

Write-Host "`nRunning unit tests..."
python -m pytest tests/ -v --tb=short

Write-Host "`nRunning proof verification (quick)..."
python verify.py --quick

Write-Host "`nRunning falsification audit (quick)..."
python falsify.py --quick

Write-Host "`n=== Bootstrap complete ===" -ForegroundColor Green
Write-Host "To run the full rigorous verification:  python verify.py"
Write-Host "To run all 32 falsification attacks:    python falsify.py"
Write-Host "To build the paper:                     cd paper; pdflatex main.tex; bibtex main; pdflatex main.tex; pdflatex main.tex"
