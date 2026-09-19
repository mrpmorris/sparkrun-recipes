# @eugr/glm-5.3-flash benchmark results

Generated UTC: 2026-09-19T09:31:18.143037+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --force --recipe @eugr/glm-5.3-flash |
| Total duration | 64039 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| pipeline_parallel | 1 |
| decode_context_parallel | 1 |
| block_size | 256 |
| max_model_len | 1048576 |
| max_num_seqs | 4 |
| max_num_batched_tokens | 4096 |
| num_speculative_tokens | 5 |
| kv_cache_memory_bytes | 8G |
| gpu_memory_utilization | 0.87 |

## Speed vs prompt size (single request)

_Speed benchmark failed: no prompt-size rung completed (see the run's speed-*.json and serve log)._

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

_Concurrency sweep produced no data (see the run's speed-*.json and serve log)._

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| GLM-5.3-Flash-NVFP4-Spark@bfcl_v4 | 0.3793 |  |
| acc | 0.3793 | 406 |
| irrelevance | 0.8400 | 25 |
| live_irrelevance | 0.8000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_parallel | 0.7500 | 16 |
| live_parallel_multiple | 0.6250 | 24 |
| live_relevance | 0.8750 | 16 |
| live_simple | 0.9200 | 25 |
| multi_turn_base | 0.6800 | 25 |
| multi_turn_long_context | 0.6000 | 25 |
| multi_turn_miss_func | 0.0800 | 25 |
| multi_turn_miss_param | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_java | 0.0000 | 25 |
| simple_javascript | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| MULTI_TURN | 0.3400 | 100 |
| NON_LIVE | 0.0000 | 150 |
| LIVE | 0.7222 | 90 |
| HALLUCINATION | 0.8200 | 50 |
| OVERALL | 0.3982 | 390 |
| OVERALL_RAW | 0.2562 | 390 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | STARTUP | General knowledge across 57 academic subjects | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |
| gsm8k | STARTUP | Grade-school math word problems (multi-step reasoning) | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |
| arc_challenge | STARTUP | Hard science exam questions (reasoning) | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |
| hellaswag | STARTUP | Commonsense sentence completion | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |
| humaneval | STARTUP | Coding: write Python functions that pass unit tests | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |
| mbpp | STARTUP | Coding: basic Python programming problems, graded by unit tests | skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log) |  |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- Recipe max_model_len=1048576 but the server reports 262144; using the server value.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- before loglikelihood probe: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- echo+logprobs probe skipped: server was down [STARTUP] (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log); multiple-choice tasks were attempted anyway.
- before mmlu: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before gsm8k: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before arc_challenge: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before hellaswag: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before humaneval: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before mbpp: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- before speed: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- [STARTUP] Speed benchmark skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log).
- before concurrency: server was down [HANG] and could not be restarted: sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log
- [STARTUP] Concurrency sweep skipped: server could not be started (sparkrun run failed (exit 1); see /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-5.3-flash/20260918-154358/sparkrun.log).
