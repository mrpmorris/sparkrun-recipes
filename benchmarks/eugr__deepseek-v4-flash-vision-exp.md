# @eugr/deepseek-v4-flash-vision-exp benchmark results

Generated UTC: 2026-09-15T22:28:00.568452+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/deepseek-v4-flash-vision-exp |
| Model | deepseek-ai/DeepSeek-V4-Flash-Vision-Exp |
| Served model name | deepseek-ai/DeepSeek-V4-Flash-Vision-Exp |
| Runtime | vllm-distributed |
| Container | vllm-node-b12x |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 7.0.0-1019-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__deepseek-v4-flash-vision-exp/20260915-171301 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/deepseek-v4-flash-vision-exp |
| Total duration | 18899 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| gpu_memory_utilization | 0.85 |
| max_model_len | auto |
| block_size | 256 |
| max_num_seqs | 8 |
| max_num_batched_tokens | 8192 |
| max_cudagraph_capture_size | 48 |
| num_speculative_tokens | 6 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 340 | 0.320 | 27.8 | 1062.9 | 36.13 | 7.41 |
| 1024 | 1109 | 0.688 | 31.3 | 1611.3 | 32.03 | 8.68 |
| 4096 | 4180 | 1.804 | 15.1 | 2317.6 | 66.39 | 5.66 |
| 16384 | 16468 | 7.344 | 25.8 | 2242.2 | 38.90 | 13.92 |
| 65536 | 65620 | 29.970 | 23.6 | 2189.5 | 42.55 | 35.99 |
| 260000 | 260085 | 142.725 | 29.0 | 1822.3 | 34.66 | 150.11 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 8 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.600 | 0.600 | 36.38 | 33.5 | 7.64 |
| 2 | 2 | 0 | 0.955 | 1.243 | 30.24 | 44.8 | 11.42 |
| 4 | 4 | 0 | 1.622 | 2.096 | 25.48 | 82.8 | 12.37 |
| 8 | 8 | 0 | 3.770 | 3.772 | 12.23 | 72.1 | 28.42 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8737 | 0.0133 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3980 | 0.0135 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.8666 | 0.0094 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6067 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6527 | 0.0139 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5400 | 0.0501 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7600 | 0.0429 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0915 | 0.0226 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3980 | 0.0219 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-Vision-Exp@bfcl_v4 | 0.6946 |  |
| acc | 0.6946 | 406 |
| irrelevance | 0.9600 | 25 |
| live_irrelevance | 0.8000 | 25 |
| live_multiple | 0.7200 | 25 |
| live_parallel | 0.8125 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 0.9200 | 25 |
| multi_turn_base | 0.7200 | 25 |
| multi_turn_long_context | 0.5200 | 25 |
| multi_turn_miss_func | 0.2400 | 25 |
| multi_turn_miss_param | 0.3600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4000 | 25 |
| simple_javascript | 0.2000 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4600 | 100 |
| NON_LIVE | 0.8200 | 150 |
| LIVE | 0.7889 | 90 |
| HALLUCINATION | 0.8800 | 50 |
| OVERALL | 0.6996 | 390 |
| OVERALL_RAW | 0.3869 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Generative tasks (gsm8k) auto-fell back to /v1/chat/completions: this recipe serves a reasoning model (--reasoning-parser), whose base-style few-shot prompts emit EOS as the first token over /v1/completions (empty generations). Chat applies the template (<|im_start|>assistant<think>) so only message.content is graded and thinking is excluded.
- Code tasks (mbpp) auto-fell back to /v1/chat/completions with thinking disabled (chat_template_kwargs enable_thinking=False): completions emit empty/think-tagged generations that break prompt+generation execution, while no-think chat yields raw executable code.
- Top prompt rung capped at 260000 tokens (max length 1042176 minus 256 output tokens and 10421 tokenizer-skew margin).
- Concurrency levels [16, 32, 64] exceed the recipe's declared max concurrency (8); skipped.
