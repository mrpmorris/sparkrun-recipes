# @eugr/deepseek-v4-flash-0731 benchmark results

Generated UTC: 2026-08-21T20:36:15.695117+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__deepseek-v4-flash-0731/20260821-192132 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/deepseek-v4-flash-0731 |
| Total duration | 4484 s |

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
| 256 | 340 | 0.374 | 24.3 | 908.9 | 41.24 | 6.58 |
| 1024 | 1108 | 0.582 | 16.3 | 1903.7 | 61.59 | 4.74 |
| 4096 | 4180 | 1.711 | 23.3 | 2443.3 | 43.09 | 7.65 |
| 16384 | 16468 | 7.356 | 23.6 | 2238.6 | 42.61 | 13.37 |
| 65536 | 65620 | 30.152 | 18.7 | 2176.3 | 53.74 | 34.92 |
| 260000 | 260084 | 137.881 | 20.1 | 1886.3 | 50.00 | 143.00 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.575 | 0.575 | 55.00 | 49.0 | 5.23 |
| 2 | 2 | 0 | 0.888 | 1.166 | 37.75 | 58.3 | 8.79 |
| 4 | 4 | 0 | 1.968 | 1.973 | 27.97 | 82.8 | 12.37 |
| 8 | 8 | 0 | 3.685 | 3.687 | 17.07 | 104.4 | 19.61 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8842 | 0.0130 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9500 | 0.0060 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9500 | 0.0060 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6476 | 0.0140 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6706 | 0.0137 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5671 | 0.0388 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8040 | 0.0178 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-0731@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.5600 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2660 | 175 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 260000 tokens (max length 925696 minus 256 output tokens and 9256 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
