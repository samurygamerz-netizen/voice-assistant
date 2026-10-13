@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer from python.org and enable "Add Python to PATH".
  pause
  exit /b 1
)
python main.py
if errorlevel 1 (
  echo FOXSI exited with an error. Read the message above.
  pause
)
endlocal
