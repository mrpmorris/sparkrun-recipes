# poolside__Laguna-S-2-1-NVFP4.yaml benchmark results

Generated UTC: 2026-07-22T14:31:17.370543+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/poolside__Laguna-S-2-1-NVFP4.yaml/20260722-120629 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe poolside__Laguna-S-2-1-NVFP4.yaml |
| Total duration | 8688 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_seqs | 64 |
| speculative_config | {"model":"poolside/Laguna-S-2.1-DFlash-NVFP4","num_speculative_tokens":15} |
| generation_config | {"temperature":0.7,"top_p":0.95,"repetition_penalty":1.1} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 308 | 0.451 | 52.8 | 683.1 | 19.02 | 13.91 |
| 1024 | 1075 | 0.555 | 68.6 | 1938.1 | 14.63 | 18.05 |
| 4096 | 4147 | 1.739 | 65.6 | 2385.1 | 15.31 | 18.47 |
| 16384 | 16434 | 6.688 | 68.5 | 2457.3 | 14.66 | 24.15 |
| 65536 | 65587 | 31.627 | 73.6 | 2073.8 | 13.64 | 50.39 |
| 259267 | 259314 | 220.365 | 87.0 | 1176.7 | 11.53 | 242.56 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 64 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.561 | 0.561 | 14.46 | 14.0 | 18.27 |
| 2 | 2 | 0 | 0.988 | 1.052 | 11.96 | 22.7 | 22.54 |
| 4 | 4 | 0 | 1.611 | 1.984 | 10.43 | 33.7 | 30.35 |
| 8 | 8 | 0 | 2.602 | 3.885 | 7.76 | 55.6 | 36.82 |
| 16 | 16 | 0 | 4.550 | 8.225 | 5.90 | 80.0 | 51.17 |
| 32 | 32 | 0 | 9.045 | 19.248 | 4.38 | 106.5 | 76.94 |
| 64 | 64 | 0 | 16.457 | 47.501 | 2.07 | 79.0 | 58.67 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.5544 | 0.0204 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8620 | 0.0095 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5246 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2995 | 0.0134 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3328 | 0.0138 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3800 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.5200 | 0.0502 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.4146 | 0.0386 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7280 | 0.0199 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Laguna-S-2.1-NVFP4@bfcl_v4 | 0.5771 |  |
| acc | 0.5771 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.5200 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.7200 | 25 |
| parallel | 0.0800 | 25 |
| parallel_multiple | 0.1600 | 25 |
| simple_python | 0.7200 | 25 |
| NON_LIVE | 0.4200 | 100 |
| LIVE | 0.7000 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2080 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
