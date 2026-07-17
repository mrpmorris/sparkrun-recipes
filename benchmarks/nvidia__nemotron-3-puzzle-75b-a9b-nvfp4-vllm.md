# nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml benchmark results

Generated UTC: 2026-07-17T09:33:49.142297+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml/20260717-074825 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/recipes/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml --cleanup |
| Total duration | 6323 s |

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
| 256 | 276 | 0.246 | 50.1 | 1124.1 | 20.03 | 13.03 |
| 1024 | 1048 | 0.436 | 50.1 | 2401.3 | 20.03 | 13.22 |
| 4096 | 4119 | 1.490 | 50.2 | 2763.9 | 20.00 | 14.29 |
| 16384 | 16406 | 5.846 | 50.5 | 2806.6 | 19.88 | 18.72 |
| 65536 | 65556 | 25.678 | 51.4 | 2553.0 | 19.53 | 38.79 |
| 259267 | 259286 | 142.334 | 54.5 | 1821.7 | 18.42 | 156.23 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.441 | 0.441 | 19.85 | 19.2 | 13.34 |
| 2 | 2 | 0 | 0.862 | 0.868 | 19.21 | 36.0 | 14.22 |
| 4 | 4 | 0 | 1.588 | 1.595 | 17.65 | 63.9 | 16.02 |
| 8 | 8 | 0 | 2.820 | 3.087 | 15.21 | 105.1 | 19.49 |
| 16 | 16 | 0 | 4.371 | 6.070 | 12.04 | 158.8 | 25.79 |
| 32 | 32 | 0 | 7.277 | 12.147 | 8.34 | 211.2 | 38.78 |
| 64 | 64 | 0 | 13.277 | 25.024 | 5.47 | 261.8 | 62.59 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9204 | 0.0075 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9219 | 0.0074 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6135 | 0.0142 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6433 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.4573 | 0.0390 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7780 | 0.0186 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4@bfcl_v4 | 0.6971 |  |
| acc | 0.6971 | 175 |
| irrelevance | 0.8400 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.1600 | 25 |
| parallel_multiple | 0.3600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.5900 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.8400 | 25 |
| OVERALL | 0.2270 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
