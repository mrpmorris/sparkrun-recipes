# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-03T11:08:09.376738+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260703-101447 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml |
| Total duration | 3202 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | nvidia/Qwen3.6-27B-NVFP4 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.7 |
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
| 32500 | 32513 | 30.627 | 1061.6 | 12.26 | 51.50 |
| 65000 | 65019 | 68.650 | 947.1 | 11.62 | 90.68 |
| 97500 | 97515 | 113.427 | 859.7 | 11.11 | 136.46 |
| 130000 | 130015 | 166.527 | 780.7 | 10.62 | 190.63 |
| 162500 | 162515 | 225.466 | 720.8 | 10.18 | 250.61 |
| 195000 | 195013 | 292.458 | 666.8 | 9.76 | 318.69 |
| 227500 | 227516 | 368.303 | 617.7 | 9.36 | 395.67 |
| 260000 | 260014 | 451.100 | 576.4 | 9.07 | 479.32 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8614 | 0.0142 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6300 | 0.0485 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6500 | 0.0479 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6300 | 0.0485 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6000 | 0.0492 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7700 | 0.0423 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.9000 | 0.0302 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5200 | 0.0502 | 100 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
