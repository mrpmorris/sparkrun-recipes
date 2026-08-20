# @eugr/qwen3-coder-next-int4-autoround benchmark results

Generated UTC: 2026-08-20T15:31:02.331682+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/qwen3-coder-next-int4-autoround |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3-coder-next-int4-autoround/20260820-143612 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3-coder-next-int4-autoround --cleanup |
| Total duration | 3290 s |

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
| 256 | 270 | 0.152 | 13.5 | 1775.9 | 74.34 | 3.60 |
| 1024 | 1035 | 0.329 | 13.6 | 3141.3 | 73.94 | 3.79 |
| 4096 | 4111 | 1.022 | 13.9 | 4023.6 | 72.21 | 4.57 |
| 16384 | 16397 | 3.981 | 15.0 | 4118.3 | 66.90 | 7.81 |
| 65536 | 65550 | 19.919 | 20.1 | 3290.8 | 50.05 | 25.03 |
| 259267 | 259279 | 146.755 | 40.0 | 1766.7 | 25.11 | 156.95 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.355 | 0.355 | 73.09 | 66.4 | 3.86 |
| 2 | 2 | 0 | 0.531 | 0.600 | 59.78 | 106.2 | 4.82 |
| 4 | 4 | 0 | 0.923 | 1.046 | 44.24 | 152.4 | 6.72 |
| 8 | 8 | 0 | 1.650 | 2.039 | 28.21 | 192.1 | 10.66 |
| 16 | 16 | 0 | 2.621 | 3.963 | 17.77 | 238.1 | 17.20 |
| 32 | 32 | 0 | 4.713 | 8.211 | 11.15 | 289.5 | 28.30 |
| 64 | 64 | 0 | 8.994 | 17.529 | 6.90 | 339.7 | 48.24 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8386 | 0.0150 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9166 | 0.0076 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9204 | 0.0075 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6075 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6391 | 0.0140 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7200 | 0.0451 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6524 | 0.0373 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7540 | 0.0193 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.8914 |  |
| acc | 0.8914 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 0.8000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2710 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
