# Qwen3.6-atlas-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-07-07T14:22:36.224138+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-atlas-27b-fp8-vllm.yaml |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-atlas-27b-fp8-vllm.yaml/20260707-103703 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-atlas-27b-fp8-vllm.yaml --cleanup |
| Total duration | 13533 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| max_model_len | 262144 |
| max_batch_size | 2 |
| max_num_seqs | 16 |
| kv_cache_dtype | fp8 |
| kv_high_precision_layers | auto |
| gpu_memory_utilization | 0.88 |
| scheduling_policy | slai |
| speculative | False |
| mtp_quantization | bf16 |
| enable_prefix_caching | True |
| oom_guard_mb | 1024 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.998 | 66.6 | 271.6 | 15.06 | 20.85 |
| 1024 | 1040 | 2.662 | 67.3 | 390.7 | 14.93 | 18.87 |
| 4096 | 4115 | 9.320 | 70.6 | 441.5 | 14.22 | 27.75 |
| 16384 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0600 | 0.0239 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0800 | 0.0273 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0000 | 0.0000 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.1600 | 0.0368 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.2686 |  |
| acc | 0.2686 | 175 |
| irrelevance | 0.6000 | 25 |
| live_multiple | 0.0800 | 25 |
| live_simple | 0.4800 | 25 |
| multiple | 0.2400 | 25 |
| parallel | 0.0400 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.4400 | 25 |
| NON_LIVE | 0.1800 | 100 |
| LIVE | 0.2800 | 50 |
| HALLUCINATION | 0.6000 | 25 |
| OVERALL | 0.1060 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Speed point 16384 tokens failed: JSONDecodeError: Unterminated string starting at: line 1 column 223 (char 222)
- Speed ladder stopped after the 16384-token failure; skipped larger rungs: [65536, 259267].
