# @eugr/glm-4.7-flash-awq benchmark results

Generated UTC: 2026-07-12T01:10:44.166910+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @eugr/glm-4.7-flash-awq |
| Model | cyankiwi/GLM-4.7-Flash-AWQ-4bit |
| Served model name | glm-4.7-flash |
| Runtime | vllm-distributed |
| Container | vllm-node |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/eugr__glm-4.7-flash-awq/20260712-004410 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @eugr/glm-4.7-flash-awq --cleanup |
| Total duration | 1594 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| gpu_memory_utilization | 0.8 |
| max_model_len | 202752 |
| max_num_batched_tokens | 4096 |
| max_num_seqs | 64 |
| served_model_name | glm-4.7-flash |

## Speed vs prompt size (single request)

_Speed benchmark failed: no prompt-size rung completed (see the run's speed-*.json and serve log)._

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

_Concurrency sweep produced no data (see the run's speed-*.json and serve log)._

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| glm-4.7-flash@bfcl_v4 | 0.1429 |  |
| acc | 0.1429 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.0000 | 25 |
| live_simple | 0.0000 | 25 |
| multiple | 0.0000 | 25 |
| parallel | 0.0000 | 25 |
| parallel_multiple | 0.0000 | 25 |
| simple_python | 0.0000 | 25 |
| NON_LIVE | 0.0000 | 100 |
| LIVE | 0.0000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.1000 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | server stopped generating (no OOM event in syslog; crashed or wedged); server restarted, task skipped | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| hellaswag | Commonsense sentence completion | skipped: server does not support echo+logprobs (required for loglikelihood scoring of multiple-choice tasks) |  |
| humaneval | Coding: write Python functions that pass unit tests | server stopped generating (no OOM event in syslog; crashed or wedged); HTTP 500 from inference server: EngineCore encountered an issue. See stack trace (above) for the root cause. | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | skipped: server stopped generating (no OOM event in syslog; crashed or wedged) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- server stopped generating (no OOM event in syslog; crashed or wedged) (before gsm8k); server restarted (1/2).
- server stopped generating (no OOM event in syslog; crashed or wedged) (during gsm8k); server restarted (2/2).
- server stopped generating (no OOM event in syslog; crashed or wedged) (during humaneval); restart budget exhausted (2/2).
- Server died during humaneval and could not be restarted; remaining eval tasks skipped: mbpp:0.
- server stopped generating (no OOM event in syslog; crashed or wedged) (before speed); restart budget exhausted (2/2).
- Speed benchmark skipped: server down and not restartable.
- server stopped generating (no OOM event in syslog; crashed or wedged) (before concurrency); restart budget exhausted (2/2).
- Concurrency sweep skipped: server down and not restartable.
