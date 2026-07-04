# Qwen3.6-35B-A3B-FP8.yaml benchmark results

Generated UTC: 2026-07-04T16:52:53.408096+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-FP8.yaml |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-FP8.yaml/20260704-164150 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-35B-A3B-FP8.yaml |
| Total duration | 663 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| port | 8000 |
| host | 0.0.0.0 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.9 |
| max_model_len | 262144 |
| max_num_batched_tokens | 16384 |
| max_num_seqs | 16 |
| load_format | instanttensor |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| speculative_config | {"method": "mtp", "num_speculative_tokens": 3} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.279 | 15.4 | 973.0 | 65.13 | 4.21 |
| 1024 | 1038 | 0.327 | 14.4 | 3175.1 | 69.60 | 4.01 |
| 4096 | 4115 | 1.266 | 17.9 | 3250.0 | 56.17 | 5.82 |
| 16384 | 16400 | 3.159 | 15.8 | 5191.7 | 63.36 | 7.20 |
| 65536 | 65554 | 16.888 | 16.3 | 3881.6 | 61.67 | 21.04 |
| 262144 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

1 task(s) completed, 5 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7123 | 0.0186 |  |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-arc_challenge.log |
| hellaswag | Commonsense sentence completion | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-hellaswag.log |
| humaneval | Coding: write Python functions that pass unit tests | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Prompt sizes beyond 262144 tokens skipped (next x4 step 1048576 exceeds the max length; max_model_len=262144, --max-prompt=260000).
- Speed point 262144 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
