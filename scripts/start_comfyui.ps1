$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root '.venv\python.exe'
$Main = Join-Path $Root 'ComfyUI\main.py'
$PidFile = Join-Path $Root 'comfyui.pid'

if (-not (Test-Path $Python)) { throw "未找到项目 Python：$Python。请先运行 setup.bat" }
if (-not (Test-Path $Main)) { throw "未找到 ComfyUI：$Main。请先运行 setup.bat" }
if (Test-Path $PidFile) {
    $OldPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($OldPid -and (Get-Process -Id $OldPid -ErrorAction SilentlyContinue)) {
        throw "ComfyUI 似乎已运行（PID $OldPid）。访问 http://127.0.0.1:8188"
    }
    Remove-Item $PidFile -Force
}

$Arguments = @(
    $Main,
    '--listen', '127.0.0.1',
    '--port', '8188',
    '--input-directory', (Join-Path $Root 'input'),
    '--output-directory', (Join-Path $Root 'output'),
    '--preview-method', 'auto',
    '--reserve-vram', '2'
)
Write-Host 'ComfyUI 正在使用 NVIDIA GPU 启动...'
Write-Host '访问地址：http://127.0.0.1:8188'
$Process = Start-Process -FilePath $Python -ArgumentList $Arguments -WorkingDirectory (Join-Path $Root 'ComfyUI') -NoNewWindow -PassThru
Set-Content -Path $PidFile -Value $Process.Id -Encoding ascii
try {
    Wait-Process -Id $Process.Id
    $Process.Refresh()
    if ($Process.ExitCode -ne 0) { throw "ComfyUI 异常退出，代码 $($Process.ExitCode)" }
}
finally {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
}
