# nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml benchmark results

Generated UTC: 2026-07-08T05:00:02.655568+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml |
| Model | nvidia/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml/20260708-031622 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml --cleanup |
| Total duration | 6220 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 275 | 0.258 | 50.2 | 1066.9 | 19.99 | 13.06 |
| 1024 | 1048 | 0.437 | 50.3 | 2396.5 | 19.95 | 13.27 |
| 4096 | 4115 | 1.488 | 50.4 | 2764.6 | 19.92 | 14.34 |
| 16384 | 16403 | 5.844 | 50.6 | 2806.7 | 19.83 | 18.75 |
| 65536 | 65558 | 25.642 | 51.5 | 2556.7 | 19.50 | 38.77 |
| 259267 | 259287 | 141.626 | 54.7 | 1830.8 | 18.36 | 155.57 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8351 | 0.0151 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9174 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9219 | 0.0074 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6015 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6382 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.4695 | 0.0391 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7900 | 0.0182 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-NVFP4@bfcl_v4 | 0.6914 |  |
| acc | 0.6914 | 175 |
| irrelevance | 0.8800 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.1600 | 25 |
| parallel_multiple | 0.2400 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.5800 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 0.8800 | 25 |
| OVERALL | 0.2280 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
