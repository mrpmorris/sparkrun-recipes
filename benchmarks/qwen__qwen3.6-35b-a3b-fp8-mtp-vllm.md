# qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml benchmark results

Generated UTC: 2026-07-09T03:01:42.168689+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml/20260709-020614 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml --cleanup |
| Total duration | 3328 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.9 |
| max_model_len | 262144 |
| max_num_batched_tokens | 16384 |
| max_num_seqs | 16 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| speculative_config | {"method": "mtp", "num_speculative_tokens": 3} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 274 | 0.239 | 13.7 | 1146.3 | 73.18 | 3.74 |
| 1024 | 1040 | 0.316 | 16.2 | 3294.4 | 62.04 | 4.44 |
| 4096 | 4112 | 0.740 | 16.3 | 5555.1 | 61.72 | 4.89 |
| 16384 | 16398 | 3.096 | 13.1 | 5296.0 | 76.71 | 6.43 |
| 65536 | 65552 | 16.863 | 13.9 | 3887.3 | 72.00 | 20.42 |
| 259267 | 259282 | 145.985 | 23.4 | 1776.1 | 42.94 | 151.95 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7526 | 0.0177 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3487 | 0.0131 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3662 | 0.0133 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.3038 | 0.0134 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3336 | 0.0138 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3300 | 0.0473 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4300 | 0.0498 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5976 | 0.0384 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6840 | 0.0208 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.9143 |  |
| acc | 0.9143 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9400 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2760 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
