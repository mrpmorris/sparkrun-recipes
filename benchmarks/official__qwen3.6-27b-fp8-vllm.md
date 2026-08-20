# @official/qwen3.6-27b-fp8-vllm benchmark results

Generated UTC: 2026-08-20T12:34:00.388492+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-27b-fp8-vllm |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-27b-fp8-vllm/20260820-090101 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-27b-fp8-vllm |
| Total duration | 12779 s |

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

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 270 | 0.239 | 119.4 | 1129.5 | 8.41 | 30.69 |
| 1024 | 1037 | 0.756 | 119.7 | 1371.0 | 8.39 | 31.27 |
| 4096 | 4114 | 2.469 | 120.2 | 1666.6 | 8.35 | 33.11 |
| 16384 | 16401 | 19.328 | 121.9 | 848.6 | 8.23 | 50.42 |
| 65536 | 65551 | 87.582 | 129.7 | 748.5 | 7.74 | 120.65 |
| 259267 | 259281 | 526.800 | 156.8 | 492.2 | 6.40 | 566.78 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.771 | 0.771 | 8.40 | 8.2 | 31.24 |
| 2 | 2 | 0 | 1.070 | 1.247 | 8.41 | 16.2 | 31.57 |
| 4 | 4 | 0 | 5.214 | 5.216 | 8.10 | 28.2 | 36.30 |
| 8 | 8 | 0 | 16.839 | 16.843 | 7.69 | 41.5 | 49.29 |
| 16 | 16 | 0 | 51.281 | 51.288 | 7.00 | 47.1 | 86.91 |
| 32 | 32 | 0 | 105.358 | 105.366 | 5.93 | 55.4 | 147.81 |
| 64 | 64 | 0 | 186.121 | 211.255 | 3.44 | 61.1 | 267.99 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8544 | 0.0144 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6012 | 0.0135 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6224 | 0.0134 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6007 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6007 | 0.0143 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6100 | 0.0490 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7800 | 0.0416 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8171 | 0.0303 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6200 | 0.0217 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2760 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
