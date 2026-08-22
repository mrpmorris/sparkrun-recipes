# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-08-22T15:55:52.369254+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260822-150718 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm |
| Total duration | 2914 s |

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
| 256 | 269 | 0.151 | 13.9 | 1776.6 | 71.98 | 3.71 |
| 1024 | 1034 | 0.282 | 14.0 | 3665.4 | 71.80 | 3.85 |
| 4096 | 4109 | 0.934 | 14.1 | 4397.3 | 71.01 | 4.54 |
| 16384 | 16396 | 3.670 | 15.0 | 4467.0 | 67.09 | 7.49 |
| 65536 | 65549 | 20.096 | 17.6 | 3261.8 | 57.00 | 24.59 |
| 259267 | 259282 | 171.398 | 28.2 | 1512.7 | 35.62 | 178.59 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 128 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.298 | 0.298 | 71.50 | 66.0 | 3.88 |
| 2 | 2 | 0 | 0.496 | 0.548 | 59.09 | 105.9 | 4.83 |
| 4 | 4 | 0 | 0.962 | 0.963 | 43.49 | 150.9 | 6.78 |
| 8 | 8 | 0 | 1.746 | 1.748 | 29.43 | 197.3 | 10.38 |
| 16 | 16 | 0 | 3.342 | 3.347 | 19.38 | 248.2 | 16.50 |
| 32 | 32 | 0 | 6.007 | 6.562 | 12.06 | 301.1 | 27.21 |
| 64 | 64 | 0 | 11.558 | 12.924 | 7.43 | 368.0 | 44.52 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8421 | 0.0148 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9158 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9204 | 0.0075 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6007 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6399 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6829 | 0.0364 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7520 | 0.0193 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8686 |  |
| acc | 0.8686 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.8686 | 175 |
| OVERALL_RAW | 0.2640 | 175 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 7 of 22 scoring categories (--bfcl-subsets quick). The OVERALL row is an unweighted mean across all 22, so the 15 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
