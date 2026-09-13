# @eugr/qwen3.8-flash-next-nvfp4-cluster benchmark results

Generated UTC: 2026-09-12T22:56:17.257424+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/qwen3.8-flash-next-nvfp4-cluster |
| Model | local-inference-lab/Qwen3.8-Flash-Next-NVFP4 |
| Served model name | local-inference-lab/Qwen3.8-Flash-Next-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node-b12x |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1032-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3.8-flash-next-nvfp4-cluster/20260912-200258 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe @eugr/qwen3.8-flash-next-nvfp4-cluster |
| Total duration | 10399 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| block_size | 16 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 4096 |
| num_speculative_tokens | 4 |
| gpu_memory_utilization | 0.7 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 315 | 0.366 | 18.4 | 861.1 | 54.50 | 5.06 |
| 1024 | 1080 | 0.489 | 22.0 | 2208.9 | 45.55 | 6.11 |
| 4096 | 4156 | 1.503 | 35.1 | 2764.7 | 28.57 | 10.46 |
| 16384 | 16443 | 5.508 | 21.3 | 2985.2 | 47.10 | 10.94 |
| 65536 | 65595 | 23.400 | 14.6 | 2803.2 | 68.74 | 27.12 |
| 259267 | 259324 | 121.982 | 17.3 | 2125.9 | 58.04 | 126.39 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.549 | 0.549 | 46.85 | 42.6 | 6.01 |
| 2 | 2 | 0 | 0.722 | 0.940 | 27.78 | 40.0 | 12.80 |
| 4 | 4 | 0 | 1.724 | 1.725 | 34.41 | 84.0 | 12.19 |
| 8 | 8 | 0 | 3.095 | 3.147 | 27.45 | 130.2 | 15.73 |
| 16 | 16 | 0 | 5.407 | 6.267 | 15.75 | 159.8 | 25.63 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8123 | 0.0157 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.9052 | 0.0081 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9060 | 0.0080 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6092 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6237 | 0.0142 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6200 | 0.0488 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7800 | 0.0416 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7988 | 0.0314 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6460 | 0.0214 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-Flash-Next-NVFP4@bfcl_v4 | 0.6970 |  |
| acc | 0.6970 | 406 |
| irrelevance | 1.0000 | 25 |
| live_irrelevance | 0.8400 | 25 |
| live_multiple | 0.6400 | 25 |
| live_parallel | 0.7500 | 16 |
| live_parallel_multiple | 0.5833 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 1.0000 | 25 |
| multi_turn_base | 0.6400 | 25 |
| multi_turn_long_context | 0.6000 | 25 |
| multi_turn_miss_func | 0.3600 | 25 |
| multi_turn_miss_param | 0.3200 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4400 | 25 |
| simple_javascript | 0.2000 | 25 |
| simple_python | 0.9600 | 25 |
| MULTI_TURN | 0.4800 | 100 |
| NON_LIVE | 0.8233 | 150 |
| LIVE | 0.7444 | 90 |
| HALLUCINATION | 0.9200 | 50 |
| OVERALL | 0.7003 | 390 |
| OVERALL_RAW | 0.3928 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Generative tasks (gsm8k) auto-fell back to /v1/chat/completions: this recipe serves a reasoning model (--reasoning-parser), whose base-style few-shot prompts emit EOS as the first token over /v1/completions (empty generations). Chat applies the template (<|im_start|>assistant<think>) so only message.content is graded and thinking is excluded.
- Code tasks (mbpp) auto-fell back to /v1/chat/completions with thinking disabled (chat_template_kwargs enable_thinking=False): completions emit empty/think-tagged generations that break prompt+generation execution, while no-think chat yields raw executable code.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
