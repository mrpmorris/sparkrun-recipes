# miaai__deepseek-v4.1-flash-exl3-2.9bpw-dspark-k3-2x-vllm.yaml benchmark results

Generated UTC: 2026-09-17T03:53:52.668061+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/miaai__deepseek-v4.1-flash-exl3-2.9bpw-dspark-k3-2x-vllm.yaml |
| Model | Mia-AiLab/DeepSeek-V4.1-Flash-EXL3-2.9bpw |
| Served model name | DeepSeek-v4.1-Flash-EXL3 |
| Runtime | vllm |
| Container | ghcr.io/miaai-lab/deepseek-v4.1-flash-exl3-2x-dgx-sparks:2.9bpw |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 7.0.0-1019-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/miaai__deepseek-v4.1-flash-exl3-2.9bpw-dspark-k3-2x-vllm.yaml/20260916-215846 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe miaai__deepseek-v4.1-flash-exl3-2.9bpw-dspark-k3-2x-vllm.yaml |
| Total duration | 21306 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| served_model_name | DeepSeek-v4.1-Flash-EXL3 |
| revision | 64ba41b6c916a587db06eae2e19b7845f7be6e6b |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| distributed_executor_backend | mp |
| quantization | exl3 |
| max_model_len | 800000 |
| max_num_seqs | 2 |
| max_num_batched_tokens | 1024 |
| long_prefill_token_threshold | 768 |
| gpu_memory_utilization | 0.88 |
| kv_cache_memory_bytes | 2684354560 |
| block_size | 64 |
| speculative_config | {"method":"dspark","num_speculative_tokens":3} |
| engram_dir | /home/mrpmorris/dsv41-engram |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 287 | 0.626 | 50.6 | 458.4 | 19.85 | 13.52 |
| 1024 | 1055 | 1.581 | 36.8 | 667.4 | 27.32 | 10.95 |
| 4096 | 4127 | 5.389 | 52.5 | 765.8 | 19.11 | 18.78 |
| 16384 | 16415 | 20.201 | 55.7 | 812.6 | 18.03 | 34.40 |
| 65536 | 65567 | 81.358 | 61.7 | 805.9 | 16.28 | 97.09 |
| 260000 | 260031 | 348.035 | 56.0 | 747.1 | 17.92 | 362.32 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 2 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.553 | 1.553 | 15.42 | 14.1 | 18.15 |
| 2 | 2 | 0 | 2.354 | 3.068 | 15.74 | 24.2 | 21.19 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8368 | 0.0148 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3230 | 0.0129 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9454 | 0.0063 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5742 | 0.0144 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6015 | 0.0143 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7300 | 0.0446 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7500 | 0.0339 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8280 | 0.0169 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-v4.1-Flash-EXL3@bfcl_v4 | 0.7069 |  |
| acc | 0.7069 | 406 |
| irrelevance | 0.9200 | 25 |
| live_irrelevance | 0.8000 | 25 |
| live_multiple | 0.6800 | 25 |
| live_parallel | 0.8125 | 16 |
| live_parallel_multiple | 0.6250 | 24 |
| live_relevance | 1.0000 | 16 |
| live_simple | 0.9600 | 25 |
| multi_turn_base | 0.6800 | 25 |
| multi_turn_long_context | 0.6400 | 25 |
| multi_turn_miss_func | 0.3200 | 25 |
| multi_turn_miss_param | 0.3600 | 25 |
| multiple | 0.8400 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_java | 0.5200 | 25 |
| simple_javascript | 0.2400 | 25 |
| simple_python | 0.9200 | 25 |
| MULTI_TURN | 0.5000 | 100 |
| NON_LIVE | 0.8100 | 150 |
| LIVE | 0.7667 | 90 |
| HALLUCINATION | 0.8600 | 50 |
| OVERALL | 0.7151 | 390 |
| OVERALL_RAW | 0.3937 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Generative tasks (gsm8k) auto-fell back to /v1/chat/completions: this recipe serves a reasoning model (--reasoning-parser), whose base-style few-shot prompts emit EOS as the first token over /v1/completions (empty generations). Chat applies the template (<|im_start|>assistant<think>) so only message.content is graded and thinking is excluded.
- Code tasks (mbpp) auto-fell back to /v1/chat/completions with thinking disabled (chat_template_kwargs enable_thinking=False): completions emit empty/think-tagged generations that break prompt+generation execution, while no-think chat yields raw executable code.
- Top prompt rung capped at 260000 tokens (max length 800000 minus 256 output tokens and 8000 tokenizer-skew margin).
- Concurrency levels [4, 8, 16, 32, 64] exceed the recipe's declared max concurrency (2); skipped.
