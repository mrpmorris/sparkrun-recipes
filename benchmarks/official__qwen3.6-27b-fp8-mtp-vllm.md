# @official/qwen3.6-27b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-07-13T23:28:56.878528+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-27b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-27b-fp8-mtp-vllm/20260713-211122 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-27b-fp8-mtp-vllm --cleanup |
| Total duration | 8254 s |

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
| 256 | 270 | 0.417 | 59.5 | 647.4 | 16.88 | 15.59 |
| 1024 | 1043 | 0.963 | 60.1 | 1082.5 | 16.70 | 16.29 |
| 4096 | 4113 | 4.883 | 59.9 | 842.3 | 16.77 | 20.15 |
| 16384 | 16396 | 18.871 | 59.3 | 868.8 | 16.94 | 33.98 |
| 65536 | 65549 | 90.185 | 60.6 | 726.8 | 16.57 | 105.64 |
| 259267 | 259282 | 537.834 | 74.6 | 482.1 | 13.46 | 556.86 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.731 | 0.731 | 18.38 | 17.5 | 14.66 |
| 2 | 2 | 0 | 1.463 | 1.534 | 16.89 | 30.8 | 16.63 |
| 4 | 4 | 0 | 2.839 | 2.840 | 17.46 | 53.8 | 19.04 |
| 8 | 8 | 0 | 9.281 | 9.284 | 15.81 | 76.7 | 26.71 |
| 16 | 16 | 0 | 19.505 | 19.509 | 13.38 | 102.7 | 39.89 |
| 32 | 32 | 0 | 114.827 | 114.833 | 10.48 | 58.2 | 140.81 |
| 64 | 64 | 0 | 75.317 | 75.527 | 7.40 | 146.9 | 111.50 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5815 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5967 | 0.0135 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2637 | 0.0129 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.2901 | 0.0133 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.2600 | 0.0441 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.2700 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7073 | 0.0356 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4020 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.9200 |  |
| acc | 0.9200 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2800 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | ERROR | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
