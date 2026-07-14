# @official/qwen3.6-27b-fp8-vllm benchmark results

Generated UTC: 2026-07-14T03:01:09.216120+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-27b-fp8-vllm |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-27b-fp8-vllm/20260713-232857 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-27b-fp8-vllm --cleanup |
| Total duration | 12732 s |

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
| 256 | 273 | 0.228 | 125.0 | 1196.4 | 8.03 | 32.11 |
| 1024 | 1040 | 0.520 | 125.4 | 2000.4 | 8.01 | 32.49 |
| 4096 | 4113 | 2.512 | 125.9 | 1637.2 | 7.97 | 34.61 |
| 16384 | 16399 | 18.509 | 127.6 | 886.0 | 7.87 | 51.04 |
| 65536 | 65551 | 87.634 | 134.7 | 748.0 | 7.45 | 121.97 |
| 259267 | 259282 | 524.214 | 161.4 | 494.6 | 6.22 | 565.38 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.778 | 0.778 | 7.97 | 7.8 | 32.90 |
| 2 | 2 | 0 | 1.307 | 1.485 | 7.96 | 15.3 | 33.55 |
| 4 | 4 | 0 | 5.467 | 5.468 | 7.66 | 26.7 | 38.33 |
| 8 | 8 | 0 | 17.595 | 17.597 | 7.32 | 39.6 | 51.69 |
| 16 | 16 | 0 | 54.560 | 54.563 | 6.66 | 44.5 | 91.97 |
| 32 | 32 | 0 | 37.724 | 37.733 | 5.70 | 99.6 | 82.22 |
| 64 | 64 | 0 | 67.369 | 76.846 | 3.86 | 121.4 | 135.00 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8561 | 0.0143 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5770 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5989 | 0.0135 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6024 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6007 | 0.0143 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6100 | 0.0490 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7800 | 0.0416 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8537 | 0.0277 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6040 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.9257 |  |
| acc | 0.9257 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9400 | 100 |
| LIVE | 0.8600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2800 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
