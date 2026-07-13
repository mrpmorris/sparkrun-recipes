# @eugr/nemotron-3-nano-nvfp4 benchmark results

Generated UTC: 2026-07-13T20:13:09.455719+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/nemotron-3-nano-nvfp4 |
| Model | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3-nano-nvfp4/20260713-190750 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3-nano-nvfp4 --cleanup |
| Total duration | 3919 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 277 | 0.128 | 17.1 | 2165.9 | 58.55 | 4.50 |
| 1024 | 1044 | 0.205 | 17.1 | 5101.7 | 58.55 | 4.58 |
| 4096 | 4118 | 0.654 | 17.2 | 6298.5 | 58.38 | 5.04 |
| 16384 | 16404 | 2.528 | 17.3 | 6489.8 | 57.93 | 6.95 |
| 65536 | 65559 | 11.927 | 17.8 | 5496.7 | 56.27 | 16.48 |
| 259267 | 259285 | 78.191 | 19.8 | 3316.0 | 50.71 | 83.24 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.206 | 0.206 | 58.37 | 55.8 | 4.59 |
| 2 | 2 | 0 | 0.382 | 0.384 | 54.30 | 100.3 | 5.10 |
| 4 | 4 | 0 | 0.698 | 0.702 | 45.13 | 161.6 | 6.33 |
| 8 | 8 | 0 | 1.205 | 1.321 | 38.16 | 261.1 | 7.84 |
| 16 | 16 | 0 | 1.853 | 2.556 | 27.48 | 365.1 | 11.22 |
| 32 | 32 | 0 | 3.073 | 5.076 | 19.64 | 498.8 | 16.42 |
| 64 | 64 | 0 | 5.611 | 10.502 | 12.75 | 612.8 | 26.73 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7105 | 0.0180 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8249 | 0.0105 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.4738 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4514 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4778 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5200 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6600 | 0.0476 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.2195 | 0.0324 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5960 | 0.0220 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9600 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9500 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2710 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
