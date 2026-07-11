# nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml benchmark results

Generated UTC: 2026-07-11T07:21:35.410346+00:00

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
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml/20260711-045059 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml --cleanup |
| Total duration | 9036 s |

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
| 256 | 275 | 0.625 | 30.3 | 440.2 | 33.09 | 8.36 |
| 1024 | 1040 | 1.183 | 35.3 | 879.1 | 28.47 | 10.18 |
| 4096 | 4113 | 4.002 | 35.0 | 1027.8 | 28.65 | 12.94 |
| 16384 | 16401 |  |  |  |  | 15.22 |
| 65536 | 65549 |  |  |  |  | 3.48 |
| 259267 |  |  |  |  |  | 12.12 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

4 task(s) completed, 2 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.6012 | 0.0135 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.6111 | 0.0134 | 1319 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3000 | 0.0461 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.3900 | 0.0490 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7500 | 0.0339 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.3200 | 0.0209 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B-NVFP4@bfcl_v4 | 0.9314 |  |
| acc | 0.9314 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.8000 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.9200 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9400 | 100 |
| LIVE | 0.8800 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2820 | 175 |

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | server OOM (2026-07-11T05:57:14.911583+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2806237 uid 1000 "VLLM::EngineCor": badness 994, VmRSS 4229 MiB); server restarted, task skipped | lm-eval-mmlu.log |
| arc_challenge | Hard science exam questions (reasoning) | server OOM (2026-07-11T06:53:41.777197+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2833199 uid 1000 "VLLM::EngineCor": badness 1006, VmRSS 6832 MiB); server restarted, task skipped | lm-eval-arc_challenge.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- server OOM (2026-07-11T05:57:14.911583+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2806237 uid 1000 "VLLM::EngineCor": badness 994, VmRSS 4229 MiB) (during mmlu); server restarted (1/2).
- server OOM (2026-07-11T06:53:41.777197+00:00 sparky1 earlyoom[1593]: sending SIGTERM to process 2833199 uid 1000 "VLLM::EngineCor": badness 1006, VmRSS 6832 MiB) (during arc_challenge); server restarted (2/2).
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
