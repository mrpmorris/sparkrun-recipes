# @eugr/qwen3-coder-next-int4-autoround benchmark results

Generated UTC: 2026-07-06T19:21:42.461066+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3-coder-next-int4-autoround/20260706-184414 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3-coder-next-int4-autoround --cleanup |
| Total duration | 2248 s |

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
| 256 | 269 | 0.177 | 14.1 | 1522.9 | 71.14 | 3.78 |
| 1024 | 1038 | 0.338 | 14.3 | 3072.9 | 70.29 | 3.98 |
| 4096 | 4107 | 1.078 | 14.5 | 3809.1 | 69.01 | 4.79 |
| 16384 | 16399 | 4.184 | 15.7 | 3919.7 | 63.98 | 8.18 |
| 65536 | 65547 | 20.821 | 21.0 | 3148.1 | 47.80 | 26.18 |
| 259267 | 259279 | 153.425 | 40.7 | 1689.9 | 24.69 | 163.79 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8421 | 0.0147 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9400 | 0.0239 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9400 | 0.0239 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6400 | 0.0482 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7000 | 0.0461 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7300 | 0.0446 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8200 | 0.0386 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8514 |  |
| acc | 0.8514 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.7600 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8000 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8800 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2580 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
