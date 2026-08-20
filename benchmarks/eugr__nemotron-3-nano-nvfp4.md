# @eugr/nemotron-3-nano-nvfp4 benchmark results

Generated UTC: 2026-08-20T14:36:11.652343+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/nemotron-3-nano-nvfp4 |
| Model | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Served model name | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1029-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__nemotron-3-nano-nvfp4/20260820-133203 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/nemotron-3-nano-nvfp4 --cleanup |
| Total duration | 3848 s |

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
| 256 | 277 | 0.132 | 16.5 | 2094.0 | 60.73 | 4.35 |
| 1024 | 1045 | 0.188 | 16.5 | 5569.3 | 60.67 | 4.41 |
| 4096 | 4118 | 0.647 | 16.6 | 6364.6 | 60.64 | 4.87 |
| 16384 | 16405 | 2.600 | 16.7 | 6310.2 | 60.11 | 6.86 |
| 65536 | 65551 | 12.601 | 17.2 | 5202.2 | 58.25 | 17.00 |
| 259267 | 259290 | 82.074 | 19.5 | 3159.2 | 51.46 | 87.05 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe declares no max_num_seqs / max_batch_size — full ladder run.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.187 | 0.187 | 59.98 | 57.5 | 4.45 |
| 2 | 2 | 0 | 0.289 | 0.353 | 53.99 | 101.6 | 5.04 |
| 4 | 4 | 0 | 0.594 | 0.666 | 45.58 | 166.4 | 6.15 |
| 8 | 8 | 0 | 0.980 | 1.276 | 37.08 | 260.7 | 7.86 |
| 16 | 16 | 0 | 1.578 | 2.495 | 27.69 | 375.2 | 10.92 |
| 32 | 32 | 0 | 2.776 | 4.871 | 18.84 | 490.9 | 16.69 |
| 64 | 64 | 0 | 5.230 | 10.085 | 12.31 | 605.5 | 27.06 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

_humaneval ran with 4 of its 5 `until` stop sequences (`\nprint` dropped): vLLM 0.27+ enforces the OpenAI cap of 4 `stop` entries, and lm-eval's local-completions path does not trim (its chat paths do). Applied by patch-lm-eval-stop.py. Not bit-identical to canonical HumanEval - do not quote pass@1 against published figures without this caveat._

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7158 | 0.0180 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.8362 | 0.0102 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.4738 | 0.0138 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4514 | 0.0145 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4693 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.2195 | 0.0324 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.5820 | 0.0221 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4@bfcl_v4 | 0.8800 |  |
| acc | 0.8800 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9100 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.2630 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
