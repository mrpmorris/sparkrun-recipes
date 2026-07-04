# Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml benchmark results

Generated UTC: 2026-07-04T22:37:16.901924+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml |
| Model | AEON-7/Qwen3.6-35B-A3B-heretic-NVFP4 |
| Served model name | Qwen/Qwen3.6-35B |
| Runtime | vllm |
| Container | ghcr.io/aeon-7/aeon-vllm-ultimate:latest |
| Base URL | http://127.0.0.1:8000/v1 |
| Host | Linux 6.17.0-1026-nvidia aarch64 GNU/Linux |
| GPU | NVIDIA GB10 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml/20260704-223533 |
| Command | /home/mrpmorris/sparkrun-recipes/benchllm.py --recipe Qwen3.6-35B-A3B-heretic-NVFP4-DFlash.yaml |
| Total duration | 103 s |

## Recipe settings

| Setting | Value |
| --- | --- |
| host | 0.0.0.0 |
| port | 8000 |
| served_model_name | Qwen/Qwen3.6-35B |
| tensor_parallel | 1 |
| pipeline_parallel | 1 |
| gpu_memory_utilization | 0.85 |
| max_model_len | 262144 |
| max_num_seqs | 64 |
| max_num_batched_tokens | 16384 |
| quantization | compressed-tensors |
| attention_backend | flash_attn |
| reasoning_parser | qwen3 |
| tool_call_parser | qwen3_coder |
| speculative_config | {"method":"dflash","model":"z-lab/Qwen3.6-35B-A3B-DFlash","revision":"42d3b34d588423cdae7ba8f53a8cf7789346a719","num_speculative_tokens":11} |
| generation_config | {"temperature":0.6,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0} |

## Speed vs prompt size (single request)

| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |
| --- | --- | --- | --- | --- | --- | --- |
| 256 | 269 | 0.330 | 9.0 | 814.3 | 111.96 | 2.62 |
| 1024 | 1041 | 0.561 | 7.9 | 1855.8 | 126.80 | 2.58 |
| 4096 | 4110 | 0.750 | 12.0 | 5477.3 | 83.77 | 3.81 |
| 16384 | 16401 | 2.767 | 13.3 | 5928.0 | 75.35 | 6.16 |
| 65536 | 65551 | 13.971 | 23.9 | 4692.0 | 41.98 | 20.07 |
| 262144 | | FAILED | | | | |

TTFT = time to first token. TPOT = time per output token (mean inter-token latency after the first token). Prefill tok/s = prompt tokens / TTFT. Generation tok/s = output tokens per second after the first token.

## Intelligence (lm-eval)

0 task(s) completed, 6 failed.

## Tool calling (BFCL v4 via EvalScope)

_Skipped (pass --with-bfcl to run)._

### Failed benchmarks

These benchmarks could not complete as the model is currently served — a failure here is itself a result: the model/config could not perform this evaluation. Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the inference server; generative tasks do not.

| Task | Description | Reason | Log |
| --- | --- | --- | --- |
| mmlu | General knowledge across 57 academic subjects | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-mmlu.log |
| gsm8k | Grade-school math word problems (multi-step reasoning) | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-gsm8k.log |
| arc_challenge | Hard science exam questions (reasoning) | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-arc_challenge.log |
| hellaswag | Commonsense sentence completion | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-hellaswag.log |
| humaneval | Coding: write Python functions that pass unit tests | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-humaneval.log |
| mbpp | Coding: basic Python programming problems, graded by unit tests | OSError: Qwen/Qwen3.6-35B is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models' | lm-eval-mbpp.log |

## Warnings

- lm-eval ran with sample limits (default 100, per task/subtask; tasks: mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp); scores are comparative samples, not full-benchmark numbers.
- Prompt sizes beyond 262144 tokens skipped (next x4 step 1048576 exceeds the max length; max_model_len=262144, --max-prompt=260000).
- Speed point 262144 tokens failed: HTTPError: 400 Client Error: Bad Request for url: http://127.0.0.1:8000/v1/chat/completions
