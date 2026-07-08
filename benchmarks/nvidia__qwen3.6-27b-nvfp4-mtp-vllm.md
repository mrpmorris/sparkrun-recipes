# nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml benchmark results

Generated UTC: 2026-07-08T00:07:46.801201+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml/20260707-224419 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml --cleanup |
| Total duration | 5007 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | nvidia/Qwen3.6-27B-NVFP4 |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.7 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 16384 |
| quantization | modelopt |
| load_format | fastsafetensors |
| attention_backend | flashinfer |
| moe_backend | marlin |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"mtp","num_speculative_tokens":3,"moe_backend":"triton"} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":1.5,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

3 task(s) completed, 3 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5914 | 0.0135 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6073 | 0.0135 | 1319 |
| hellaswag | Commonsense sentence completion | acc,none | 0.4300 | 0.0498 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.5300 | 0.0502 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7622 | 0.0333 | 164 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.9429 |  |
| acc | 0.9429 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9400 | 100 |
| LIVE | 0.9200 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2860 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |
| arc_challenge | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host 127.0.0.1:8000 ssl:default [Connect call failed ('127.0.0.1', 8000)] | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Server stopped generating after mbpp; remaining eval tasks skipped: none.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Speed point 256 tokens failed: ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8000): Max retries exceeded with url: /v1/chat/completions (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=8000): Failed to establish a new connection: [Errno 111] Connection refused"))
- Speed ladder stopped after the 256-token failure; skipped larger rungs: [1024, 4096, 16384, 65536, 259267].
