# @eugr/glm-4.7-flash-awq benchmark results

Generated UTC: 2026-07-13T19:07:50.021606+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/glm-4.7-flash-awq |
| Model | cyankiwi/GLM-4.7-Flash-AWQ-4bit |
| Served model name | glm-4.7-flash |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-4.7-flash-awq/20260713-182941 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/glm-4.7-flash-awq --cleanup |
| Total duration | 2289 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 202752 |
| max_num_batched_tokens | 4096 |
| max_num_seqs | 64 |
| served_model_name | glm-4.7-flash |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 264 | 0.134 | 22.0 | 1972.4 | 45.55 | 5.75 |
| 1024 | 1031 | 0.210 | 22.3 | 4907.1 | 45.11 | 5.89 |
| 4096 |  |  |  |  |  | 8.73 |
| 16384 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 64 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.227 | 0.227 | 45.26 | 43.5 | 5.88 |
| 2 | 2 | 0 | 0.679 | 0.727 | 40.09 | 72.4 | 7.07 |
| 4 | 4 | 0 | 0.706 | 0.707 | 31.19 | 115.5 | 8.86 |
| 8 | 8 | 0 | 0.546 | 0.546 | 0.11 | 0.1 | 9.55 |
| 16 | 16 | 0 | 0.898 | 0.898 | 0.11 | 0.1 | 10.17 |
| 32 | 32 | 0 | 0.895 | 0.895 | 0.11 | 0.1 | 9.94 |
| 64 | 64 | 0 | 0.925 | 0.925 | 0.11 | 0.1 | 10.26 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| glm-4.7-flash@bfcl_v4 | 0.1429 |  |
| acc | 0.1429 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.0000 | 25 |
| live_simple | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| NON_LIVE | 0.0000 | 100 |
| LIVE | 0.0000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.1000 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | CRASH | Grade-school math word problems (multi-step reasoning) | [CRASH] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.; HTTP 500 from inference server: EngineCore encountered an issue. See stack trace (above) for the root cause. | lm-eval-gsm8k.log |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| humaneval | CRASH | Coding: write Python functions that pass unit tests | [CRASH] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.; HTTP 500 from inference server: EngineCore encountered an issue. See stack trace (above) for the root cause. | lm-eval-humaneval.log |
| mbpp | CRASH | Coding: basic Python programming problems, graded by unit tests | [CRASH] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.; HTTP 500 from inference server: EngineCore encountered an issue. See stack trace (above) for the root cause. | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- before gsm8k: server was down [CRASH]; restarted (start #1).
- before humaneval: server was down [CRASH]; restarted (start #2).
- before mbpp: server was down [CRASH]; restarted (start #3).
- before speed: server was down [CRASH]; restarted (start #4).
- Top prompt rung capped at 200469 tokens (max length 202752 minus 256 output tokens and 2027 tokenizer-skew margin).
- [CRASH] Speed point 16384 tokens failed (vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.): HTTPError: 500 Server Error: Internal Server Error for url: http://127.0.0.1:8000/v1/chat/completions
- Speed ladder stopped after the 16384-token failure; skipped larger rungs: [65536, 200469].
- before concurrency: server was down [CRASH]; restarted (start #5).
- before concurrency 16: server was down [CRASH]; restarted (start #6).
- before concurrency 32: server was down [CRASH]; restarted (start #7).
- before concurrency 64: server was down [CRASH]; restarted (start #8).
