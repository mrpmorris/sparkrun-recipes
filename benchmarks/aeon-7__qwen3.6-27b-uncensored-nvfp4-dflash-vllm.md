# aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-08T21:52:12.706075+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml/20260708-193940 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 7952 s |

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
| 256 | 271 | 0.213 | 23.4 | 1270.0 | 42.96 | 6.17 |
| 1024 | 1041 | 0.556 | 24.4 | 1871.6 | 41.09 | 6.79 |
| 4096 | 4110 | 1.839 | 31.6 | 2234.3 | 31.76 | 9.90 |
| 16384 | 16398 | 10.109 | 32.6 | 1622.2 | 30.78 | 18.43 |
| 65536 | 65554 | 46.817 | 44.7 | 1400.2 | 22.46 | 58.22 |
| 259267 | 259283 | 329.575 | 104.2 | 786.7 | 9.64 | 356.14 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7877 | 0.0170 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0682 | 0.0069 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0773 | 0.0074 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4974 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5162 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5600 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7622 | 0.0333 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6660 | 0.0211 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.8800 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.8800 | 25 |
| OVERALL | 0.2630 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
