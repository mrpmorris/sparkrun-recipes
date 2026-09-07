# miaai__qwen3.8-flash-next-nvfp4-mtp3-2x-vllm.yaml benchmark results

Generated UTC: 2026-09-07T11:07:52.802012+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/miaai__qwen3.8-flash-next-nvfp4-mtp3-2x-vllm.yaml |
| Model | /srv/hf/q38-flash-next-nvfp4 |
| Served model name | qwen3.8-flash-next |
| Runtime | vllm |
| Container | vllm/vllm-openai:qwen38-flash-next |
| Base URL | http://127.0.0.1:8888/v1 |
| Host | Linux 6.17.0-1032-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/miaai__qwen3.8-flash-next-nvfp4-mtp3-2x-vllm.yaml/20260907-082250 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe miaai__qwen3.8-flash-next-nvfp4-mtp3-2x-vllm |
| Total duration | 9903 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8888 |
| served_model_name | qwen3.8-flash-next |
| tensor_parallel | 2 |
| gpu_memory_utilization | 0.835 |
| max_model_len | 262144 |
| max_num_seqs | 8 |
| max_num_batched_tokens | 8192 |
| kv_cache_dtype | fp8 |
| mm_encoder_tp_mode | data |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"mtp","num_speculative_tokens":3} |
| compilation_config | {"mode":0,"cudagraph_mode":"FULL_DECODE_ONLY"} |
| hf_overrides | {"text_config":{"ple_embedding_dtype":"float8_e4m3fn"}} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 316 | 0.324 | 27.2 | 975.3 | 36.86 | 7.27 |
| 1024 | 1082 | 0.471 | 30.5 | 2298.7 | 32.91 | 8.25 |
| 4096 | 4155 | 1.417 | 21.7 | 2932.1 | 46.24 | 6.95 |
| 16384 | 16444 | 5.074 | 23.5 | 3240.8 | 42.81 | 11.05 |
| 65536 | 65592 | 20.634 | 27.4 | 3178.9 | 36.66 | 27.62 |
| 259267 | 259325 | 97.127 | 28.4 | 2670.0 | 35.40 | 104.36 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.455 | 0.455 | 34.53 | 32.5 | 7.87 |
| 2 | 2 | 0 | 0.705 | 0.920 | 35.35 | 60.7 | 8.44 |
| 4 | 4 | 0 | 1.561 | 1.561 | 25.51 | 69.0 | 14.84 |
| 8 | 8 | 0 | 2.777 | 2.780 | 26.51 | 140.2 | 14.61 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8404 | 0.0148 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0045 | 0.0019 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0045 | 0.0019 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5990 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6075 | 0.0143 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6400 | 0.0482 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7800 | 0.0416 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8171 | 0.0303 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0560 | 0.0103 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| qwen3.8-flash-next@bfcl_v4 | 0.6552 |  |
| acc | 0.6552 | 406 |
| irrelevance | 0.9600 | 25 |
| live_irrelevance | 0.7200 | 25 |
| live_multiple | 0.6800 | 25 |
| live_parallel | 0.7500 | 16 |
| live_parallel_multiple | 0.5417 | 24 |
| live_relevance | 0.7500 | 16 |
| live_simple | 0.9600 | 25 |
| multi_turn_base | 0.6000 | 25 |
| multi_turn_long_context | 0.4400 | 25 |
| multi_turn_miss_func | 0.2800 | 25 |
| multi_turn_miss_param | 0.3200 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_java | 0.4000 | 25 |
| simple_javascript | 0.2000 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4100 | 100 |
| NON_LIVE | 0.7900 | 150 |
| LIVE | 0.7333 | 90 |
| HALLUCINATION | 0.8400 | 50 |
| OVERALL | 0.6589 | 390 |
| OVERALL_RAW | 0.3593 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
