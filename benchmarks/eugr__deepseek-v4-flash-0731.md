# @eugr/deepseek-v4-flash-0731 benchmark results

Generated UTC: 2026-08-22T20:34:48.723410+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/deepseek-v4-flash-0731 |
| Model | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Served model name | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Runtime | vllm-distributed |
| Container | vllm-node-b12x |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__deepseek-v4-flash-0731/20260822-174134 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/deepseek-v4-flash-0731 |
| Total duration | 10395 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| gpu_memory_utilization | 0.85 |
| max_model_len | auto |
| block_size | 256 |
| max_num_seqs | 8 |
| max_num_batched_tokens | 8192 |
| max_cudagraph_capture_size | 64 |
| num_speculative_tokens | 5 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 340 | 0.378 | 20.9 | 898.8 | 48.04 | 5.71 |
| 1024 | 1108 | 0.629 | 30.4 | 1760.8 | 32.99 | 8.39 |
| 4096 | 4180 | 1.682 | 18.1 | 2485.5 | 55.59 | 6.29 |
| 16384 | 16468 | 6.844 | 22.8 | 2406.2 | 43.98 | 12.66 |
| 65536 | 65620 | 29.965 | 27.0 | 2189.9 | 37.19 | 36.85 |
| 260000 | 260084 | 144.699 | 24.3 | 1797.4 | 41.27 | 150.90 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.596 | 0.596 | 60.53 | 53.1 | 4.83 |
| 2 | 2 | 0 | 0.928 | 1.238 | 29.60 | 51.7 | 9.90 |
| 4 | 4 | 0 | 2.012 | 2.013 | 23.93 | 65.7 | 15.58 |
| 8 | 8 | 0 | 3.666 | 3.670 | 17.16 | 98.0 | 20.90 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8807 | 0.0132 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9522 | 0.0059 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9530 | 0.0058 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6391 | 0.0140 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6698 | 0.0137 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7700 | 0.0423 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7378 | 0.0345 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8200 | 0.0172 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-0731@bfcl_v4 | 0.6921 |  |
| acc | 0.6921 | 406 |
| irrelevance | 0.9200 | 25 |
| live_irrelevance | 0.7600 | 25 |
| live_multiple | 0.6000 | 25 |
| live_parallel | 0.8750 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8750 | 16 |
| live_simple | 0.9600 | 25 |
| multi_turn_base | 0.6000 | 25 |
| multi_turn_long_context | 0.6800 | 25 |
| multi_turn_miss_func | 0.2400 | 25 |
| multi_turn_miss_param | 0.4000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4400 | 25 |
| simple_javascript | 0.2000 | 25 |
| simple_python | 0.9200 | 25 |
| MULTI_TURN | 0.4800 | 100 |
| NON_LIVE | 0.8100 | 150 |
| LIVE | 0.7778 | 90 |
| HALLUCINATION | 0.8400 | 50 |
| OVERALL | 0.6999 | 390 |
| OVERALL_RAW | 0.3868 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 260000 tokens (max length 767488 minus 256 output tokens and 7674 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
