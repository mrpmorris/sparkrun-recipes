# @official/qwen3.6-35b-a3b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-07-06T09:14:28.107563+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-35b-a3b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-35b-a3b-fp8-mtp-vllm/20260706-084116 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-35b-a3b-fp8-mtp-vllm --cleanup |
| Total duration | 1992 s |

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
| speculative_config | {"method": "mtp", "num_speculative_tokens": 2} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.252 | 16.6 | 1083.8 | 60.58 | 4.48 |
| 1024 | 1041 | 0.325 | 17.7 | 3199.5 | 56.79 | 4.83 |
| 4096 | 4112 | 0.738 | 18.1 | 5568.3 | 55.34 | 5.36 |
| 16384 | 16401 | 3.431 | 17.7 | 4779.6 | 56.65 | 7.95 |
| 65536 | 65554 | 17.145 | 20.9 | 3823.4 | 48.15 | 22.46 |
| 259267 | 259283 | 147.780 | 27.0 | 1754.5 | 37.12 | 154.68 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.3333 | 0.0191 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3800 | 0.0488 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3900 | 0.0490 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2300 | 0.0423 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3000 | 0.0461 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.2300 | 0.0423 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3300 | 0.0473 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5800 | 0.0496 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5100 | 0.0502 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
