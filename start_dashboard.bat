@echo off
echo Starting the Kino Dashboard...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run kino_overseer_web.py
pause
