# @official/qwen3.8-27b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-08-17T14:24:06.120153+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-mtp-vllm/20260817-121210 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.8-27b-fp8-mtp-vllm |
| Total duration | 7915 s |

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
| 256 | 313 | 0.288 | 74.6 | 1088.3 | 13.45 | 19.32 |
| 1024 | 1081 | 1.006 | 63.5 | 1074.8 | 15.81 | 17.20 |
| 4096 | 4156 | 2.411 | 58.8 | 1723.9 | 17.08 | 17.40 |
| 16384 | 16442 | 20.097 | 46.7 | 818.1 | 21.50 | 32.00 |
| 65536 | 65593 | 89.702 | 83.0 | 731.2 | 12.10 | 110.86 |
| 259267 | 259321 | 531.944 | 81.8 | 487.5 | 12.28 | 552.79 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.617 | 0.617 | 12.99 | 12.6 | 20.33 |
| 2 | 2 | 0 | 1.062 | 1.176 | 15.11 | 25.0 | 20.48 |
| 4 | 4 | 0 | 5.938 | 5.940 | 15.55 | 39.7 | 25.83 |
| 8 | 8 | 0 | 9.496 | 9.500 | 14.76 | 68.6 | 29.83 |
| 16 | 16 | 0 | 19.033 | 19.039 | 12.60 | 92.9 | 44.07 |
| 32 | 32 | 0 | 74.222 | 78.077 | 8.21 | 73.8 | 110.97 |
| 64 | 64 | 0 | 67.466 | 78.626 | 4.48 | 129.3 | 126.67 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.2895 | 0.0187 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6634 | 0.0130 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6922 | 0.0127 | 1319 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4340 | 0.0222 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2740 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| arc_challenge | ERROR | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |
| hellaswag | ERROR | Commonsense sentence completion | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-hellaswag.log |
| humaneval | ERROR | Coding: write Python functions that pass unit tests | HTTP 400 from inference server: 2 validation errors:
  {'type': 'string_type', 'loc': ('body', 'stop', 'str'), 'msg': 'Input should be a valid string', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint']}
  {'type': 'too_long', 'loc': ('body', 'stop', 'list[str]'), 'msg': 'List should have at most 4 items after validation, not 5', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint'], 'ctx': | lm-eval-humaneval.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
