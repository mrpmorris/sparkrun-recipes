# @atlas/qwen3.5-27b-dense-nvfp4 benchmark results

Generated UTC: 2026-07-15T06:33:42.856184+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3.5-27b-dense-nvfp4 |
| Model | Kbenkhaled/Qwen3.5-27B-NVFP4 |
| Served model name | Kbenkhaled/Qwen3.5-27B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3.5-27b-dense-nvfp4/20260714-231949 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3.5-27b-dense-nvfp4 --cleanup |
| Total duration | 26034 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 8192 |
| kv_cache_dtype | fp8 |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 2.619 | 151.4 | 103.5 | 6.63 | 47.72 |
| 1024 | 1041 | 2.030 | 72.6 | 512.9 | 13.83 | 19.03 |
| 4096 | 4114 | 6.897 | 76.0 | 596.5 | 13.21 | 26.20 |
| 7680 | 7694 | 12.687 | 79.9 | 606.4 | 12.57 | 34.81 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2.019 | 2.019 | 13.81 | 12.4 | 20.49 |
| 2 | 2 | 0 | 3.922 | 3.966 | 10.49 | 18.0 | 28.05 |
| 4 | 4 | 0 | 8.115 | 8.117 | 3.67 | 12.9 | 76.80 |
| 8 | 8 | 0 | 16.160 | 16.164 | 1.84 | 12.9 | 151.06 |
| 16 | 16 | 0 | 83.802 | 168.468 | 1.74 | 12.9 | 300.30 |
| 32 | 32 | 0 | 151.274 | 297.574 | 1.90 | 11.8 | 326.75 |
| 64 | 64 | 0 | 138.442 | 277.919 | 1.85 | 10.1 | 386.64 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

1 task(s) completed, 5 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0122 | 0.0086 | 164 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.5-27B-NVFP4@bfcl_v4 | 0.4057 |  |
| acc | 0.4057 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.2400 | 25 |
| live_simple | 0.6000 | 25 |
| multiple | 0.4800 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.6000 | 25 |
| NON_LIVE | 0.2700 | 100 |
| LIVE | 0.4200 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.1610 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | ERROR | Grade-school math word problems (multi-step reasoning) | killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| mbpp | ERROR | Coding: basic Python programming problems, graded by unit tests | killed by watchdog (exceeded 2h hard cap) | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 7680 tokens (max length 8192 minus 256 output tokens and 256 tokenizer-skew margin).
