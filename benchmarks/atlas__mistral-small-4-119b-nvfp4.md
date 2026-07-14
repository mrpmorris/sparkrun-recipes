# @atlas/mistral-small-4-119b-nvfp4 benchmark results

Generated UTC: 2026-07-14T09:10:46.481507+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/mistral-small-4-119b-nvfp4 |
| Model | mistralai/Mistral-Small-4-119B-2603-NVFP4 |
| Served model name | mistralai/Mistral-Small-4-119B-2603-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__mistral-small-4-119b-nvfp4/20260714-051037 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/mistral-small-4-119b-nvfp4 --cleanup |
| Total duration | 14409 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 8192 |
| kv_cache_dtype | bf16 |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 276 | 1.554 | 32.0 | 177.6 | 62.41 | 1.59 |
| 1024 | 1044 | 2.776 | 33.7 | 376.1 | 59.30 | 2.81 |
| 4096 | 4116 | 8.111 | 41.6 | 507.5 | 48.07 | 8.15 |
| 7680 | 7699 | 14.618 | 54.6 | 526.7 | 36.65 | 14.67 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2.787 | 2.787 | 60.76 | 0.7 | 2.82 |
| 2 | 2 | 0 | 4.211 | 5.478 | 59.36 | 0.7 | 5.65 |
| 4 | 4 | 0 | 7.037 | 10.822 | 20.00 | 0.7 | 11.34 |
| 8 | 8 | 0 | 12.611 | 21.438 | 8.38 | 0.7 | 22.61 |
| 16 | 16 | 0 | 23.832 | 42.951 | 5.18 | 0.7 | 45.26 |
| 32 | 32 | 0 | 46.434 | 85.954 | 3.34 | 0.7 | 90.51 |
| 64 | 64 | 0 | 91.600 | 171.872 | 2.11 | 0.7 | 180.91 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

2 task(s) completed, 4 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0000 | 0.0000 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0240 | 0.0069 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Mistral-Small-4-119B-2603-NVFP4@bfcl_v4 | 0.6457 |  |
| acc | 0.6457 | 175 |
| irrelevance | 0.8800 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.6800 | 25 |
| parallel | 0.2800 | 25 |
| parallel_multiple | 0.0800 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.4800 | 100 |
| LIVE | 0.8600 | 50 |
| HALLUCINATION | 0.8800 | 25 |
| OVERALL | 0.2220 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | ERROR | Grade-school math word problems (multi-step reasoning) | killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 7680 tokens (max length 8192 minus 256 output tokens and 256 tokenizer-skew margin).
