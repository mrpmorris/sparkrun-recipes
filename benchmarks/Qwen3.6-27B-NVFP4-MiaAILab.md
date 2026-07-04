# Qwen3.6-27B-NVFP4-MiaAILab.yaml benchmark results

Generated UTC: 2026-07-04T18:19:06.424365+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-NVFP4-MiaAILab.yaml |
| Model | nvidia/Qwen3.6-27B-NVFP4 |
| Served model name | nvidia/Qwen3.6-27B-NVFP4 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-NVFP4-MiaAILab.yaml/20260704-175255 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-27B-NVFP4-MiaAILab.yaml |
| Total duration | 1571 s |

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
| 256 | 271 | 0.843 | 27.9 | 321.5 | 35.96 | 7.96 |
| 1024 | 1038 | 1.199 | 32.2 | 865.6 | 31.15 | 9.42 |
| 4096 | 4112 | 4.293 | 33.0 | 957.9 | 30.41 | 12.71 |
| 16384 | 16397 | 15.453 | 36.8 | 1061.1 | 27.26 | 24.84 |
| 65536 | 65553 | 72.028 | 37.6 | 910.1 | 26.72 | 81.61 |
| 262144 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

5 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6500 | 0.0479 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6900 | 0.0465 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2900 | 0.0456 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.2400 | 0.0429 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3700 | 0.0485 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4200 | 0.0496 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8100 | 0.0394 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.2800 | 0.0451 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Prompt sizes beyond 262144 tokens skipped (next x4 step 1048576 exceeds the max length; max_model_len=262144, --max-prompt=260000).
- Speed point 262144 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
