# Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml benchmark results

Generated UTC: 2026-07-04T23:19:25.523514+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml |
| Model | AEON-7/Qwen3.6-35B-A3B-heretic-NVFP4 |
| Served model name | Qwen/Qwen3.6-35B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml/20260704-230921 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml --skip-eval |
| Total duration | 604 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | Qwen/Qwen3.6-35B |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.85 |
| max_model_len | 262144 |
| max_num_seqs | 64 |
| max_num_batched_tokens | 16384 |
| quantization | compressed-tensors |
| attention_backend | flash_attn |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-35B-A3B-DFlash","revision":"42d3b34d588423cdae7ba8f53a8cf7789346a719","num_speculative_tokens":11} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 272 | 0.172 | 13.0 | 1584.0 | 77.47 | 3.48 |
| 1024 | 1039 | 0.241 | 8.7 | 4302.8 | 114.93 | 2.47 |
| 4096 | 4111 | 0.731 | 10.3 | 5625.3 | 97.03 | 3.37 |
| 16384 | 16398 | 2.760 | 12.7 | 5942.2 | 79.01 | 6.00 |
| 65536 | 65549 | 13.998 | 25.9 | 4682.7 | 38.77 | 20.60 |
| 259267 | 259286 | 113.589 | 68.4 | 2282.7 | 14.68 | 131.03 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

_Skipped (--skip-eval)._

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
