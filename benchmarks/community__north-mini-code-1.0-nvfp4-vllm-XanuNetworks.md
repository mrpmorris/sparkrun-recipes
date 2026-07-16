# @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks benchmark results

Generated UTC: 2026-07-16T20:22:44.055685+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks |
| Model | XanuNetworks/North-Mini-Code-1.0-NVFP4 |
| Served model name | north-mini-code-nvfp4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__north-mini-code-1.0-nvfp4-vllm-XanuNetworks/20260716-194310 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks --cleanup |
| Total duration | 2374 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| kv_cache_dtype | fp8 |
| served_model_name | north-mini-code-nvfp4 |
| tool_call_parser | cohere_command4 |
| reasoning_parser | cohere_command4 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 372 | 0.123 | 16.5 | 3019.3 | 60.66 | 4.34 |
| 1024 | 1140 | 0.134 | 16.8 | 8495.5 | 59.66 | 4.42 |
| 4096 | 4212 | 0.458 | 17.4 | 9204.2 | 57.63 | 4.90 |
| 16384 | 16499 | 2.087 | 18.2 | 7907.2 | 55.08 | 6.73 |
| 65536 | 65652 | 12.753 | 21.0 | 5148.1 | 47.91 | 18.10 |
| 259267 | 259383 |  |  |  |  | 126.33 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.131 | 0.131 | 59.32 | 57.6 | 4.45 |
| 2 | 2 | 0 | 0.211 | 0.252 | 53.61 | 102.5 | 4.99 |
| 4 | 4 | 0 | 0.379 | 0.427 | 42.42 | 160.2 | 6.39 |
| 8 | 8 | 0 | 0.601 | 0.775 | 34.78 | 257.3 | 7.96 |
| 16 | 16 | 0 | 0.963 | 1.491 | 28.73 | 411.4 | 9.96 |
| 32 | 32 | 0 | 1.658 | 2.897 | 20.57 | 569.3 | 14.39 |
| 64 | 64 | 0 | 3.116 | 5.849 | 14.82 | 774.0 | 21.17 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7789 | 0.0162 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8817 | 0.0089 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.8840 | 0.0088 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5384 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5717 | 0.0145 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5000 | 0.0503 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6500 | 0.0479 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5793 | 0.0387 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5860 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| north-mini-code-nvfp4@bfcl_v4 | 0.8800 |  |
| acc | 0.8800 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 1.0000 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
