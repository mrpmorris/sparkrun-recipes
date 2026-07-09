# unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml benchmark results

Generated UTC: 2026-07-09T08:02:07.424634+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml |
| Model | unsloth/Qwen3.6-27B-NVFP4 |
| Served model name | unsloth/Qwen3.6-27B-NVFP4 |
| Runtime | atlas |
| Container | avarok/atlas-gb10:dev |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml/20260709-030746 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml --cleanup |
| Total duration | 17661 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 275 | 0.518 | 70.4 | 530.9 | 14.26 | 17.14 |
| 1024 | 1041 | 1.662 | 71.4 | 626.3 | 14.07 | 18.44 |
| 4096 | 4109 | 6.304 | 74.9 | 651.8 | 13.41 | 23.83 |
| 16384 | 16400 | 26.388 | 87.9 | 621.5 | 11.43 | 47.21 |
| 65536 | 65553 | 125.958 | 142.0 | 520.4 | 7.14 | 136.18 |
| 257144 | 257160 | 814.598 | 355.0 | 315.7 | 5.63 | 814.95 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.8400 |  |
| acc | 0.8400 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.8000 | 25 |
| multiple | 0.7600 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.8800 | 25 |
| NON_LIVE | 0.8700 | 100 |
| LIVE | 0.7000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2570 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | killed by watchdog (exceeded 2h hard cap) | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| humaneval | Coding: write Python functions that pass unit tests | exit code 1 | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | exit code 1 | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Top prompt rung capped at 257144 tokens (max length 260000 minus 256 output tokens and 2600 tokenizer-skew margin).
