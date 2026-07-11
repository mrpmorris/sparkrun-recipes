# unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml benchmark results

Generated UTC: 2026-07-11T10:18:23.531560+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml |
| Model | unsloth/DeepSeek-V4-Flash-GGUF:UD-IQ2_M |
| Served model name | unsloth/DeepSeek-V4-Flash-GGUF:UD-IQ2_M |
| Runtime | llama-cpp |
| Container | scitrera/dgx-spark-llama-cpp:b9898-cu131 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml/20260711-091721 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml --cleanup |
| Total duration | 3662 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| max_model_len | 32768 |
| n_gpu_layers | 99 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 261 | 1.509 | 65.7 | 173.0 | 15.27 | 18.27 |
| 1024 | 1029 | 2.943 | 65.9 | 349.7 | 15.23 | 19.75 |
| 4096 | 4101 | 11.086 | 68.3 | 369.9 | 14.70 | 28.50 |
| 16384 | 16389 | 53.381 | 75.4 | 307.0 | 13.32 | 72.61 |
| 32185 | 32190 | 133.655 | 82.8 | 240.8 | 12.13 | 154.76 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

1 task(s) completed, 5 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7060 | 0.0204 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-GGUF_UD-IQ2_M@bfcl_v4 | 0.1429 |  |
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

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | server OOM (2026-07-11T09:23:10.078908+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2941007 uid 1000 "llama-server": badness 998, VmRSS 3984 MiB); server restarted, task skipped | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| humaneval | Coding: write Python functions that pass unit tests | server OOM (2026-07-11T09:28:54.584272+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2942337 uid 1000 "llama-server": badness 997, VmRSS 3896 MiB); server restarted, task skipped | lm-eval-humaneval.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- server OOM (2026-07-11T09:23:10.078908+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2941007 uid 1000 "llama-server": badness 998, VmRSS 3984 MiB) (during gsm8k); server restarted (1/2).
- server OOM (2026-07-11T09:28:54.584272+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2942337 uid 1000 "llama-server": badness 997, VmRSS 3896 MiB) (during humaneval); server restarted (2/2).
- Top prompt rung capped at 32185 tokens (max length 32768 minus 256 output tokens and 327 tokenizer-skew margin).
