# qwen__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-14T21:51:56.942974+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/qwen__qwen3.8-27b-fp8-vllm.yaml/20260814-182554 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe qwen__qwen3.8-27b-fp8-vllm.yaml |
| Total duration | 12362 s |

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
| 256 | 316 | 0.246 | 126.8 | 1283.9 | 7.92 | 32.58 |
| 1024 | 1083 | 0.796 | 127.1 | 1360.7 | 7.90 | 33.20 |
| 4096 | 4153 | 2.503 | 127.5 | 1659.1 | 7.87 | 35.02 |
| 16384 | 16441 | 18.928 | 129.6 | 868.6 | 7.74 | 51.98 |
| 65536 | 65592 | 84.120 | 137.4 | 779.7 | 7.31 | 119.15 |
| 259267 | 259326 | 514.765 | 166.7 | 503.8 | 6.02 | 557.26 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.829 | 0.829 | 7.86 | 7.7 | 33.38 |
| 2 | 2 | 0 | 1.378 | 1.567 | 7.84 | 15.0 | 34.09 |
| 4 | 4 | 0 | 5.700 | 5.702 | 7.56 | 26.3 | 39.00 |
| 8 | 8 | 0 | 18.404 | 18.408 | 7.21 | 38.6 | 53.02 |
| 16 | 16 | 0 | 19.087 | 19.093 | 6.65 | 71.7 | 57.09 |
| 32 | 32 | 0 | 36.685 | 36.696 | 5.62 | 100.0 | 81.95 |
| 64 | 64 | 0 | 230.797 | 230.820 | 3.30 | 56.5 | 290.01 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8544 | 0.0142 |  |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5674 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5870 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7600 | 0.0429 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4000 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.9029 |  |
| acc | 0.9029 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8400 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.8800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2770 | 175 |

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
