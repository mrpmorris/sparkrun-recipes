# @official/qwen3.8-27b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-08-19T15:48:30.155130+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.8-27b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.8-27B-FP8 |
| Served model name | Qwen/Qwen3.8-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-mtp-vllm/20260819-133453 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.8-27b-fp8-mtp-vllm |
| Total duration | 8016 s |

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
| 256 | 313 | 0.292 | 56.5 | 1073.5 | 17.75 | 14.71 |
| 1024 | 1084 | 0.753 | 58.5 | 1438.6 | 17.15 | 15.68 |
| 4096 | 4151 | 4.701 | 55.4 | 882.9 | 18.12 | 18.83 |
| 16384 | 16442 | 20.636 | 73.8 | 796.8 | 13.61 | 39.44 |
| 65536 | 65594 | 93.186 | 71.0 | 703.9 | 14.15 | 111.28 |
| 259267 | 259322 | 550.207 | 79.3 | 471.3 | 12.65 | 570.44 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.610 | 0.610 | 17.47 | 16.8 | 15.27 |
| 2 | 2 | 0 | 1.287 | 1.445 | 16.96 | 29.7 | 17.27 |
| 4 | 4 | 0 | 2.684 | 2.685 | 16.88 | 47.9 | 21.36 |
| 8 | 8 | 0 | 10.022 | 10.025 | 15.55 | 67.9 | 30.17 |
| 16 | 16 | 0 | 55.762 | 55.767 | 13.39 | 52.8 | 77.52 |
| 32 | 32 | 0 | 100.591 | 111.253 | 7.21 | 57.2 | 143.18 |
| 64 | 64 | 0 | 126.521 | 155.751 | 3.52 | 80.2 | 204.23 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.2719 | 0.0182 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6694 | 0.0130 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6975 | 0.0127 | 1319 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7927 | 0.0318 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4240 | 0.0221 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.9143 |  |
| acc | 0.9143 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.9000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2800 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| arc_challenge | ERROR | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |
| hellaswag | ERROR | Commonsense sentence completion | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-hellaswag.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
