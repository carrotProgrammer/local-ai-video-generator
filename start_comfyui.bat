@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_comfyui.ps1"

if errorlevel 1 (
    echo.
    echo ComfyUI failed to start. See error above.
)

echo.
echo Press any key to close.
pause >nul