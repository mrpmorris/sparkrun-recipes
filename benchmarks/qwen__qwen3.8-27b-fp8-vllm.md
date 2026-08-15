# qwen__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-15T01:41:42.951701+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/qwen__qwen3.8-27b-fp8-vllm.yaml |
| Model | Qwen/Qwen3.8-27B-FP8 |
| Served model name | Qwen/Qwen3.8-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/qwen__qwen3.8-27b-fp8-vllm.yaml/20260814-220505 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe qwen__qwen3.8-27b-fp8-vllm.yaml |
| Total duration | 12997 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 262144 |
| max_num_batched_tokens | 32768 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 313 | 0.241 | 125.8 | 1297.7 | 7.98 | 32.32 |
| 1024 | 1082 | 0.784 | 126.1 | 1379.8 | 7.96 | 32.93 |
| 4096 | 4156 | 2.270 | 126.6 | 1830.9 | 7.93 | 34.56 |
| 16384 | 16442 | 18.835 | 128.6 | 873.0 | 7.81 | 51.62 |
| 65536 | 65595 | 86.381 | 136.3 | 759.4 | 7.37 | 121.13 |
| 259267 | 259325 | 517.375 | 165.5 | 501.2 | 6.07 | 559.58 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.809 | 0.809 | 7.92 | 7.7 | 33.14 |
| 2 | 2 | 0 | 1.362 | 1.548 | 7.89 | 15.1 | 33.87 |
| 4 | 4 | 0 | 5.658 | 5.659 | 7.60 | 26.4 | 38.76 |
| 8 | 8 | 0 | 17.999 | 18.003 | 7.25 | 39.1 | 52.39 |
| 16 | 16 | 0 | 56.900 | 56.905 | 6.61 | 43.3 | 94.57 |
| 32 | 32 | 0 | 114.874 | 114.883 | 5.63 | 51.3 | 159.68 |
| 64 | 64 | 0 | 73.229 | 73.256 | 3.84 | 123.8 | 132.34 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8526 | 0.0143 |  |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5691 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5913 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4480 | 0.0223 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.8914 |  |
| acc | 0.8914 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2690 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| gsm8k | ERROR | Grade-school math word problems (multi-step reasoning) | killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| humaneval | ERROR | Coding: write Python functions that pass unit tests | HTTP 400 from inference server: 2 validation errors:
  {'type': 'string_type', 'loc': ('body', 'stop', 'str'), 'msg': 'Input should be a valid string', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint']}
  {'type': 'too_long', 'loc': ('body', 'stop', 'list[str]'), 'msg': 'List should have at most 4 items after validation, not 5', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint'], 'ctx': | lm-eval-humaneval.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
