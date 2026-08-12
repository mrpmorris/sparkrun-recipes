# @eugr/nemotron-3.5-lightning benchmark results

Generated UTC: 2026-08-12T16:36:33.035911+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/nemotron-3.5-lightning |
| Model | nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3.5-lightning/20260812-160312 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3.5-lightning |
| Total duration | 2001 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 2 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 1048576 |
| max_num_batched_tokens | 16384 |
| num_speculative_tokens | 3 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 277 | 0.129 | 8.9 | 2154.5 | 112.24 | 2.41 |
| 1024 | 1045 | 0.211 | 8.5 | 4941.3 | 117.92 | 2.38 |
| 4096 | 4116 | 0.587 | 8.8 | 7013.7 | 113.55 | 2.84 |
| 16384 | 16406 | 2.247 | 8.3 | 7301.4 | 121.27 | 4.36 |
| 65536 | 65557 | 10.530 | 8.2 | 6225.7 | 121.95 | 12.63 |
| 259267 | 259287 | 71.832 | 8.0 | 3609.7 | 124.79 | 73.88 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.220 | 0.220 | 125.99 | 113.7 | 2.25 |
| 2 | 2 | 0 | 0.333 | 0.396 | 84.03 | 148.7 | 3.44 |
| 4 | 4 | 0 | 0.659 | 0.660 | 70.26 | 239.3 | 4.28 |
| 8 | 8 | 0 | 1.163 | 1.165 | 54.29 | 346.2 | 5.92 |
| 16 | 16 | 0 | 2.137 | 2.142 | 40.65 | 406.9 | 10.07 |
| 32 | 32 | 0 | 3.182 | 4.156 | 28.41 | 642.1 | 12.76 |
| 64 | 64 | 0 | 6.060 | 8.046 | 18.01 | 794.5 | 20.62 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.8000 | 0.0162 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8264 | 0.0104 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.8393 | 0.0101 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.6195 | 0.0142 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.6561 | 0.0139 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5600 | 0.0499 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.7000 | 0.0461 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.1707 | 0.0295 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6840 | 0.0208 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 1.0000 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8000 | 25 |
| parallel_multiple | 0.8800 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.8900 | 100 |
| LIVE | 0.9000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2790 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Recipe max_model_len=1048576 but the server reports 262144; using the server value.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
