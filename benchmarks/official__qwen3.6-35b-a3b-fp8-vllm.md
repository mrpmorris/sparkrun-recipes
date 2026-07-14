# @official/qwen3.6-35b-a3b-fp8-vllm benchmark results

Generated UTC: 2026-07-14T05:10:37.205680+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-35b-a3b-fp8-vllm |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-35b-a3b-fp8-vllm/20260714-040327 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-35b-a3b-fp8-vllm --cleanup |
| Total duration | 4030 s |

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
| 256 | 272 | 0.181 | 20.1 | 1500.1 | 49.91 | 5.31 |
| 1024 | 1037 | 0.260 | 20.1 | 3989.7 | 49.85 | 5.40 |
| 4096 | 4111 | 0.771 | 20.4 | 5333.9 | 49.21 | 5.97 |
| 16384 | 16399 | 2.906 | 20.9 | 5643.1 | 48.11 | 8.23 |
| 65536 | 65551 | 15.727 | 23.0 | 4167.9 | 43.70 | 21.59 |
| 259267 | 259282 | 135.435 | 31.2 | 1914.4 | 32.17 | 143.39 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.279 | 0.279 | 49.61 | 47.1 | 5.44 |
| 2 | 2 | 0 | 0.439 | 0.496 | 40.02 | 74.8 | 6.84 |
| 4 | 4 | 0 | 1.091 | 1.091 | 30.68 | 109.6 | 9.34 |
| 8 | 8 | 0 | 1.877 | 1.880 | 21.51 | 149.6 | 13.69 |
| 16 | 16 | 0 | 3.192 | 3.197 | 15.96 | 213.8 | 19.16 |
| 32 | 32 | 0 | 5.893 | 5.901 | 11.40 | 289.6 | 28.28 |
| 64 | 64 | 0 | 8.820 | 10.080 | 7.74 | 390.6 | 41.95 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8544 | 0.0141 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3480 | 0.0131 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3677 | 0.0133 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5410 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5478 | 0.0145 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6000 | 0.0492 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7600 | 0.0429 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5854 | 0.0386 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6720 | 0.0210 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.8800 |  |
| acc | 0.8800 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2670 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
