# @community/qwen3.6-35b-a3b-fp8-vllm-povedaaqui benchmark results

Generated UTC: 2026-07-16T23:59:37.766971+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/qwen3.6-35b-a3b-fp8-vllm-povedaaqui |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | qwen36 |
| Runtime | vllm |
| Container | vllm/vllm-openai:cu130-nightly |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__qwen3.6-35b-a3b-fp8-vllm-povedaaqui/20260716-230125 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/qwen3.6-35b-a3b-fp8-vllm-povedaaqui --cleanup |
| Total duration | 3492 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| served_model_name | qwen36 |
| gpu_memory_utilization | 0.85 |
| dtype | auto |
| kv_cache_dtype | fp8 |
| max_model_len | 262144 |
| max_num_batched_tokens | 32768 |
| max_num_seqs | 8 |
| attention_backend | flashinfer |
| load_format | instanttensor |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| performance_mode | throughput |
| speculative_config | {"method":"mtp","num_speculative_tokens":3} |
| default_chat_template_kwargs | {"preserve_thinking":true} |
| override_generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 275 | 0.240 | 13.1 | 1144.7 | 76.36 | 3.59 |
| 1024 | 1038 | 0.328 | 16.2 | 3167.4 | 62.00 | 4.46 |
| 4096 | 4114 | 1.131 | 15.4 | 3637.3 | 65.39 | 5.05 |
| 16384 | 16400 | 3.048 | 15.8 | 5380.9 | 63.63 | 7.07 |
| 65536 | 65549 | 16.694 | 16.8 | 3926.5 | 59.66 | 20.98 |
| 259267 | 259283 | 143.503 | 28.9 | 1806.8 | 34.73 | 150.87 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.324 | 0.324 | 63.08 | 58.4 | 4.38 |
| 2 | 2 | 0 | 0.571 | 0.597 | 54.39 | 96.9 | 5.28 |
| 4 | 4 | 0 | 0.920 | 0.921 | 42.81 | 141.3 | 7.25 |
| 8 | 8 | 0 | 2.014 | 2.016 | 31.27 | 193.2 | 10.60 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8351 | 0.0150 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3700 | 0.0133 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3836 | 0.0134 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4684 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4846 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5061 | 0.0392 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6000 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| qwen36@bfcl_v4 | 0.9029 |  |
| acc | 0.9029 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2750 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
