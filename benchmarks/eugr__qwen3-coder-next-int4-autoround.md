# @eugr/qwen3-coder-next-int4-autoround benchmark results

Generated UTC: 2026-07-13T21:05:10.176737+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3-coder-next-int4-autoround/20260713-201503 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3-coder-next-int4-autoround --cleanup |
| Total duration | 3007 s |

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
| 256 | 268 | 0.167 | 14.1 | 1607.9 | 71.12 | 3.77 |
| 1024 | 1038 | 0.338 | 14.3 | 3071.9 | 70.30 | 3.98 |
| 4096 | 4109 | 1.053 | 14.6 | 3901.6 | 68.55 | 4.79 |
| 16384 | 16396 | 4.108 | 15.9 | 3991.3 | 63.09 | 8.17 |
| 65536 | 65545 | 20.540 | 21.2 | 3191.1 | 47.25 | 25.96 |
| 259267 | 259282 | 151.227 | 41.3 | 1714.5 | 24.32 | 161.75 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.352 | 0.352 | 70.03 | 63.9 | 4.01 |
| 2 | 2 | 0 | 0.540 | 0.607 | 59.95 | 106.3 | 4.82 |
| 4 | 4 | 0 | 0.953 | 1.079 | 46.97 | 159.6 | 6.42 |
| 8 | 8 | 0 | 1.707 | 2.095 | 30.70 | 205.2 | 9.98 |
| 16 | 16 | 0 | 2.709 | 4.079 | 20.47 | 265.9 | 15.40 |
| 32 | 32 | 0 | 4.868 | 8.427 | 13.21 | 329.3 | 24.88 |
| 64 | 64 | 0 | 9.265 | 17.836 | 8.56 | 397.4 | 41.23 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8421 | 0.0148 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9181 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9204 | 0.0075 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6041 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6399 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7073 | 0.0356 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7680 | 0.0189 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 0.8000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2670 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
