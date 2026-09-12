# @eugr/qwen3.8-flash-next-nvfp4-cluster benchmark results

Generated UTC: 2026-09-12T14:27:17.820624+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/qwen3.8-flash-next-nvfp4-cluster |
| Model | local-inference-lab/Qwen3.8-Flash-Next-NVFP4 |
| Served model name | local-inference-lab/Qwen3.8-Flash-Next-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node-b12x |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1032-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3.8-flash-next-nvfp4-cluster/20260912-142646 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3.8-flash-next-nvfp4-cluster --force --skip-run --skip-speed --skip-concurrency --skip-bfcl --eval-tasks mbpp --eval-limit 20 |
| Total duration | 31 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| block_size | 16 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 4096 |
| num_speculative_tokens | 4 |
| gpu_memory_utilization | 0.7 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 313 | 0.361 | 18.1 | 866.9 | 55.49 | 4.97 |
| 1024 | 1081 | 0.520 | 23.8 | 2078.2 | 42.24 | 6.58 |
| 4096 | 4154 | 1.387 | 20.5 | 2994.4 | 48.98 | 6.61 |
| 16384 | 16441 | 5.220 | 19.2 | 3149.4 | 52.37 | 10.11 |
| 65536 | 65594 | 22.078 | 21.0 | 2971.0 | 47.74 | 27.44 |
| 259267 | 259325 | 117.229 | 18.1 | 2212.1 | 55.57 | 121.84 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

_Skipped (--skip-concurrency)._

## Intelligence (lm-eval)

1 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7000 | 0.1051 | 20 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (--skip-bfcl)._

## Warnings

- lm-eval ran with sample limits (mbpp:20); those scores are comparative samples, not full-benchmark numbers.
- Code tasks (mbpp) auto-fell back to /v1/chat/completions with thinking disabled (chat_template_kwargs enable_thinking=False): completions emit empty/think-tagged generations that break prompt+generation execution, while no-think chat yields raw executable code.
- Speed section reused from earlier run 20260912-105812 (--skip-speed).
