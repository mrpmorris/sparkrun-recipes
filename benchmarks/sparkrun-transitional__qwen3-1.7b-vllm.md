# @sparkrun-transitional/qwen3-1.7b-vllm benchmark results

Generated UTC: 2026-07-05T02:15:28.979767+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @sparkrun-transitional/qwen3-1.7b-vllm |
| Model | Qwen/Qwen3-1.7B |
| Served model name | qwen3-1.7b |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly-tf5:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/sparkrun-transitional__qwen3-1.7b-vllm/20260705-020528 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @sparkrun-transitional/qwen3-1.7b-vllm --cleanup |
| Total duration | 600 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.3 |
| served_model_name | qwen3-1.7b |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 266 | 0.073 | 20.4 | 3659.3 | 49.22 | 5.27 |
| 1024 | 1038 | 0.085 | 20.8 | 12219.9 | 48.37 | 5.38 |
| 4096 | 4108 | 0.271 | 22.3 | 15182.1 | 45.08 | 5.95 |
| 16384 | 16397 | 1.255 | 28.3 | 13067.5 | 35.52 | 8.46 |
| 40295 | 40308 | 4.544 | 39.7 | 8869.8 | 25.31 | 14.66 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.5895 | 0.0192 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6800 | 0.0469 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6800 | 0.0469 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4900 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4600 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4400 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4600 | 0.0501 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5200 | 0.0502 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4400 | 0.0499 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 40295 tokens (max length 40960 minus 256 output tokens and 409 tokenizer-skew margin).
