# Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml benchmark results

Generated UTC: 2026-07-04T14:39:37.613734+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Model | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-Multimodal-NVFP4-MTP-XS |
| Served model name | Qwen/Qwen3.6-27B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml/20260704-140355 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Total duration | 2142 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | Qwen/Qwen3.6-27B |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.85 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 16384 |
| quantization | modelopt |
| mamba_cache_dtype | float32 |
| attention_backend | flash_attn |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-27B-DFlash","num_speculative_tokens":10} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 250 | 263 | 0.393 | 22.5 | 669.5 | 44.60 | 6.13 |
| 1000 | 1016 | 0.742 | 25.8 | 1368.7 | 38.89 | 7.33 |
| 4000 | 4014 | 1.881 | 34.3 | 2133.7 | 29.26 | 10.63 |
| 16000 | 16013 | 9.586 | 30.1 | 1670.4 | 33.30 | 17.27 |
| 64000 | 64015 | 44.486 | 48.6 | 1439.0 | 20.67 | 56.87 |
| 256000 | 256014 | 315.576 | 91.0 | 811.3 | 11.04 | 338.77 |
| 260000 | 260015 | 324.162 | 94.4 | 802.1 | 10.63 | 348.24 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8018 | 0.0166 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0700 | 0.0256 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0900 | 0.0288 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5100 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5200 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6000 | 0.0492 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8400 | 0.0368 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5100 | 0.0502 | 100 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
