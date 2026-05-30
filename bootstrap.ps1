# Bootstrap script for riemann-solver
# Usage: .\bootstrap.ps1

Write-Host "=== Riemann Solver Bootstrap ===" -ForegroundColor Cyan

# Install Python dependencies
Write-Host "`nInstalling dependencies..."
pip install -r requirements.txt
pip install -e .

# Run tests
Write-Host "`nRunning tests..."
python -m pytest tests/ -v --tb=short

# Run lint
Write-Host "`nRunning lint..."
ruff check src/ tests/ --select E,F,W --ignore E501

# Run proof verification (fast version)
Write-Host "`nRunning proof verification (log-concavity on [0, 0.5])..."
python proof/verify_logconcavity.py

Write-Host "`n=== Bootstrap complete ===" -ForegroundColor Green
Write-Host "To run the full rigorous verification: python proof/verify_logconcavity_rigorous.py"
Write-Host "To run all 32 falsification attacks:   python falsification/run_all.py"
Write-Host "To build the paper:                    cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex"
