# @eugr/glm-5.3-flash benchmark results

Generated UTC: 2026-09-20T01:13:04.539580+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/glm-5.3-flash |
| Model | local-inference-lab/GLM-5.3-Flash-NVFP4-Spark |
| Served model name | local-inference-lab/GLM-5.3-Flash-NVFP4-Spark |
| Runtime | vllm-distributed |
| Container | vllm-node-b12x |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 7.0.0-1019-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260919-195844 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe @eugr/glm-5.3-flash |
| Total duration | 18861 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| decode_context_parallel | 1 |
| block_size | 256 |
| max_model_len | 500000 |
| max_num_seqs | 4 |
| max_num_batched_tokens | 4096 |
| num_speculative_tokens | 5 |
| kv_cache_memory_bytes | 8G |
| gpu_memory_utilization | 0.87 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 269 | 0.659 | 44.6 | 408.3 | 22.52 | 12.03 |
| 1024 | 1037 | 0.833 | 33.9 | 1245.1 | 29.64 | 9.47 |
| 4096 | 4109 | 2.151 | 40.8 | 1910.0 | 24.58 | 12.57 |
| 16384 | 16398 | 7.621 | 32.9 | 2151.6 | 30.54 | 16.00 |
| 65536 | 65550 | 30.327 | 29.4 | 2161.5 | 34.18 | 37.82 |
| 260000 | 260013 | 138.269 | 28.6 | 1880.5 | 35.14 | 145.55 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 4 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.841 | 0.841 | 32.52 | 29.4 | 8.71 |
| 2 | 2 | 0 | 1.290 | 1.686 | 19.26 | 33.6 | 15.22 |
| 4 | 4 | 0 | 2.497 | 2.499 | 14.57 | 44.9 | 22.80 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8737 | 0.0134 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9719 | 0.0045 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9712 | 0.0046 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6758 | 0.0137 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.7108 | 0.0133 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5700 | 0.0498 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7400 | 0.0441 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7927 | 0.0318 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.8560 | 0.0157 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| GLM-5.3-Flash-NVFP4-Spark@bfcl_v4 | 0.6798 |  |
| acc | 0.6798 | 406 |
| irrelevance | 0.7200 | 25 |
| live_irrelevance | 0.7600 | 25 |
| live_multiple | 0.5600 | 25 |
| live_parallel | 0.8125 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 0.9600 | 25 |
| multi_turn_base | 0.6400 | 25 |
| multi_turn_long_context | 0.5200 | 25 |
| multi_turn_miss_func | 0.4400 | 25 |
| multi_turn_miss_param | 0.4400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4000 | 25 |
| simple_javascript | 0.2400 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.5100 | 100 |
| NON_LIVE | 0.8033 | 150 |
| LIVE | 0.7555 | 90 |
| HALLUCINATION | 0.7400 | 50 |
| OVERALL | 0.6855 | 390 |
| OVERALL_RAW | 0.3829 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Generative tasks (gsm8k) auto-fell back to /v1/chat/completions: this recipe serves a reasoning model (--reasoning-parser), whose base-style few-shot prompts emit EOS as the first token over /v1/completions (empty generations). Chat applies the template (<|im_start|>assistant<think>) so only message.content is graded and thinking is excluded.
- Code tasks (mbpp) auto-fell back to /v1/chat/completions with thinking suppressed (chat_template_kwargs reasoning_effort=low): completions emit empty/think-tagged generations that break prompt+generation execution, while no-think chat yields raw executable code.
- Top prompt rung capped at 260000 tokens (max length 500000 minus 256 output tokens and 5000 tokenizer-skew margin).
- Concurrency levels [8, 16, 32, 64] exceed the recipe's declared max concurrency (4); skipped.
