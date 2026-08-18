from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from model_manifest import MODEL_GROUPS

ROOT = Path(__file__).resolve().parents[1]
COMFY = ROOT / "ComfyUI"


def download_with_curl(url: str, final: Path, expected: int) -> Path:
    """Download to a stable .part path so interrupted Windows jobs can resume."""
    curl = shutil.which("curl.exe") or shutil.which("curl")
    if not curl:
        raise FileNotFoundError("curl")
    partial = final.with_name(final.name + ".part")
    if partial.exists() and partial.stat().st_size > expected:
        partial.unlink()
    subprocess.run(
        [
            curl,
            "-L",
            "--fail",
            "--retry",
            "5",
            "--retry-delay",
            "3",
            "--continue-at",
            "-",
            "--output",
            str(partial),
            url,
        ],
        check=True,
    )
    if partial.stat().st_size != expected:
        raise RuntimeError(f"大小校验失败：{partial}，实际 {partial.stat().st_size}，应为 {expected}")
    partial.replace(final)
    return final


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="下载项目所需的 ComfyUI 模型，支持断点续传。")
    parser.add_argument(
        "group",
        nargs="?",
        choices=MODEL_GROUPS,
        default="all",
        help="下载范围：wan、h3 或 all（默认）。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = MODEL_GROUPS[args.group]
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
    from huggingface_hub import hf_hub_download

    total = sum(item[3] for item in files)
    print(f"将核对/下载 {len(files)} 个模型文件，共 {total / 1024**3:.2f} GiB（范围：{args.group}）")

    for index, (repo, remote, folder, expected) in enumerate(files, 1):
        destination = COMFY / "models" / folder
        destination.mkdir(parents=True, exist_ok=True)
        name = Path(remote).name
        final = destination / name
        if final.is_file() and final.stat().st_size == expected:
            print(f"[{index}/{len(files)}] 已完整，跳过：{name}")
            continue
        if final.exists():
            print(f"[{index}/{len(files)}] 文件不完整，将从 Hub 缓存继续：{name}")
            final.unlink()

        print(f"[{index}/{len(files)}] 下载：{name} ({expected / 1024**3:.3f} GiB)")
        url = f"https://huggingface.co/{repo}/resolve/main/{remote}"
        try:
            path = download_with_curl(url, final, expected)
        except FileNotFoundError:
            path = Path(hf_hub_download(repo_id=repo, filename=remote, local_dir=destination))
        if path.stat().st_size != expected:
            raise RuntimeError(f"大小校验失败：{path}，实际 {path.stat().st_size}，应为 {expected}")
        if path.resolve() != final.resolve():
            path.replace(final)
        if final.stat().st_size != expected:
            raise RuntimeError(f"最终文件大小校验失败：{final}")

    print("所选模型文件已下载并通过字节数校验。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("下载已中断；再次运行相同命令会从 Hugging Face 缓存续传。", file=sys.stderr)
        raise SystemExit(130)
