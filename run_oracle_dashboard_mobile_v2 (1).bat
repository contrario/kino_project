@echo off
echo Starting Oracle Dashboard...
start /B cmd /C "streamlit run oracle_dashboard.py"
timeout /t 10 > nul
echo Launching ngrok tunnel on port 8501...
start /B cmd /C "ngrok http 8501"
pause
