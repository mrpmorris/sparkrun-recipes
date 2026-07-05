# @sparkrun-transitional/qwen3-1.7b-llama-cpp benchmark results

Generated UTC: 2026-07-05T01:47:42.469052+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | @sparkrun-transitional/qwen3-1.7b-llama-cpp |
| Model | Qwen/Qwen3-1.7B-GGUF:Q8_0 |
| Served model name | Qwen/Qwen3-1.7B-GGUF:Q8_0 |
| Runtime | llama-cpp |
| Container | ghcr.io/spark-arena/dgx-llama-cpp:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/sparkrun-transitional__qwen3-1.7b-llama-cpp/20260705-014448 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe @sparkrun-transitional/qwen3-1.7b-llama-cpp --cleanup |
| Total duration | 174 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| n_gpu_layers | 99 |
| ctx_size | 8192 |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 270 | 0.062 | 9.1 | 4382.0 | 110.14 | 2.39 |
| 1024 | 1039 | 0.141 | 9.5 | 7345.0 | 105.60 | 2.57 |
| 4096 | 4109 | 0.439 | 11.0 | 9366.7 | 91.65 | 3.23 |
| 16384 | | FAILED | | | | |
| 65536 | | FAILED | | | | |
| 257144 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-mmlu.log |
| gsm8k | Grade-school math word problems (multi-step reasoning) | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-arc_challenge.log |
| hellaswag | Commonsense sentence completion | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-hellaswag.log |
| humaneval | Coding: write Python functions that pass unit tests | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | OSError: Repo id must use alphanumeric chars, '-', '_' or '.'. The name cannot start or end with '-' or '.' and the maximum length is 96: 'Qwen/Qwen3-1.7B-GGUF:Q8_0'. | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 257144 tokens (max length 260000 minus 256 output tokens and 2600 tokenizer-skew margin).
- Speed point 16384 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
- Speed point 65536 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
- Speed point 257144 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
