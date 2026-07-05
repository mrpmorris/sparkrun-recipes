# Qwen3.6-35B-A3B-FP8.yaml benchmark results

Generated UTC: 2026-07-05T01:27:29.594099+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-FP8.yaml/20260705-010942 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-FP8.yaml --cleanup |
| Total duration | 1067 s |

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
| 256 | 272 | 0.245 | 13.1 | 1109.2 | 76.82 | 3.58 |
| 1024 | 1037 | 0.378 | 15.1 | 2741.8 | 66.58 | 4.22 |
| 4096 | 4113 | 1.142 | 15.3 | 3600.7 | 65.71 | 5.04 |
| 16384 | 16401 | 3.378 | 17.4 | 4855.9 | 57.57 | 7.82 |
| 65536 | 65552 | 16.907 | 20.0 | 3877.2 | 50.13 | 22.01 |
| 259267 | 259284 | 145.692 | 22.6 | 1779.7 | 44.47 | 151.45 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7333 | 0.0183 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3600 | 0.0482 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3700 | 0.0485 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2700 | 0.0446 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.2800 | 0.0451 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4200 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.5400 | 0.0501 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7300 | 0.0446 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7500 | 0.0435 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
