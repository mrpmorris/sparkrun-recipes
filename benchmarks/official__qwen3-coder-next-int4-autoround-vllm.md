# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-07-09T09:01:20.803804+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260709-080209 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm --cleanup |
| Total duration | 3552 s |

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
| 256 | 270 | 0.175 | 14.4 | 1546.5 | 69.49 | 3.86 |
| 1024 | 1036 | 0.293 | 14.5 | 3541.4 | 69.38 | 3.98 |
| 4096 | 4107 | 0.972 | 14.7 | 4224.7 | 68.34 | 4.72 |
| 16384 | 16399 | 3.780 | 15.6 | 4338.9 | 64.26 | 7.76 |
| 65536 | 65548 | 20.376 | 18.2 | 3217.0 | 55.12 | 25.02 |
| 259267 | 259276 | 169.361 | 28.8 | 1530.9 | 34.85 | 176.71 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9174 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9181 | 0.0076 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6101 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6399 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6707 | 0.0368 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7580 | 0.0192 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8457 |  |
| acc | 0.8457 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.7600 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.6800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2570 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
