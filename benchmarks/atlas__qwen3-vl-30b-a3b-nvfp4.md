# @atlas/qwen3-vl-30b-a3b-nvfp4 benchmark results

Generated UTC: 2026-07-14T19:00:51.286401+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3-vl-30b-a3b-nvfp4 |
| Model | ig1/Qwen3-VL-30B-A3B-Instruct-NVFP4 |
| Served model name | ig1/Qwen3-VL-30B-A3B-Instruct-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3-vl-30b-a3b-nvfp4/20260714-163458 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3-vl-30b-a3b-nvfp4 --cleanup |
| Total duration | 8753 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 32768 |
| kv_cache_dtype | fp8 |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 268 | 0.505 | 13.6 | 530.7 | 74.06 | 3.53 |
| 1024 | 1035 | 1.111 | 16.5 | 931.3 | 60.66 | 7.00 |
| 4096 | 4106 | 3.778 | 29.6 | 1086.9 | 33.97 | 9.87 |
| 16384 | 16395 | 17.537 | 76.9 | 934.9 | 13.05 | 34.77 |
| 32185 | 32197 | 42.727 | 130.8 | 753.5 | 7.68 | 73.86 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.108 | 1.108 | 60.46 | 46.1 | 4.66 |
| 2 | 2 | 0 | 1.665 | 2.168 | 42.39 | 62.0 | 12.13 |
| 4 | 4 | 0 | 2.783 | 4.278 | 18.25 | 58.0 | 15.31 |
| 8 | 8 | 0 | 4.982 | 8.473 | 10.26 | 61.7 | 43.27 |
| 16 | 16 | 0 | 19.579 | 43.785 | 9.90 | 62.0 | 71.09 |
| 32 | 32 | 0 | 61.869 | 123.596 | 9.13 | 65.1 | 149.36 |
| 64 | 64 | 0 | 124.591 | 245.655 | 8.53 | 63.0 | 282.25 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.1061 | 0.0085 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1001 | 0.0083 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0183 | 0.0105 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0040 | 0.0028 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-VL-30B-A3B-Instruct-NVFP4@bfcl_v4 | 0.1086 |  |
| acc | 0.1086 | 175 |
| irrelevance | 0.0400 | 25 |
| live_multiple | 0.0000 | 25 |
| live_simple | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.4400 | 25 |
| parallel_multiple | 0.2400 | 25 |
| simple_python | 0.0400 | 25 |
| NON_LIVE | 0.1800 | 100 |
| LIVE | 0.0000 | 50 |
| HALLUCINATION | 0.0400 | 25 |
| OVERALL | 0.0220 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 32185 tokens (max length 32768 minus 256 output tokens and 327 tokenizer-skew margin).
