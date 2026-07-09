# unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml benchmark results

Generated UTC: 2026-07-09T03:07:42.549716+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml |
| Model | unsloth/DeepSeek-V4-Flash-GGUF:UD-IQ2_M |
| Served model name | unsloth/DeepSeek-V4-Flash-GGUF:UD-IQ2_M |
| Runtime | llama-cpp |
| Container | scitrera/dgx-spark-llama-cpp:b9898-cu131 |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml/20260709-030143 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml --cleanup |
| Total duration | 359 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| max_model_len | 32768 |
| n_gpu_layers | 99 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| DeepSeek-V4-Flash-GGUF_UD-IQ2_M@bfcl_v4 | 0.1429 |  |
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
| gsm8k | Grade-school math word problems (multi-step reasoning) | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | skipped: server stopped generating (wedged after gsm8k) |  |
| hellaswag | Commonsense sentence completion | skipped: server stopped generating (wedged after gsm8k) |  |
| humaneval | Coding: write Python functions that pass unit tests | skipped: server stopped generating (wedged after gsm8k) |  |
| mbpp | Coding: basic Python programming problems, graded by unit tests | skipped: server stopped generating (wedged after gsm8k) |  |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server does not support echo+logprobs on /v1/completions (loglikelihood scoring); multiple-choice tasks skipped.
- Server stopped generating after gsm8k; remaining eval tasks skipped: arc_challenge:0, hellaswag, humaneval:0, mbpp:0.
- Top prompt rung capped at 32185 tokens (max length 32768 minus 256 output tokens and 327 tokenizer-skew margin).
- Speed point 256 tokens failed: ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /v1/chat/completions (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=8000): Failed to establish a new connection: [Errno 111] Connection refused"))
- Speed ladder stopped after the 256-token failure; skipped larger rungs: [1024, 4096, 16384, 32185].
