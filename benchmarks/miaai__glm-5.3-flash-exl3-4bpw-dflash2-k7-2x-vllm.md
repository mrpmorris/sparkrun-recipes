# miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm.yaml benchmark results

Generated UTC: 2026-09-07T01:25:15.382839+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm.yaml |
| Model | Mia-AiLab/GLM-5.3-Flash-EXL3-TR3-4bpw |
| Served model name | GLM-5.3-Flash-EXL3 |
| Runtime | vllm |
| Container | ghcr.io/miaai-lab/glm-5.3-flash-2x-dgx-sparks@sha256:9bb1557a4234fce63d59599e44d10747eabd742beb337eebf9e7070be8a0fd58 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1032-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm.yaml/20260906-183948 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm |
| Total duration | 24327 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| served_model_name | GLM-5.3-Flash-EXL3 |
| revision | 25a44fdbf16862a46b7cc9921142c6c81350af2f |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| distributed_executor_backend | mp |
| gpu_memory_utilization | 0.85 |
| max_model_len | 1000000 |
| max_num_seqs | 4 |
| max_num_batched_tokens | 7168 |
| quantization | exl3 |
| load_format | auto |
| kv_cache_dtype | fp8 |
| speculative_config | {"method":"dflash","model":"incoai/GLM-5.3-Flash-DFlash2","num_speculative_tokens":7,"kv_cache_dtype":"auto","draft_tensor_parallel_size":2,"draft_sample_method":"probabilistic","rejection_sample_method":"standard","revision":"bf582e4eacc1810f76656d1811693ff6c6737d2a"} |
| local_speculative_config | {"method":"dflash","model":"/cache/huggingface/hub/models--incoai--GLM-5.3-Flash-DFlash2/snapshots/bf582e4eacc1810f76656d1811693ff6c6737d2a","num_speculative_tokens":7,"kv_cache_dtype":"auto","draft_tensor_parallel_size":2,"draft_sample_method":"probabilistic","rejection_sample_method":"standard","revision":"bf582e4eacc1810f76656d1811693ff6c6737d2a"} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 268 | 0.774 | 39.3 | 346.5 | 25.57 | 10.78 |
| 1024 | 1039 | 1.480 | 40.8 | 701.8 | 24.63 | 11.88 |
| 4096 | 4110 | 3.778 | 39.5 | 1087.9 | 25.41 | 13.85 |
| 16384 | 16398 | 13.489 | 43.9 | 1215.7 | 22.86 | 24.68 |
| 65536 | 65550 | 52.544 | 42.7 | 1247.5 | 23.52 | 63.43 |
| 260000 | 260013 | 213.398 | 37.5 | 1218.4 | 26.79 | 222.95 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 4 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.321 | 1.321 | 21.15 | 19.1 | 13.43 |
| 2 | 2 | 0 | 7.905 | 13.838 | 22.72 | 20.2 | 25.33 |
| 4 | 4 | 0 | 13.654 | 13.655 | 19.26 | 34.1 | 29.99 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8930 | 0.0128 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9318 | 0.0069 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9318 | 0.0069 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6792 | 0.0136 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.7022 | 0.0134 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5500 | 0.0500 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7100 | 0.0456 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.6890 | 0.0363 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7840 | 0.0184 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| GLM-5.3-Flash-EXL3@bfcl_v4 | 0.6798 |  |
| acc | 0.6798 | 406 |
| irrelevance | 0.8400 | 25 |
| live_irrelevance | 0.7600 | 25 |
| live_multiple | 0.6000 | 25 |
| live_parallel | 0.7500 | 16 |
| live_parallel_multiple | 0.7500 | 24 |
| live_relevance | 0.7500 | 16 |
| live_simple | 0.9600 | 25 |
| multi_turn_base | 0.6000 | 25 |
| multi_turn_long_context | 0.4800 | 25 |
| multi_turn_miss_func | 0.3600 | 25 |
| multi_turn_miss_param | 0.4000 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4800 | 25 |
| simple_javascript | 0.2400 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4600 | 100 |
| NON_LIVE | 0.8100 | 150 |
| LIVE | 0.7667 | 90 |
| HALLUCINATION | 0.8000 | 50 |
| OVERALL | 0.6829 | 390 |
| OVERALL_RAW | 0.3757 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Top prompt rung capped at 260000 tokens (max length 1000000 minus 256 output tokens and 10000 tokenizer-skew margin).
- Concurrency levels [8, 16, 32, 64] exceed the recipe's declared max concurrency (4); skipped.
