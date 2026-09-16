#!/usr/bin/env python3
"""Build the slim Engram source dir this recipe mounts at /engram-src.

DeepSeek-V4.1-Flash keeps its n-gram (Engram) tables unquantized, so the EXL3
2.9bpw pack does not contain them: they live in shards 47+48 of the ORIGINAL
48-shard checkpoint (~95 GiB each). vLLM's DefaultModelLoader would walk the
whole 476 GiB tree if engram_table_dir pointed at the native snapshot, so this
hardlinks only those two shards into a fresh dir and writes an index whose
weight_map lists the *.engram.embed.{weight,scale} tensors only.

Port of upstream scripts/prepare_engram_src.py (MiaAI-Lab), with two changes
for sparkrun: --src may be an HF cache repo dir (the snapshot is resolved), and
the work is done under a lock + temp dir so head and worker can both run it in
pre_exec on the shared /srv/hf without racing.

Hardlinks need src and dst on one filesystem: /srv/hf is one ext4 volume on
sparky1 and the same volume over NFS on sparky2 (the worker sees the finished
dir and does nothing).
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import shutil
import sys
from pathlib import Path

SHARDS = (
    "model-00047-of-00048.safetensors",
    "model-00048-of-00048.safetensors",
)
KEEP_SUFFIXES = (".engram.embed.weight", ".engram.embed.scale")


def resolve_src(src: Path) -> Path:
    """Accept a plain checkpoint dir or an HF cache models--*/ dir."""
    if (src / "model.safetensors.index.json").is_file():
        return src
    snapshots = src / "snapshots"
    if snapshots.is_dir():
        candidates = sorted(
            (p for p in snapshots.iterdir() if (p / "model.safetensors.index.json").is_file()),
            key=lambda p: p.stat().st_mtime,
        )
        if candidates:
            return candidates[-1]
    raise SystemExit(f"no model.safetensors.index.json under {src}")


def slim_weight_map(weight_map: dict) -> dict:
    return {n: s for n, s in weight_map.items() if n.endswith(KEEP_SUFFIXES)}


def link_or_copy(src: Path, dst: Path) -> str:
    src = src.resolve()  # HF snapshots are symlinks into blobs/
    if dst.exists():
        s, d = src.stat(), dst.stat()
        if (d.st_ino, d.st_dev) == (s.st_ino, s.st_dev):
            return "exists"
        if d.st_size == s.st_size:
            return "exists-copy"
        dst.unlink()
    try:
        os.link(src, dst)
        return "hardlink"
    except OSError:
        shutil.copy2(src, dst)
        return "copy"


def prepare(src: Path, dst: Path) -> dict:
    src = resolve_src(src)
    index_path = src / "model.safetensors.index.json"
    for shard in SHARDS:
        if not (src / shard).is_file():
            raise SystemExit(f"missing Engram shard {src / shard}")

    raw = json.loads(index_path.read_text())
    keep = slim_weight_map(raw.get("weight_map") or {})
    if not keep:
        raise SystemExit(f"no {KEEP_SUFFIXES} keys in {index_path} - is --src the native V4.1 tree?")
    unexpected = sorted({s for s in keep.values() if s not in SHARDS})
    if unexpected:
        raise SystemExit(f"embed tables outside shards 47/48: {unexpected}")

    dst.mkdir(parents=True, exist_ok=True)
    actions = {}
    for shard in SHARDS:
        actions[shard] = link_or_copy(src / shard, dst / shard)

    slim = {
        "metadata": {
            "total_size": raw.get("metadata", {}).get("total_size"),
            "dsv41_engram_src": "embed-only",
        },
        "weight_map": keep,
    }
    tmp = dst / "model.safetensors.index.json.tmp"
    tmp.write_text(json.dumps(slim, indent=2) + "\n")
    tmp.replace(dst / "model.safetensors.index.json")
    cfg = src / "config.json"
    if cfg.is_file():
        shutil.copy2(cfg, dst / "config.json")
        actions["config.json"] = "copy"
    return {"src": str(src), "dst": str(dst), "tensors": sorted(keep), "files": actions}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path, help="native DeepSeek-V4.1-Flash tree or its HF cache dir")
    ap.add_argument("--dst", required=True, type=Path)
    args = ap.parse_args()

    dst = args.dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    lock_path = dst.parent / (dst.name + ".lock")
    with open(lock_path, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        info = prepare(args.src, dst)
    dstr, sstr, ntensors = info["dst"], info["src"], len(info["tensors"])
    print(
        f"engram-src {dstr} <- {sstr}: {ntensors} embed tensors, "
        + ", ".join(f"{k}={v}" for k, v in info["files"].items()),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
