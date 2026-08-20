# official__qwen3.8-27b-fp8-vllm.yaml benchmark results

Generated UTC: 2026-08-20T22:46:53.770723+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/official__qwen3.8-27b-fp8-vllm.yaml/20260820-170732 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe official__qwen3.8-27b-fp8-vllm.yaml |
| Total duration | 20362 s |

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
| 256 | 312 | 0.233 | 121.1 | 1337.7 | 8.29 | 31.11 |
| 1024 | 1082 | 0.529 | 121.3 | 2046.6 | 8.28 | 31.45 |
| 4096 | 4156 | 2.251 | 121.7 | 1845.9 | 8.25 | 33.30 |
| 16384 | 16442 | 18.638 | 123.6 | 882.2 | 8.12 | 50.17 |
| 65536 | 65595 | 85.890 | 131.1 | 763.7 | 7.66 | 119.31 |
| 259267 | 259326 | 522.482 | 159.8 | 496.3 | 6.28 | 563.22 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.537 | 0.537 | 8.22 | 8.1 | 31.67 |
| 2 | 2 | 0 | 0.920 | 1.044 | 8.23 | 16.0 | 32.08 |
| 4 | 4 | 0 | 2.423 | 2.424 | 7.99 | 29.9 | 34.24 |
| 8 | 8 | 0 | 9.150 | 9.153 | 7.61 | 48.4 | 42.30 |
| 16 | 16 | 0 | 18.639 | 18.643 | 6.93 | 74.3 | 55.14 |
| 32 | 32 | 0 | 32.658 | 37.156 | 5.33 | 101.2 | 80.93 |
| 64 | 64 | 0 | 64.452 | 74.286 | 3.44 | 123.7 | 132.48 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8579 | 0.0140 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6520 | 0.0131 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.7127 | 0.0125 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5683 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5922 | 0.0144 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7500 | 0.0435 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0000 | 0.0000 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0260 | 0.0071 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-27B-FP8@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2670 | 175 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- Generative tasks (gsm8k, humaneval, mbpp) were scored over /v1/chat/completions with the model's chat template applied and a 2048-token generation budget; only message.content is graded, so a --reasoning-parser server's thinking is excluded. Multiple-choice tasks stay on /v1/completions (loglikelihood). Pass --eval-completions-only for the old raw-text protocol, whose scores are NOT comparable to these.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
