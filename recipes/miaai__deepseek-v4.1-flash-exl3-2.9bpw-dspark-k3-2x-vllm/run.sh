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
# Runs on both nodes, and DST is deliberately NODE-LOCAL (not the shared /srv/hf).
#
# row_store.cpp gathers each 264 B Engram row from disk on a cache miss, per
# lookup, during prefill. With DST on /srv/hf the worker served every one of
# those over NFS from the head: a long prefill drove sparky2 into sustained
# memory-reclaim pressure (PSI some avg10 ~21-39, head flat at 0.00) and wedged
# the box, needing a power cycle. Upstream says the same thing in
# row_store.cpp:126 - "on a worker it is a local read instead of an NFS round
# trip to the head".
#
# So each node stages its own copy. On the head /home and /srv/hf are one ext4
# volume, so prepare_engram_src.py hardlinks and costs nothing; on the worker
# /cache is NFS and /home is local, so it falls back to one sequential 190 GiB
# copy at startup - paid once, instead of millions of random NFS reads per
# prefill.
set -euo pipefail

SRC="${DSV41_ENGRAM_SRC:-/cache/huggingface/hub/models--deepseek-ai--DeepSeek-V4.1-Flash}"
DST="${DSV41_ENGRAM_DST:-/home/mrpmorris/dsv41-engram}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[dsv41-engram] staging $SRC -> $DST"
python3 "$HERE/prepare_engram_src.py" --src "$SRC" --dst "$DST"
ls -la "$DST"
