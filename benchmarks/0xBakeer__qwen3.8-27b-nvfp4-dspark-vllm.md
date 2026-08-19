# 0xBakeer__qwen3.8-27b-nvfp4-dspark-vllm.yaml benchmark results

Generated UTC: 2026-08-19T03:47:27.751904+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/0xBakeer__qwen3.8-27b-nvfp4-dspark-vllm.yaml |
| Model | unsloth/Qwen3.8-27B-NVFP4 |
| Served model name | qwen3.8-27b |
| Runtime | vllm |
| Container | vllm/vllm-openai:v0.27.1-aarch64 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/0xBakeer__qwen3.8-27b-nvfp4-dspark-vllm.yaml/20260819-021142 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/recipes/0xBakeer__qwen3.8-27b-nvfp4-dspark-vllm.yaml --cleanup |
| Total duration | 5746 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | qwen3.8-27b |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.85 |
| max_model_len | 262144 |
| max_num_batched_tokens | 16384 |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_xml |
| speculative_config | {"method":"dspark","model":"Doopeworld/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7,"draft_sample_method":"probabilistic"} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 316 | 0.347 | 59.1 | 911.0 | 16.98 | 15.42 |
| 1024 | 1082 | 0.559 | 53.7 | 1936.0 | 18.71 | 14.24 |
| 4096 | 4154 | 2.141 | 56.0 | 1940.3 | 17.94 | 16.41 |
| 16384 | 16443 | 12.465 | 51.9 | 1319.1 | 19.34 | 25.70 |
| 65536 | 65592 | 60.595 | 66.3 | 1082.5 | 15.15 | 77.49 |
| 259267 | 259327 | 421.096 | 96.1 | 615.8 | 10.44 | 445.61 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.570 | 0.570 | 17.81 | 17.1 | 14.94 |
| 2 | 2 | 0 | 0.989 | 1.047 | 13.89 | 26.0 | 19.66 |
| 4 | 4 | 0 | 2.134 | 2.135 | 12.96 | 44.6 | 22.98 |
| 8 | 8 | 0 | 5.887 | 5.889 | 11.36 | 62.6 | 32.70 |
| 16 | 16 | 0 | 15.597 | 15.603 | 8.22 | 79.8 | 51.31 |
| 32 | 32 | 0 | 24.339 | 25.118 | 5.01 | 101.1 | 81.05 |
| 64 | 64 | 0 | 36.040 | 109.285 | 3.89 | 104.8 | 156.30 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7895 | 0.0164 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.7528 | 0.0119 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.7695 | 0.0116 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5503 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5751 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5900 | 0.0494 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4420 | 0.0222 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| qwen3.8-27b@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8800 | 25 |
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
