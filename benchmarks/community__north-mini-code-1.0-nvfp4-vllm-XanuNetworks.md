# @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks benchmark results

Generated UTC: 2026-08-18T23:25:13.756859+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks |
| Model | XanuNetworks/North-Mini-Code-1.0-NVFP4 |
| Served model name | north-mini-code-nvfp4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__north-mini-code-1.0-nvfp4-vllm-XanuNetworks/20260818-224713 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/north-mini-code-1.0-nvfp4-vllm-XanuNetworks --cleanup |
| Total duration | 2280 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| kv_cache_dtype | fp8 |
| served_model_name | north-mini-code-nvfp4 |
| tool_call_parser | cohere_command4 |
| reasoning_parser | cohere_command4 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 372 | 0.126 | 16.4 | 2947.6 | 61.18 | 4.31 |
| 1024 | 1140 | 0.134 | 16.6 | 8532.4 | 60.47 | 4.37 |
| 4096 | 4211 | 0.444 | 17.2 | 9492.5 | 58.45 | 4.82 |
| 16384 | 16500 | 2.072 | 17.8 | 7961.4 | 56.29 | 6.62 |
| 65536 | 65652 | 12.803 | 20.7 | 5128.0 | 48.58 | 18.07 |
| 259267 | 259383 | 120.616 | 32.0 | 2150.5 | 31.39 | 128.77 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.129 | 0.129 | 59.67 | 57.9 | 4.42 |
| 2 | 2 | 0 | 0.220 | 0.263 | 53.35 | 101.9 | 5.03 |
| 4 | 4 | 0 | 0.371 | 0.421 | 42.40 | 160.4 | 6.39 |
| 8 | 8 | 0 | 0.584 | 0.765 | 31.73 | 236.6 | 8.66 |
| 16 | 16 | 0 | 0.929 | 1.460 | 23.31 | 340.9 | 12.02 |
| 32 | 32 | 0 | 1.628 | 2.832 | 17.82 | 502.6 | 16.30 |
| 64 | 64 | 0 | 3.075 | 5.792 | 12.49 | 669.1 | 24.49 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7754 | 0.0168 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8923 | 0.0085 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.8931 | 0.0085 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5401 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5768 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5100 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6400 | 0.0482 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6100 | 0.0218 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| north-mini-code-nvfp4@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9600 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2720 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| humaneval | ERROR | Coding: write Python functions that pass unit tests | HTTP 400 from inference server: 2 validation errors:
  {'type': 'string_type', 'loc': ('body', 'stop', 'str'), 'msg': 'Input should be a valid string', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint']}
  {'type': 'too_long', 'loc': ('body', 'stop', 'list[str]'), 'msg': 'List should have at most 4 items after validation, not 5', 'input': ['\nclass', '\ndef', '\n#', '\nif', '\nprint'], 'ctx': | lm-eval-humaneval.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
