# eugr__diffusion-gemma-bf16-thinking.yaml benchmark results

Generated UTC: 2026-07-10T11:19:21.800900+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/eugr__diffusion-gemma-bf16-thinking.yaml |
| Model | google/diffusiongemma-26B-A4B-it |
| Served model name | google/diffusiongemma-26B-A4B-it |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__diffusion-gemma-bf16-thinking.yaml/20260710-111636 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe eugr__diffusion-gemma-bf16-thinking.yaml --force --skip-bfcl --skip-eval --max-prompt 1024 --steps 1 |
| Total duration | 165 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_seqs | 10 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 278 | 2.386 | 0.0 | 116.5 | 791559.97 | 2.39 |
| 1024 | 1043 | 2.569 | 0.0 | 406.1 | 1270629.16 | 2.57 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

_Skipped (--skip-eval)._

## Tool calling (BFCL v4 via EvalScope)

_Skipped (--skip-bfcl)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
