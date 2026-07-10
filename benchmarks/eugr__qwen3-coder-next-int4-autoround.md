# @eugr/qwen3-coder-next-int4-autoround benchmark results

Generated UTC: 2026-07-10T03:17:09.015891+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/qwen3-coder-next-int4-autoround |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3-coder-next-int4-autoround/20260710-022931 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3-coder-next-int4-autoround --cleanup |
| Total duration | 2858 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 268 | 0.157 | 14.2 | 1706.8 | 70.47 | 3.79 |
| 1024 | 1037 | 0.338 | 14.3 | 3070.6 | 70.02 | 3.99 |
| 4096 | 4108 | 1.075 | 14.7 | 3820.8 | 68.38 | 4.82 |
| 16384 | 16398 | 4.196 | 15.9 | 3908.4 | 63.13 | 8.25 |
| 65536 | 65546 | 20.840 | 21.4 | 3145.3 | 46.81 | 26.31 |
| 259267 | 259278 | 153.391 | 41.5 | 1690.3 | 24.20 | 163.97 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8386 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9174 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9227 | 0.0074 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6007 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6391 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7000 | 0.0461 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6646 | 0.0370 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7600 | 0.0191 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8457 |  |
| acc | 0.8457 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.7600 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8800 | 100 |
| LIVE | 0.7000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2580 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
