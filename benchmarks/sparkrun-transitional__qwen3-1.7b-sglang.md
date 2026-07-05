# @sparkrun-transitional/qwen3-1.7b-sglang benchmark results

Generated UTC: 2026-07-05T02:05:28.166156+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @sparkrun-transitional/qwen3-1.7b-sglang |
| Model | Qwen/Qwen3-1.7B |
| Served model name | qwen3-1.7b |
| Runtime | sglang |
| Container | scitrera/dgx-spark-sglang:0.5.10 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/sparkrun-transitional__qwen3-1.7b-sglang/20260705-014742 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @sparkrun-transitional/qwen3-1.7b-sglang --cleanup |
| Total duration | 1065 s |

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
| 256 | 266 | 0.052 | 20.1 | 5093.9 | 49.87 | 5.19 |
| 1024 | 1037 | 0.154 | 20.5 | 6742.9 | 48.98 | 5.38 |
| 4096 | 4110 | 0.279 | 22.2 | 14724.5 | 45.26 | 5.94 |
| 16384 | 16394 | 1.168 | 28.2 | 14034.7 | 35.59 | 8.36 |
| 40295 | 40308 | 3.999 | 40.1 | 10080.1 | 25.03 | 14.23 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.5912 | 0.0191 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.7100 | 0.0456 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.7100 | 0.0456 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4800 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4600 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4400 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4700 | 0.0502 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5300 | 0.0502 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4300 | 0.0498 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 40295 tokens (max length 40960 minus 256 output tokens and 409 tokenizer-skew margin).
