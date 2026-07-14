# @official/qwen3.6-35b-a3b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-07-14T04:03:27.189587+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-35b-a3b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-35b-a3b-fp8-mtp-vllm/20260714-030109 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-35b-a3b-fp8-mtp-vllm --cleanup |
| Total duration | 3738 s |

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
| 256 | 271 | 0.243 | 18.4 | 1114.1 | 54.59 | 4.93 |
| 1024 | 1039 | 0.323 | 17.2 | 3214.2 | 58.49 | 4.70 |
| 4096 | 4114 | 1.134 | 18.4 | 3628.8 | 54.57 | 5.82 |
| 16384 | 16398 | 3.415 | 18.4 | 4801.5 | 54.50 | 8.11 |
| 65536 | 65552 | 16.643 | 21.3 | 3938.6 | 47.05 | 22.08 |
| 259267 | 259282 | 147.369 | 30.0 | 1759.4 | 33.44 | 155.03 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.330 | 0.330 | 55.68 | 51.9 | 4.93 |
| 2 | 2 | 0 | 0.563 | 0.588 | 47.51 | 84.4 | 6.07 |
| 4 | 4 | 0 | 1.216 | 1.217 | 33.94 | 112.0 | 9.14 |
| 8 | 8 | 0 | 2.033 | 2.036 | 29.12 | 185.9 | 11.02 |
| 16 | 16 | 0 | 3.576 | 3.581 | 23.21 | 273.4 | 14.98 |
| 32 | 32 | 0 | 6.241 | 6.250 | 17.65 | 380.4 | 21.54 |
| 64 | 64 | 0 | 10.586 | 10.698 | 12.86 | 524.3 | 31.25 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.2807 | 0.0177 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3533 | 0.0132 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3730 | 0.0133 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2022 | 0.0117 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.2543 | 0.0127 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.2200 | 0.0416 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3200 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5061 | 0.0392 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4980 | 0.0224 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.8914 |  |
| acc | 0.8914 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2700 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
