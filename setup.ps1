$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
Set-Location $Root

if (-not (Test-Path '.venv\python.exe')) {
    conda create --prefix .venv python=3.12 git -y
}
$Python = Join-Path $Root '.venv\python.exe'
$Git = Join-Path $Root '.venv\Library\bin\git.exe'
if (-not (Test-Path 'ComfyUI\main.py')) {
    & $Git clone --depth 1 https://github.com/Comfy-Org/ComfyUI.git ComfyUI
}

& $Python -m pip install torch==2.12.1 torchvision==0.27.1 --index-url https://download.pytorch.org/whl/cu130
& $Python -m pip install -r ComfyUI\requirements.txt
& $Python scripts\download_models.py all
& $Python scripts\verify_install.py all
Write-Host '安装与静态验证完成。运行 start_comfyui.bat 启动。'
