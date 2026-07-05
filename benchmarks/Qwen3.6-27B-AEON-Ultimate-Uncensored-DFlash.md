# Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml benchmark results

Generated UTC: 2026-07-05T00:35:13.998052+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml/20260705-000552 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml --cleanup |
| Total duration | 1762 s |

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
| 256 | 272 | 0.372 | 23.1 | 731.0 | 43.47 | 6.26 |
| 1024 | 1040 | 0.735 | 17.0 | 1414.8 | 59.01 | 5.07 |
| 4096 | 4112 | 1.764 | 34.5 | 2330.6 | 29.14 | 10.55 |
| 16384 | 16397 | 10.259 | 29.4 | 1598.2 | 34.09 | 17.77 |
| 65536 | 65553 | 47.918 | 46.9 | 1368.0 | 21.40 | 59.88 |
| 259267 | 259282 | 332.032 | 104.0 | 780.9 | 9.65 | 358.56 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7930 | 0.0166 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0700 | 0.0256 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0900 | 0.0288 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5400 | 0.0501 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5100 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8200 | 0.0386 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7000 | 0.0461 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
