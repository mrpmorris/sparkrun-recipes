# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-07-06T01:53:57.536897+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3-coder-next-int4-autoround-vllm |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly-tf5:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260706-011856 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm --cleanup |
| Total duration | 2101 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| tool_call_parser | qwen3_coder |
| max_num_seqs | 128 |
| max_num_batched_tokens | 16384 |
| kv_cache_dtype | fp8 |
| optimization_level | 3 |
| performance_mode | throughput |
| mamba_cache_mode | align |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.162 | 14.5 | 1669.9 | 69.14 | 3.87 |
| 1024 | 1037 | 0.291 | 14.6 | 3561.7 | 68.80 | 4.01 |
| 4096 | 4109 | 0.975 | 14.9 | 4214.1 | 67.51 | 4.77 |
| 16384 | 16395 | 3.780 | 15.4 | 4337.7 | 65.00 | 7.72 |
| 65536 | 65549 | 20.378 | 18.1 | 3216.7 | 55.55 | 24.99 |
| 259267 | 259282 | 169.011 | 28.6 | 1534.1 | 35.10 | 176.31 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8368 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9400 | 0.0239 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9100 | 0.0288 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6300 | 0.0485 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7400 | 0.0441 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7900 | 0.0409 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8686 |  |
| acc | 0.8686 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.8000 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2640 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
