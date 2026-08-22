# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-08-22T17:39:18.077056+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3-coder-next-int4-autoround-vllm |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly-tf5:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260822-160534 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm |
| Total duration | 5624 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| tool_call_parser | qwen3_coder |
| max_num_seqs | 128 |
| max_num_batched_tokens | 16384 |
| kv_cache_dtype | fp8 |
| optimization_level | 3 |
| performance_mode | throughput |
| mamba_cache_mode | align |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 267 | 0.151 | 14.0 | 1768.1 | 71.75 | 3.72 |
| 1024 | 1036 | 0.287 | 14.0 | 3610.5 | 71.62 | 3.86 |
| 4096 | 4112 | 0.931 | 14.2 | 4416.6 | 70.51 | 4.56 |
| 16384 | 16401 | 3.636 | 14.9 | 4510.3 | 67.29 | 7.44 |
| 65536 | 65550 | 19.988 | 17.6 | 3279.5 | 56.96 | 24.48 |
| 259267 | 259279 | 170.747 | 28.4 | 1518.5 | 35.36 | 177.99 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 128 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.292 | 0.292 | 70.98 | 65.7 | 3.90 |
| 2 | 2 | 0 | 0.487 | 0.541 | 58.73 | 105.5 | 4.85 |
| 4 | 4 | 0 | 0.957 | 0.958 | 42.63 | 148.5 | 6.89 |
| 8 | 8 | 0 | 1.728 | 1.731 | 29.43 | 197.5 | 10.37 |
| 16 | 16 | 0 | 3.316 | 3.323 | 18.52 | 239.6 | 17.09 |
| 32 | 32 | 0 | 5.958 | 6.512 | 12.13 | 302.8 | 27.05 |
| 64 | 64 | 0 | 11.499 | 12.858 | 7.47 | 370.0 | 44.29 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9189 | 0.0075 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9174 | 0.0076 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6041 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6408 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7000 | 0.0461 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6707 | 0.0368 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7580 | 0.0192 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.6429 |  |
| acc | 0.6429 | 406 |
| irrelevance | 1.0000 | 25 |
| live_irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_parallel | 0.6875 | 16 |
| live_parallel_multiple | 0.5833 | 24 |
| live_relevance | 0.7500 | 16 |
| live_simple | 0.8000 | 25 |
| multi_turn_base | 0.4400 | 25 |
| multi_turn_long_context | 0.3600 | 25 |
| multi_turn_miss_func | 0.0400 | 25 |
| multi_turn_miss_param | 0.2400 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4800 | 25 |
| simple_javascript | 0.3200 | 25 |
| simple_python | 0.9200 | 25 |
| MULTI_TURN | 0.2700 | 100 |
| NON_LIVE | 0.7933 | 150 |
| LIVE | 0.7111 | 90 |
| HALLUCINATION | 1.0000 | 50 |
| OVERALL | 0.6459 | 390 |
| OVERALL_RAW | 0.3314 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
