# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-08-22T13:18:31.592025+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260822-123026 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm |
| Total duration | 2885 s |

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
| 256 | 271 | 0.168 | 13.8 | 1617.6 | 72.79 | 3.68 |
| 1024 | 1036 | 0.276 | 13.9 | 3758.8 | 72.40 | 3.81 |
| 4096 | 4107 | 0.924 | 14.0 | 4444.6 | 71.60 | 4.50 |
| 16384 | 16394 | 3.612 | 14.8 | 4538.2 | 68.05 | 7.37 |
| 65536 | 65548 | 19.851 | 17.4 | 3302.0 | 57.57 | 24.30 |
| 259267 | 259279 | 169.776 | 27.8 | 1527.2 | 36.13 | 176.86 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 128 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.287 | 0.287 | 72.07 | 66.7 | 3.84 |
| 2 | 2 | 0 | 0.486 | 0.542 | 60.00 | 107.6 | 4.76 |
| 4 | 4 | 0 | 0.946 | 0.946 | 44.91 | 155.6 | 6.58 |
| 8 | 8 | 0 | 1.715 | 1.718 | 30.74 | 205.2 | 9.98 |
| 16 | 16 | 0 | 3.286 | 3.291 | 18.94 | 244.4 | 16.76 |
| 32 | 32 | 0 | 5.910 | 6.457 | 12.27 | 306.1 | 26.76 |
| 64 | 64 | 0 | 11.359 | 12.709 | 7.51 | 372.4 | 43.99 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8386 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9151 | 0.0077 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9204 | 0.0075 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6092 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6433 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7200 | 0.0451 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6707 | 0.0368 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7680 | 0.0189 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8743 |  |
| acc | 0.8743 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.5600 | 25 |
| live_simple | 0.8400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.7000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2630 | 175 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
