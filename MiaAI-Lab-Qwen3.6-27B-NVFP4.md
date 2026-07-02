# MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml benchmark results

Generated UTC: 2026-07-02T22:33:36.728895+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml/20260702-214259 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml |
| Total duration | 3037 s |

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
| 32500 | 32515 | 32.279 | 1007.3 | 26.67 | 41.88 |
| 65000 | 65015 | 71.290 | 912.0 | 30.65 | 79.64 |
| 97500 | 97516 | 118.500 | 822.9 | 28.84 | 127.38 |
| 130000 | 130017 | 173.529 | 749.3 | 28.10 | 182.64 |
| 162500 | 162514 | 235.460 | 690.2 | 25.21 | 245.61 |
| 195000 | 195012 | 305.368 | 638.6 | 23.70 | 316.17 |
| 227500 | 227515 | 383.763 | 592.9 | 23.39 | 394.71 |
| 260000 | 260016 | 469.252 | 554.1 | 22.59 | 480.59 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8491 | 0.0148 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6500 | 0.0479 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8500 | 0.0359 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3000 | 0.0461 | 100 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- lm-eval arc_challenge failed (exit 1); see lm-eval-arc_challenge.log
- lm-eval hellaswag failed (exit 1); see lm-eval-hellaswag.log
