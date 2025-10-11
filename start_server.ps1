# PowerShell script to start Mistral Assistant
Write-Host "Starting Mistral Assistant..." -ForegroundColor Green

# Change to script directory
Set-Location $PSScriptRoot

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install/update dependencies
Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Download NLTK data if needed
Write-Host "Checking NLTK data..." -ForegroundColor Yellow
python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Start the server
Write-Host "Starting server..." -ForegroundColor Green
python api\app.py
