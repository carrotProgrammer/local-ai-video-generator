@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\stop_comfyui.ps1"
if errorlevel 1 echo 停止失败，错误信息见上方。
pause
