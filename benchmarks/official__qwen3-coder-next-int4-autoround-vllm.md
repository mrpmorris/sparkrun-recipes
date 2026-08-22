# @official/qwen3-coder-next-int4-autoround-vllm benchmark results

Generated UTC: 2026-08-22T14:44:12.140388+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3-coder-next-int4-autoround-vllm |
| Model | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Served model name | Intel/Qwen3-Coder-Next-int4-AutoRound |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly-tf5:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3-coder-next-int4-autoround-vllm/20260822-141301 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3-coder-next-int4-autoround-vllm --skip-speed --skip-concurrency --skip-eval --bfcl-subsets all-local |
| Total duration | 1871 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| tool_call_parser | qwen3_coder |
| max_num_seqs | 128 |
| max_num_batched_tokens | 16384 |
| kv_cache_dtype | fp8 |
| optimization_level | 3 |
| performance_mode | throughput |
| mamba_cache_mode | align |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.168 | 13.8 | 1617.6 | 72.79 | 3.68 |
| 1024 | 1040 | 0.287 | 13.9 | 3629.7 | 72.07 | 3.84 |
| 4096 | 4107 | 0.924 | 14.0 | 4444.6 | 71.60 | 4.50 |
| 16384 | 16394 | 3.612 | 14.8 | 4538.2 | 68.05 | 7.37 |
| 65536 | 65548 | 19.851 | 17.4 | 3302.0 | 57.57 | 24.30 |
| 259267 | 259279 | 169.776 | 27.8 | 1527.2 | 36.13 | 176.86 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

_Skipped (--skip-concurrency)._

## Intelligence (lm-eval)

_Skipped (--skip-eval)._

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3-Coder-Next-int4-AutoRound@bfcl_v4 | 0.6576 |  |
| acc | 0.6576 | 406 |
| irrelevance | 1.0000 | 25 |
| live_irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_parallel | 0.6250 | 16 |
| live_parallel_multiple | 0.6250 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 0.8000 | 25 |
| multi_turn_base | 0.4800 | 25 |
| multi_turn_long_context | 0.3600 | 25 |
| multi_turn_miss_func | 0.1200 | 25 |
| multi_turn_miss_param | 0.2400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_java | 0.4800 | 25 |
| simple_javascript | 0.3200 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.3000 | 100 |
| NON_LIVE | 0.8267 | 150 |
| LIVE | 0.6889 | 90 |
| HALLUCINATION | 1.0000 | 50 |
| OVERALL | 0.3416 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Speed section reused from earlier run 20260822-123026 (--skip-speed).
