# nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml benchmark results

Generated UTC: 2026-07-12T22:06:09.385112+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml |
| Model | nvidia/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml/20260712-195704 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml |
| Total duration | 7745 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 277 | 0.248 | 51.0 | 1116.4 | 19.68 | 13.25 |
| 1024 | 1043 | 0.441 | 51.0 | 2367.5 | 19.68 | 13.45 |
| 4096 | 4115 | 1.496 | 51.1 | 2750.9 | 19.65 | 14.52 |
| 16384 | 16405 | 5.886 | 51.3 | 2787.1 | 19.55 | 18.98 |
| 65536 | 65557 | 25.854 | 52.3 | 2535.6 | 19.20 | 39.18 |
| 259267 | 259290 | 143.161 | 55.4 | 1811.2 | 18.14 | 157.28 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.456 | 0.456 | 19.61 | 18.9 | 13.51 |
| 2 | 2 | 0 | 0.867 | 0.872 | 19.35 | 36.2 | 14.13 |
| 4 | 4 | 0 | 1.599 | 1.608 | 18.05 | 65.2 | 15.71 |
| 8 | 8 | 0 | 2.935 | 3.312 | 15.08 | 103.6 | 19.76 |
| 16 | 16 | 0 | 4.398 | 6.324 | 11.87 | 156.4 | 26.18 |
| 32 | 32 | 0 | 7.350 | 12.556 | 8.27 | 209.1 | 39.17 |
| 64 | 64 | 0 | 13.393 | 25.439 | 5.40 | 258.2 | 63.46 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9174 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9204 | 0.0075 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6058 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6365 | 0.0141 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.4878 | 0.0392 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7740 | 0.0187 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4@bfcl_v4 | 0.6629 |  |
| acc | 0.6629 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.0800 | 25 |
| parallel_multiple | 0.2000 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.5300 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.2250 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
