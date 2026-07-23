# poolside__Laguna-S-2-1-NVFP4.yaml benchmark results

Generated UTC: 2026-07-23T17:54:51.895807+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/poolside__Laguna-S-2-1-NVFP4.yaml |
| Model | poolside/Laguna-S-2.1-NVFP4 |
| Served model name | poolside/Laguna-S-2.1-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/poolside__Laguna-S-2-1-NVFP4.yaml/20260723-151924 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe poolside__Laguna-S-2-1-NVFP4.yaml |
| Total duration | 9327 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_seqs | 64 |
| speculative_config | {"model":"poolside/Laguna-S-2.1-DFlash-NVFP4","num_speculative_tokens":1} |
| generation_config | {"temperature":0.0,"top_p":0.95,"repetition_penalty":1.1} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 308 | 0.404 | 41.1 | 762.3 | 24.42 | 10.89 |
| 1024 | 1072 | 0.525 | 47.2 | 2040.1 | 21.25 | 12.57 |
| 4096 | 4148 | 1.570 | 45.5 | 2641.9 | 22.07 | 13.17 |
| 16384 | 16436 | 5.819 | 46.3 | 2824.5 | 21.69 | 17.62 |
| 65536 | 65586 | 28.102 | 49.3 | 2333.8 | 20.36 | 40.68 |
| 259267 | 259319 | 201.556 | 61.6 | 1286.6 | 16.29 | 217.27 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 64 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.541 | 0.541 | 21.70 | 20.7 | 12.34 |
| 2 | 2 | 0 | 0.962 | 0.998 | 19.34 | 35.0 | 14.65 |
| 4 | 4 | 0 | 1.672 | 1.715 | 15.70 | 56.0 | 18.29 |
| 8 | 8 | 0 | 2.779 | 3.139 | 12.22 | 83.2 | 24.60 |
| 16 | 16 | 0 | 4.260 | 6.069 | 9.06 | 120.5 | 33.99 |
| 32 | 32 | 0 | 7.044 | 11.965 | 6.96 | 175.8 | 46.59 |
| 64 | 64 | 0 | 13.077 | 23.903 | 5.11 | 240.3 | 68.18 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7895 | 0.0162 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8476 | 0.0099 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5231 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4940 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5111 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5600 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.3659 | 0.0377 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7640 | 0.0190 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Laguna-S-2.1-NVFP4@bfcl_v4 | 0.5714 |  |
| acc | 0.5714 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.5200 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.7600 | 25 |
| parallel | 0.0800 | 25 |
| parallel_multiple | 0.0400 | 25 |
| simple_python | 0.7200 | 25 |
| NON_LIVE | 0.4000 | 100 |
| LIVE | 0.7000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2100 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
