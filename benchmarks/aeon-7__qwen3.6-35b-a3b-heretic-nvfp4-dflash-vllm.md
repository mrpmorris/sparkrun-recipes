# aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-08T13:47:20.097345+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml/20260708-125143 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 3336 s |

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
| 256 | 269 | 0.140 | 12.8 | 1916.9 | 78.56 | 3.40 |
| 1024 | 1039 | 0.243 | 13.2 | 4282.9 | 75.80 | 3.62 |
| 4096 | 4113 | 0.722 | 13.4 | 5693.9 | 74.74 | 4.15 |
| 16384 | 16401 | 2.710 | 17.4 | 6051.8 | 57.59 | 7.16 |
| 65536 | 65552 | 14.312 | 24.6 | 4580.2 | 40.80 | 20.59 |
| 259267 | 259281 | 115.982 | 66.1 | 2235.5 | 15.18 | 132.84 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8439 | 0.0150 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0978 | 0.0082 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1281 | 0.0092 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5239 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5230 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6000 | 0.0492 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6220 | 0.0380 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5900 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2730 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
