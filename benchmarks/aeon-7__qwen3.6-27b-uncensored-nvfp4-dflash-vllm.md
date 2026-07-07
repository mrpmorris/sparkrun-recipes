# aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-07T18:33:36.800850+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml |
| Model | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-Multimodal-NVFP4-MTP-XS |
| Served model name | Qwen/Qwen3.6-27B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml/20260707-171447 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 4729 s |

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
| 256 | 271 | 0.224 | 16.0 | 1211.6 | 62.90 | 4.29 |
| 1024 | 1037 | 0.613 | 27.2 | 1691.5 | 36.98 | 7.54 |
| 4096 | 4112 | 1.724 | 35.5 | 2384.5 | 28.25 | 10.79 |
| 16384 | 16400 | 8.869 | 28.4 | 1849.2 | 35.31 | 16.12 |
| 65536 | 65553 | 43.854 | 45.7 | 1494.8 | 21.96 | 55.51 |
| 259267 | 259284 | 314.775 | 83.7 | 823.7 | 11.99 | 336.12 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7860 | 0.0169 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0644 | 0.0068 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0751 | 0.0073 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5094 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5162 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5700 | 0.0498 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8049 | 0.0310 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6360 | 0.0215 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B@bfcl_v4 | 0.8743 |  |
| acc | 0.8743 | 175 |
| irrelevance | 0.8400 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.8400 | 25 |
| OVERALL | 0.2580 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
