# Qwen3.6-35B-A3B-FP8.yaml benchmark results

Generated UTC: 2026-07-06T01:08:47.907979+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-FP8.yaml |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-FP8.yaml/20260706-003507 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-FP8.yaml --cleanup |
| Total duration | 2020 s |

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
| 256 | 271 | 0.822 | 12.3 | 329.9 | 81.85 | 3.95 |
| 1024 | 1041 | 0.339 | 16.7 | 3069.1 | 60.02 | 4.60 |
| 4096 | 4110 | 1.145 | 16.1 | 3590.1 | 62.54 | 5.24 |
| 16384 | 16398 | 3.263 | 15.8 | 5025.8 | 63.59 | 7.29 |
| 65536 | 65555 | 17.909 | 16.4 | 3660.5 | 61.30 | 22.08 |
| 259267 | 259284 | 147.925 | 24.9 | 1752.8 | 40.32 | 154.27 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7596 | 0.0176 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3600 | 0.0482 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3700 | 0.0485 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2500 | 0.0435 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3000 | 0.0461 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3800 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4600 | 0.0501 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7300 | 0.0446 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7500 | 0.0435 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2710 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
