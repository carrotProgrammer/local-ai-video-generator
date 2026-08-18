# 本地 ComfyUI 首尾帧音视频项目

本项目在同一个 ComfyUI 环境中提供两套相互独立的工作流：

- **Wan2.2 Fun InP A14B**：首帧 + 尾帧视频，包含质量与 LightX2V 快速模式。
- **MiniMax H3 FL2VA**：首帧 + 尾帧生成视频，并在同一次推理中生成同步双声道音频。

> [!IMPORTANT]
> 当前一键安装脚本是针对 **Windows 11 + NVIDIA GeForce RTX 5090（32 GB 显存）+ CUDA 13.0** 编写并实际验证的。脚本固定安装 PyTorch 2.12.1 的 `cu130` 构建，不会自动根据显卡选择其他 PyTorch/CUDA 版本。其他 NVIDIA 显卡可能需要自行调整依赖和显存参数；AMD、Intel、Apple Silicon 及纯 CPU 环境没有经过验证，也不属于当前脚本的支持范围。

## 仓库内容与隐私

GitHub 仓库只包含安装/启停脚本、模型清单和三份通用工作流模板，不包含以下本地内容：

- ComfyUI 源码副本和项目虚拟环境；
- 任何模型权重或未完成的模型下载；
- `input` 中的图片、视频等输入素材；
- `output` 中的生成结果和运行日志；
- Hugging Face 缓存、PID 文件、环境变量文件或其他本地实验数据。

这些内容均由 `.gitignore` 排除。三个工作流只引用通用的 `start_image.png` 与 `end_image.png` 占位名称；使用时请在 ComfyUI 中选择自己的素材。若创建包含私人提示词或素材路径的工作流，请不要直接提交到公开仓库。

## 硬件、软件和空间要求

已实际验证的环境：

| 项目 | 已验证配置 |
| --- | --- |
| 操作系统 | Windows 11、Windows PowerShell 5.1 |
| 显卡 | NVIDIA GeForce RTX 5090，31.84 GiB 可用显存 |
| PyTorch / CUDA | PyTorch 2.12.1 + CUDA 13.0，包含 `sm_120` |
| ComfyUI | 0.30.0 或更高版本；发布前验证版本为 0.31.0 |

首次安装前还需要：

- 已安装 Conda，并且 PowerShell 中执行 `conda --version` 能正常返回；
- 能访问 GitHub、PyTorch 下载源和 Hugging Face；
- 稳定网络连接，模型下载总量约 **75 GiB**；
- 建议至少预留 **100 GiB** 磁盘空间；若下载回退到 Hugging Face 缓存或保留其他模型，需要更多空间；
- 足够的系统内存用于 ComfyUI 模型卸载。32 GB 显存是本项目唯一实际验证过的显存配置，低显存显卡不保证能够运行这些工作流。

当前脚本不自动检测显卡型号，也不自动为 RTX 4090、RTX 3090、专业卡或较低显存显卡更换 PyTorch/CUDA 构建。若不是 RTX 5090，请先检查驱动、CUDA 兼容性和显存需求，不要直接假定一键安装配置适用。

## 从 Git clone 到首次启动

在 PowerShell 中运行：

```powershell
git clone https://github.com/carrotProgrammer/comfyui-video-project.git
cd comfyui-video-project
.\setup.bat
```

也可以从 GitHub 下载 ZIP、解压后双击 `setup.bat`。首次运行时，`setup.bat` 会自动：

1. 使用 Conda 在项目内创建 `.venv`，包含 Python 3.12 和 Git；
2. 从 [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) 克隆官方 ComfyUI 到本地 `ComfyUI` 文件夹；
3. 安装 PyTorch 2.12.1、TorchVision 0.27.1、CUDA 13.0 构建和 ComfyUI 依赖；
4. 从 Hugging Face 下载 Wan2.2 与 MiniMax H3 的全部模型，总计约 75 GiB；
5. 校验 CUDA、显卡、ComfyUI 版本、三份工作流以及每个模型文件的大小。

GitHub 仓库本身不包含 ComfyUI 源码或模型权重；这些内容只会由 `setup.bat` 下载到用户自己的电脑。重复运行 `setup.bat` 时，字节数正确的模型会跳过，未完成的下载会尝试续传。

安装与校验成功后再运行：

```powershell
.\start_comfyui.bat
```

`start_comfyui.bat` 只负责启动已经安装好的 ComfyUI，不会代替首次安装。如果 `.venv` 或 `ComfyUI\main.py` 不存在，启动脚本会提示先运行 `setup.bat`。

## 单独下载 MiniMax H3 模型

如果 Wan2.2 已安装，只想下载 H3（约 39.56 GiB）：

```powershell
.\download_h3_models.bat
```

也可以使用不会停留窗口的命令：

```powershell
.\.venv\python.exe .\scripts\download_models.py h3
.\.venv\python.exe .\scripts\verify_install.py h3
```

H3 使用以下 ComfyUI 官方量化组件：

- `diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors`（19.53 GiB）
- `text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`（14.61 GiB）
- `vae/minimax_h3_video_vae_fp16.safetensors`（4.85 GiB）
- `vae/minimax_h3_audio_vae_fp32.safetensors`（0.56 GiB）

模型来源：[Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)。

## 启动与停止

```powershell
.\start_comfyui.bat
```

浏览器打开 <http://127.0.0.1:8188>。输入素材目录为 `input`，生成结果位于 `output`。启动脚本会预留 2 GiB 显存，并通过项目根目录的 `comfyui.pid` 防止重复启动。

停止服务：

```powershell
.\stop_comfyui.bat
```

## MiniMax H3 FL2VA 使用方法

1. 将 `workflows/MiniMax_H3_FL2VA_官方.json` 拖入 ComfyUI 画布。
2. 在两个 `Load Image` 节点分别选择首帧和尾帧。它们已经连接到主节点的 `first_frame` 与 `last_frame` 接口；断开尾帧时则是普通 I2V。
4. 首尾图尽量采用相同宽高比。通过 `Resolution Selector` 设置输出尺寸，先用 `0.4 MP` 预览，满意后再提高至约 `0.98 MP`（16:9 时约 1344×768）。
5. 在提示词中同时描述画面、动作、镜头和音频，例如：

   `镜头缓慢推进，人物从首帧姿态自然转向尾帧姿态，身份和服装保持一致。Audio: 安静室内环境声，轻柔脚步声，无音乐。`

6. 默认时长为 5 秒。H3 按 24 fps 生成，并自动将长度对齐到模型要求的 `17k+5` 帧网格。
7. 按 `Ctrl+Enter` 生成，带音频 MP4 保存到 `output/video`。

本项目在 ComfyUI 官方 I2V 模板上预先连接了尾帧节点，不修改官方采样子图，也不需要安装自定义节点。

## H3 显存与性能建议

- RTX 5090 32GB 建议先用 `0.4 MP / 5 秒` 验证，再提升到约 `0.98 MP`。
- H3 文本编码器与扩散模型合计较大，依赖 ComfyUI 将部分权重卸载到系统内存；不要添加 `--highvram`。
- 生成时关闭其他占用 GPU 的程序，不要同时运行 Wan2.2 和 H3 任务。
- 首次加载会明显慢于后续任务。若出现内存不足，降低分辨率或时长并重启 ComfyUI，以释放显存碎片。
- 本地 H3 工作流的原生画布建议短边不超过 768，宽高为 32 的倍数。官方所说的 2K 输出涉及更高分辨率再生成流程，并不是本工作流的默认设置。

## Wan2.2 使用方法

- 快速测试：`workflows/Wan2.2_Fun_InP_快速测试_512_33帧.json`
- 质量与快速双模式：`workflows/Wan2.2_Fun_InP_官方_质量与快速.json`

把工作流拖入画布，在两个 `Load Image` 节点选择首帧和尾帧，填写正向提示词后按 `Ctrl+Enter`。Wan 帧数采用 `4n+1`，例如 33、49、81 帧；工作流以 16 fps 保存视频。

## 故障检查

运行完整校验：

```powershell
.\.venv\python.exe .\scripts\verify_install.py all
```

常见问题：

- `MISSING/INCOMPLETE`：重新运行相应下载命令，脚本会续传。
- 找不到 `MiniMaxH3ImageToVideo`：ComfyUI 版本低于 0.30.0，需要更新 ComfyUI。
- H3 节点模型下拉框为空：确认四个文件分别位于 `diffusion_models`、`text_encoders` 和 `vae` 目录，然后重启 ComfyUI。
- PID 文件存在但服务未运行：启动脚本会自动清理失效 PID；也可以先运行 `stop_comfyui.bat`。
