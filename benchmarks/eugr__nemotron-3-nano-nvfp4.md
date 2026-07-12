# @eugr/nemotron-3-nano-nvfp4 benchmark results

Generated UTC: 2026-07-12T02:24:04.672145+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/nemotron-3-nano-nvfp4 |
| Model | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3-nano-nvfp4/20260712-011044 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3-nano-nvfp4 --cleanup |
| Total duration | 4400 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 279 | 0.137 | 17.5 | 2039.4 | 57.39 | 4.60 |
| 1024 | 1044 | 0.196 | 17.5 | 5323.0 | 57.32 | 4.66 |
| 4096 | 4115 | 0.658 | 17.5 | 6253.5 | 57.24 | 5.13 |
| 16384 | 16403 | 2.558 | 17.7 | 6413.1 | 56.77 | 7.07 |
| 65536 | 65555 | 12.029 | 18.2 | 5449.7 | 55.17 | 16.67 |
| 259267 | 259288 | 78.377 | 20.4 | 3308.2 | 49.13 | 83.59 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.199 | 0.199 | 57.29 | 54.8 | 4.67 |
| 2 | 2 | 0 | 0.395 | 0.397 | 51.92 | 96.0 | 5.33 |
| 4 | 4 | 0 | 0.699 | 0.703 | 45.21 | 161.9 | 6.33 |
| 8 | 8 | 0 | 1.220 | 1.333 | 37.83 | 258.6 | 7.92 |
| 16 | 16 | 0 | 1.897 | 2.616 | 28.25 | 371.9 | 11.01 |
| 32 | 32 | 0 | 3.127 | 5.163 | 19.24 | 489.1 | 16.75 |
| 64 | 64 | 0 | 5.651 | 10.594 | 12.51 | 603.1 | 27.17 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7053 | 0.0180 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8302 | 0.0103 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.4845 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4445 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4744 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.2378 | 0.0333 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5720 | 0.0221 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.8629 |  |
| acc | 0.8629 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2630 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
