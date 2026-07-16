# @atlas/qwen3.6-27b-nvfp4-prefill-record benchmark results

Generated UTC: 2026-07-16T04:07:30.493450+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3.6-27b-nvfp4-prefill-record |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3.6-27b-nvfp4-prefill-record/20260715-220640 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3.6-27b-nvfp4-prefill-record --cleanup |
| Total duration | 21650 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 36864 |
| max_batch_size | 1 |
| kv_cache_dtype | fp8 |
| kv_high_precision_layers | auto |
| gpu_memory_utilization | 0.72 |
| enable_prefix_caching | True |
| ssm_cache_slots | 256 |
| ssm_checkpoint_interval | 16 |
| tool_call_parser | hermes |
| disable_thinking | True |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.741 | 79.0 | 365.7 | 25.33 | 0.82 |
| 1024 | 1045 | 2.098 | 73.2 | 498.2 | 13.76 | 12.49 |
| 4096 | 4116 | 7.677 | 82.2 | 536.1 | 24.35 | 7.76 |
| 16384 | 16401 | 32.530 | 94.5 | 504.2 | 21.16 | 32.62 |
| 36240 | 36258 | 82.026 | 116.4 | 442.0 | 17.18 | 82.14 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 1 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2.115 | 2.115 | 25.38 | 0.9 | 2.19 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

2 task(s) completed, 4 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0244 | 0.0121 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.1100 | 0.0140 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.2857 |  |
| acc | 0.2857 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.2000 | 25 |
| live_simple | 0.3600 | 25 |
| multiple | 0.1600 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0400 | 25 |
| simple_python | 0.2400 | 25 |
| NON_LIVE | 0.1100 | 100 |
| LIVE | 0.2800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.1390 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | HANG | Grade-school math word problems (multi-step reasoning) | [HANG] server alive but stopped generating (no OOM or fatal engine error in logs); killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 36240 tokens (max length 36864 minus 256 output tokens and 368 tokenizer-skew margin).
- Concurrency levels [2, 4, 8, 16, 32, 64] exceed the recipe's declared max concurrency (1); skipped.
