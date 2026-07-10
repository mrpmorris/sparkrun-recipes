# eugr__diffusion-gemma-bf16-test.yaml benchmark results

Generated UTC: 2026-07-10T17:45:06.794097+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/eugr__diffusion-gemma-bf16-test.yaml |
| Model | google/diffusiongemma-26B-A4B-it |
| Served model name | google/diffusiongemma-26B-A4B-it |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__diffusion-gemma-bf16-test.yaml/20260710-173642 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe eugr__diffusion-gemma-bf16-test.yaml --force --skip-bfcl --skip-speed --eval-tasks gsm8k:20,mbpp:10 |
| Total duration | 504 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 131072 |
| max_num_seqs | 10 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 272 | 0.687 | 0.0 | 395.8 | 791268.81 | 0.69 |
| 1024 | 1042 | 0.876 | 0.0 | 1189.7 | 4481793.30 | 0.88 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

1 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4000 | 0.1633 | 10 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (--skip-bfcl)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | server stopped generating (no OOM event in syslog; crashed or wedged); server restarted, task skipped | lm-eval-gsm8k.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: gsm8k:20,mbpp:10); scores are comparative samples, not full-benchmark numbers.
- server stopped generating (no OOM event in syslog; crashed or wedged) (during gsm8k); server restarted (1/2).
- Speed section reused from earlier run 20260710-123238 (--skip-speed).
