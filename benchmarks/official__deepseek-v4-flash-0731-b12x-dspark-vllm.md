# @official/deepseek-v4-flash-0731-b12x-dspark-vllm benchmark results

Generated UTC: 2026-08-22T23:54:44.111087+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/deepseek-v4-flash-0731-b12x-dspark-vllm |
| Model | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Served model name | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly-b12x:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__deepseek-v4-flash-0731-b12x-dspark-vllm/20260822-205115 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/deepseek-v4-flash-0731-b12x-dspark-vllm |
| Total duration | 11009 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| gpu_memory_utilization | 0.85 |
| kv_cache_dtype | fp8 |
| max_model_len | auto |
| block_size | 256 |
| max_num_seqs | 8 |
| max_num_batched_tokens | 8192 |
| max_cudagraph_capture_size | 64 |
| num_speculative_tokens | 5 |
| thinking | true |
| reasoning_effort | high |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 340 | 0.377 | 26.6 | 900.7 | 37.78 | 7.15 |
| 1024 | 1109 | 0.633 | 29.1 | 1752.3 | 34.51 | 8.05 |
| 4096 | 4180 | 1.746 | 23.8 | 2393.8 | 42.11 | 7.82 |
| 16384 | 16468 | 7.014 | 20.3 | 2348.0 | 49.55 | 12.18 |
| 65536 | 65620 | 28.903 | 23.3 | 2270.3 | 43.16 | 34.84 |
| 260000 | 260085 | 141.844 | 21.1 | 1833.6 | 47.51 | 147.23 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.583 | 0.583 | 43.77 | 39.8 | 6.43 |
| 2 | 2 | 0 | 0.977 | 1.319 | 27.66 | 50.0 | 10.25 |
| 4 | 4 | 0 | 2.026 | 2.027 | 21.95 | 67.6 | 15.15 |
| 8 | 8 | 0 | 3.648 | 3.649 | 16.10 | 95.7 | 21.40 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8737 | 0.0134 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9515 | 0.0059 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9515 | 0.0059 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6459 | 0.0140 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6672 | 0.0138 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7195 | 0.0352 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8200 | 0.0172 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-0731@bfcl_v4 | 0.7020 |  |
| acc | 0.7020 | 406 |
| irrelevance | 0.9200 | 25 |
| live_irrelevance | 0.7600 | 25 |
| live_multiple | 0.6800 | 25 |
| live_parallel | 0.8125 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8750 | 16 |
| live_simple | 0.9200 | 25 |
| multi_turn_base | 0.7200 | 25 |
| multi_turn_long_context | 0.5200 | 25 |
| multi_turn_miss_func | 0.3600 | 25 |
| multi_turn_miss_param | 0.3600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4400 | 25 |
| simple_javascript | 0.2800 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4900 | 100 |
| NON_LIVE | 0.8200 | 150 |
| LIVE | 0.7778 | 90 |
| HALLUCINATION | 0.8400 | 50 |
| OVERALL | 0.7080 | 390 |
| OVERALL_RAW | 0.3908 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 260000 tokens (max length 962304 minus 256 output tokens and 9623 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
