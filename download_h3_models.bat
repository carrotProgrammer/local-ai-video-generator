@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\python.exe" (
    echo Project Python was not found. Run setup.bat first.
    pause
    exit /b 1
)
".venv\python.exe" "scripts\download_models.py" h3
if errorlevel 1 (
    echo MiniMax H3 model download failed. See error above.
    pause
    exit /b 1
)
echo MiniMax H3 models are ready.
pause
