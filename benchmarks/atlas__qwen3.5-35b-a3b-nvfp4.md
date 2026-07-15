# @atlas/qwen3.5-35b-a3b-nvfp4 benchmark results

Generated UTC: 2026-07-15T08:10:06.713409+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3.5-35b-a3b-nvfp4 |
| Model | Sehyo/Qwen3.5-35B-A3B-NVFP4 |
| Served model name | Sehyo/Qwen3.5-35B-A3B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3.5-35b-a3b-nvfp4/20260715-063343 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3.5-35b-a3b-nvfp4 --cleanup |
| Total duration | 5783 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 8192 |
| max_batch_size | 2 |
| max_num_seqs | 2 |
| kv_cache_dtype | fp8 |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |
| speculative | True |
| mtp_quantization | bf16 |
| enable_prefix_caching | True |
| oom_guard_mb | 1024 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 270 | 0.203 | 9.6 | 1328.7 | 103.82 | 5.51 |
| 1024 | 1041 | 0.438 | 11.4 | 2377.1 | 88.46 | 3.19 |
| 4096 | 4113 | 1.535 | 13.3 | 2679.6 | 75.54 | 4.66 |
| 7680 | 7695 | 2.863 | 15.6 | 2687.8 | 64.53 | 6.64 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 2 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.438 | 0.438 | 88.60 | 76.0 | 3.09 |
| 2 | 2 | 0 | 0.868 | 0.877 | 48.03 | 82.2 | 6.13 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8976 | 0.0083 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.8605 | 0.0095 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0427 | 0.0158 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0000 | 0.0000 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.5-35B-A3B-NVFP4@bfcl_v4 | 0.7086 |  |
| acc | 0.7086 | 175 |
| irrelevance | 0.1200 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.8400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8000 | 25 |
| parallel_multiple | 0.7600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8400 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 0.1200 | 25 |
| OVERALL | 0.1700 | 175 |

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
- Top prompt rung capped at 7680 tokens (max length 8192 minus 256 output tokens and 256 tokenizer-skew margin).
- Concurrency levels [4, 8, 16, 32, 64] exceed the recipe's declared max concurrency (2); skipped.
