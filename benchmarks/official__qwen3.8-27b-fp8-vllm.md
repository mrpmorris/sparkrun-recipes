# official__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-22T00:19:21.667682+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/official__qwen3.8-27b-fp8-vllm.yaml |
| Model | Qwen/Qwen3.8-27B-FP8 |
| Served model name | Qwen/Qwen3.8-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-vllm.yaml/20260821-204528 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe official__qwen3.8-27b-fp8-vllm |
| Total duration | 12833 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_batched_tokens | 16384 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| mm_encoder_tp_mode | data |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 315 | 0.241 | 120.2 | 1309.0 | 8.35 | 30.89 |
| 1024 | 1079 | 0.538 | 120.3 | 2007.4 | 8.34 | 31.22 |
| 4096 | 4158 | 2.270 | 120.9 | 1831.6 | 8.31 | 33.09 |
| 16384 | 16445 | 18.043 | 122.9 | 911.5 | 8.17 | 49.37 |
| 65536 | 65593 | 83.574 | 130.3 | 784.9 | 7.70 | 116.80 |
| 259267 | 259323 | 513.110 | 158.8 | 505.4 | 6.32 | 553.60 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.556 | 0.556 | 8.31 | 8.2 | 31.36 |
| 2 | 2 | 0 | 0.926 | 1.051 | 8.31 | 16.1 | 31.81 |
| 4 | 4 | 0 | 2.446 | 2.447 | 8.05 | 30.1 | 34.02 |
| 8 | 8 | 0 | 8.865 | 8.866 | 7.68 | 49.1 | 41.74 |
| 16 | 16 | 0 | 18.124 | 18.129 | 6.97 | 75.3 | 54.37 |
| 32 | 32 | 0 | 31.518 | 36.001 | 5.37 | 103.2 | 79.41 |
| 64 | 64 | 0 | 62.186 | 71.907 | 3.46 | 126.1 | 129.92 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8579 | 0.0139 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6785 | 0.0129 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.7036 | 0.0126 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5691 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5922 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7683 | 0.0330 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4400 | 0.0222 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.8800 |  |
| acc | 0.8800 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8000 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.8800 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
