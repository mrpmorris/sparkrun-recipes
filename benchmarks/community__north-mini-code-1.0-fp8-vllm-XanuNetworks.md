# @community/north-mini-code-1.0-fp8-vllm-XanuNetworks benchmark results

Generated UTC: 2026-07-16T19:43:09.756419+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/north-mini-code-1.0-fp8-vllm-XanuNetworks |
| Model | CohereLabs/North-Mini-Code-1.0-fp8 |
| Served model name | north-mini-code |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__north-mini-code-1.0-fp8-vllm-XanuNetworks/20260716-183812 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/north-mini-code-1.0-fp8-vllm-XanuNetworks --cleanup |
| Total duration | 3898 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| kv_cache_dtype | fp8 |
| served_model_name | north-mini-code |
| tool_call_parser | cohere_command4 |
| reasoning_parser | cohere_command4 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 372 | 0.178 | 27.7 | 2084.9 | 36.24 | 7.24 |
| 1024 | 1140 | 0.215 | 27.6 | 5292.3 | 36.34 | 7.26 |
| 4096 | 4212 | 0.734 | 28.3 | 5741.2 | 35.42 | 7.96 |
| 16384 | 16500 | 3.183 | 29.0 | 5184.1 | 34.61 | 10.58 |
| 65536 | 65652 | 17.041 | 31.8 | 3852.6 | 31.60 | 25.14 |
| 259267 | 259383 | 134.802 | 42.7 | 1924.2 | 23.50 | 145.70 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.213 | 0.213 | 36.16 | 35.1 | 7.29 |
| 2 | 2 | 0 | 0.337 | 0.427 | 33.14 | 63.4 | 8.07 |
| 4 | 4 | 0 | 0.633 | 0.734 | 24.80 | 93.9 | 10.90 |
| 8 | 8 | 0 | 1.005 | 1.371 | 22.48 | 165.2 | 12.40 |
| 16 | 16 | 0 | 1.639 | 2.653 | 18.00 | 255.8 | 16.02 |
| 32 | 32 | 0 | 2.924 | 5.146 | 13.99 | 377.9 | 21.68 |
| 64 | 64 | 0 | 5.520 | 10.344 | 10.29 | 518.1 | 31.62 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7860 | 0.0161 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9083 | 0.0080 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9083 | 0.0080 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5589 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5853 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4900 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6400 | 0.0482 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5610 | 0.0389 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6220 | 0.0217 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| north-mini-code@bfcl_v4 | 0.9029 |  |
| acc | 0.9029 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2750 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
