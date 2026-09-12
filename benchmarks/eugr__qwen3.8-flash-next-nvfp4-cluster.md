# @eugr/qwen3.8-flash-next-nvfp4-cluster benchmark results

Generated UTC: 2026-09-12T14:00:25.600759+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__qwen3.8-flash-next-nvfp4-cluster/20260912-105812 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/qwen3.8-flash-next-nvfp4-cluster --force --continue-on-fail |
| Total duration | 10933 s |

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
| 256 | 313 | 0.361 | 18.1 | 866.9 | 55.49 | 4.97 |
| 1024 | 1083 | 0.572 | 19.4 | 1893.5 | 51.71 | 5.52 |
| 4096 | 4154 | 1.387 | 20.5 | 2994.4 | 48.98 | 6.61 |
| 16384 | 16441 | 5.220 | 19.2 | 3149.4 | 52.37 | 10.11 |
| 65536 | 65594 | 22.078 | 21.0 | 2971.0 | 47.74 | 27.44 |
| 259267 | 259325 | 117.229 | 18.1 | 2212.1 | 55.57 | 121.84 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.520 | 0.520 | 42.24 | 38.9 | 6.58 |
| 2 | 2 | 0 | 0.690 | 0.900 | 41.22 | 64.7 | 7.91 |
| 4 | 4 | 0 | 1.575 | 1.576 | 36.21 | 101.9 | 10.05 |
| 8 | 8 | 0 | 2.904 | 2.957 | 29.38 | 136.5 | 15.00 |
| 16 | 16 | 0 | 5.103 | 5.932 | 18.86 | 169.6 | 24.16 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8386 | 0.0153 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8992 | 0.0083 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.9030 | 0.0082 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6084 | 0.0143 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6314 | 0.0141 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.6300 | 0.0485 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.8000 | 0.0402 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8537 | 0.0277 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0840 | 0.0124 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.8-Flash-Next-NVFP4@bfcl_v4 | 0.6823 |  |
| acc | 0.6823 | 406 |
| irrelevance | 1.0000 | 25 |
| live_irrelevance | 0.8400 | 25 |
| live_multiple | 0.6800 | 25 |
| live_parallel | 0.6250 | 16 |
| live_parallel_multiple | 0.5833 | 24 |
| live_relevance | 0.8750 | 16 |
| live_simple | 0.9200 | 25 |
| multi_turn_base | 0.5600 | 25 |
| multi_turn_long_context | 0.6000 | 25 |
| multi_turn_miss_func | 0.3600 | 25 |
| multi_turn_miss_param | 0.2800 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_java | 0.4800 | 25 |
| simple_javascript | 0.2400 | 25 |
| simple_python | 0.9200 | 25 |
| MULTI_TURN | 0.4500 | 100 |
| NON_LIVE | 0.8067 | 150 |
| LIVE | 0.7111 | 90 |
| HALLUCINATION | 0.9200 | 50 |
| OVERALL | 0.6849 | 390 |
| OVERALL_RAW | 0.3788 | 390 |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Generative tasks (gsm8k) auto-fell back to /v1/chat/completions: this recipe serves a reasoning model (--reasoning-parser), whose base-style few-shot prompts emit EOS as the first token over /v1/completions (empty generations). Chat applies the template (<|im_start|>assistant<think>) so only message.content is graded and thinking is excluded. Code tasks stay on completions.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
