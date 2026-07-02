#!/usr/bin/env bash
set -Eeuo pipefail

RECIPE=""
HOST=""
MODE="full"

WAIT_TIMEOUT_SECONDS="${WAIT_TIMEOUT_SECONDS:-3600}"
POLL_SECONDS="${POLL_SECONDS:-10}"

OUTPUT_TOKENS="${OUTPUT_TOKENS:-512}"

SPEED_CONTEXT_TOKENS_QUICK=(${SPEED_CONTEXT_TOKENS_QUICK:-512 2000 8000 32000})
SPEED_CONTEXT_TOKENS_FULL=(${SPEED_CONTEXT_TOKENS_FULL:-512 2000 8000 16000 32000 64000 128000 200000})

NEEDLE_CONTEXT_TOKENS_QUICK=(${NEEDLE_CONTEXT_TOKENS_QUICK:-8000 32000})
NEEDLE_CONTEXT_TOKENS_FULL=(${NEEDLE_CONTEXT_TOKENS_FULL:-8000 32000 64000 128000 200000})
NEEDLE_POSITIONS=(${NEEDLE_POSITIONS:-10 50 90})

THROUGHPUT_CONTEXT_TOKENS="${THROUGHPUT_CONTEXT_TOKENS:-1024}"
THROUGHPUT_CONCURRENCY="${THROUGHPUT_CONCURRENCY:-8}"

LM_EVAL_VERSION="${LM_EVAL_VERSION:-0.4.12}"
BIGCODEBENCH_VERSION="${BIGCODEBENCH_VERSION:-0.2.5}"
OPENAI_VERSION="${OPENAI_VERSION:-2.44.0}"
REQUESTS_VERSION="${REQUESTS_VERSION:-2.32.5}"
TQDM_VERSION="${TQDM_VERSION:-4.67.1}"
TIKTOKEN_VERSION="${TIKTOKEN_VERSION:-0.13.0}"
PYYAML_VERSION="${PYYAML_VERSION:-6.0.3}"

usage() {
  cat <<'USAGE'
Usage:
  ./benchllm.sh --recipe Qwen3.6-35B-A3B-FP8.yaml --host sparky1.local

Optional:
  --quick
  --full
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recipe) RECIPE="${2:-}"; shift 2 ;;
    --host) HOST="${2:-}"; shift 2 ;;
    --quick) MODE="quick"; shift ;;
    --full) MODE="full"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: Unknown argument: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$RECIPE" || -z "$HOST" ]]; then
  usage
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

RECIPE_PATH="$RECIPE"
if [[ "$RECIPE_PATH" != /* ]]; then
  RECIPE_PATH="$SCRIPT_DIR/$RECIPE_PATH"
fi

if [[ ! -f "$RECIPE_PATH" ]]; then
  echo "ERROR: Recipe file not found: $RECIPE_PATH"
  exit 1
fi

RECIPE_FILE="$(basename "$RECIPE_PATH")"
OUT="$SCRIPT_DIR/bench-results/$RECIPE_FILE/$(date +%Y%m%d-%H%M%S)"
REPORT="$SCRIPT_DIR/$RECIPE_FILE.md"
VENV="$SCRIPT_DIR/.benchllm-venv"

mkdir -p "$OUT"

run_lm_eval() {
  local task="$1"
  local fewshot="$2"
  local model_args="$3"
  local output_path="$4"

  echo
  echo "lm-eval task=$task fewshot=$fewshot"

  if ! lm_eval \
    --model local-completions \
    --model_args "$model_args" \
    --tasks "$task" \
    --num_fewshot "$fewshot" \
    --output_path "$output_path" \
    --log_samples \
    "${LM_LIMIT_ARGS[@]}" \
    2>&1 | tee "$output_path.log"; then

    echo "WARN: lm-eval failed for $task"
  fi
}

write_helper() {
  cat > "$OUT/helper.py" <<'PY'
import argparse
import concurrent.futures
import json
import os
import re
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

try:
    import tiktoken
    ENC = tiktoken.get_encoding("o200k_base")
except Exception:
    ENC = None

def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2), encoding="utf-8")

def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None

def token_count(text):
    if ENC:
        return len(ENC.encode(text))
    return max(1, len(text.split()))

def make_text_with_token_budget(target_tokens, marker=""):
    prefix = (
        "You are running a local LLM benchmark. "
        "Read the whole prompt. "
    )
    suffix = (
        "\n\nEnd of prompt. "
        "Continue with plain text until stopped. "
        f"{marker}\n"
    )

    if ENC:
        prefix_ids = ENC.encode(prefix)
        suffix_ids = ENC.encode(suffix)
        remaining = max(1, target_tokens - len(prefix_ids) - len(suffix_ids))
        unit = " The quick brown fox jumps over the lazy dog."
        unit_ids = ENC.encode(unit)
        repeated = (unit_ids * ((remaining // max(1, len(unit_ids))) + 2))[:remaining]
        ids = prefix_ids + repeated + suffix_ids
        return ENC.decode(ids)

    unit = "word "
    return prefix + (unit * max(1, target_tokens)) + suffix

def parse_recipe(args):
    recipe = yaml.safe_load(Path(args.recipe).read_text(encoding="utf-8")) or {}
    defaults = recipe.get("defaults") or {}

    info = {
        "model": recipe.get("model"),
        "runtime": recipe.get("runtime"),
        "container": recipe.get("container"),
        "port": defaults.get("port", 8000),
        "host": defaults.get("host"),
        "max_model_len": defaults.get("max_model_len"),
        "gpu_memory_utilization": defaults.get("gpu_memory_utilization"),
        "max_num_batched_tokens": defaults.get("max_num_batched_tokens"),
        "max_num_seqs": defaults.get("max_num_seqs"),
        "kv_cache_dtype": defaults.get("kv_cache_dtype"),
        "attention_backend": defaults.get("attention_backend"),
        "tool_call_parser": defaults.get("tool_call_parser"),
        "reasoning_parser": defaults.get("reasoning_parser"),
        "speculative_config": defaults.get("speculative_config"),
    }

    write_json(args.out, info)

def wait_model(args):
    url = args.base_url.rstrip("/") + "/v1/models"
    deadline = time.time() + args.timeout

    last_error = None
    last_models = []

    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()

            models = [
                item.get("id")
                for item in payload.get("data", [])
                if isinstance(item, dict) and item.get("id")
            ]

            last_models = models
            print(f"models: {models}", flush=True)

            if args.model in models:
                write_json(args.out, {
                    "base_url": args.base_url,
                    "expected_model": args.model,
                    "matched_model": args.model,
                    "models": models,
                    "raw": payload,
                })
                return
        except Exception as ex:
            last_error = repr(ex)
            print(f"not ready: {last_error}", flush=True)

        time.sleep(args.poll)

    write_json(args.out, {
        "base_url": args.base_url,
        "expected_model": args.model,
        "matched_model": None,
        "models": last_models,
        "last_error": last_error,
    })

    raise SystemExit(1)

def percentile(values, p):
    values = sorted(v for v in values if v is not None)

    if not values:
        return None

    k = (len(values) - 1) * p / 100
    f = int(k)
    c = min(f + 1, len(values) - 1)

    if f == c:
        return values[f]

    return values[f] + (values[c] - values[f]) * (k - f)

def post_chat_stream(base_url, payload):
    variants = [
        payload,
        {k: v for k, v in payload.items() if k != "ignore_eos"},
        {k: v for k, v in payload.items() if k not in ("ignore_eos", "stream_options")},
    ]

    last_error = None

    for body in variants:
        try:
            response = requests.post(
                base_url.rstrip("/") + "/v1/chat/completions",
                json=body,
                stream=True,
                timeout=1200,
            )

            if response.status_code < 400:
                return response

            last_error = f"{response.status_code}: {response.text[:2000]}"
            response.close()
        except Exception as ex:
            last_error = repr(ex)

    raise RuntimeError(last_error)

def run_one_speed(index, base_url, model, context_tokens, max_tokens):
    prompt = make_text_with_token_budget(
        context_tokens,
        marker=f"Request {index}. Target context tokens {context_tokens}."
    )

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": True,
        "stream_options": {"include_usage": True},
        "ignore_eos": True,
    }

    started = time.perf_counter()
    first_token = None
    text_parts = []
    usage = {}

    try:
        with post_chat_stream(base_url, payload) as response:
            for raw_line in response.iter_lines(decode_unicode=True):
                if not raw_line or not raw_line.startswith("data: "):
                    continue

                data = raw_line[6:]
                if data == "[DONE]":
                    break

                obj = json.loads(data)

                if obj.get("usage"):
                    usage = obj["usage"]

                choices = obj.get("choices") or []
                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                chunk = delta.get("content") or ""

                if chunk:
                    if first_token is None:
                        first_token = time.perf_counter()
                    text_parts.append(chunk)

        ended = time.perf_counter()
        text = "".join(text_parts)

        completion_tokens = usage.get("completion_tokens")
        estimated = False
        estimated_by = None

        if completion_tokens is None:
            completion_tokens = token_count(text)
            estimated = True
            estimated_by = "tiktoken_o200k_base" if ENC else "word_count"

        return {
            "request": index,
            "ok": True,
            "target_context_tokens": context_tokens,
            "local_prompt_token_estimate": token_count(prompt),
            "server_prompt_tokens": usage.get("prompt_tokens"),
            "server_total_tokens": usage.get("total_tokens"),
            "latency_s": ended - started,
            "ttft_s": None if first_token is None else first_token - started,
            "completion_tokens": completion_tokens,
            "token_count_estimated": estimated,
            "estimated_by": estimated_by,
            "chars": len(text),
            "error": None,
        }
    except Exception as ex:
        ended = time.perf_counter()
        return {
            "request": index,
            "ok": False,
            "target_context_tokens": context_tokens,
            "local_prompt_token_estimate": token_count(prompt),
            "server_prompt_tokens": None,
            "server_total_tokens": None,
            "latency_s": ended - started,
            "ttft_s": None,
            "completion_tokens": 0,
            "token_count_estimated": None,
            "estimated_by": None,
            "chars": 0,
            "error": repr(ex),
        }

def speed(args):
    base_url = os.environ["BASE_URL"]
    model = os.environ["MODEL"]

    started = time.perf_counter()
    rows = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [
            executor.submit(
                run_one_speed,
                i,
                base_url,
                model,
                args.context_tokens,
                args.max_tokens,
            )
            for i in range(args.requests)
        ]

        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            rows.append(row)
            print(f"done {len(rows)}/{args.requests} ok={row['ok']}", flush=True)

    wall_time = time.perf_counter() - started
    ok_rows = [r for r in rows if r["ok"]]

    latencies = [r["latency_s"] for r in ok_rows]
    ttfts = [r["ttft_s"] for r in ok_rows if r["ttft_s"] is not None]
    output_tokens = sum(r["completion_tokens"] for r in ok_rows)

    estimated = any(r.get("token_count_estimated") for r in ok_rows)

    warnings = []
    if estimated:
        warnings.append("Server did not return completion_tokens for at least one request. Output tok/s is estimated.")

    if len(ok_rows) != len(rows):
        warnings.append(f"{len(rows) - len(ok_rows)} speed requests failed.")

    summary = {
        "model": model,
        "base_url": base_url,
        "requests": args.requests,
        "ok_requests": len(ok_rows),
        "failed_requests": len(rows) - len(ok_rows),
        "concurrency": args.concurrency,
        "target_context_tokens": args.context_tokens,
        "max_tokens": args.max_tokens,
        "wall_time_s": wall_time,
        "output_tokens": output_tokens,
        "output_tokens_per_s": output_tokens / max(0.001, wall_time),
        "latency_mean_s": statistics.mean(latencies) if latencies else None,
        "latency_p50_s": percentile(latencies, 50),
        "latency_p95_s": percentile(latencies, 95),
        "ttft_mean_s": statistics.mean(ttfts) if ttfts else None,
        "ttft_p50_s": percentile(ttfts, 50),
        "ttft_p95_s": percentile(ttfts, 95),
        "server_prompt_tokens_mean": statistics.mean([r["server_prompt_tokens"] for r in ok_rows if r["server_prompt_tokens"] is not None]) if any(r["server_prompt_tokens"] is not None for r in ok_rows) else None,
        "token_count_estimated": estimated,
        "warnings": warnings,
        "results": sorted(rows, key=lambda x: x["request"]),
    }

    write_json(args.out, summary)
    print(json.dumps(summary, indent=2))

def post_chat(base_url, payload, timeout=1200):
    response = requests.post(
        base_url.rstrip() + "/v1/chat/completions",
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()

def needle(args):
    base_url = os.environ["BASE_URL"]
    model = os.environ["MODEL"]

    needle_id = f"NEEDLE-{args.context_tokens}-{args.position_percent}"
    answer = f"answer-{args.context_tokens}-{args.position_percent}-blue-rabbit"
    needle_text = f"\n\nIMPORTANT FACT: The secret benchmark answer for {needle_id} is {answer}.\n\n"

    before_tokens = int(args.context_tokens * args.position_percent / 100)
    after_tokens = max(1, args.context_tokens - before_tokens)

    before = make_text_with_token_budget(before_tokens, marker="before needle")
    after = make_text_with_token_budget(after_tokens, marker="after needle")

    prompt = (
        before
        + needle_text
        + after
        + "\n\nQuestion: What is the exact secret benchmark answer? Reply with only the answer string."
    )

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 64,
    }

    started = time.perf_counter()

    try:
        response = post_chat(base_url, payload)
        elapsed = time.perf_counter() - started

        content = (((response.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
        usage = response.get("usage") or {}

        result = {
            "ok": True,
            "model": model,
            "base_url": base_url,
            "target_context_tokens": args.context_tokens,
            "position_percent": args.position_percent,
            "expected": answer,
            "actual": content,
            "passed": answer in content,
            "latency_s": elapsed,
            "server_prompt_tokens": usage.get("prompt_tokens"),
            "server_completion_tokens": usage.get("completion_tokens"),
            "server_total_tokens": usage.get("total_tokens"),
            "error": None,
            "raw": response,
        }
    except Exception as ex:
        result = {
            "ok": False,
            "model": model,
            "base_url": base_url,
            "target_context_tokens": args.context_tokens,
            "position_percent": args.position_percent,
            "expected": answer,
            "actual": "",
            "passed": False,
            "latency_s": time.perf_counter() - started,
            "server_prompt_tokens": None,
            "server_completion_tokens": None,
            "server_total_tokens": None,
            "error": repr(ex),
            "raw": None,
        }

    write_json(args.out, result)
    print(json.dumps(result, indent=2))

def patch_bcb(args):
    try:
        import bigcodebench.provider.openai as openai_provider
        path = Path(openai_provider.__file__)
        text = path.read_text(encoding="utf-8")

        old = "outputs.append(item.message.content)"

        new = """content = getattr(item.message, "content", None)
                if content is None:
                    content = getattr(item.message, "reasoning", None)
                if content is None:
                    content = getattr(item.message, "reasoning_content", None)
                if content is None:
                    content = ""
                outputs.append(content)"""

        if old in text and new not in text:
            path.write_text(text.replace(old, new), encoding="utf-8")
            result = {"patched": True, "file": str(path)}
        else:
            result = {"patched": False, "file": str(path), "reason": "pattern not found or already patched"}

        write_json(args.out, result)
        print(json.dumps(result, indent=2))
    except Exception as ex:
        result = {"patched": False, "error": repr(ex)}
        write_json(args.out, result)
        print(json.dumps(result, indent=2))

def fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value).replace("\n", " ").replace("|", "\\|")

def table(headers, rows):
    if not rows:
        return "\n_None._\n"

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in rows:
        lines.append("| " + " | ".join(fmt(x) for x in row) + " |")

    return "\n" + "\n".join(lines) + "\n"

def collect_lm_eval(out_dir):
    rows = []

    for path in sorted(Path(out_dir).glob("lm-eval*/**/results_*.json")):
        payload = read_json(path) or {}
        results = payload.get("results") or {}

        for task, metrics in sorted(results.items()):
            if not isinstance(metrics, dict):
                continue

            for metric, value in sorted(metrics.items()):
                if metric == "alias" or metric.endswith("_stderr"):
                    continue

                if isinstance(value, (int, float, str, bool)) or value is None:
                    rows.append([
                        task,
                        metric,
                        value,
                        metrics.get(metric + "_stderr"),
                        str(path.relative_to(out_dir)),
                    ])

    return rows

def collect_bcb(out_dir):
    rows = []

    for pattern in ["**/*pass_at_k.json", "**/*eval_results.json", "**/*results.json"]:
        for path in sorted(Path(out_dir).glob(pattern)):
            payload = read_json(path)

            if not isinstance(payload, dict):
                continue

            for key, value in sorted(payload.items()):
                if isinstance(value, (int, float, str, bool)) or value is None:
                    rows.append([key, value, str(path.relative_to(out_dir))])
                elif isinstance(value, dict):
                    for key2, value2 in sorted(value.items()):
                        if isinstance(value2, (int, float, str, bool)) or value2 is None:
                            rows.append([f"{key}.{key2}", value2, str(path.relative_to(out_dir))])

    return rows

def report(args):
    out = Path(args.out_dir)
    recipe = Path(args.recipe)
    info = read_json(args.recipe_info) or {}

    speed_rows = []
    for path in sorted(out.glob("speed-context-*.json")):
        data = read_json(path) or {}
        speed_rows.append([
            data.get("target_context_tokens"),
            data.get("ok_requests"),
            data.get("failed_requests"),
            data.get("concurrency"),
            data.get("server_prompt_tokens_mean"),
            data.get("output_tokens"),
            data.get("output_tokens_per_s"),
            data.get("ttft_mean_s"),
            data.get("ttft_p50_s"),
            data.get("ttft_p95_s"),
            data.get("latency_mean_s"),
            data.get("latency_p50_s"),
            data.get("latency_p95_s"),
        ])

    throughput_rows = []
    for path in sorted(out.glob("speed-throughput-*.json")):
        data = read_json(path) or {}
        throughput_rows.append([
            data.get("target_context_tokens"),
            data.get("ok_requests"),
            data.get("failed_requests"),
            data.get("concurrency"),
            data.get("server_prompt_tokens_mean"),
            data.get("output_tokens"),
            data.get("output_tokens_per_s"),
            data.get("ttft_mean_s"),
            data.get("latency_p95_s"),
        ])

    needle_rows = []
    for path in sorted(out.glob("needle-*.json")):
        data = read_json(path) or {}
        needle_rows.append([
            data.get("target_context_tokens"),
            data.get("position_percent"),
            data.get("passed"),
            data.get("server_prompt_tokens"),
            data.get("latency_s"),
            data.get("expected"),
            data.get("actual"),
            data.get("error"),
        ])

    lm_rows = collect_lm_eval(out)
    bcb_rows = collect_bcb(out)

    warnings = []

    for path in sorted(out.glob("speed-*.json")):
        data = read_json(path) or {}
        warnings.extend(data.get("warnings") or [])

    for path in sorted(out.glob("needle-*.json")):
        data = read_json(path) or {}
        if data.get("error"):
            warnings.append(f"Needle failed for {path.name}: {data.get('error')}")

    if not any((out / name).exists() for name in [
        "bigcodebench-evaluate-docker.log",
        "bigcodebench-evaluate-host.log",
        "bigcodebench-evaluate-gradio.log",
    ]):
        warnings.append("BigCodeBench execution did not run. Generated samples may exist, but Pass@1 may be absent.")

    files = [str(path.relative_to(out)) for path in sorted(out.rglob("*")) if path.is_file()]

    md = [
        f"# {recipe.name} benchmark results",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Run",
        table(["Key", "Value"], [
            ["Recipe", str(recipe)],
            ["Model", info.get("model")],
            ["Runtime", info.get("runtime")],
            ["Container", info.get("container")],
            ["Base URL", args.base_url],
            ["Output dir", str(out)],
        ]),
        "## Recipe settings",
        table(["Setting", "Value"], [[key, value] for key, value in info.items() if value is not None]),
        "## Speed by prompt size",
        table([
            "Target tokens",
            "OK",
            "Failed",
            "Concurrency",
            "Server prompt tokens mean",
            "Output tokens",
            "Output tok/s",
            "TTFT mean s",
            "TTFT p50 s",
            "TTFT p95 s",
            "Latency mean s",
            "Latency p50 s",
            "Latency p95 s",
        ], speed_rows),
        "## Throughput",
        table([
            "Target tokens",
            "OK",
            "Failed",
            "Concurrency",
            "Server prompt tokens mean",
            "Output tokens",
            "Output tok/s",
            "TTFT mean s",
            "Latency p95 s",
        ], throughput_rows),
        "## Long-context needle retrieval",
        table([
            "Target tokens",
            "Needle position %",
            "Passed",
            "Server prompt tokens",
            "Latency s",
            "Expected",
            "Actual",
            "Error",
        ], needle_rows),
        "## Intelligence, lm-eval",
        table(["Task", "Metric", "Value", "Stderr", "File"], lm_rows),
        "## Coding, BigCodeBench",
        table(["Metric", "Value", "File"], bcb_rows),
        "## Warnings",
        table(["Warning"], [[warning] for warning in sorted(set(warnings))]),
        "## Output files",
        table(["File"], [[file] for file in files]),
        "",
    ]

    Path(args.report).write_text("\n".join(md), encoding="utf-8")
    print(args.report)

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("parse")
    p.add_argument("--recipe", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=parse_recipe)

    p = sub.add_parser("wait")
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--timeout", type=int, required=True)
    p.add_argument("--poll", type=int, required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=wait_model)

    p = sub.add_parser("speed")
    p.add_argument("--requests", type=int, required=True)
    p.add_argument("--concurrency", type=int, required=True)
    p.add_argument("--context-tokens", type=int, required=True)
    p.add_argument("--max-tokens", type=int, required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=speed)

    p = sub.add_parser("needle")
    p.add_argument("--context-tokens", type=int, required=True)
    p.add_argument("--position-percent", type=int, required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=needle)

    p = sub.add_parser("patch-bcb")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=patch_bcb)

    p = sub.add_parser("report")
    p.add_argument("--recipe", required=True)
    p.add_argument("--recipe-info", required=True)
    p.add_argument("--base-url", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--report", required=True)
    p.set_defaults(fn=report)

    args = parser.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()
PY
}

main() {
  echo "Recipe: $RECIPE_PATH"
  echo "Host: $HOST"
  echo "Mode: $MODE"
  echo "Output: $OUT"
  echo "Report: $REPORT"

  if ! command -v apt-get >/dev/null 2>&1; then
    echo "ERROR: apt-get not found. This script expects DGXOS/Ubuntu/Debian."
    exit 1
  fi

  if [[ "$(id -u)" -eq 0 ]]; then
    SUDO=""
  else
    SUDO="sudo"
  fi

  $SUDO apt-get update

  $SUDO apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    jq \
    ca-certificates \
    coreutils

  python3 -m venv "$VENV"
  source "$VENV/bin/activate"

  python -m pip install --upgrade pip wheel setuptools

  python -m pip install \
    "PyYAML==$PYYAML_VERSION" \
    "requests==2.32.5" \
    "urllib3<3" \
    "charset-normalizer<4" \
    "chardet<6" \
    "tqdm==$TQDM_VERSION" \
    "openai==$OPENAI_VERSION" \
    "tiktoken==$TIKTOKEN_VERSION" \
    "lm-eval[api]==$LM_EVAL_VERSION" \
    "bigcodebench==$BIGCODEBENCH_VERSION"

  if ! command -v sparkrun >/dev/null 2>&1; then
    python -m pip install sparkrun
  fi

  python -m pip freeze | sort > "$OUT/pip-freeze.txt"
  dpkg-query -W > "$OUT/dpkg-versions.txt" || true
  uname -a > "$OUT/uname.txt"

  write_helper

  python "$OUT/helper.py" parse \
    --recipe "$RECIPE_PATH" \
    --out "$OUT/recipe-info.json"

  RECIPE_MODEL="$(jq -r '.model // empty' "$OUT/recipe-info.json")"
  RECIPE_PORT="$(jq -r '.port // 8000' "$OUT/recipe-info.json")"

  if [[ -z "$RECIPE_MODEL" ]]; then
    echo "ERROR: recipe has no top-level model value"
    cat "$OUT/recipe-info.json"
    exit 1
  fi

  HOST_NO_SCHEME="$HOST"
  URL_SCHEME="http"

  if [[ "$HOST_NO_SCHEME" == http://* ]]; then
    HOST_NO_SCHEME="${HOST_NO_SCHEME#http://}"
    URL_SCHEME="http"
  fi

  if [[ "$HOST_NO_SCHEME" == https://* ]]; then
    HOST_NO_SCHEME="${HOST_NO_SCHEME#https://}"
    URL_SCHEME="https"
  fi

  HOST_NO_PATH="${HOST_NO_SCHEME%%/*}"
  HOST_ONLY="${HOST_NO_PATH%%:*}"

  if [[ "$HOST_NO_PATH" == *:* ]]; then
    BASE_URL="$URL_SCHEME://$HOST_NO_PATH"
  else
    BASE_URL="$URL_SCHEME://$HOST_ONLY:$RECIPE_PORT"
  fi

  echo "Recipe model: $RECIPE_MODEL"
  echo "Recipe port: $RECIPE_PORT"
  echo "Base URL: $BASE_URL"

  export OPENAI_API_KEY="${OPENAI_API_KEY:-EMPTY}"
  export BASE_URL
  export RECIPE_MODEL

  echo
  echo "Starting recipe with sparkrun"
  echo "Command: sparkrun run '$RECIPE_PATH' --hosts '$HOST_ONLY' --ensure --no-follow"

  set +e
  (
    cd "$SCRIPT_DIR"
    sparkrun run "$RECIPE_PATH" --hosts "$HOST_ONLY" --ensure --no-follow
  ) > "$OUT/sparkrun-run.log" 2>&1 &
  SPARKRUN_PID=$!
  set -e

  echo "$SPARKRUN_PID" > "$OUT/sparkrun-run.pid"

  echo
  echo "Waiting for $BASE_URL/v1/models to show $RECIPE_MODEL"

  python "$OUT/helper.py" wait \
    --base-url "$BASE_URL" \
    --model "$RECIPE_MODEL" \
    --timeout "$WAIT_TIMEOUT_SECONDS" \
    --poll "$POLL_SECONDS" \
    --out "$OUT/models-ready.json" \
    2>&1 | tee "$OUT/wait-for-model.log"

  MODEL="$(jq -r '.matched_model' "$OUT/models-ready.json")"
  export MODEL

  echo
  echo "Patching BigCodeBench null-content handling"
  python "$OUT/helper.py" patch-bcb \
    --out "$OUT/bigcodebench-patch.json" \
    2>&1 | tee "$OUT/bigcodebench-patch.log"

  if [[ "$MODE" == "quick" ]]; then
    SPEED_CONTEXT_TOKENS=("${SPEED_CONTEXT_TOKENS_QUICK[@]}")
    NEEDLE_CONTEXT_TOKENS=("${NEEDLE_CONTEXT_TOKENS_QUICK[@]}")
    SPEED_REQUESTS=1
    THROUGHPUT_REQUESTS=16
    LM_LIMIT_ARGS=(--limit 50)
    BCB_ID_RANGE_ARGS=(--id_range 0-20)
  else
    SPEED_CONTEXT_TOKENS=("${SPEED_CONTEXT_TOKENS_FULL[@]}")
    NEEDLE_CONTEXT_TOKENS=("${NEEDLE_CONTEXT_TOKENS_FULL[@]}")
    SPEED_REQUESTS=1
    THROUGHPUT_REQUESTS=100
    LM_LIMIT_ARGS=()
    BCB_ID_RANGE_ARGS=()
  fi

  echo
  echo "Smoke test"

  jq -n --arg model "$MODEL" '{
    model: $model,
    messages: [{"role":"user","content":"Reply with OK only."}],
    temperature: 0,
    max_tokens: 8
  }' > "$OUT/chat-smoke-request.json"

  curl -fsS \
    -H "Content-Type: application/json" \
    "$BASE_URL/v1/chat/completions" \
    -d @"$OUT/chat-smoke-request.json" \
    -o "$OUT/chat-smoke-response.json"

  cat "$OUT/chat-smoke-response.json"
  echo

  echo
  echo "Running speed benchmarks by prompt size"

  for TOKENS in "${SPEED_CONTEXT_TOKENS[@]}"; do
    echo
    echo "Speed context tokens: $TOKENS"

    python "$OUT/helper.py" speed \
      --requests "$SPEED_REQUESTS" \
      --concurrency 1 \
      --context-tokens "$TOKENS" \
      --max-tokens "$OUTPUT_TOKENS" \
      --out "$OUT/speed-context-$TOKENS.json" \
      2>&1 | tee "$OUT/speed-context-$TOKENS.log"
  done

  echo
  echo "Running throughput benchmark"

  python "$OUT/helper.py" speed \
    --requests "$THROUGHPUT_REQUESTS" \
    --concurrency "$THROUGHPUT_CONCURRENCY" \
    --context-tokens "$THROUGHPUT_CONTEXT_TOKENS" \
    --max-tokens "$OUTPUT_TOKENS" \
    --out "$OUT/speed-throughput-${THROUGHPUT_CONTEXT_TOKENS}tok-c${THROUGHPUT_CONCURRENCY}.json" \
    2>&1 | tee "$OUT/speed-throughput-${THROUGHPUT_CONTEXT_TOKENS}tok-c${THROUGHPUT_CONCURRENCY}.log"

  echo
  echo "Running long-context needle retrieval"

  for TOKENS in "${NEEDLE_CONTEXT_TOKENS[@]}"; do
    for POS in "${NEEDLE_POSITIONS[@]}"; do
      echo
      echo "Needle context tokens: $TOKENS position: $POS"

      python "$OUT/helper.py" needle \
        --context-tokens "$TOKENS" \
        --position-percent "$POS" \
        --out "$OUT/needle-${TOKENS}tok-pos${POS}.json" \
        2>&1 | tee "$OUT/needle-${TOKENS}tok-pos${POS}.log"
    done
  done

  echo
  echo "Running lm-eval chat-only GSM8K"

  CHAT_ARGS="model=$MODEL,base_url=$BASE_URL/v1/chat/completions,num_concurrent=1,max_retries=3"

  if ! lm_eval \
    --model local-chat-completions \
    --model_args "$CHAT_ARGS" \
    --tasks gsm8k \
    --num_fewshot 5 \
    --output_path "$OUT/lm-eval-chat-gsm8k" \
    --log_samples \
    --apply_chat_template \
    "${LM_LIMIT_ARGS[@]}" \
    2>&1 | tee "$OUT/lm-eval-chat-gsm8k.log"; then

    echo "WARN: lm-eval chat GSM8K failed"
  fi

  echo
  echo "Running BigCodeBench generation"

  BCB_ROOT="$OUT/bigcodebench"
  mkdir -p "$BCB_ROOT"

  BCB_CONTENT_OK=0

  jq -n --arg model "$MODEL" '{
    model: $model,
    messages: [
      {
        role: "user",
        content: "Write only Python code. Define function add(a, b) that returns a + b."
      }
    ],
    temperature: 0,
    max_tokens: 512
  }' > "$OUT/bigcodebench-smoke-request.json"

  if curl -fsS \
    -H "Content-Type: application/json" \
    "$BASE_URL/v1/chat/completions" \
    -d @"$OUT/bigcodebench-smoke-request.json" \
    -o "$OUT/bigcodebench-smoke-response.json"; then

    CONTENT="$(jq -r '.choices[0].message.content // empty' "$OUT/bigcodebench-smoke-response.json")"

    if [[ -n "$CONTENT" ]]; then
      BCB_CONTENT_OK=1
    fi
  fi

  if [[ "$BCB_CONTENT_OK" != "1" ]]; then
    echo "WARN: Skipping BigCodeBench. Endpoint returned empty/null message.content."
    echo "See: $OUT/bigcodebench-smoke-response.json"
  else
    if ! bigcodebench.generate \
      --model "$MODEL" \
      --split instruct \
      --subset hard \
      --backend openai \
      --base_url "$BASE_URL/v1" \
      --root "$BCB_ROOT" \
      --bs 1 \
      --temperature 0 \
      --n_samples 1 \
      --greedy \
      --max_new_tokens 4096 \
      "${BCB_ID_RANGE_ARGS[@]}" \
      2>&1 | tee "$OUT/bigcodebench-generate.log"; then

      echo "WARN: BigCodeBench generation failed"
    fi
  fi

  SAMPLES="$(find "$BCB_ROOT" -type f -name '*sanitized_calibrated.jsonl' | sort | tail -n 1 || true)"

  if [[ -z "$SAMPLES" ]]; then
    echo "WARN: BigCodeBench sample file not found"
  else
    echo "BigCodeBench samples: $SAMPLES"

    DOCKER_CMD=()
    ARCH="$(uname -m)"

    if command -v docker >/dev/null 2>&1; then
      if docker ps >/dev/null 2>&1; then
        DOCKER_CMD=(docker)
      elif $SUDO docker ps >/dev/null 2>&1; then
        DOCKER_CMD=($SUDO docker)
      fi
    fi

    if [[ "${#DOCKER_CMD[@]}" -gt 0 && ( "$ARCH" == "x86_64" || "$ARCH" == "amd64" ) ]]; then
      "${DOCKER_CMD[@]}" pull bigcodebench/bigcodebench-evaluate:latest

      SAMPLES_IN_CONTAINER="/app/$(realpath --relative-to="$BCB_ROOT" "$SAMPLES")"

      if ! "${DOCKER_CMD[@]}" run --rm \
        -v "$BCB_ROOT":/app \
        bigcodebench/bigcodebench-evaluate:latest \
        --execution local \
        --split instruct \
        --subset hard \
        --samples "$SAMPLES_IN_CONTAINER" \
        --save_pass_rate \
        --pass_k 1 \
        --parallel "$(nproc)" \
        2>&1 | tee "$OUT/bigcodebench-evaluate-docker.log"; then

        echo "WARN: BigCodeBench Docker evaluation failed"
      fi
    elif [[ "${ALLOW_UNSANDBOXED_BCB:-0}" == "1" ]]; then
      echo "WARN: Running model-generated code directly on this host."

      if ! bigcodebench.evaluate \
        --execution local \
        --split instruct \
        --subset hard \
        --samples "$SAMPLES" \
        --save_pass_rate \
        --pass_k 1 \
        --parallel "$(nproc)" \
        2>&1 | tee "$OUT/bigcodebench-evaluate-host.log"; then

        echo "WARN: BigCodeBench host evaluation failed"
      fi
    elif [[ "${ALLOW_REMOTE_BCB:-0}" == "1" ]]; then
      echo "WARN: Sending generated code to remote BigCodeBench Gradio evaluator."

      if ! bigcodebench.evaluate \
        --execution gradio \
        --split instruct \
        --subset hard \
        --samples "$SAMPLES" \
        --save_pass_rate \
        --pass_k 1 \
        --parallel "$(nproc)" \
        2>&1 | tee "$OUT/bigcodebench-evaluate-gradio.log"; then

        echo "WARN: BigCodeBench remote evaluation failed"
      fi
    else
      echo "WARN: Skipping BigCodeBench execution."
      echo "Reason: no supported local Docker evaluator available."
      echo "Set ALLOW_REMOTE_BCB=1 to use remote Gradio execution."
      echo "Set ALLOW_UNSANDBOXED_BCB=1 to execute generated code on host."
    fi
  fi

  echo
  echo "Building Markdown report"

  python "$OUT/helper.py" report \
    --recipe "$RECIPE_PATH" \
    --recipe-info "$OUT/recipe-info.json" \
    --base-url "$BASE_URL" \
    --out-dir "$OUT" \
    --report "$REPORT" \
    2>&1 | tee "$OUT/make-report.log"

  find "$OUT" -type f | sort | tee "$OUT/files.txt" >/dev/null

  echo
  echo "Done"
  echo "$REPORT"
}

main "$@" 2>&1 | tee -a "$OUT/run.log"
exit "${PIPESTATUS[0]}"
