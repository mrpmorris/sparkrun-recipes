# official__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-19T20:55:55.690668+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-vllm.yaml/20260819-171640 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe official__qwen3.8-27b-fp8-vllm.yaml |
| Total duration | 13155 s |

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
| 256 | 313 | 0.232 | 119.3 | 1346.5 | 8.42 | 30.64 |
| 1024 | 1079 | 0.792 | 119.5 | 1362.3 | 8.40 | 31.26 |
| 4096 | 4156 | 2.321 | 119.9 | 1790.8 | 8.37 | 32.90 |
| 16384 | 16442 | 19.754 | 121.9 | 832.3 | 8.24 | 50.83 |
| 65536 | 65594 | 90.882 | 130.9 | 721.7 | 7.67 | 124.25 |
| 259267 | 259324 | 538.623 | 158.4 | 481.5 | 6.34 | 579.02 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.807 | 0.807 | 8.37 | 8.2 | 31.39 |
| 2 | 2 | 0 | 1.387 | 1.574 | 8.39 | 16.0 | 31.97 |
| 4 | 4 | 0 | 5.476 | 5.477 | 8.07 | 27.9 | 36.67 |
| 8 | 8 | 0 | 17.686 | 17.688 | 7.69 | 40.9 | 50.12 |
| 16 | 16 | 0 | 54.162 | 54.168 | 6.98 | 45.6 | 89.88 |
| 32 | 32 | 0 | 61.019 | 74.019 | 4.79 | 69.9 | 117.16 |
| 64 | 64 | 0 | 155.283 | 182.072 | 2.73 | 68.3 | 239.78 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8526 | 0.0144 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6611 | 0.0130 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6929 | 0.0127 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5674 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5836 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7988 | 0.0314 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.4480 | 0.0223 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.9029 |  |
| acc | 0.9029 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7200 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9000 | 100 |
| LIVE | 0.8600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2760 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
