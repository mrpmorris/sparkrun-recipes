# aeon-7__ornith-1.0-35b-uncensored-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-17T03:12:12.773981+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/aeon-7__ornith-1.0-35b-uncensored-nvfp4-dflash-vllm.yaml |
| Model | AEON-7/Ornith-1.0-35B-AEON-Ultimate-Uncensored-NVFP4 |
| Served model name | AEON-7/Ornith-1.0-35B-AEON-Ultimate-Uncensored-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__ornith-1.0-35b-uncensored-nvfp4-dflash-vllm.yaml/20260717-022413 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe aeon-7__ornith-1.0-35b-uncensored-nvfp4-dflash-vllm --cleanup |
| Total duration | 2880 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | AEON-7/Ornith-1.0-35B-AEON-Ultimate-Uncensored-NVFP4 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.6 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 16384 |
| quantization | compressed-tensors |
| attention_backend | flash_attn |
| mamba_cache_dtype | float32 |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-35B-A3B-DFlash","revision":"42d3b34d588423cdae7ba8f53a8cf7789346a719","num_speculative_tokens":6} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 269 | 0.138 | 8.1 | 1953.2 | 123.20 | 2.22 |
| 1024 | 1039 | 0.249 | 11.4 | 4172.3 | 88.04 | 3.16 |
| 4096 | 4111 | 0.777 | 13.1 | 5290.5 | 76.68 | 4.12 |
| 16384 | 16398 | 3.020 | 15.2 | 5429.4 | 66.26 | 6.88 |
| 65536 | 65551 | 15.125 | 25.4 | 4334.0 | 39.56 | 21.60 |
| 259267 | 259283 | 113.661 | 73.5 | 2281.2 | 13.65 | 132.42 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.245 | 0.245 | 93.67 | 86.0 | 2.98 |
| 2 | 2 | 0 | 0.397 | 0.446 | 66.92 | 115.5 | 4.43 |
| 4 | 4 | 0 | 0.825 | 0.826 | 52.26 | 173.9 | 5.89 |
| 8 | 8 | 0 | 1.507 | 1.510 | 43.63 | 268.4 | 7.63 |
| 16 | 16 | 0 | 3.020 | 3.024 | 30.46 | 337.7 | 12.13 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8421 | 0.0139 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0455 | 0.0057 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0607 | 0.0066 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5427 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5623 | 0.0145 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5183 | 0.0391 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6100 | 0.0218 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Ornith-1.0-35B-AEON-Ultimate-Uncensored-NVFP4@bfcl_v4 | 0.8800 |  |
| acc | 0.8800 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8000 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
