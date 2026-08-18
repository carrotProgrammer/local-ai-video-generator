from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

from model_manifest import MODEL_GROUPS

ROOT = Path(__file__).resolve().parents[1]
COMFY = ROOT / "ComfyUI"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 CUDA、工作流和模型文件。")
    parser.add_argument("group", nargs="?", choices=MODEL_GROUPS, default="all")
    return parser.parse_args()


def all_nodes(workflow: dict):
    yield from workflow.get("nodes", [])
    for subgraph in workflow.get("definitions", {}).get("subgraphs", []):
        yield from subgraph.get("nodes", [])


def verify_workflow(filename: str, required: set[str]) -> None:
    path = ROOT / "workflows" / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    kinds = {node["type"] for node in all_nodes(data)}
    missing = required - kinds
    if missing:
        raise SystemExit(f"工作流 {filename} 缺少节点定义：{sorted(missing)}")
    print(f"workflow OK: {filename} nodes: {len(list(all_nodes(data)))}")


def main() -> int:
    args = parse_args()
    print("torch:", torch.__version__, "CUDA runtime:", torch.version.cuda)
    print("CUDA available:", torch.cuda.is_available())
    if not torch.cuda.is_available():
        raise SystemExit("CUDA 不可用")
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM GiB:", round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2))
    print("Capability:", torch.cuda.get_device_capability(0), "sm_120 in build:", "sm_120" in torch.cuda.get_arch_list())

    version_file = COMFY / "comfyui_version.py"
    namespace: dict[str, str] = {}
    exec(version_file.read_text(encoding="utf-8"), namespace)
    version = namespace["__version__"]
    print("ComfyUI:", version)
    if tuple(map(int, version.split(".")[:2])) < (0, 30):
        raise SystemExit("MiniMax H3 需要 ComfyUI 0.30.0 或更高版本")
    h3_source = COMFY / "comfy_extras" / "nodes_minimax_h3.py"
    if not h3_source.is_file() or "MiniMaxH3ImageToVideo" not in h3_source.read_text(encoding="utf-8"):
        raise SystemExit("当前 ComfyUI 不包含 MiniMax H3 原生节点，请更新 ComfyUI")

    verify_workflow(
        "Wan2.2_Fun_InP_官方_质量与快速.json",
        {"LoadImage", "WanFunInpaintToVideo", "SaveVideo", "CLIPTextEncode"},
    )
    verify_workflow(
        "Wan2.2_Fun_InP_快速测试_512_33帧.json",
        {"LoadImage", "WanFunInpaintToVideo", "SaveVideo", "CLIPTextEncode"},
    )
    verify_workflow(
        "MiniMax_H3_FL2VA_官方.json",
        {"LoadImage", "MiniMaxH3ImageToVideo", "SaveVideo", "CreateVideo"},
    )

    missing_models = []
    for _, remote, folder, size in MODEL_GROUPS[args.group]:
        relative = Path(folder) / Path(remote).name
        path = COMFY / "models" / relative
        ok = path.is_file() and path.stat().st_size == size
        print(f"{'OK' if ok else 'MISSING/INCOMPLETE'}: {relative.as_posix()}")
        if not ok:
            missing_models.append(relative.as_posix())
    if missing_models:
        print(f"缺少或未完成 {len(missing_models)} 个模型文件。", file=sys.stderr)
        return 1
    print(f"安装校验通过（范围：{args.group}）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
