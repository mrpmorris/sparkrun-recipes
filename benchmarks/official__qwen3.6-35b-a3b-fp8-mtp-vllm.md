# @official/qwen3.6-35b-a3b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-08-19T11:51:05.928147+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-35b-a3b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-35b-a3b-fp8-mtp-vllm/20260819-105355 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-35b-a3b-fp8-mtp-vllm |
| Total duration | 3430 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_batched_tokens | 32768 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| speculative_config | {"method": "mtp", "num_speculative_tokens": 2} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.185 | 14.0 | 1474.1 | 71.74 | 3.75 |
| 1024 | 1040 | 0.290 | 15.8 | 3586.4 | 63.51 | 4.32 |
| 4096 | 4111 | 1.077 | 13.7 | 3815.8 | 73.44 | 4.56 |
| 16384 | 16401 | 3.383 | 15.7 | 4847.4 | 64.05 | 7.38 |
| 65536 | 65555 | 17.042 | 17.4 | 3846.6 | 57.61 | 21.49 |
| 259267 | 259282 | 148.923 | 25.4 | 1741.1 | 39.47 | 155.41 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.285 | 0.285 | 64.66 | 60.3 | 4.24 |
| 2 | 2 | 0 | 0.486 | 0.537 | 56.40 | 98.6 | 5.19 |
| 4 | 4 | 0 | 0.845 | 0.846 | 32.72 | 114.5 | 8.94 |
| 8 | 8 | 0 | 1.895 | 1.899 | 28.43 | 180.7 | 11.34 |
| 16 | 16 | 0 | 2.870 | 2.874 | 22.11 | 267.2 | 15.33 |
| 32 | 32 | 0 | 6.706 | 6.717 | 16.19 | 349.9 | 23.41 |
| 64 | 64 | 0 | 10.547 | 11.993 | 10.72 | 459.1 | 35.68 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.2596 | 0.0178 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3245 | 0.0129 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3442 | 0.0131 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2304 | 0.0123 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.2619 | 0.0128 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.2300 | 0.0423 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3300 | 0.0473 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5976 | 0.0384 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6720 | 0.0210 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.9029 |  |
| acc | 0.9029 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2750 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
