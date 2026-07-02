# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-02T14:26:24.780514+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260702-142545 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml --max-prompt 4096 --concurrency 1,4 --sweep-sizes 1024 --output-tokens 64 --eval-tasks gsm8k,arc_challenge --eval-limit 3 |
| Total duration | 39 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8888 |
| served_model_name | nvidia/Qwen3.6-27B-NVFP4 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.4 |
| max_model_len | 262144 |
| max_num_seqs | 4 |
| max_num_batched_tokens | 8192 |
| quantization | modelopt |
| load_format | fastsafetensors |
| attention_backend | flashinfer |
| moe_backend | marlin |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"mtp","num_speculative_tokens":3,"moe_backend":"triton"} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (concurrency 1)

| Prompt tokens | Concurrency | OK | Failed | Server prompt tokens | TTFT mean s | TTFT p50 s | TTFT p95 s | Prefill tok/s | Decode tok/s (per req) | Aggregate output tok/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | 1 | 1 | 0 | 1040 | 1.306 | 1.306 | 1.306 | 796.3 | 32.76 | 19.63 |
| 2048 | 1 | 1 | 0 | 2065 | 2.442 | 2.442 | 2.442 | 845.6 | 32.62 | 14.53 |
| 4096 | 1 | 1 | 0 | 4111 | 4.362 | 4.362 | 4.362 | 942.4 | 29.04 | 9.75 |

## Concurrency scaling

### Prompt size 1024 tokens

| Prompt tokens | Concurrency | OK | Failed | Server prompt tokens | TTFT mean s | TTFT p50 s | TTFT p95 s | Prefill tok/s | Decode tok/s (per req) | Aggregate output tok/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | 1 | 1 | 0 | 1041 | 1.327 | 1.327 | 1.327 | 784.7 | 34.67 | 20.17 |
| 1024 | 4 | 4 | 0 | 1040 | 4.070 | 3.274 | 5.982 | 278.5 | 29.61 | 30.37 |

## Intelligence (lm-eval)

_None._

## Warnings

- lm-eval ran with --limit 3 (per task/subtask); scores are comparative samples, not full-benchmark numbers.
- lm-eval gsm8k failed (exit 1); see lm-eval-gsm8k.log
- lm-eval arc_challenge failed (exit 1); see lm-eval-arc_challenge.log
