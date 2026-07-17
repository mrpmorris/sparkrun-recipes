# aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml benchmark results

Generated UTC: 2026-07-17T05:30:26.594656+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml |
| Model | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-Multimodal-NVFP4-MTP-XS |
| Served model name | Qwen/Qwen3.6-27B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml/20260717-031213 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/recipes/aeon-7__qwen3.6-27b-uncensored-nvfp4-dflash-vllm.yaml --cleanup |
| Total duration | 8293 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | Qwen/Qwen3.6-27B |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.85 |
| max_model_len | 262144 |
| max_num_seqs | 16 |
| max_num_batched_tokens | 16384 |
| quantization | modelopt |
| mamba_cache_dtype | float32 |
| attention_backend | flash_attn |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-27B-DFlash","num_speculative_tokens":10} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 271 | 0.202 | 24.9 | 1340.1 | 40.40 | 6.54 |
| 1024 | 1038 | 0.531 | 23.6 | 1954.7 | 42.46 | 6.56 |
| 4096 | 4112 | 1.777 | 27.4 | 2314.5 | 36.63 | 8.76 |
| 16384 | 16399 | 9.683 | 77.6 | 1693.6 | 12.93 | 29.48 |
| 65536 | 65551 | 46.339 | 149.9 | 1414.6 | 6.70 | 84.57 |
| 259267 | 259284 | 318.726 | 338.8 | 813.5 | 2.96 | 405.12 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Throughput vs concurrency

Fixed 1024-token prompt, 256 output tokens per request; N streaming requests issued at once. A level's requests can fail or queue when it exceeds the server's max_num_seqs / --max-batch-size.

Recipe max concurrency: 16 (from max_num_seqs / max_batch_size); levels above it were skipped.

| Concurrency | OK | Failed | TTFT p50 s | TTFT p95 s | Per-req gen tok/s | Aggregate tok/s | Wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0.549 | 0.549 | 36.70 | 34.0 | 7.52 |
| 2 | 2 | 0 | 0.924 | 0.970 | 37.34 | 64.7 | 7.91 |
| 4 | 4 | 0 | 1.747 | 1.748 | 25.68 | 83.0 | 12.34 |
| 8 | 8 | 0 | 3.785 | 3.788 | 26.71 | 125.3 | 16.34 |
| 16 | 16 | 0 | 8.616 | 8.622 | 18.44 | 156.7 | 26.14 |

Per-req gen tok/s = mean per-request generation rate (falls as concurrency rises and the GPU is shared). Aggregate tok/s = total output tokens across all concurrent requests / wall-clock (the server's real throughput under load).

## Intelligence (lm-eval)

6 task(s) completed, 0 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7930 | 0.0166 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0713 | 0.0071 | 1319 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.0864 | 0.0077 | 1319 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.4795 | 0.0146 | 1172 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.4906 | 0.0146 | 1172 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6400 | 0.0482 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.7622 | 0.0333 | 164 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.6560 | 0.0213 | 500 |

## Tool calling (BFCL v4 via EvalScope)

Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.

| Subset / Category | Score | Samples |
| --- | --- | --- |
| Qwen3.6-27B@bfcl_v4 | 0.8971 |  |
| acc | 0.8971 | 175 |
| irrelevance | 0.9200 | 25 |
| live_multiple | 0.6800 | 25 |
| live_simple | 0.9600 | 25 |
| multiple | 0.9200 | 25 |
| parallel | 0.8800 | 25 |
| parallel_multiple | 0.9600 | 25 |
| simple_python | 0.9600 | 25 |
| NON_LIVE | 0.9300 | 100 |
| LIVE | 0.8200 | 50 |
| HALLUCINATION | 0.9200 | 25 |
| OVERALL | 0.2670 | 175 |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k:0,arc_challenge:0,hellaswag,humaneval:0,mbpp:0); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
- Concurrency levels [32, 64] exceed the recipe's declared max concurrency (16); skipped.
