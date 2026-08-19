# @community/north-mini-code-1.0-fp8-vllm-XanuNetworks benchmark results

Generated UTC: 2026-08-18T22:47:13.144357+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/north-mini-code-1.0-fp8-vllm-XanuNetworks |
| Model | CohereLabs/North-Mini-Code-1.0-fp8 |
| Served model name | north-mini-code |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__north-mini-code-1.0-fp8-vllm-XanuNetworks/20260818-214618 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/north-mini-code-1.0-fp8-vllm-XanuNetworks --cleanup |
| Total duration | 3655 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| kv_cache_dtype | fp8 |
| served_model_name | north-mini-code |
| tool_call_parser | cohere_command4 |
| reasoning_parser | cohere_command4 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 372 | 0.226 | 27.3 | 1643.9 | 36.83 | 7.18 |
| 1024 | 1140 | 0.217 | 27.5 | 5257.8 | 36.50 | 7.23 |
| 4096 | 4212 | 0.744 | 27.9 | 5661.1 | 36.03 | 7.85 |
| 16384 | 16500 | 3.127 | 28.7 | 5276.1 | 35.03 | 10.44 |
| 65536 | 65652 | 16.888 | 31.6 | 3887.5 | 31.80 | 24.94 |
| 259267 | 259383 | 136.440 | 43.1 | 1901.1 | 23.31 | 147.42 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.211 | 0.211 | 36.19 | 35.1 | 7.28 |
| 2 | 2 | 0 | 0.323 | 0.413 | 32.48 | 62.3 | 8.22 |
| 4 | 4 | 0 | 0.632 | 0.731 | 23.92 | 90.7 | 11.28 |
| 8 | 8 | 0 | 0.986 | 1.347 | 20.54 | 152.1 | 13.46 |
| 16 | 16 | 0 | 1.601 | 2.583 | 15.31 | 221.6 | 18.48 |
| 32 | 32 | 0 | 2.831 | 4.986 | 11.19 | 312.8 | 26.19 |
| 64 | 63 | 1 | 5.195 | 10.064 | 8.20 | 424.5 | 37.99 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7912 | 0.0159 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9037 | 0.0081 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9067 | 0.0080 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5529 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5819 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4900 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6300 | 0.0485 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6240 | 0.0217 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| north-mini-code@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.8000 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2680 | 175 |

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
- [ERROR] Concurrency 64: 1 request(s) failed.
