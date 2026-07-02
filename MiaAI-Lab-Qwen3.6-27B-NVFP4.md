# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-02T14:48:12.905685+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260702-144313 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml --max-prompt 4096 --steps 4 --output-tokens 64 --eval-tasks humaneval,mbpp --eval-limit 2 |
| Total duration | 300 s |

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
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- |
| 1024 | 1039 | 1.283 | 810.1 | 36.81 | 3.02 |
| 2048 | 2065 | 2.118 | 975.0 | 36.63 | 3.87 |
| 3072 | 3088 | 3.091 | 999.1 | 29.12 | 5.29 |
| 4096 | 4114 | 4.331 | 950.0 | 34.08 | 6.21 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

_None._

## Warnings

- lm-eval ran with --limit 2 (per task/subtask); scores are comparative samples, not full-benchmark numbers.
- lm-eval humaneval failed (exit 1); see lm-eval-humaneval.log
- lm-eval mbpp failed (exit 1); see lm-eval-mbpp.log
