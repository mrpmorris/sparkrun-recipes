# Qwen3.6-35B-A3B-FP8.yaml benchmark results

Generated UTC: 2026-07-02T12:58:24.491194+00:00

## Run

| Key | Value |
| --- | --- |
| Recipe | /home/mrpmorris/sparkrun-recipes/Qwen3.6-35B-A3B-FP8.yaml |
| Model | Qwen/Qwen3.6-35B-A3B-FP8 |
| Runtime | vllm |
| Container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| Base URL | http://sparky1.local:8000 |
| Output dir | /home/mrpmorris/sparkrun-recipes/bench-results/Qwen3.6-35B-A3B-FP8.yaml/20260702-123424 |

## Recipe settings

| Setting | Value |
| --- | --- |
| model | Qwen/Qwen3.6-35B-A3B-FP8 |
| runtime | vllm |
| container | ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest |
| port | 8000 |
| host | 0.0.0.0 |
| max_model_len | 65536 |
| gpu_memory_utilization | 0.9000 |
| max_num_batched_tokens | 8192 |
| max_num_seqs | 4 |
| kv_cache_dtype | fp8 |
| attention_backend | flashinfer |
| tool_call_parser | qwen3_coder |
| reasoning_parser | qwen3 |
| speculative_config | {"method": "mtp", "num_speculative_tokens": 3} |

## Speed by prompt size

| Target tokens | OK | Failed | Concurrency | Server prompt tokens mean | Output tokens | Output tok/s | TTFT mean s | TTFT p50 s | TTFT p95 s | Latency mean s | Latency p50 s | Latency p95 s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2000 | 1 | 0 | 1 | 2012 | 512 | 53.0711 |  |  |  | 9.6386 | 9.6386 | 9.6386 |
| 32000 | 1 | 0 | 1 | 32013 | 512 | 32.2415 |  |  |  | 15.8702 | 15.8702 | 15.8702 |
| 512 | 1 | 0 | 1 | 524 | 512 | 63.0391 |  |  |  | 8.1163 | 8.1163 | 8.1163 |
| 8000 | 1 | 0 | 1 | 8012 | 512 | 48.8381 |  |  |  | 10.4768 | 10.4768 | 10.4768 |

## Throughput

| Target tokens | OK | Failed | Concurrency | Server prompt tokens mean | Output tokens | Output tok/s | TTFT mean s | Latency p95 s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | 16 | 0 | 8 | 1036.3750 | 8192 | 137.7460 |  | 30.2317 |

## Long-context needle retrieval

| Target tokens | Needle position % | Passed | Server prompt tokens | Latency s | Expected | Actual | Error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 32000 | 10 | no | 32062 | 7.9503 | answer-32000-10-blue-rabbit |  |  |
| 32000 | 50 | no | 32062 | 7.9794 | answer-32000-50-blue-rabbit |  |  |
| 32000 | 90 | no | 32062 | 8.0110 | answer-32000-90-blue-rabbit |  |  |
| 8000 | 10 | no | 8060 | 2.4003 | answer-8000-10-blue-rabbit |  |  |
| 8000 | 50 | no | 8060 | 2.2899 | answer-8000-50-blue-rabbit |  |  |
| 8000 | 90 | no | 8060 | 2.3015 | answer-8000-90-blue-rabbit |  |  |

## Intelligence, lm-eval

| Task | Metric | Value | Stderr | File |
| --- | --- | --- | --- | --- |
| gsm8k | exact_match,flexible-extract | 0.0000 |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| gsm8k | exact_match,strict-match | 0.0000 |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| gsm8k | exact_match_stderr,flexible-extract | 0.0000 |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| gsm8k | exact_match_stderr,strict-match | 0.0000 |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| gsm8k | name | gsm8k |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| gsm8k | sample_len | 50 |  | lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |

## Coding, BigCodeBench

_None._

## Warnings

| Warning |
| --- |
| BigCodeBench execution did not run. Generated samples may exist, but Pass@1 may be absent. |

## Output files

| File |
| --- |
| bigcodebench/Qwen--Qwen3.6-35B-A3B-FP8--main--bigcodebench-hard-instruct--openai-0-1-sanitized_calibrated.jsonl |
| bigcodebench-generate.log |
| bigcodebench-patch.json |
| bigcodebench-patch.log |
| bigcodebench-smoke-request.json |
| bigcodebench-smoke-response.json |
| chat-smoke-request.json |
| chat-smoke-response.json |
| dpkg-versions.txt |
| helper.py |
| lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/results_2026-07-02T12-37-47.444875.json |
| lm-eval-chat-gsm8k/Qwen__Qwen3.6-35B-A3B-FP8/samples_gsm8k_2026-07-02T12-37-47.444875.jsonl |
| lm-eval-chat-gsm8k.log |
| make-report.log |
| models-ready.json |
| needle-32000tok-pos10.json |
| needle-32000tok-pos10.log |
| needle-32000tok-pos50.json |
| needle-32000tok-pos50.log |
| needle-32000tok-pos90.json |
| needle-32000tok-pos90.log |
| needle-8000tok-pos10.json |
| needle-8000tok-pos10.log |
| needle-8000tok-pos50.json |
| needle-8000tok-pos50.log |
| needle-8000tok-pos90.json |
| needle-8000tok-pos90.log |
| pip-freeze.txt |
| recipe-info.json |
| run.log |
| sparkrun-run.log |
| sparkrun-run.pid |
| speed-context-2000.json |
| speed-context-2000.log |
| speed-context-32000.json |
| speed-context-32000.log |
| speed-context-512.json |
| speed-context-512.log |
| speed-context-8000.json |
| speed-context-8000.log |
| speed-throughput-1024tok-c8.json |
| speed-throughput-1024tok-c8.log |
| uname.txt |
| wait-for-model.log |

