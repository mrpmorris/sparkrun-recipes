# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-02T17:22:38.001355+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260702-163222 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml |
| Total duration | 3016 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
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
| 32500 | 32517 | 32.437 | 1002.5 | 28.52 | 41.41 |
| 65000 | 65018 | 71.291 | 912.0 | 28.29 | 80.34 |
| 97500 | 97513 | 118.814 | 820.7 | 23.57 | 129.67 |
| 130000 | 130014 | 174.024 | 747.1 | 25.31 | 184.14 |
| 162500 | 162515 | 236.461 | 687.3 | 24.50 | 246.91 |
| 195000 | 195016 | 306.559 | 636.1 | 23.89 | 317.27 |
| 227500 | 227515 | 385.792 | 589.7 | 24.25 | 396.35 |
| 260000 | 260017 | 470.809 | 552.3 | 21.04 | 482.98 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8526 | 0.0145 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6300 | 0.0485 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6500 | 0.0479 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8200 | 0.0386 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3200 | 0.0469 | 100 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- lm-eval arc_challenge failed (exit 1); see lm-eval-arc_challenge.log
- lm-eval hellaswag failed (exit 1); see lm-eval-hellaswag.log
