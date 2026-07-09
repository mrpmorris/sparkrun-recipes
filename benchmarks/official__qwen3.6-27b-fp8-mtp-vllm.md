# @official/qwen3.6-27b-fp8-mtp-vllm benchmark results

Generated UTC: 2026-07-09T15:22:04.672380+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @official/qwen3.6-27b-fp8-mtp-vllm |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.6-27b-fp8-mtp-vllm/20260709-130131 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @official/qwen3.6-27b-fp8-mtp-vllm --cleanup |
| Total duration | 8433 s |

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
| speculative_config | {"method": "mtp", "num_speculative_tokens": 2} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 273 | 0.424 | 58.0 | 644.4 | 17.30 | 15.22 |
| 1024 | 1041 | 0.970 | 56.2 | 1072.9 | 17.87 | 15.30 |
| 4096 | 4113 | 4.954 | 59.5 | 830.2 | 16.86 | 20.14 |
| 16384 | 16401 | 20.313 | 61.0 | 807.4 | 16.46 | 35.86 |
| 65536 | 65549 | 183.180 | 61.1 | 357.8 | 16.42 | 198.77 |
| 259267 | 259282 | 859.804 | 74.4 | 301.6 | 13.49 | 878.78 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5883 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6042 | 0.0135 | 1319 |
| hellaswag | Commonsense sentence completion | acc,none | 0.2500 | 0.0435 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.2900 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7744 | 0.0327 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3980 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2720 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |
| arc_challenge | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
