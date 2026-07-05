# Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml benchmark results

Generated UTC: 2026-07-05T19:40:13.744333+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Model | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-Multimodal-NVFP4-MTP-XS |
| Served model name | Qwen/Qwen3.6-27B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml/20260705-181927 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml --cleanup |
| Total duration | 4846 s |

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
| 256 | 273 | 0.482 | 22.0 | 566.6 | 45.62 | 6.09 |
| 1024 | 1042 | 0.899 | 27.8 | 1158.7 | 36.05 | 8.00 |
| 4096 | 4113 | 1.846 | 36.9 | 2228.7 | 27.21 | 11.25 |
| 16384 | 16398 | 9.902 | 40.3 | 1656.0 | 24.92 | 20.17 |
| 65536 | 65550 | 44.450 | 64.5 | 1474.7 | 15.56 | 60.91 |
| 259267 | 259284 | 320.049 | 107.8 | 810.1 | 9.31 | 347.54 |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

6 task(s) completed, 1 failed.

| Task | Description | Metric | Value | Stderr | Samples |
| --- | --- | --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | acc,none | 0.7982 | 0.0168 |  |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,strict-match | 0.0600 | 0.0239 | 100 |
| gsm8k | Grade-school math word problems (multi-step reasoning) | exact_match,flexible-extract | 0.1000 | 0.0302 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc,none | 0.5300 | 0.0502 | 100 |
| arc_challenge | Hard science exam questions (reasoning) | acc_norm,none | 0.5300 | 0.0502 | 100 |
| hellaswag | Commonsense sentence completion | acc,none | 0.5500 | 0.0500 | 100 |
| hellaswag | Commonsense sentence completion | acc_norm,none | 0.6800 | 0.0469 | 100 |
| humaneval | Coding: write Python functions that pass unit tests | pass@1,create_test | 0.8500 | 0.0359 | 100 |
| mbpp | Coding: basic Python programming problems, graded by unit tests | pass_at_1,none | 0.7200 | 0.0451 | 100 |

## Tool calling (BFCL v4 via EvalScope)

_No scores (see Failed benchmarks / bfcl.log)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| bfcl | Tool/function calling (BFCL v4 via EvalScope) | ModuleNotFoundError: No module named 'soundfile' | bfcl.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Top prompt rung capped at 259267 tokens (max length 262144 minus 256 output tokens and 2621 tokenizer-skew margin).
