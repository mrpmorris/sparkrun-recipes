# nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml benchmark results

Generated UTC: 2026-08-15T16:07:55.982705+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml/20260815-135830 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml --cleanup |
| Total duration | 7766 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | nvidia/Qwen3.6-27B-NVFP4 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 16384 |
| quantization | modelopt |
| load_format | fastsafetensors |
| attention_backend | flashinfer |
| moe_backend | marlin |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"mtp","num_speculative_tokens":3,"moe_backend":"triton"} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 272 | 0.365 | 29.1 | 745.3 | 34.52 | 7.78 |
| 1024 | 1041 | 1.037 | 34.2 | 1003.5 | 29.34 | 9.76 |
| 4096 | 4110 | 3.815 | 36.5 | 1077.5 | 27.49 | 13.13 |
| 16384 | 16403 | 15.076 | 37.8 | 1088.0 | 26.54 | 24.72 |
| 65536 | 65550 | 71.511 | 34.7 | 916.6 | 28.95 | 80.35 |
| 259267 | 259284 | 470.363 | 48.5 | 551.2 | 20.69 | 482.74 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.997 | 0.997 | 29.97 | 26.8 | 9.54 |
| 2 | 2 | 0 | 1.811 | 1.988 | 29.39 | 47.1 | 10.88 |
| 4 | 4 | 0 | 3.823 | 3.824 | 29.71 | 78.7 | 13.01 |
| 8 | 8 | 0 | 7.402 | 7.404 | 22.80 | 108.2 | 18.93 |
| 16 | 16 | 0 | 14.558 | 14.565 | 19.34 | 144.2 | 28.40 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7632 | 0.0176 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5792 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.5982 | 0.0135 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.3345 | 0.0138 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3507 | 0.0139 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3400 | 0.0476 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3700 | 0.0485 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4100 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 0.8800 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2750 | 175 |

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
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
