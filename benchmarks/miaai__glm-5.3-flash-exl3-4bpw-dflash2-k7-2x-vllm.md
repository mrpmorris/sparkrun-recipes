# miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm.yaml benchmark results

Generated UTC: 2026-09-06T13:27:57.652874+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm.yaml/20260906-100322 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe miaai__glm-5.3-flash-exl3-4bpw-dflash2-k7-2x-vllm |
| Total duration | 12276 s |

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
| gpu_memory_utilization | 0.87 |
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
| 256 | 270 | 0.908 | 39.9 | 297.5 | 25.17 | 11.08 |
| 1024 | 1038 | 1.358 | 38.8 | 764.4 | 25.86 | 11.26 |
| 4096 | 4109 | 3.840 | 34.8 | 1070.0 | 28.82 | 12.72 |
| 16384 | 16397 | 14.282 | 43.4 | 1148.1 | 23.14 | 25.34 |
| 65536 | 65550 | 52.384 | 42.1 | 1251.3 | 23.84 | 63.12 |
| 260000 | 260015 | 212.441 | 48.3 | 1223.9 | 20.77 | 224.77 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 4 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.335 | 1.335 | 20.87 | 18.8 | 13.60 |
| 2 | 2 | 0 | 7.198 | 12.496 | 23.98 | 21.4 | 23.95 |
| 4 | 4 | 0 | 11.206 | 11.207 | 19.75 | 33.0 | 31.00 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

2 task(s) completed, 4 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7378 | 0.0345 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7860 | 0.0184 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1). OVERALL is rescaled to cover only the categories that ran, so partial coverage does not depress it; OVERALL_RAW is BFCL's own full-suite aggregate, which scores every category that did not run as 0. Neither is comparable to published BFCL figures unless all 22 scoring categories ran.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| GLM-5.3-Flash-EXL3@bfcl_v4 | 0.3744 |  |
| acc | 0.3744 | 406 |
| irrelevance | 0.8800 | 25 |
| live_irrelevance | 0.8400 | 25 |
| live_multiple | 0.6400 | 25 |
| live_parallel | 0.7500 | 16 |
| live_parallel_multiple | 0.7083 | 24 |
| live_relevance | 0.8125 | 16 |
| live_simple | 0.8800 | 25 |
| multi_turn_base | 0.6400 | 25 |
| multi_turn_long_context | 0.5200 | 25 |
| multi_turn_miss_func | 0.0000 | 25 |
| multi_turn_miss_param | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_java | 0.0000 | 25 |
| simple_javascript | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| MULTI_TURN | 0.2900 | 100 |
| NON_LIVE | 0.0000 | 150 |
| LIVE | 0.7444 | 90 |
| HALLUCINATION | 0.8600 | 50 |
| OVERALL | 0.3924 | 390 |
| OVERALL_RAW | 0.2474 | 390 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

Code: `OOM` out-of-memory kill · `CRASH` fatal engine error in the serve log · `HANG` server alive but stopped generating · `STARTUP` server could not be (re)started · `UNSUPPORTED` server can't perform this eval · `ERROR` step failed with the server still healthy.

| Task | Code | Description | Reason | Log |
| --- | --- | --- | --- | --- |
| mmlu | UNSUPPORTED | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | STARTUP | Grade-school math word problems (multi-step reasoning) | skipped: server could not be started (model endpoint did not become ready in time) |  |
| arc_challenge | UNSUPPORTED | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | UNSUPPORTED | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (mmlu:10, hellaswag:100; MMLU's limit is per subtask across 57 subtasks); those scores are comparative samples, not full-benchmark numbers.
- BFCL ran 17 of 22 scoring categories (--bfcl-subsets all-local). The OVERALL row is an unweighted mean across all 22, so the 5 that did not run count as 0 and drag it down: IGNORE OVERALL at partial coverage and read acc instead. Published leaderboard figures (~0.73-0.77 for frontier models) are full-coverage OVERALL and are not comparable to either number here.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- before gsm8k: server was down [OOM] and could not be restarted: model endpoint did not become ready in time
- before humaneval: server was down [OOM]; restarted (start #2).
- Top prompt rung capped at 260000 tokens (max length 1000000 minus 256 output tokens and 10000 tokenizer-skew margin).
- Concurrency levels [8, 16, 32, 64] exceed the recipe's declared max concurrency (4); skipped.
