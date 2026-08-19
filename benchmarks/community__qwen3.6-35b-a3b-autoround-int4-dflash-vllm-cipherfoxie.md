# @community/qwen3.6-35b-a3b-autoround-int4-dflash-vllm-cipherfoxie benchmark results

Generated UTC: 2026-08-19T01:52:31.941263+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @community/qwen3.6-35b-a3b-autoround-int4-dflash-vllm-cipherfoxie |
| Model | Intel/Qwen3.6-35B-A3B-int4-mixed-AutoRound |
| Served model name | qwen3.6-35b |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/community__qwen3.6-35b-a3b-autoround-int4-dflash-vllm-cipherfoxie/20260819-011301 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @community/qwen3.6-35b-a3b-autoround-int4-dflash-vllm-cipherfoxie --cleanup |
| Total duration | 2371 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| served_model_name | qwen3.6-35b |
| gpu_memory_utilization | 0.5 |
| dtype | auto |
| kv_cache_dtype | auto |
| max_model_len | 262144 |
| max_num_batched_tokens | 32768 |
| max_num_seqs | 4 |
| attention_backend | flash_attn |
| load_format | fastsafetensors |
| quantization | gptq |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| performance_mode | throughput |
| optimization_level | 3 |
| extra_flags | --language-model-only |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-35B-A3B-DFlash","num_speculative_tokens":3} |
| default_chat_template_kwargs | {"enable_thinking":false} |
| override_generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.121 | 18.1 | 2259.6 | 55.54 | 4.73 |
| 1024 | 1043 | 0.211 | 19.1 | 4947.7 | 52.52 | 5.08 |
| 4096 | 4117 | 0.696 | 18.0 | 5913.0 | 55.89 | 5.28 |
| 16384 | 16405 | 2.682 | 27.3 | 6117.5 | 36.84 | 9.63 |
| 65536 | 65556 | 14.079 | 38.9 | 4656.3 | 25.78 | 24.01 |
| 259267 | 259283 | 109.125 | 78.3 | 2376.0 | 12.83 | 129.08 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 4 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.203 | 0.203 | 72.16 | 68.3 | 3.75 |
| 2 | 2 | 0 | 0.370 | 0.412 | 58.23 | 82.0 | 6.25 |
| 4 | 4 | 0 | 0.726 | 0.727 | 39.08 | 138.8 | 7.38 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8509 | 0.0143 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.4056 | 0.0135 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.4526 | 0.0137 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5461 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5580 | 0.0145 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5700 | 0.0498 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7140 | 0.0202 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| qwen3.6-35b@bfcl_v4 | 0.8686 |  |
| acc | 0.8686 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.8000 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.8800 | 100 |
| LIVE | 0.7800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2660 | 175 |

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
- Concurrency levels [8, 16, 32, 64] exceed the recipe's declared max concurrency (4); skipped.
