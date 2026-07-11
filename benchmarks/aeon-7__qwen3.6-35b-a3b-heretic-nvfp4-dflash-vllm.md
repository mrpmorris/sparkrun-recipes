# aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-11T00:46:33.555723+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml |
| Model | AEON-7/Qwen3.6-35B-A3B-heretic-NVFP4 |
| Served model name | Qwen/Qwen3.6-35B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml/20260710-234135 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 3898 s |

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
| max_num_seqs | 16 |
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
| 256 | 273 | 0.136 | 13.2 | 2004.9 | 76.04 | 3.50 |
| 1024 | 1037 | 0.241 | 10.8 | 4311.1 | 92.97 | 2.99 |
| 4096 | 4112 | 0.731 | 11.0 | 5627.9 | 91.01 | 3.54 |
| 16384 | 16401 | 2.638 | 13.0 | 6216.3 | 77.20 | 5.95 |
| 65536 | 65553 | 14.074 | 24.9 | 4657.8 | 40.39 | 20.41 |
| 259267 | 259282 | 113.215 | 95.9 | 2290.2 | 10.47 | 137.67 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8439 | 0.0145 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.1069 | 0.0085 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1319 | 0.0093 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5265 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5230 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6159 | 0.0381 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6000 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2690 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
