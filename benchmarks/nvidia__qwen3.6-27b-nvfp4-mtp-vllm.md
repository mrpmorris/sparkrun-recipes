# nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml benchmark results

Generated UTC: 2026-07-08T07:09:47.460987+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml/20260708-050005 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml --cleanup |
| Total duration | 7782 s |

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
| 256 | 272 | 0.451 | 28.0 | 603.1 | 35.81 | 7.60 |
| 1024 | 1042 | 1.105 | 32.4 | 943.2 | 30.95 | 9.38 |
| 4096 | 4113 | 4.054 | 35.3 | 1014.6 | 28.48 | 13.04 |
| 16384 | 16398 | 15.650 | 37.2 | 1047.8 | 26.95 | 25.15 |
| 65536 | 65553 | 72.433 | 34.6 | 905.0 | 29.04 | 81.25 |
| 259267 | 259285 | 468.378 | 49.5 | 553.6 | 20.30 | 480.99 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.5861 | 0.0136 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6042 | 0.0135 | 1319 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3200 | 0.0469 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4100 | 0.0494 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7439 | 0.0342 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3240 | 0.0210 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.9086 |  |
| acc | 0.9086 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.7600 | 25 |
| live_simple | 0.8400 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9400 | 100 |
| LIVE | 0.8000 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2740 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |
| arc_challenge | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
