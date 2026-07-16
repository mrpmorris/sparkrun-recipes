# @atlas/qwen3.6-27b-nvfp4 benchmark results

Generated UTC: 2026-07-15T22:06:40.390720+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/qwen3.6-27b-nvfp4 |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:dev |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__qwen3.6-27b-nvfp4/20260715-174913 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/qwen3.6-27b-nvfp4 --cleanup |
| Total duration | 15447 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8888 |
| host | 0.0.0.0 |
| max_model_len | 32768 |
| max_batch_size | 1 |
| kv_cache_dtype | bf16 |
| gpu_memory_utilization | 0.85 |
| enable_prefix_caching | True |
| ssm_cache_slots | 128 |
| ssm_checkpoint_interval | 32 |
| speculative | True |
| num_drafts | 1 |
| mtp_quantization | bf16 |
| tool_call_parser | qwen3_coder |
| disable_tool_grammar | True |
| disable_thinking | True |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.637 | 3.0 | 428.8 | 657.80 | 0.64 |
| 1024 | 1042 | 1.824 | 3.0 | 571.4 | 672.70 | 1.83 |
| 4096 | 4117 | 6.573 | 3.1 | 626.4 | 646.86 | 6.58 |
| 16384 | 16401 | 27.046 | 3.3 | 606.4 | 614.77 | 27.05 |
| 32185 | 32205 | 56.360 | 3.2 | 571.4 | 631.48 | 56.36 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 1 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.838 | 1.838 | 556.38 | 1.1 | 1.84 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

2 task(s) completed, 4 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0549 | 0.0178 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0820 | 0.0123 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.9257 |  |
| acc | 0.9257 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.8800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2810 | 175 |

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
- before humaneval: server was down [HANG]; restarted (start #1).
- Top prompt rung capped at 32185 tokens (max length 32768 minus 256 output tokens and 327 tokenizer-skew margin).
- Concurrency levels [2, 4, 8, 16, 32, 64] exceed the recipe's declared max concurrency (1); skipped.
