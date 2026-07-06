# @official/qwen3.6-35b-a3b-fp8-vllm benchmark results

Generated UTC: 2026-07-06T09:48:37.550078+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-35b-a3b-fp8-vllm |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-35b-a3b-fp8-vllm/20260706-091428 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-35b-a3b-fp8-vllm --cleanup |
| Total duration | 2049 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_batched_tokens | 32768 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.191 | 20.1 | 1430.6 | 49.85 | 5.33 |
| 1024 | 1038 | 0.261 | 20.2 | 3978.6 | 49.67 | 5.41 |
| 4096 | 4113 | 0.784 | 20.4 | 5246.5 | 49.16 | 5.99 |
| 16384 | 16399 | 2.924 | 21.1 | 5608.5 | 47.63 | 8.30 |
| 65536 | 65553 | 15.741 | 23.4 | 4164.5 | 42.96 | 21.70 |
| 259267 | 259284 | 135.086 | 31.6 | 1919.4 | 31.79 | 143.14 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8456 | 0.0146 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3900 | 0.0490 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3900 | 0.0490 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5600 | 0.0499 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5700 | 0.0498 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7600 | 0.0429 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7200 | 0.0451 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7600 | 0.0429 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.9143 |  |
| acc | 0.9143 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2780 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
