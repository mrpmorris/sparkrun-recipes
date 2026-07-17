# aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-17T06:48:06.260137+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml |
| Model | AEON-7/Qwen3.6-35B-A3B-heretic-NVFP4 |
| Served model name | Qwen/Qwen3.6-35B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml/20260717-053027 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/recipes/aeon-7__qwen3.6-35b-a3b-heretic-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 4659 s |

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
| 256 | 274 | 0.151 | 8.6 | 1813.7 | 116.47 | 2.35 |
| 1024 | 1040 | 0.237 | 10.1 | 4394.9 | 99.20 | 2.82 |
| 4096 | 4111 | 0.697 | 11.7 | 5901.2 | 85.90 | 3.68 |
| 16384 | 16398 | 2.640 | 16.3 | 6212.5 | 61.76 | 6.78 |
| 65536 | 65552 | 13.823 | 21.0 | 4742.2 | 47.81 | 19.18 |
| 259267 | 259284 | 109.371 | 79.2 | 2370.7 | 12.67 | 129.57 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.228 | 0.228 | 82.20 | 76.6 | 3.34 |
| 2 | 2 | 0 | 0.372 | 0.418 | 77.72 | 109.3 | 4.68 |
| 4 | 4 | 0 | 0.778 | 0.780 | 59.52 | 184.8 | 5.54 |
| 8 | 8 | 0 | 1.334 | 1.336 | 43.97 | 254.3 | 8.05 |
| 16 | 16 | 0 | 2.594 | 2.597 | 30.12 | 324.4 | 12.63 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8281 | 0.0153 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.1001 | 0.0083 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1365 | 0.0095 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5205 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5324 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5800 | 0.0496 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7700 | 0.0423 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6159 | 0.0381 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5940 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B@bfcl_v4 | 0.8914 |  |
| acc | 0.8914 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
