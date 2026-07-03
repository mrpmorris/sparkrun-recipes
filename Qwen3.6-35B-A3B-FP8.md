# Qwen3.6-35B-A3B-FP8.yaml benchmark results

Generated UTC: 2026-07-03T12:04:44.762985+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-FP8.yaml/20260703-114103 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-35B-A3B-FP8.yaml |
| Total duration | 1422 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.9 |
| max_model_len | 262144 |
| max_num_batched_tokens | 8192 |
| max_num_seqs | 4 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| speculative_config | {"method": "mtp", "num_speculative_tokens": 3} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- |
| 32500 | 32516 | 6.622 | 4910.4 | 61.03 | 10.82 |
| 65000 | 65016 | 20.298 | 3203.1 | 60.11 | 24.56 |
| 97500 | 97518 | 30.264 | 3222.3 | 54.15 | 34.99 |
| 130000 | 130016 | 46.744 | 2781.4 | 53.55 | 51.52 |
| 162500 | 162513 | 67.309 | 2414.4 | 46.03 | 72.87 |
| 195000 | 195015 | 90.960 | 2144.0 | 48.47 | 96.24 |
| 227500 | 227515 | 117.794 | 1931.5 | 44.19 | 123.59 |
| 260000 | 260016 | 147.308 | 1765.1 | 43.27 | 153.22 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8509 | 0.0142 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3600 | 0.0482 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3700 | 0.0485 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5300 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5100 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6100 | 0.0490 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7000 | 0.0461 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7400 | 0.0441 | 100 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
