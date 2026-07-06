# @eugr/nemotron-3-nano-nvfp4 benchmark results

Generated UTC: 2026-07-06T16:44:08.728692+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3-nano-nvfp4/20260706-160859 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3-nano-nvfp4 --cleanup |
| Total duration | 2110 s |

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
| 256 | 277 | 0.128 | 17.4 | 2164.9 | 57.76 | 4.56 |
| 1024 | 1045 | 0.196 | 17.4 | 5319.2 | 57.73 | 4.63 |
| 4096 | 4115 | 0.651 | 17.4 | 6320.7 | 57.63 | 5.09 |
| 16384 | 16406 | 2.551 | 17.6 | 6430.1 | 57.15 | 7.03 |
| 65536 | 65558 | 11.933 | 18.1 | 5493.8 | 55.48 | 16.55 |
| 259267 | 259285 | 77.856 | 20.4 | 3330.3 | 49.26 | 83.05 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7000 | 0.0182 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9000 | 0.0302 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5700 | 0.0498 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4500 | 0.0500 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4800 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5200 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6700 | 0.0473 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.3400 | 0.0476 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5900 | 0.0494 | 100 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.8571 |  |
| acc | 0.8571 | 175 |
| irrelevance | 0.8800 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.8400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 0.8800 | 25 |
| OVERALL | 0.2540 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
