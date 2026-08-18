# Local AI Video Generator

**First/last-frame animation and synchronized audio with ComfyUI**

**English** | [简体中文](README.zh-CN.md)

[![Windows 11](https://img.shields.io/badge/Windows-11-0078D4?logo=windows11&logoColor=white)](https://www.microsoft.com/windows/)
[![ComfyUI 0.30+](https://img.shields.io/badge/ComfyUI-0.30%2B-222222)](https://github.com/Comfy-Org/ComfyUI)
[![RTX 5090 verified](https://img.shields.io/badge/GPU-RTX%205090%20verified-76B900?logo=nvidia&logoColor=white)](https://www.nvidia.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Run advanced image-to-video workflows locally on Windows. This repository installs and manages a dedicated ComfyUI environment for two model families:

- **Wan2.2 Fun InP A14B** — first-frame and last-frame video generation with quality and LightX2V fast modes.
- **MiniMax H3 FL2VA** — first-frame and last-frame video generation with synchronized stereo audio in the same inference pass.

> [!IMPORTANT]
> The one-click installer is written and tested for **Windows 11 + NVIDIA GeForce RTX 5090 (32 GB VRAM) + CUDA 13.0**. It installs the PyTorch 2.12.1 `cu130` build and does not automatically select a different build for other GPUs. Other NVIDIA cards may require dependency and memory-setting changes. AMD, Intel, Apple Silicon, and CPU-only environments are not currently supported.

## Highlights

- Animate the transition between a chosen start image and end image.
- Generate synchronized stereo audio with MiniMax H3 FL2VA.
- Switch between Wan2.2 quality and LightX2V fast modes.
- Install ComfyUI, Python dependencies, and approximately 75 GiB of models with `setup.bat`.
- Resume interrupted Hugging Face downloads and skip already verified files.
- Validate CUDA, GPU support, ComfyUI, workflows, and every model file.
- Keep model weights, prompts, input media, outputs, caches, and logs off GitHub.

## Included workflows

| Workflow | Input | Output | Best for |
| --- | --- | --- | --- |
| `Wan2.2_Fun_InP_快速测试_512_33帧.json` | Start + end image | 512px, 33-frame video | Fast installation checks |
| `Wan2.2_Fun_InP_官方_质量与快速.json` | Start + end image | Quality or LightX2V video | Final silent video generation |
| `MiniMax_H3_FL2VA_官方.json` | Start image, optional end image | 5-second video with stereo audio | Audio-video generation |

The MiniMax workflow extends the official ComfyUI I2V template by connecting the last-frame input. It keeps the official sampling graph and requires no custom nodes.

## Requirements

The following configuration is the only one verified end to end:

| Component | Verified configuration |
| --- | --- |
| Operating system | Windows 11 with Windows PowerShell 5.1 |
| GPU | NVIDIA GeForce RTX 5090, 31.84 GiB available VRAM |
| PyTorch / CUDA | PyTorch 2.12.1 + CUDA 13.0 with `sm_120` support |
| ComfyUI | 0.30.0 or later; 0.31.0 used for release verification |

Before installation, make sure you also have:

- Conda installed and available through `conda --version` in PowerShell.
- Access to GitHub, the PyTorch package index, and Hugging Face.
- A stable connection for approximately **75 GiB** of model downloads.
- At least **100 GiB** of free disk space; allow more if download caches are retained.
- Enough system memory for ComfyUI to offload model weights.

The scripts do not detect the GPU model or automatically reconfigure PyTorch for RTX 4090, RTX 3090, workstation, or lower-VRAM cards.

## Quick start

Open PowerShell and run:

```powershell
git clone https://github.com/carrotProgrammer/local-ai-video-generator.git
cd local-ai-video-generator
.\setup.bat
```

You can also download the repository ZIP and double-click `setup.bat`.

The setup script will:

1. Create a project-local Conda environment in `.venv` with Python 3.12 and Git.
2. Clone the official [ComfyUI](https://github.com/Comfy-Org/ComfyUI) repository into `ComfyUI`.
3. Install PyTorch 2.12.1, TorchVision 0.27.1, the CUDA 13.0 build, and ComfyUI dependencies.
4. Download all Wan2.2 and MiniMax H3 models, approximately 75 GiB in total.
5. Verify CUDA, GPU support, ComfyUI, all three workflows, and every model file size.

Successful model downloads are reused on later runs, while incomplete downloads are resumed when possible.

Start ComfyUI after setup and verification finish:

```powershell
.\start_comfyui.bat
```

Open <http://127.0.0.1:8188> if the browser does not open automatically.

## Generate with MiniMax H3 FL2VA

1. Drag `workflows/MiniMax_H3_FL2VA_官方.json` onto the ComfyUI canvas.
2. Select your start and end images in the two `Load Image` nodes. Disconnect the end image for regular single-image I2V.
3. Use images with a similar aspect ratio. Begin with `0.4 MP`, then increase to about `0.98 MP` after validating the motion; 16:9 is approximately 1344×768.
4. Describe the visuals, motion, camera, and sound in the prompt. For example:

   `The camera slowly pushes in as the subject moves naturally from the opening pose to the final pose, preserving identity and clothing. Audio: quiet indoor ambience, soft footsteps, no music.`

5. Keep the default duration at 5 seconds for the first run. H3 generates at 24 fps and aligns the frame count to the required `17k+5` grid.
6. Press `Ctrl+Enter`. The MP4 with audio is saved under `output/video`.

### H3 memory and performance

- Start with `0.4 MP / 5 seconds` on the RTX 5090, then increase the resolution.
- Do not add `--highvram`; ComfyUI needs to offload some H3 weights to system memory.
- Close other GPU-heavy applications and do not run Wan2.2 and H3 jobs simultaneously.
- Restart ComfyUI after an out-of-memory error to release fragmented VRAM.
- Keep the native H3 canvas short edge at or below 768 and dimensions divisible by 32.

## Generate with Wan2.2

Choose one of the included workflows:

- Fast check: `workflows/Wan2.2_Fun_InP_快速测试_512_33帧.json`
- Quality and fast modes: `workflows/Wan2.2_Fun_InP_官方_质量与快速.json`

Drag the workflow onto the canvas, choose the start and end images, enter a positive prompt, and press `Ctrl+Enter`. Wan frame counts follow `4n+1`, such as 33, 49, or 81 frames. The workflows save video at 16 fps.

## Download only MiniMax H3

If Wan2.2 is already installed, download and verify only the H3 models, approximately 39.56 GiB:

```powershell
.\download_h3_models.bat
```

Non-interactive equivalents:

```powershell
.\.venv\python.exe .\scripts\download_models.py h3
.\.venv\python.exe .\scripts\verify_install.py h3
```

The workflow uses the official quantized components from [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3):

| Component | Size |
| --- | ---: |
| `diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors` | 19.53 GiB |
| `text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 14.61 GiB |
| `vae/minimax_h3_video_vae_fp16.safetensors` | 4.85 GiB |
| `vae/minimax_h3_audio_vae_fp32.safetensors` | 0.56 GiB |

## Start, stop, and verify

```powershell
# Start the installed ComfyUI service
.\start_comfyui.bat

# Stop the service
.\stop_comfyui.bat

# Validate the complete installation
.\.venv\python.exe .\scripts\verify_install.py all
```

Inputs belong in `input`; generated media is written to `output`. The launcher reserves 2 GiB of VRAM and uses `comfyui.pid` to prevent duplicate instances.

## Privacy and repository scope

The public repository contains only setup and service scripts, the model manifest, and reusable workflow templates. `.gitignore` excludes:

- The cloned ComfyUI source and project environment.
- Model weights and interrupted downloads.
- Input images, videos, generated output, and logs.
- Hugging Face caches, PID files, environment files, and local experiment data.

Workflow templates use generic `start_image.png` and `end_image.png` placeholders. Review newly saved workflows before committing them if they contain private prompts or local paths.

## Troubleshooting

- **`MISSING/INCOMPLETE`** — rerun the relevant download command; the script will attempt to resume.
- **`MiniMaxH3ImageToVideo` is missing** — update ComfyUI to version 0.30.0 or later.
- **H3 model selectors are empty** — confirm the four model files are in `diffusion_models`, `text_encoders`, and `vae`, then restart ComfyUI.
- **A PID file exists but the service is stopped** — the launcher removes stale PID files automatically; `stop_comfyui.bat` can also clean it up.
- **Out of memory** — lower resolution or duration, close other GPU applications, and restart ComfyUI.

## Repository structure

| Path | Purpose |
| --- | --- |
| `setup.bat` / `setup.ps1` | Install ComfyUI, dependencies, and all models |
| `start_comfyui.bat` | Start the local ComfyUI service |
| `stop_comfyui.bat` | Stop the service cleanly |
| `download_h3_models.bat` | Download and verify only MiniMax H3 |
| `scripts/model_manifest.py` | Model URLs, destinations, and expected sizes |
| `scripts/download_models.py` | Resumable model downloader |
| `scripts/verify_install.py` | Environment, workflow, and model validation |
| `workflows/` | Three ready-to-use ComfyUI workflow templates |

## License

[MIT](LICENSE)

---

This is an independent community project and is not affiliated with ComfyUI, Alibaba, MiniMax, NVIDIA, or Hugging Face. Follow the licenses and acceptable-use terms of the models and services you use.
