# @atlas/nemotron-3-nano-30b-a3b-nvfp4 benchmark results

Generated UTC: 2026-07-14T13:12:23.679273+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @atlas/nemotron-3-nano-30b-a3b-nvfp4 |
| Model | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/atlas__nemotron-3-nano-30b-a3b-nvfp4/20260714-102228 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @atlas/nemotron-3-nano-30b-a3b-nvfp4 --cleanup |
| Total duration | 10196 s |

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
| 256 | 276 | 0.614 | 10.3 | 449.9 | 98.68 | 1.46 |
| 1024 | 1047 | 1.273 | 11.1 | 822.7 | 90.23 | 6.77 |
| 4096 | 4118 | 4.207 | 12.3 | 978.8 | 81.66 | 10.44 |
| 7680 | 7702 | 7.499 | 14.2 | 1027.1 | 70.40 | 14.66 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.275 | 1.275 | 92.30 | 68.9 | 5.03 |
| 2 | 2 | 0 | 2.639 | 2.648 | 50.81 | 69.9 | 11.37 |
| 4 | 4 | 0 | 5.096 | 5.117 | 24.30 | 73.0 | 24.96 |
| 8 | 8 | 0 | 10.182 | 10.184 | 12.24 | 72.3 | 51.64 |
| 16 | 16 | 0 | 20.801 | 61.922 | 11.36 | 67.3 | 92.43 |
| 32 | 32 | 0 | 71.012 | 148.616 | 10.53 | 73.0 | 181.05 |
| 64 | 64 | 0 | 145.065 | 286.478 | 9.51 | 70.4 | 306.33 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0008 | 0.0008 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0030 | 0.0015 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0000 | 0.0000 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0000 | 0.0000 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.1314 |  |
| acc | 0.1314 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.0000 | 25 |
| live_simple | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| NON_LIVE | 0.0000 | 100 |
| LIVE | 0.0000 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.0920 | 175 |

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
