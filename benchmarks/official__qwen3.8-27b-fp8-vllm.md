# official__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-17T19:50:54.564705+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/official__qwen3.8-27b-fp8-vllm.yaml |
| Model | Qwen/Qwen3.8-27B-FP8 |
| Served model name | Qwen/Qwen3.8-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-vllm.yaml/20260817-161212 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe official__qwen3.8-27b-fp8-vllm.yaml |
| Total duration | 13122 s |

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
| 256 | 316 | 0.241 | 126.8 | 1312.1 | 7.92 | 32.57 |
| 1024 | 1081 | 0.782 | 127.0 | 1383.2 | 7.90 | 33.18 |
| 4096 | 4157 | 2.553 | 127.6 | 1628.3 | 7.87 | 35.10 |
| 16384 | 16442 | 19.194 | 129.5 | 856.6 | 7.75 | 52.23 |
| 65536 | 65596 | 87.357 | 137.6 | 750.9 | 7.30 | 122.45 |
| 259267 | 259326 | 527.024 | 167.5 | 492.1 | 5.99 | 569.73 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.802 | 0.802 | 7.85 | 7.7 | 33.40 |
| 2 | 2 | 0 | 1.350 | 1.534 | 7.83 | 15.0 | 34.09 |
| 4 | 4 | 0 | 5.719 | 5.721 | 7.55 | 26.2 | 39.05 |
| 8 | 8 | 0 | 9.271 | 9.272 | 7.29 | 46.7 | 43.90 |
| 16 | 16 | 0 | 57.516 | 57.519 | 6.56 | 42.9 | 95.49 |
| 32 | 32 | 0 | 101.035 | 114.944 | 4.54 | 51.1 | 160.33 |
| 64 | 64 | 0 | 201.572 | 231.622 | 2.57 | 56.0 | 292.62 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8649 | 0.0139 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6611 | 0.0130 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6929 | 0.0127 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5725 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5896 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4480 | 0.0223 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.9600 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.8400 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2730 | 175 |

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
