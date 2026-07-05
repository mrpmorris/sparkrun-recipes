# Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml benchmark results

Generated UTC: 2026-07-05T01:44:46.575529+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml/20260705-012731 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml --cleanup |
| Total duration | 1035 s |

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
| 256 | 274 | 0.329 | 8.6 | 833.5 | 117.03 | 2.52 |
| 1024 | 1041 | 0.387 | 10.9 | 2692.5 | 91.76 | 3.18 |
| 4096 | 4113 | 0.728 | 11.6 | 5652.6 | 86.18 | 3.70 |
| 16384 | 16399 | 2.744 | 12.3 | 5975.6 | 81.32 | 5.89 |
| 65536 | 65554 | 13.994 | 24.3 | 4684.4 | 41.29 | 20.19 |
| 259267 | 259282 | 113.376 | 87.8 | 2286.9 | 11.44 | 135.76 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8386 | 0.0152 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0900 | 0.0288 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1000 | 0.0302 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5200 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4900 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7700 | 0.0423 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7400 | 0.0441 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6200 | 0.0488 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
