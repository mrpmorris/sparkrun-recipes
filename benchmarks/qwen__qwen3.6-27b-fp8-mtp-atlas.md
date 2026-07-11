# qwen__qwen3.6-27b-fp8-mtp-atlas.yaml benchmark results

Generated UTC: 2026-07-11T19:31:08.726561+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/qwen__qwen3.6-27b-fp8-mtp-atlas.yaml |
| Model | Qwen/Qwen3.6-27B-FP8 |
| Served model name | Qwen/Qwen3.6-27B-FP8 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:dev |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/qwen__qwen3.6-27b-fp8-mtp-atlas.yaml/20260711-140522 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe qwen__qwen3.6-27b-fp8-mtp-atlas |
| Total duration | 19547 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 270 | 0.548 | 78.9 | 492.3 | 12.72 | 24.05 |
| 1024 | 1038 | 1.760 | 79.9 | 589.7 | 12.56 | 21.11 |
| 4096 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

2 task(s) completed, 4 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.0244 | 0.0121 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.0040 | 0.0028 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-FP8@bfcl_v4 | 0.8171 |  |
| acc | 0.8171 | 175 |
| irrelevance | 0.9600 | 25 |
| live_multiple | 0.6400 | 25 |
| live_simple | 0.8400 | 25 |
| multiple | 0.8800 | 25 |
| parallel | 0.7200 | 25 |
| parallel_multiple | 0.8400 | 25 |
| simple_python | 0.8400 | 25 |
| NON_LIVE | 0.8200 | 100 |
| LIVE | 0.7400 | 50 |
| HALLUCINATION | 0.9600 | 25 |
| OVERALL | 0.2520 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 257144 tokens (max length 260000 minus 256 output tokens and 2600 tokenizer-skew margin).
- Speed point 4096 tokens failed: JSONDecodeError: Unterminated string starting at: line 1 column 223 (char 222)
- Speed ladder stopped after the 4096-token failure; skipped larger rungs: [16384, 65536, 257144].
