# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-02T14:32:43.753842+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260702-142749 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml --skip-speed --eval-tasks gsm8k,arc_challenge --eval-limit 3 |
| Total duration | 295 s |

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

## Intelligence (lm-eval)

| Task | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- |
| gsm8k | sample_len | 3 |  | 3 |
| gsm8k | exact_match,strict-match | 0.3333 | 0.3333 | 3 |
| gsm8k | exact_match,flexible-extract | 0.3333 | 0.3333 | 3 |
| arc_challenge | sample_len | 3 |  | 3 |
| arc_challenge | acc,none | 0.6667 | 0.3333 | 3 |
| arc_challenge | acc_norm,none | 0.3333 | 0.3333 | 3 |

## Warnings

- Recipe max_num_seqs=4 is below the highest tested concurrency (16); excess requests queue server-side, inflating TTFT.
- lm-eval ran with --limit 3 (per task/subtask); scores are comparative samples, not full-benchmark numbers.
