@echo off
echo Starting Mistral Assistant...
cd /d "%~dp0"
call venv\Scripts\activate
python api\app.py
pause
