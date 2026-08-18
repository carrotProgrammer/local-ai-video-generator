$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $Root 'comfyui.pid'
if (-not (Test-Path $PidFile)) {
    Write-Host '未发现本项目的 ComfyUI PID 文件；服务可能未运行。'
    exit 0
}
$ComfyPid = [int](Get-Content $PidFile)
$Process = Get-Process -Id $ComfyPid -ErrorAction SilentlyContinue
if (-not $Process) {
    Remove-Item $PidFile -Force
    Write-Host '记录的进程已停止，已清理 PID 文件。'
    exit 0
}
$Expected = (Resolve-Path (Join-Path $Root '.venv\python.exe')).Path
$Actual = $Process.Path
if ($Actual -ne $Expected) { throw "PID $ComfyPid 不是本项目 Python（$Actual），拒绝停止。" }
Stop-Process -Id $ComfyPid
Wait-Process -Id $ComfyPid -ErrorAction SilentlyContinue
Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
Write-Host "ComfyUI 已停止（PID $ComfyPid）。"
