# aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-10T23:41:34.748201+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml/20260710-212030 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 8464 s |

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
| 256 | 270 | 0.229 | 16.9 | 1179.3 | 59.47 | 4.53 |
| 1024 | 1044 | 0.627 | 15.6 | 1666.3 | 64.18 | 4.62 |
| 4096 | 4109 | 1.875 | 34.8 | 2191.4 | 28.88 | 10.74 |
| 16384 | 16402 | 9.095 | 32.3 | 1803.5 | 31.09 | 17.33 |
| 65536 | 65551 | 44.261 | 46.4 | 1481.0 | 21.66 | 56.08 |
| 259267 | 259282 | 316.444 | 91.7 | 819.4 | 10.95 | 339.82 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7912 | 0.0170 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0811 | 0.0075 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0895 | 0.0079 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5102 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5205 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5600 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6600 | 0.0476 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7622 | 0.0333 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6480 | 0.0214 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B@bfcl_v4 | 0.8514 |  |
| acc | 0.8514 | 175 |
| irrelevance | 0.8800 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8000 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 0.8800 | 25 |
| OVERALL | 0.2530 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
