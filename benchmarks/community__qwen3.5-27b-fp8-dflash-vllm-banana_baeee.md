# @community/qwen3.5-27b-fp8-dflash-vllm-banana_baeee benchmark results

Generated UTC: 2026-08-19T01:13:00.751849+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/qwen3.5-27b-fp8-dflash-vllm-banana_baeee |
| Model | Qwen/Qwen3.5-27B-FP8 |
| Served model name | Qwen/Qwen3.5-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly@sha256:7758869bb489d93a4658d009554f598f18bbef0d07bbc38df49bf586a1874279 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__qwen3.5-27b-fp8-dflash-vllm-banana_baeee/20260818-232514 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/qwen3.5-27b-fp8-dflash-vllm-banana_baeee --cleanup |
| Total duration | 6467 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.94 |
| max_model_len | 131072 |
| max_num_batched_tokens | 16384 |
| max_num_seqs | 10 |
| speculative_config | {"method":"dflash","num_speculative_tokens":15,"model":"z-lab/Qwen3.5-27B-DFlash"} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 270 | 0.432 | 44.3 | 624.9 | 22.65 | 11.73 |
| 1024 | 1040 | 0.843 | 39.6 | 1233.0 | 25.33 | 10.95 |
| 4096 | 4112 | 2.908 | 66.4 | 1413.9 | 15.13 | 19.83 |
| 16384 | 16400 | 20.180 | 169.2 | 812.7 | 5.93 | 63.33 |
| 65536 | 65552 | 91.387 | 239.0 | 717.3 | 4.20 | 152.33 |
| 129506 | 129522 | 203.402 | 300.4 | 636.8 | 3.34 | 279.99 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 10 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.052 | 1.052 | 21.79 | 20.0 | 12.80 |
| 2 | 2 | 0 | 3.635 | 3.635 | 21.79 | 33.1 | 15.48 |
| 4 | 4 | 0 | 6.409 | 6.410 | 19.81 | 46.7 | 21.91 |
| 8 | 8 | 0 | 19.336 | 19.340 | 14.10 | 51.4 | 39.82 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8702 | 0.0135 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5815 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6171 | 0.0134 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5964 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6109 | 0.0142 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6100 | 0.0490 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7600 | 0.0429 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6220 | 0.0380 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5000 | 0.0224 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.5-27B-FP8@bfcl_v4 | 0.1429 |  |
| acc | 0.1429 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.0000 | 25 |
| live_simple | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| NON_LIVE | 0.0000 | 100 |
| LIVE | 0.0000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.1000 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 129506 tokens (max length 131072 minus 256 output tokens and 1310 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (10); skipped.
