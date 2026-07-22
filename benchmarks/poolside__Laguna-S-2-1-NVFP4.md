# poolside__Laguna-S-2-1-NVFP4.yaml benchmark results

Generated UTC: 2026-07-22T21:44:30.519788+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/poolside__Laguna-S-2-1-NVFP4.yaml/20260722-190323 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe poolside__Laguna-S-2-1-NVFP4.yaml |
| Total duration | 9667 s |

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
| 256 | 306 | 0.402 | 45.1 | 760.4 | 22.28 | 11.90 |
| 1024 | 1074 | 0.535 | 47.3 | 2008.1 | 21.25 | 12.58 |
| 4096 | 4143 | 1.559 | 48.7 | 2656.7 | 20.63 | 13.97 |
| 16384 | 16436 | 5.808 | 48.8 | 2829.9 | 20.56 | 18.26 |
| 65536 | 65586 | 27.646 | 52.1 | 2372.4 | 19.28 | 40.92 |
| 259267 | 259315 | 195.588 | 73.5 | 1325.8 | 13.65 | 214.34 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 64 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.555 | 0.555 | 20.74 | 19.8 | 12.90 |
| 2 | 2 | 0 | 0.973 | 1.012 | 17.46 | 31.6 | 16.23 |
| 4 | 4 | 0 | 1.668 | 1.716 | 14.84 | 53.0 | 19.33 |
| 8 | 8 | 0 | 2.774 | 3.149 | 11.77 | 81.7 | 25.05 |
| 16 | 16 | 0 | 4.259 | 6.078 | 8.56 | 115.5 | 35.45 |
| 32 | 32 | 0 | 7.067 | 11.970 | 6.87 | 177.0 | 46.28 |
| 64 | 64 | 0 | 13.010 | 23.785 | 5.01 | 237.7 | 68.94 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7895 | 0.0162 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8575 | 0.0096 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5262 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5026 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5230 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5600 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6900 | 0.0465 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.4146 | 0.0386 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7460 | 0.0195 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Laguna-S-2.1-NVFP4@bfcl_v4 | 0.5829 |  |
| acc | 0.5829 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.5600 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.7200 | 25 |
| parallel | 0.0800 | 25 |
| parallel_multiple | 0.0800 | 25 |
| simple_python | 0.7200 | 25 |
| NON_LIVE | 0.4000 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2140 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
