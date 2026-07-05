# Qwen3.6-27B-NVFP4-MiaAILab.yaml benchmark results

Generated UTC: 2026-07-05T01:09:40.551773+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-NVFP4-MiaAILab.yaml/20260705-003514 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-NVFP4-MiaAILab.yaml --cleanup |
| Total duration | 2066 s |

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
| 256 | 271 | 0.957 | 28.3 | 283.1 | 35.45 | 8.18 |
| 1024 | 1040 | 1.296 | 32.7 | 802.6 | 30.71 | 9.63 |
| 4096 | 4111 | 4.297 | 32.1 | 956.6 | 31.30 | 12.48 |
| 16384 | 16399 | 15.772 | 36.2 | 1039.7 | 27.71 | 25.01 |
| 65536 | 65552 | 71.727 | 33.8 | 913.9 | 29.73 | 80.34 |
| 259267 | 259282 | 466.066 | 44.3 | 556.3 | 22.66 | 477.36 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6500 | 0.0479 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6700 | 0.0473 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3100 | 0.0465 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3900 | 0.0490 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8400 | 0.0368 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3100 | 0.0465 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-mmlu.log |
| arc_challenge | Hard science exam questions (reasoning) | HTTP 400 from inference server: Out of range float values are not JSON compliant: nan | lm-eval-arc_challenge.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
