# qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml benchmark results

Generated UTC: 2026-07-11T09:17:20.880194+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Served model name | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml/20260711-082155 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/qwen__qwen3.6-35b-a3b-fp8-mtp-vllm.yaml --cleanup |
| Total duration | 3326 s |

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
| 256 | 269 | 0.248 | 13.3 | 1086.7 | 75.24 | 3.65 |
| 1024 | 1039 | 0.327 | 16.0 | 3177.4 | 62.64 | 4.41 |
| 4096 | 4113 | 1.132 | 15.9 | 3633.7 | 63.11 | 5.19 |
| 16384 | 16401 | 3.055 | 15.0 | 5368.8 | 67.12 | 6.87 |
| 65536 | 65552 | 16.762 | 19.7 | 3910.8 | 50.98 | 21.78 |
| 259267 | 259283 | 145.748 | 24.8 | 1779.0 | 40.53 | 152.06 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7140 | 0.0181 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.3487 | 0.0131 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.3662 | 0.0133 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.2662 | 0.0129 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.3131 | 0.0136 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.3400 | 0.0476 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.4300 | 0.0498 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.5976 | 0.0384 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6840 | 0.0208 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-35B-A3B-FP8@bfcl_v4 | 0.8857 |  |
| acc | 0.8857 | 175 |
| irrelevance | 1.0000 | 25 |
| live_multiple | 0.6000 | 25 |
| live_simple | 0.9200 | 25 |
| multiple | 0.9600 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9200 | 25 |
| simple_python | 0.9200 | 25 |
| NON_LIVE | 0.9200 | 100 |
| LIVE | 0.7600 | 50 |
| HALLUCINATION | 1.0000 | 25 |
| OVERALL | 0.2680 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
