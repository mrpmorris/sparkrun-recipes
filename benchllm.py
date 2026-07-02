#!/usr/bin/env python3
"""benchllm.py — Benchmark a sparkrun recipe: speed (TTFT, tokens/sec) and intelligence (lm-eval).

Run via ./benchllm.sh, which provisions the virtualenv and dependencies, e.g.:

  ./benchllm.sh --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml

The script launches the recipe with `sparkrun run`, waits for the OpenAI-compatible
endpoint to come up, measures speed across prompt sizes and concurrency levels,
runs lm-eval intelligence benchmarks, writes `<recipe stem>.md` next to the recipe,
and stops the workload again (guaranteed via atexit/signal traps).
"""

from __future__ import annotations

import argparse
import atexit
import concurrent.futures
import datetime as dt
import json
import math
import random
import shutil
import signal
import statistics
import subprocess
import sys
import time
from pathlib import Path

import requests
import tiktoken
import yaml

ENC = tiktoken.get_encoding("o200k_base")
SCRIPT_DIR = Path(__file__).resolve().parent

# Common English words used as prompt filler. Prompts are salted and randomized
# per request so vLLM prefix caching cannot skew the timings.
VOCAB = (
    "the quick brown fox jumps over lazy dog time person year way day thing man "
    "world life hand part child eye woman place work week case point government "
    "company number group problem fact leave call good new first last long great "
    "little own other old right big high different small large next early young "
    "important few public bad same able house service friend father power hour "
    "game line end member law car city community name president team minute idea "
    "kid body information back parent face others level office door health person "
    "art war history party result change morning reason research girl guy moment "
    "air teacher force education foot boy age policy process music market sense "
    "nation plan college interest death experience effect use class control care "
    "field development role effort rate heart drug show leader light voice wife "
    "whole police mind finally return free military price report less according "
    "decision explain son hope even develop view relationship carry town road"
).split()


def log(msg: str) -> None:
    print(f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Benchmark a sparkrun recipe (speed + intelligence).")
    p.add_argument("--recipe", required=True, help="Recipe filename or path (resolved relative to this script)")
    p.add_argument("--max-prompt", type=int, default=260_000, help="Ceiling for the prompt-size ladder (default 260000)")
    p.add_argument("--concurrency", default="1,4,8,16", help="Comma list of concurrency levels for the sweep (default 1,4,8,16)")
    p.add_argument("--sweep-sizes", default="1024,32768", help="Prompt sizes used for the concurrency sweep (default 1024,32768)")
    p.add_argument("--output-tokens", type=int, default=256, help="Generation length for speed tests (default 256)")
    p.add_argument("--eval-tasks", default="mmlu,gsm8k,arc_challenge,hellaswag", help="lm-eval tasks (default mmlu,gsm8k,arc_challenge,hellaswag)")
    p.add_argument("--eval-limit", type=int, default=100, help="Samples per lm-eval task, 0 = full run (default 100)")
    p.add_argument("--eval-concurrency", type=int, default=4, help="Concurrent lm-eval requests (default 4)")
    p.add_argument("--ready-timeout", type=int, default=3600, help="Seconds to wait for the model endpoint (default 3600)")
    p.add_argument("--request-timeout", type=int, default=1800, help="Per-request read timeout in seconds (default 1800)")
    p.add_argument("--seed", type=int, default=0, help="Base seed for prompt generation (default 0)")
    p.add_argument("--skip-speed", action="store_true", help="Skip the speed benchmark")
    p.add_argument("--skip-eval", action="store_true", help="Skip the intelligence benchmark")
    return p.parse_args()


def resolve_recipe(arg: str) -> Path:
    for candidate in (Path(arg), SCRIPT_DIR / arg, SCRIPT_DIR / f"{arg}.yaml"):
        if candidate.is_file():
            return candidate.resolve()
    sys.exit(f"ERROR: recipe not found: {arg}")


def find_sparkrun() -> str:
    exe = shutil.which("sparkrun") or str(Path.home() / ".local" / "bin" / "sparkrun")
    if not Path(exe).is_file():
        sys.exit("ERROR: sparkrun executable not found (looked on PATH and in ~/.local/bin)")
    return exe


# ---------------------------------------------------------------------------
# Workload lifecycle
# ---------------------------------------------------------------------------

class Workload:
    """Starts the recipe with sparkrun and guarantees it is stopped on exit."""

    def __init__(self, sparkrun: str, recipe_path: Path, log_path: Path):
        self.sparkrun = sparkrun
        self.recipe_path = recipe_path
        self.log_path = log_path
        self.stopped = False

    def start(self, timeout: int = 900) -> None:
        log(f"Launching workload: sparkrun run {self.recipe_path.name} --ensure --no-follow")
        with open(self.log_path, "ab") as f:
            proc = subprocess.run(
                [self.sparkrun, "run", str(self.recipe_path), "--ensure", "--no-follow"],
                stdout=f, stderr=subprocess.STDOUT, timeout=timeout,
            )
        if proc.returncode != 0:
            sys.exit(f"ERROR: sparkrun run failed (exit {proc.returncode}); see {self.log_path}")
        atexit.register(self.stop)

    def stop(self) -> None:
        if self.stopped:
            return
        self.stopped = True
        log(f"Stopping workload: sparkrun stop {self.recipe_path.name}")
        try:
            with open(self.log_path, "ab") as f:
                subprocess.run(
                    [self.sparkrun, "stop", str(self.recipe_path)],
                    stdout=f, stderr=subprocess.STDOUT, timeout=300,
                )
        except Exception as exc:  # noqa: BLE001 - best-effort cleanup
            log(f"WARN: sparkrun stop failed: {exc}")


def wait_for_ready(base_url: str, timeout: int) -> None:
    log(f"Waiting for {base_url}/models (timeout {timeout}s)...")
    deadline = time.monotonic() + timeout
    last_note = 0.0
    while time.monotonic() < deadline:
        try:
            r = requests.get(f"{base_url}/models", timeout=5)
            if r.status_code == 200 and r.json().get("data"):
                log("Endpoint is ready.")
                return
        except requests.RequestException:
            pass
        if time.monotonic() - last_note > 60:
            remaining = int(deadline - time.monotonic())
            log(f"  ...still waiting ({remaining}s left)")
            last_note = time.monotonic()
        time.sleep(5)
    sys.exit("ERROR: model endpoint did not become ready in time")


def warmup(base_url: str, model: str, timeout: int = 600) -> None:
    log("Sending warm-up request...")
    r = requests.post(
        f"{base_url}/chat/completions",
        json={"model": model, "messages": [{"role": "user", "content": "Reply with the word ok."}],
              "max_tokens": 8, "temperature": 0},
        timeout=(30, timeout),
    )
    r.raise_for_status()
    log("Warm-up complete.")


# ---------------------------------------------------------------------------
# Speed benchmark
# ---------------------------------------------------------------------------

def build_prompt(target_tokens: int, rng: random.Random) -> str:
    """Build a unique prompt of ~target_tokens (o200k_base count)."""
    header = (
        f"Benchmark {rng.getrandbits(64):016x}: read the text below carefully, "
        "then reply with the single word ok.\n\n"
    )
    ids = ENC.encode(header)
    while len(ids) < target_tokens:
        chunk = " ".join(rng.choice(VOCAB) for _ in range(4096))
        ids += ENC.encode(" " + chunk)
    return ENC.decode(ids[:target_tokens])


def stream_request(base_url: str, model: str, prompt: str, max_tokens: int,
                   timeout: int, use_ignore_eos: bool = True) -> dict:
    """One streaming chat completion. Returns timing + token metrics."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if use_ignore_eos:
        payload["ignore_eos"] = True  # vLLM extension: guarantees exactly max_tokens output

    t0 = time.perf_counter()
    r = requests.post(f"{base_url}/chat/completions", json=payload, stream=True, timeout=(30, timeout))
    if r.status_code == 400 and use_ignore_eos:
        # Server rejected the ignore_eos extension - retry without it.
        return stream_request(base_url, model, prompt, max_tokens, timeout, use_ignore_eos=False)
    r.raise_for_status()

    ttft = None
    usage = None
    chunk_count = 0
    for line in r.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        obj = json.loads(data)
        if obj.get("usage"):
            usage = obj["usage"]
        for choice in obj.get("choices", []):
            delta = choice.get("delta") or {}
            if delta.get("content") or delta.get("reasoning_content") or delta.get("reasoning"):
                chunk_count += 1
                if ttft is None:
                    ttft = time.perf_counter() - t0
    t_end = time.perf_counter()

    prompt_tokens = (usage or {}).get("prompt_tokens")
    completion_tokens = (usage or {}).get("completion_tokens") or chunk_count
    total = t_end - t0
    decode_time = (t_end - t0 - ttft) if ttft is not None else None
    return {
        "start": t0,
        "end": t_end,
        "ttft_s": ttft,
        "total_s": total,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "decode_tok_s": (completion_tokens / decode_time) if decode_time and decode_time > 0 else None,
        "prefill_tok_s": (prompt_tokens / ttft) if prompt_tokens and ttft else None,
    }


def percentile(values: list[float], p: float):
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * p / 100.0
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] + (s[c] - s[f]) * (k - f)


def run_speed_point(base_url: str, model: str, size: int, concurrency: int,
                    output_tokens: int, timeout: int, seed: int, outdir: Path) -> dict:
    log(f"Speed point: {size} prompt tokens x concurrency {concurrency}")
    prompts = [
        build_prompt(size, random.Random(f"{seed}/{size}/{concurrency}/{i}/{time.time_ns()}"))
        for i in range(concurrency)
    ]
    results: list[dict] = []
    errors: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(stream_request, base_url, model, pr, output_tokens, timeout) for pr in prompts]
        for fut in concurrent.futures.as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001 - collect failures per request
                errors.append(f"{type(exc).__name__}: {exc}"[:300])

    point: dict = {"target_tokens": size, "concurrency": concurrency,
                   "output_tokens": output_tokens, "ok": len(results), "failed": len(errors),
                   "errors": errors[:3]}
    if results:
        ttfts = [r["ttft_s"] for r in results if r["ttft_s"] is not None]
        wall = max(r["end"] for r in results) - min(r["start"] for r in results)
        total_out = sum(r["completion_tokens"] or 0 for r in results)
        prompt_counts = [r["prompt_tokens"] for r in results if r["prompt_tokens"]]
        decode_rates = [r["decode_tok_s"] for r in results if r["decode_tok_s"]]
        prefill_rates = [r["prefill_tok_s"] for r in results if r["prefill_tok_s"]]
        point.update({
            "prompt_tokens_mean": statistics.mean(prompt_counts) if prompt_counts else None,
            "ttft_mean_s": statistics.mean(ttfts) if ttfts else None,
            "ttft_p50_s": percentile(ttfts, 50),
            "ttft_p95_s": percentile(ttfts, 95),
            "decode_tok_s_mean": statistics.mean(decode_rates) if decode_rates else None,
            "prefill_tok_s_mean": statistics.mean(prefill_rates) if prefill_rates else None,
            "aggregate_tok_s": (total_out / wall) if wall > 0 else None,
            "wall_s": wall,
        })
        log(f"  ok={point['ok']} failed={point['failed']} "
            f"ttft_mean={point['ttft_mean_s']:.3f}s agg={point['aggregate_tok_s']:.1f} tok/s")
    else:
        log(f"  ALL {concurrency} requests failed: {errors[:1]}")
    (outdir / f"speed-{size}tok-c{concurrency}.json").write_text(json.dumps(point, indent=2))
    return point


def prompt_ladder(max_prompt: int, max_model_len, output_tokens: int) -> tuple[list[int], list[str]]:
    warnings = []
    limit = max_prompt
    if max_model_len:
        model_cap = max_model_len - output_tokens - 512
        if model_cap < limit:
            warnings.append(
                f"Prompt ladder truncated to {model_cap} tokens by recipe max_model_len={max_model_len}.")
            limit = model_cap
    sizes = []
    s = 1024
    while s < limit:
        sizes.append(s)
        s *= 2
    if limit >= 1024 and (not sizes or sizes[-1] != limit):
        sizes.append(limit)
    return sizes, warnings


# ---------------------------------------------------------------------------
# Intelligence benchmark (lm-eval)
# ---------------------------------------------------------------------------

def run_lm_eval_task(task: str, base_url: str, model: str, limit: int,
                     concurrency: int, outdir: Path) -> tuple[list[dict], str | None]:
    """Run one lm-eval task. Returns (metric rows, error string or None)."""
    eval_dir = outdir / f"lm-eval-{task}"
    eval_dir.mkdir(parents=True, exist_ok=True)
    model_args = (
        f"model={model},"
        f"base_url={base_url}/completions,"
        f"num_concurrent={concurrency},"
        f"max_retries=3,"
        f"max_length=8192,"
        f"tokenized_requests=False"
    )
    cmd = [sys.executable, "-m", "lm_eval",
           "--model", "local-completions",
           "--model_args", model_args,
           "--tasks", task,
           "--output_path", str(eval_dir),
           "--batch_size", "1"]
    if limit > 0:
        cmd += ["--limit", str(limit)]

    log(f"lm-eval: {task} (limit={limit or 'full'})")
    log_path = outdir / f"lm-eval-{task}.log"
    with open(log_path, "wb") as f:
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        return [], f"lm-eval {task} failed (exit {proc.returncode}); see {log_path.name}"

    result_files = sorted(eval_dir.rglob("results_*.json"), key=lambda p: p.stat().st_mtime)
    if not result_files:
        return [], f"lm-eval {task} produced no results JSON"
    data = json.loads(result_files[-1].read_text())

    entries = {}
    for source in (data.get("groups") or {}, data.get("results") or {}):
        for name, metrics in source.items():
            if name == task:
                entries[name] = metrics
    if not entries:  # fall back to whatever was produced
        entries = dict(list((data.get("results") or {}).items())[:20])

    n_samples = data.get("n-samples") or {}
    rows = []
    for name, metrics in entries.items():
        n = (n_samples.get(name) or {}).get("effective")
        for key, value in metrics.items():
            if key in ("alias", "sample_len") or "_stderr" in key or not isinstance(value, (int, float)):
                continue
            if "," in key:
                base, variant = key.split(",", 1)
                stderr = metrics.get(f"{base}_stderr,{variant}")
            else:
                stderr = metrics.get(f"{key}_stderr")
            rows.append({"task": name, "metric": key, "value": value,
                         "stderr": stderr if isinstance(stderr, (int, float)) else None,
                         "n": n})
    return rows, None


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def fmt(v, digits=3):
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    return str(v)


def speed_table(points: list[dict]) -> list[str]:
    lines = [
        "| Prompt tokens | Concurrency | OK | Failed | Server prompt tokens | TTFT mean s | TTFT p50 s | TTFT p95 s | Prefill tok/s | Decode tok/s (per req) | Aggregate output tok/s |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for p in points:
        lines.append(
            f"| {p['target_tokens']} | {p['concurrency']} | {p['ok']} | {p['failed']} "
            f"| {fmt(p.get('prompt_tokens_mean'), 0)} | {fmt(p.get('ttft_mean_s'))} "
            f"| {fmt(p.get('ttft_p50_s'))} | {fmt(p.get('ttft_p95_s'))} "
            f"| {fmt(p.get('prefill_tok_s_mean'), 1)} | {fmt(p.get('decode_tok_s_mean'), 2)} "
            f"| {fmt(p.get('aggregate_tok_s'), 2)} |"
        )
    return lines


def host_info() -> dict:
    info = {}
    for key, cmd in {
        "uname": ["uname", "-srmo"],
        "gpu": ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
    }.items():
        try:
            info[key] = subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip()
        except Exception:  # noqa: BLE001
            info[key] = "unknown"
    return info


def write_report(report_path: Path, ctx: dict) -> None:
    a = ctx["args"]
    lines = [f"# {ctx['recipe_path'].name} benchmark results", ""]
    lines += [f"Generated UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}", ""]

    lines += ["## Run", "", "| Key | Value |", "| --- | --- |"]
    for k, v in [
        ("Recipe", ctx["recipe_path"]), ("Model", ctx["model_id"]),
        ("Served model name", ctx["served"]), ("Runtime", ctx["recipe"].get("runtime", "")),
        ("Container", ctx["recipe"].get("container", "")), ("Base URL", ctx["base_url"]),
        ("Host", ctx["host"]["uname"]), ("GPU", ctx["host"]["gpu"]),
        ("Output dir", ctx["outdir"]),
        ("Command", " ".join(sys.argv)),
        ("Total duration", f"{ctx['duration_s']:.0f} s"),
    ]:
        lines.append(f"| {k} | {v} |")
    lines.append("")

    lines += ["## Recipe settings", "", "| Setting | Value |", "| --- | --- |"]
    for k, v in ctx["defaults"].items():
        lines.append(f"| {k} | {v} |")
    lines.append("")

    if ctx["ladder_points"] is not None:
        lines += ["## Speed vs prompt size (concurrency 1)", ""]
        lines += speed_table(ctx["ladder_points"]) if ctx["ladder_points"] else ["_None._"]
        lines.append("")
        lines += ["## Concurrency scaling", ""]
        if ctx["sweep_points"]:
            for size, points in ctx["sweep_points"].items():
                lines += [f"### Prompt size {size} tokens", ""]
                lines += speed_table(points)
                lines.append("")
        else:
            lines += ["_None._", ""]

    if ctx["eval_rows"] is not None:
        lines += ["## Intelligence (lm-eval)", ""]
        if ctx["eval_rows"]:
            lines += ["| Task | Metric | Value | Stderr | Samples |", "| --- | --- | --- | --- | --- |"]
            for r in ctx["eval_rows"]:
                lines.append(f"| {r['task']} | {r['metric']} | {fmt(r['value'], 4)} "
                             f"| {fmt(r['stderr'], 4)} | {fmt(r['n'], 0)} |")
        else:
            lines += ["_None._"]
        lines.append("")

    lines += ["## Warnings", ""]
    if ctx["warnings"]:
        lines += [f"- {w}" for w in ctx["warnings"]]
    else:
        lines += ["_None._"]
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Report written: {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    t_start = time.monotonic()

    recipe_path = resolve_recipe(args.recipe)
    recipe = yaml.safe_load(recipe_path.read_text(encoding="utf-8"))
    defaults = recipe.get("defaults") or {}
    model_id = recipe.get("model", "")
    served = defaults.get("served_model_name") or model_id
    port = int(defaults.get("port", 8000))
    max_model_len = defaults.get("max_model_len")
    max_model_len = int(max_model_len) if max_model_len else None
    max_num_seqs = defaults.get("max_num_seqs")
    base_url = f"http://127.0.0.1:{port}/v1"

    concurrency_levels = [int(x) for x in str(args.concurrency).split(",") if x.strip()]
    sweep_sizes = [int(x) for x in str(args.sweep_sizes).split(",") if x.strip()]

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = SCRIPT_DIR / "bench-results" / recipe_path.name / ts
    outdir.mkdir(parents=True, exist_ok=True)
    report_path = recipe_path.with_name(recipe_path.stem + ".md")
    log(f"Recipe: {recipe_path.name} | model {served} | port {port} | artifacts {outdir}")

    warnings: list[str] = []
    if max_num_seqs and max(concurrency_levels, default=0) > int(max_num_seqs):
        warnings.append(
            f"Recipe max_num_seqs={max_num_seqs} is below the highest tested concurrency "
            f"({max(concurrency_levels)}); excess requests queue server-side, inflating TTFT.")
    if args.eval_limit > 0:
        warnings.append(f"lm-eval ran with --limit {args.eval_limit} (per task/subtask); "
                        "scores are comparative samples, not full-benchmark numbers.")

    # Make Ctrl+C / SIGTERM run atexit handlers (stops the workload).
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: sys.exit(128 + s))

    sparkrun = find_sparkrun()
    workload = Workload(sparkrun, recipe_path, outdir / "sparkrun.log")
    workload.start()
    wait_for_ready(base_url, args.ready_timeout)
    warmup(base_url, served)

    ladder_points = sweep_points = None
    eval_rows = None
    try:
        if not args.skip_speed:
            sizes, ladder_warnings = prompt_ladder(args.max_prompt, max_model_len, args.output_tokens)
            warnings += ladder_warnings
            log(f"Prompt ladder: {sizes}")
            ladder_points = [
                run_speed_point(base_url, served, size, 1, args.output_tokens,
                                args.request_timeout, args.seed, outdir)
                for size in sizes
            ]
            sweep_points = {}
            for size in sweep_sizes:
                if max_model_len and size > max_model_len - args.output_tokens - 512:
                    warnings.append(f"Sweep size {size} skipped: exceeds model context window.")
                    continue
                sweep_points[size] = [
                    run_speed_point(base_url, served, size, c, args.output_tokens,
                                    args.request_timeout, args.seed, outdir)
                    for c in concurrency_levels
                ]
            for p in ladder_points + [pt for pts in sweep_points.values() for pt in pts]:
                if p["failed"]:
                    warnings.append(
                        f"Speed point {p['target_tokens']} tok x c{p['concurrency']}: "
                        f"{p['failed']} request(s) failed. {'; '.join(p['errors'])}")

        if not args.skip_eval:
            eval_rows = []
            for task in [t.strip() for t in args.eval_tasks.split(",") if t.strip()]:
                rows, err = run_lm_eval_task(task, base_url, served, args.eval_limit,
                                             args.eval_concurrency, outdir)
                eval_rows += rows
                if err:
                    warnings.append(err)
    finally:
        workload.stop()
        write_report(report_path, {
            "args": args, "recipe_path": recipe_path, "recipe": recipe, "defaults": defaults,
            "model_id": model_id, "served": served, "base_url": base_url,
            "outdir": outdir, "host": host_info(),
            "ladder_points": ladder_points, "sweep_points": sweep_points,
            "eval_rows": eval_rows, "warnings": warnings,
            "duration_s": time.monotonic() - t_start,
        })


if __name__ == "__main__":
    main()
