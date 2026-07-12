# @eugr/qwen3-coder-next-int4-autoround benchmark results

Generated UTC: 2026-07-12T04:46:13.388867+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/qwen3-coder-next-int4-autoround |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3-coder-next-int4-autoround/20260712-034131 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3-coder-next-int4-autoround --cleanup |
| Total duration | 3882 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 268 | 0.165 | 14.2 | 1622.7 | 70.78 | 3.78 |
| 1024 | 1038 | 0.333 | 14.3 | 3121.2 | 70.18 | 3.98 |
| 4096 | 4104 | 1.050 | 14.6 | 3909.3 | 68.64 | 4.78 |
| 16384 | 16397 | 4.078 | 15.9 | 4021.3 | 63.26 | 8.12 |
| 65536 | 65547 | 20.359 | 21.2 | 3219.6 | 47.33 | 25.77 |
| 259267 | 259278 | 150.384 | 41.1 | 1724.1 | 24.41 | 160.87 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.350 | 0.350 | 69.69 | 63.6 | 4.02 |
| 2 | 2 | 0 | 0.537 | 0.603 | 59.71 | 106.0 | 4.83 |
| 4 | 4 | 0 | 0.940 | 1.063 | 43.88 | 150.9 | 6.79 |
| 8 | 8 | 0 | 1.699 | 2.100 | 29.95 | 201.0 | 10.19 |
| 16 | 16 | 0 | 2.703 | 4.062 | 20.29 | 264.3 | 15.50 |
| 32 | 32 | 0 | 4.877 | 8.436 | 13.14 | 327.8 | 24.99 |
| 64 | 64 | 0 | 9.230 | 17.795 | 8.50 | 395.3 | 41.44 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0149 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9121 | 0.0078 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9181 | 0.0076 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6041 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6348 | 0.0141 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6768 | 0.0366 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7620 | 0.0191 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8629 |  |
| acc | 0.8629 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.8000 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2610 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
