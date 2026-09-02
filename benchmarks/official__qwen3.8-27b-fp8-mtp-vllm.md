# @official/qwen3.8-27b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-09-02T15:15:44.465645+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.8-27b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.8-27B-FP8 |
| Served model name | Qwen/Qwen3.8-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1031-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-mtp-vllm/20260902-100402 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.8-27b-fp8-mtp-vllm |
| Total duration | 18702 s |

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
| speculative_config | {"method": "mtp", "num_speculative_tokens": 3} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 316 | 0.289 | 68.3 | 1092.0 | 14.71 | 17.70 |
| 1024 | 1083 | 0.593 | 57.7 | 1827.4 | 17.39 | 15.31 |
| 4096 | 4155 | 2.247 | 69.4 | 1848.8 | 14.47 | 19.94 |
| 16384 | 16444 | 18.303 | 61.5 | 898.4 | 16.33 | 33.98 |
| 65536 | 65597 | 87.948 | 65.8 | 745.9 | 15.25 | 104.73 |
| 259267 | 259326 | 538.279 | 74.3 | 481.8 | 13.51 | 557.23 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.605 | 0.605 | 17.75 | 17.0 | 15.03 |
| 2 | 2 | 0 | 1.059 | 1.176 | 13.76 | 25.7 | 19.92 |
| 4 | 4 | 0 | 2.634 | 2.635 | 16.77 | 53.1 | 19.28 |
| 8 | 8 | 0 | 9.300 | 9.304 | 14.94 | 68.5 | 29.91 |
| 16 | 16 | 0 | 19.017 | 19.023 | 12.71 | 91.8 | 44.60 |
| 32 | 32 | 0 | 34.022 | 37.908 | 8.40 | 115.3 | 71.03 |
| 64 | 64 | 0 | 66.725 | 78.251 | 4.42 | 129.7 | 126.37 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.2877 | 0.0180 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6748 | 0.0129 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6998 | 0.0126 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7988 | 0.0314 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4000 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.7069 |  |
| acc | 0.7069 | 406 |
| irrelevance | 1.0000 | 25 |
| live_irrelevance | 0.7600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_parallel | 0.9375 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 1.0000 | 25 |
| multi_turn_base | 0.6400 | 25 |
| multi_turn_long_context | 0.5600 | 25 |
| multi_turn_miss_func | 0.3200 | 25 |
| multi_turn_miss_param | 0.3600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_java | 0.4800 | 25 |
| simple_javascript | 0.2400 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4700 | 100 |
| NON_LIVE | 0.8000 | 150 |
| LIVE | 0.8333 | 90 |
| HALLUCINATION | 0.8800 | 50 |
| OVERALL | 0.7140 | 390 |
| OVERALL_RAW | 0.3923 | 390 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| arc_challenge | ERROR | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |
| hellaswag | ERROR | Commonsense sentence completion | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-hellaswag.log |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
