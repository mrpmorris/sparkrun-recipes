# Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml benchmark results

Generated UTC: 2026-07-03T14:31:33.410546+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Model | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-Multimodal-NVFP4-MTP-XS |
| Served model name | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml/20260703-135758 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash.yaml |
| Total duration | 2015 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash |
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

| Prompt tokens | Server prompt tokens | TTFT s | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- |
| 32500 | 32517 | 19.470 | 1670.1 | 21.87 | 31.18 |
| 65000 | 65015 | 45.081 | 1442.2 | 22.83 | 56.29 |
| 97500 | 97521 | 76.611 | 1272.9 | 18.50 | 90.45 |
| 130000 | 130015 | 113.710 | 1143.4 | 11.32 | 136.32 |
| 162500 | 162515 | 157.449 | 1032.2 | 7.80 | 190.25 |
| 195000 | 195015 | 207.198 | 941.2 | 12.96 | 226.96 |
| 227500 | 227514 | 261.995 | 868.4 | 13.20 | 281.39 |
| 260000 | 260016 | 323.931 | 802.7 | 8.43 | 354.30 |

TTFT = time to first token. Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-mmlu.log |
| gsm8k | Grade-school math word problems (multi-step reasoning) | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-arc_challenge.log |
| hellaswag | Commonsense sentence completion | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-hellaswag.log |
| humaneval | Coding: write Python functions that pass unit tests | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | OSError: AEON-7/Qwen3.6-27B-AEON-Ultimate-Uncensored-DFlash is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
