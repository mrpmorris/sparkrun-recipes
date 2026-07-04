# Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml benchmark results

Generated UTC: 2026-07-04T15:38:21.067399+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml/20260704-151259 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Total duration | 1522 s |

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
| 250 | 266 | 0.296 | 23.0 | 899.3 | 43.58 | 6.17 |
| 1000 | 1017 | 0.549 | 22.7 | 1852.0 | 44.17 | 6.34 |
| 4000 | 4015 | 1.834 | 34.8 | 2189.7 | 28.83 | 10.71 |
| 16000 | 16017 | 10.116 | 37.5 | 1583.4 | 26.77 | 19.68 |
| 64000 | 64017 | 47.180 | 40.8 | 1356.9 | 24.61 | 57.58 |
| 256000 | 256015 | 326.786 | 125.9 | 783.4 | 7.97 | 358.90 |
| 260000 | 260019 | 337.942 | 102.5 | 769.4 | 9.80 | 364.07 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8000 | 0.0167 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0900 | 0.0288 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0900 | 0.0288 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5800 | 0.0496 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5500 | 0.0500 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6600 | 0.0476 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8700 | 0.0338 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7300 | 0.0446 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
