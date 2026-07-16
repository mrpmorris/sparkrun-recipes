# @atlas/qwen3.6-35b-a3b-fp8-mtp benchmark results

Generated UTC: 2026-07-16T13:09:09.210123+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3.6-35b-a3b-fp8-mtp |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3.6-35b-a3b-fp8-mtp/20260716-100132 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3.6-35b-a3b-fp8-mtp --cleanup |
| Total duration | 11257 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 65536 |
| max_batch_size | 2 |
| max_prefill_tokens | 32768 |
| kv_cache_dtype | bf16 |
| kv_high_precision_layers | auto |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |
| speculative | True |
| mtp_quantization | bf16 |
| enable_prefix_caching | True |
| ssm_cache_slots | 256 |
| lm_head_dtype | bf16 |
| oom_guard_mb | 1024 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 2 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.682 | 0.682 | 63.47 | 54.0 | 4.56 |
| 2 | 1 | 1 | 1.367 | 1.367 | 63.72 | 46.5 | 5.05 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9022 | 0.0082 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9121 | 0.0078 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0183 | 0.0105 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.1700 | 0.0168 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.5314 |  |
| acc | 0.5314 | 175 |
| irrelevance | 0.2000 | 25 |
| live_multiple | 0.4800 | 25 |
| live_simple | 0.6400 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.3200 | 25 |
| parallel_multiple | 0.6000 | 25 |
| simple_python | 0.6400 | 25 |
| NON_LIVE | 0.6000 | 100 |
| LIVE | 0.5600 | 50 |
| HALLUCINATION | 0.2000 | 25 |
| OVERALL | 0.1360 | 175 |

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
- Top prompt rung capped at 64625 tokens (max length 65536 minus 256 output tokens and 655 tokenizer-skew margin).
- [ERROR] Speed point 256 tokens failed: JSONDecodeError: Unterminated string starting at: line 1 column 217 (char 216)
- Speed ladder stopped after the 256-token failure; skipped larger rungs: [1024, 4096, 16384, 64625].
- Concurrency levels [4, 8, 16, 32, 64] exceed the recipe's declared max concurrency (2); skipped.
- [ERROR] Concurrency 2: 1 request(s) failed.
