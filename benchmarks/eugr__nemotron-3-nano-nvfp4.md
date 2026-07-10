# @eugr/nemotron-3-nano-nvfp4 benchmark results

Generated UTC: 2026-07-10T01:13:36.534360+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/nemotron-3-nano-nvfp4 |
| Model | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3-nano-nvfp4/20260709-235934 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3-nano-nvfp4 --cleanup |
| Total duration | 4442 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 276 | 0.139 | 17.5 | 1990.3 | 57.52 | 4.59 |
| 1024 | 1046 | 0.196 | 17.4 | 5349.4 | 57.65 | 4.64 |
| 4096 | 4118 | 0.653 | 17.5 | 6303.4 | 57.51 | 5.10 |
| 16384 | 16406 | 2.542 | 17.6 | 6455.1 | 56.99 | 7.03 |
| 65536 | 65555 | 11.977 | 18.2 | 5473.5 | 55.28 | 16.61 |
| 259267 | 259289 | 77.886 | 20.6 | 3329.1 | 48.82 | 83.13 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7088 | 0.0179 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8279 | 0.0104 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.4640 | 0.0137 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4573 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4804 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6500 | 0.0479 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.2256 | 0.0327 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5860 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9600 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.2650 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
