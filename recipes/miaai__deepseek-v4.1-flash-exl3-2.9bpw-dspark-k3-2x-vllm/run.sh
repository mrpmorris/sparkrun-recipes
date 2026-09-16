#!/bin/bash
# sparkrun mod: stage the slim Engram source dir before vllm serve.
#
# DeepSeek-V4.1-Flash keeps its Engram (n-gram) tables unquantized, so the EXL3
# 2.9bpw pack has none of them: they live in shards 47+48 of the original
# 48-shard checkpoint. vLLM reads them through
# --hf-overrides '{"engram_table_dir":"/srv/hf/dsv41-engram"}' and a file-backed
# ParallelEngramEmbedding, so /srv/hf/dsv41-engram must hold exactly those two shards
# plus an index that lists only the embed tensors - point it at the native
# snapshot and DefaultModelLoader walks the whole 476 GiB tree.
#
# Runs on both nodes. /srv/hf/dsv41-engram is the shared /srv/hf/dsv41-engram (ext4 on
# sparky1, the same volume over NFS on sparky2), so the second node normally
# finds the work already done and exits after the checks.
set -euo pipefail

SRC="${DSV41_ENGRAM_SRC:-/cache/huggingface/hub/models--deepseek-ai--DeepSeek-V4.1-Flash}"
DST="${DSV41_ENGRAM_DST:-/srv/hf/dsv41-engram}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[dsv41-engram] staging $SRC -> $DST"
python3 "$HERE/prepare_engram_src.py" --src "$SRC" --dst "$DST"
ls -la "$DST"
