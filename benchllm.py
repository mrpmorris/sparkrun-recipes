#!/usr/bin/env python3
"""benchllm.py — Benchmark a sparkrun recipe: speed (TTFT, tokens/sec) and intelligence (lm-eval).

Run via ./benchllm.sh, which provisions the virtualenv and dependencies, e.g.:

  ./benchllm.sh --recipe MiaAI-Lab-Qwen3.6-27B-NVFP4.yaml
  ./benchllm.sh --recipe @sparkrun-transitional/qwen3-1.7b-vllm

--recipe accepts either a local recipe file or the name of a recipe from sparkrun's
registries (anything `sparkrun list` shows); names are resolved with
`sparkrun export recipe <name>`.

The script launches the recipe with `sparkrun run`, waits for the OpenAI-compatible
endpoint to come up, measures single-request speed (TTFT, prefill/generation tok/s)
across a ladder of prompt sizes up to the model max, runs lm-eval intelligence and
coding benchmarks, writes `benchmarks/<recipe stem>.md` next to this script, and
stops the workload again (guaranteed via atexit/signal traps).
"""

from __future__ import annotations

import argparse
import atexit
import concurrent.futures
import datetime as dt
import json
import math
import os
import random
import re
import shutil
import signal
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
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
    p.add_argument("--recipe", required=True,
                   help="Recipe file (resolved relative to this script) or the name of a recipe "
                        "from sparkrun's registries, e.g. @sparkrun-transitional/qwen3-1.7b-vllm "
                        "(see `sparkrun list`)")
    p.add_argument("--max-prompt", type=int, default=260_000, help="Ceiling for the prompt-size ladder (default 260000)")
    p.add_argument("--steps", type=int, default=8, help="Number of prompt-size steps up to the ceiling (default 8, i.e. max/8 increments)")
    p.add_argument("--output-tokens", type=int, default=256, help="Generation length for speed tests (default 256)")
    p.add_argument("--eval-tasks", default="mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp",
                   help="lm-eval tasks, each optionally with its own sample limit as task:limit. "
                        "MMLU has 57 subtasks and the limit applies per subtask, so it defaults to 10 "
                        "(= 570 questions). (default mmlu:10,gsm8k,arc_challenge,hellaswag,humaneval,mbpp)")
    p.add_argument("--eval-limit", type=int, default=100,
                   help="Samples per lm-eval task without an explicit task:limit, 0 = full run (default 100)")
    p.add_argument("--eval-concurrency", type=int, default=4, help="Concurrent lm-eval requests (default 4)")
    p.add_argument("--with-bfcl", action="store_true",
                   help="Run the BFCL v4 tool-calling benchmark (via EvalScope) against the recipe's "
                        "tools API. Requires the .benchllm-bfcl-venv that benchllm.sh builds for this flag.")
    p.add_argument("--bfcl-subsets",
                   default="simple_python,multiple,parallel,parallel_multiple,live_simple,live_multiple,irrelevance",
                   help="Comma-separated BFCL v4 subsets to run (default: non-live + live-simple, no API keys needed)")
    p.add_argument("--bfcl-limit", type=int, default=25,
                   help="Samples per BFCL subset, 0 = full (default 25)")
    p.add_argument("--ready-timeout", type=int, default=3600, help="Seconds to wait for the model endpoint (default 3600)")
    p.add_argument("--request-timeout", type=int, default=1800, help="Per-request read timeout in seconds (default 1800)")
    p.add_argument("--seed", type=int, default=0, help="Base seed for prompt generation (default 0)")
    p.add_argument("--skip-speed", action="store_true", help="Skip the speed benchmark")
    p.add_argument("--skip-eval", action="store_true", help="Skip the intelligence benchmark")
    p.add_argument("--force", action="store_true",
                   help="Re-run even if the report already exists (default: skip recipes "
                        "whose benchmarks/<stem>.md is already present).")
    p.add_argument("--cleanup", action="store_true",
                   help="Delete Hugging Face models downloaded for this run when the script "
                        "exits (models already in the HF cache at startup are kept). Lets a "
                        "batch run benchmark more models than the SSD can hold at once.")
    p.add_argument("--skip-run", action="store_true",
                   help="Don't launch or stop the model; benchmark an instance you started yourself "
                        "(e.g. with `sparkrun run <recipe> -o speculative_config=''`)")
    return p.parse_args()


@dataclass(frozen=True)
class Recipe:
    """A benchmark target: a local recipe file, or a recipe name from sparkrun's registries."""
    ref: str           # what sparkrun run/stop is given (file path, or registry recipe name)
    display: str       # short human-readable name for logs and the report title
    results_name: str  # directory name under bench-results/
    stem: str          # report file stem (benchmarks/<stem>.md)
    data: dict         # parsed recipe YAML


def resolve_recipe(arg: str, sparkrun: str) -> Recipe:
    """Resolve --recipe: a local file first, then a recipe name known to sparkrun."""
    for candidate in (Path(arg), SCRIPT_DIR / arg, SCRIPT_DIR / f"{arg}.yaml"):
        if candidate.is_file():
            path = candidate.resolve()
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return Recipe(ref=str(path), display=path.name,
                          results_name=path.name, stem=path.stem, data=data)
    # Not a file: ask sparkrun for the registry recipe of that name (as listed by `sparkrun list`).
    proc = subprocess.run([sparkrun, "export", "recipe", arg],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        detail = (proc.stderr.strip() or proc.stdout.strip()).splitlines()
        hint = f" ({detail[-1].strip()})" if detail else ""
        sys.exit(f"ERROR: recipe not found: {arg} — not a local file, and sparkrun does not "
                 f"know it{hint}. Pass a recipe YAML path or a name from `sparkrun list`.")
    data = yaml.safe_load(proc.stdout)
    if not isinstance(data, dict):
        sys.exit(f"ERROR: `sparkrun export recipe {arg}` did not return a recipe")
    safe = arg.lstrip("@").replace("/", "__")
    return Recipe(ref=arg, display=arg, results_name=safe, stem=safe, data=data)


def find_sparkrun() -> str:
    exe = shutil.which("sparkrun") or str(Path.home() / ".local" / "bin" / "sparkrun")
    if not Path(exe).is_file():
        sys.exit("ERROR: sparkrun executable not found (looked on PATH and in ~/.local/bin)")
    return exe


# ---------------------------------------------------------------------------
# --cleanup: delete HF models that this run had to download
# ---------------------------------------------------------------------------

HF_HUB = Path(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))) / "hub"


def hf_cached_models() -> set:
    """Names of the models-- snapshot dirs currently in the HF hub cache."""
    if not HF_HUB.is_dir():
        return set()
    return {d.name for d in HF_HUB.iterdir() if d.is_dir() and d.name.startswith("models--")}


def _dir_size_bytes(path: Path) -> int:
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            try:
                total += os.lstat(os.path.join(root, name)).st_size
            except OSError:
                pass
    return total


def cleanup_downloaded_models(preexisting: set) -> None:
    """atexit hook: remove every HF model cached after startup (i.e. downloaded
    by this run), keeping whatever was already on disk. Datasets are untouched."""
    new = sorted(hf_cached_models() - preexisting)
    if not new:
        log("--cleanup: no newly downloaded HF models to remove.")
        return
    freed = 0
    for name in new:
        path = HF_HUB / name
        size = _dir_size_bytes(path)
        log(f"--cleanup: removing {name} ({size / 1e9:.1f} GB)")
        shutil.rmtree(path, ignore_errors=True)
        lock = HF_HUB / ".locks" / name
        if lock.is_dir():
            shutil.rmtree(lock, ignore_errors=True)
        freed += size
    log(f"--cleanup: freed {freed / 1e9:.1f} GB ({len(new)} model(s) removed).")


# ---------------------------------------------------------------------------
# Workload lifecycle
# ---------------------------------------------------------------------------

class Workload:
    """Starts the recipe with sparkrun and guarantees it is stopped on exit."""

    def __init__(self, sparkrun: str, recipe: Recipe, log_path: Path):
        self.sparkrun = sparkrun
        self.recipe = recipe
        self.log_path = log_path
        self.stopped = False

    def start(self, timeout: int = 900) -> None:
        log(f"Launching workload: sparkrun run {self.recipe.display} --ensure --no-follow")
        with open(self.log_path, "ab") as f:
            proc = subprocess.run(
                [self.sparkrun, "run", self.recipe.ref, "--ensure", "--no-follow"],
                stdout=f, stderr=subprocess.STDOUT, timeout=timeout,
            )
        if proc.returncode != 0:
            sys.exit(f"ERROR: sparkrun run failed (exit {proc.returncode}); see {self.log_path}")
        atexit.register(self.stop)

    def stop(self) -> None:
        if self.stopped:
            return
        self.stopped = True
        log(f"Stopping workload: sparkrun stop {self.recipe.display}")
        try:
            with open(self.log_path, "ab") as f:
                subprocess.run(
                    [self.sparkrun, "stop", self.recipe.ref],
                    stdout=f, stderr=subprocess.STDOUT, timeout=300,
                )
        except Exception as exc:  # noqa: BLE001 - best-effort cleanup
            log(f"WARN: sparkrun stop failed: {exc}")


def probe_server_max_len(base_url: str):
    """Ask the server for its context window. vLLM reports max_model_len per model
    in /v1/models; other runtimes may not, in which case this returns None."""
    try:
        resp = requests.get(f"{base_url}/models", timeout=30)
        resp.raise_for_status()
        for entry in resp.json().get("data", []):
            v = entry.get("max_model_len")
            if v:
                return int(v)
    except Exception:  # noqa: BLE001 - probe is best-effort
        return None
    return None


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
        # Time per output token: mean inter-token latency for the tokens after the first.
        "tpot_s": (decode_time / (completion_tokens - 1))
                  if (decode_time and completion_tokens and completion_tokens > 1) else None,
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
        tpots = [r["tpot_s"] for r in results if r.get("tpot_s")]
        point.update({
            "prompt_tokens_mean": statistics.mean(prompt_counts) if prompt_counts else None,
            "ttft_mean_s": statistics.mean(ttfts) if ttfts else None,
            "ttft_p50_s": percentile(ttfts, 50),
            "ttft_p95_s": percentile(ttfts, 95),
            "tpot_mean_s": statistics.mean(tpots) if tpots else None,
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


def load_previous_speed(results_root: Path, current_outdir: Path):
    """With --skip-speed, reuse the newest earlier run's speed points so the report stays complete."""
    if not results_root.is_dir():
        return None, None
    for run_dir in sorted((d for d in results_root.iterdir() if d.is_dir() and d != current_outdir),
                          key=lambda d: d.name, reverse=True):
        points = []
        for f in run_dir.glob("speed-*.json"):
            try:
                p = json.loads(f.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            if p.get("ok") and p.get("concurrency", 1) == 1:
                points.append(p)
        if points:
            points.sort(key=lambda p: p["target_tokens"])
            return points, f"Speed section reused from earlier run {run_dir.name} (--skip-speed)."
    return None, None


def prompt_ladder(max_prompt: int, max_model_len, output_tokens: int, steps: int) -> tuple[list[int], list[str]]:
    """Geometric ladder: 256, then x4 each step (1024, 4096, 16384, ...). The ceiling is
    the usable prompt budget = max length minus the requested output tokens minus a small
    margin for tokenizer skew (the prompt is sized with o200k_base but the model may count
    a bit more). A top rung is added at exactly the budget so the ladder does not stop short
    of the context window."""
    warnings = []
    hard = max_model_len if max_model_len else max_prompt
    # Reserve output tokens + ~1% (min 256) for o200k_base vs model-tokenizer drift.
    margin = max(256, hard // 100)
    limit = hard - output_tokens - margin
    if max_prompt < limit:
        limit = max_prompt
    sizes = []
    size = 256
    while size <= limit:
        sizes.append(size)
        size *= 4
    # Add an exact top rung at the usable budget if the x4 ladder stopped short of it.
    if sizes and sizes[-1] < limit:
        sizes.append(limit)
        warnings.append(
            f"Top prompt rung capped at {limit} tokens (max length {hard} minus "
            f"{output_tokens} output tokens and {margin} tokenizer-skew margin).")
    return sizes, warnings


# ---------------------------------------------------------------------------
# Intelligence benchmark (lm-eval)
# ---------------------------------------------------------------------------

# Tasks whose evaluation executes model-generated code on this machine.
# lm-eval refuses to run them without an explicit opt-in flag.
CODE_TASKS = {"humaneval", "humaneval_plus", "humaneval_64", "mbpp", "mbpp_plus"}

TASK_DESCRIPTIONS = {
    "mmlu": "General knowledge across 57 academic subjects",
    "gsm8k": "Grade-school math word problems (multi-step reasoning)",
    "arc_challenge": "Hard science exam questions (reasoning)",
    "arc_easy": "Easy science exam questions",
    "hellaswag": "Commonsense sentence completion",
    "humaneval": "Coding: write Python functions that pass unit tests",
    "humaneval_plus": "Coding: HumanEval with extended unit tests",
    "mbpp": "Coding: basic Python programming problems, graded by unit tests",
    "mbpp_plus": "Coding: MBPP with extended unit tests",
    "winogrande": "Commonsense pronoun resolution",
    "ifeval": "Instruction following",
    "truthfulqa_mc2": "Resistance to common falsehoods",
    "bfcl": "Tool/function calling (BFCL v4 via EvalScope)",
}


def failure(task: str, log_path: Path, fallback: str) -> dict:
    """Build a structured failure record, extracting the server's real error from the log."""
    reason = fallback
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        text = ""
    # vLLM returns the true cause in the OpenAI-style error body echoed by lm-eval.
    m = re.findall(r'Status code:\s*(\d+),\s*Response text:\s*(\{.*\})', text)
    if m:
        code, body = m[-1]
        try:
            msg = json.loads(body).get("error", {}).get("message", body)
        except Exception:  # noqa: BLE001
            msg = body
        reason = f"HTTP {code} from inference server: {msg}"
    else:
        exc = re.findall(r'^(?:\w+\.)*\w*(?:Error|Exception):\s*.+$', text, re.MULTILINE)
        if exc:
            reason = exc[-1].strip()
    return {"task": task, "reason": reason[:400], "log": log_path.name,
            "description": TASK_DESCRIPTIONS.get(task, "")}


def run_lm_eval_task(task: str, base_url: str, model: str, tokenizer: str, limit: int,
                     concurrency: int, outdir: Path) -> tuple[list[dict], str | None]:
    """Run one lm-eval task. Returns (metric rows, error string or None)."""
    eval_dir = outdir / f"lm-eval-{task}"
    eval_dir.mkdir(parents=True, exist_ok=True)
    # model= is the API alias (served_model_name) and need not exist on the HF
    # Hub; the tokenizer must be loaded from the recipe's real model repo.
    model_args = (
        f"model={model},"
        f"tokenizer={tokenizer},"
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
    env = dict(os.environ)
    if task in CODE_TASKS:
        # pass@1 scoring executes model-generated code on this machine;
        # both the CLI flag and the HF metric env var are required opt-ins.
        cmd += ["--confirm_run_unsafe_code"]
        env["HF_ALLOW_CODE_EVAL"] = "1"

    log(f"lm-eval: {task} (limit={limit or 'full'})")
    log_path = outdir / f"lm-eval-{task}.log"
    with open(log_path, "wb") as f:
        proc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env)
    if proc.returncode != 0:
        return [], failure(task, log_path, f"exit code {proc.returncode}")

    result_files = sorted(eval_dir.rglob("results_*.json"), key=lambda p: p.stat().st_mtime)
    if not result_files:
        return [], failure(task, log_path, "produced no results JSON")
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
                         "n": n,
                         "description": TASK_DESCRIPTIONS.get(name, TASK_DESCRIPTIONS.get(task, ""))})
    return rows, None


# ---------------------------------------------------------------------------
# Tool-calling benchmark (BFCL v4 via EvalScope)
# ---------------------------------------------------------------------------

BFCL_RUNNER = '''\
import json, sys
from evalscope import TaskConfig, run_task

subsets = {subsets!r}
cfg = TaskConfig(
    model={model!r},
    api_url={api_url!r},
    api_key="EMPTY",
    eval_type="openai_api",
    datasets=["bfcl_v4"],
    dataset_args={{"bfcl_v4": {{
        "subset_list": subsets,
        "extra_params": {{"is_fc_model": True}},
    }}}},
    eval_batch_size={batch},
    limit={limit},
    work_dir={work_dir!r},
)
run_task(task_cfg=cfg)
print("BFCL_DONE")
'''


def _collect_bfcl_scores(node, out: list, overall_names=("bfcl_v4", "averageaccuracy")):
    """Recursively pull every {name, score, num} node from an EvalScope report."""
    if isinstance(node, dict):
        name = node.get("name")
        score = node.get("score")
        if isinstance(name, str) and isinstance(score, (int, float)):
            num = node.get("num") or node.get("count") or node.get("num_samples")
            out.append({"name": name, "score": score, "n": num,
                        "overall": name.lower() in overall_names})
        for v in node.values():
            _collect_bfcl_scores(v, out, overall_names)
    elif isinstance(node, list):
        for v in node:
            _collect_bfcl_scores(v, out, overall_names)


def run_bfcl(base_url: str, model: str, subsets: list, limit: int,
             outdir: Path) -> tuple[list[dict], str | None]:
    """Run BFCL v4 tool-calling eval through EvalScope. Returns (score rows, error or None)."""
    py = os.environ.get("BENCHLLM_BFCL_PYTHON")
    log_path = outdir / "bfcl.log"
    if not py or not Path(py).exists():
        return [], failure("bfcl", log_path,
                           "BFCL venv not available - run through benchllm.sh with --with-bfcl")
    work_dir = outdir / "bfcl"
    work_dir.mkdir(parents=True, exist_ok=True)
    runner = work_dir / "bfcl_runner.py"
    runner.write_text(BFCL_RUNNER.format(
        subsets=subsets, model=model, api_url=base_url,
        batch=8, limit=(limit or None), work_dir=str(work_dir)))

    log(f"BFCL: {len(subsets)} subset(s) (limit={limit or 'full'}) via EvalScope")
    with open(log_path, "wb") as f:
        proc = subprocess.run([py, str(runner)], stdout=f, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        return [], failure("bfcl", log_path, f"EvalScope exit code {proc.returncode}")

    reports = [p for p in work_dir.rglob("*.json") if "reports" in p.parts]
    if not reports:
        return [], failure("bfcl", log_path, "EvalScope produced no report JSON")
    collected: list[dict] = []
    for rf in sorted(reports, key=lambda p: p.stat().st_mtime):
        try:
            _collect_bfcl_scores(json.loads(rf.read_text(encoding="utf-8")), collected)
        except Exception:  # noqa: BLE001
            continue
    if not collected:
        return [], failure("bfcl", log_path, "could not parse scores from EvalScope report")

    seen, rows = set(), []
    for c in collected:
        if c["name"] in seen:
            continue
        seen.add(c["name"])
        rows.append(c)
    # Overall first, then the rest in the order they appeared.
    rows.sort(key=lambda r: (not r["overall"]))
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
        "| Prompt tokens | Server prompt tokens | TTFT s | TPOT ms | Prefill tok/s | Generation tok/s | Total s |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for p in points:
        if p["ok"]:
            tpot = p.get("tpot_mean_s")
            tpot_ms = tpot * 1000 if tpot is not None else None
            lines.append(
                f"| {p['target_tokens']} | {fmt(p.get('prompt_tokens_mean'), 0)} "
                f"| {fmt(p.get('ttft_mean_s'))} | {fmt(tpot_ms, 1)} | {fmt(p.get('prefill_tok_s_mean'), 1)} "
                f"| {fmt(p.get('decode_tok_s_mean'), 2)} | {fmt(p.get('wall_s'), 2)} |"
            )
        else:
            lines.append(f"| {p['target_tokens']} | | FAILED | | | | |")
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
    lines = [f"# {ctx['rec'].display} benchmark results", ""]
    lines += [f"Generated UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}", ""]

    lines += ["## Run", "", "| Key | Value |", "| --- | --- |"]
    for k, v in [
        ("Recipe", ctx["rec"].ref), ("Model", ctx["model_id"]),
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

    lines += ["## Speed vs prompt size (single request)", ""]
    lines += (["_Skipped (--skip-speed)._"] if ctx["ladder_points"] is None
              else speed_table(ctx["ladder_points"]) if ctx["ladder_points"]
              else ["_None._"])
    lines += ["", "TTFT = time to first token. TPOT = time per output token (mean inter-token "
              "latency after the first token). Prefill tok/s = prompt tokens / TTFT. "
              "Generation tok/s = output tokens per second after the first token.", ""]

    failures = ctx.get("eval_failures") or []
    lines += ["## Intelligence (lm-eval)", ""]
    if ctx["eval_rows"] is None:
        lines += ["_Skipped (--skip-eval)._", ""]
    else:
        succeeded = {r["task"] for r in ctx["eval_rows"]}
        failed = {f["task"] for f in failures}
        lines += [f"{len(succeeded)} task(s) completed, {len(failed)} failed.", ""]
        if ctx["eval_rows"]:
            lines += ["| Task | Description | Metric | Value | Stderr | Samples |",
                      "| --- | --- | --- | --- | --- | --- |"]
            for r in ctx["eval_rows"]:
                lines.append(f"| {r['task']} | {r.get('description', '')} | {r['metric']} "
                             f"| {fmt(r['value'], 4)} | {fmt(r['stderr'], 4)} | {fmt(r['n'], 0)} |")
            lines.append("")

    lines += ["## Tool calling (BFCL v4 via EvalScope)", ""]
    if not ctx.get("with_bfcl"):
        lines += ["_Skipped (pass --with-bfcl to run)._", ""]
    elif ctx.get("bfcl_rows"):
        lines += ["Berkeley Function Calling Leaderboard v4 — exercises the recipe's real tool-calling "
                  "path (OpenAI `tools` API + the recipe's tool_call_parser / auto-tool-choice). "
                  "Score is accuracy (0-1); OVERALL is BFCL's weighted aggregate.", "",
                  "| Subset / Category | Score | Samples |",
                  "| --- | --- | --- |"]
        for r in ctx["bfcl_rows"]:
            name = f"**{r['name']}**" if r.get("overall") else r["name"]
            lines.append(f"| {name} | {fmt(r['score'], 4)} | {fmt(r.get('n'), 0)} |")
        lines.append("")
    else:
        lines += ["_No scores (see Failed benchmarks / bfcl.log)._", ""]

    if failures:
        lines += ["### Failed benchmarks", "",
                  "These benchmarks could not complete as the model is currently served — a failure "
                  "here is itself a result: the model/config could not perform this evaluation. "
                  "Multiple-choice tasks (acc / acc_norm) request token log-probabilities from the "
                  "inference server; generative tasks do not.", "",
                  "| Task | Description | Reason | Log |",
                  "| --- | --- | --- | --- |"]
        for f in failures:
            lines.append(f"| {f['task']} | {f.get('description', '')} "
                         f"| {f['reason']} | {f['log']} |")
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

    sparkrun = find_sparkrun()
    rec = resolve_recipe(args.recipe, sparkrun)

    # Skip entirely if this recipe's report already exists (don't launch or download).
    existing_report = SCRIPT_DIR / "benchmarks" / f"{rec.stem}.md"
    if existing_report.exists() and not args.force:
        log(f"Report already exists, skipping: {existing_report} (delete it to re-run).")
        return

    recipe = rec.data
    defaults = recipe.get("defaults") or {}
    model_id = recipe.get("model", "")
    served = defaults.get("served_model_name") or model_id
    port = int(defaults.get("port", 8000))
    max_model_len = defaults.get("max_model_len")
    max_model_len = int(max_model_len) if max_model_len else None
    base_url = f"http://127.0.0.1:{port}/v1"

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = SCRIPT_DIR / "bench-results" / rec.results_name / ts
    outdir.mkdir(parents=True, exist_ok=True)
    report_dir = SCRIPT_DIR / "benchmarks"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{rec.stem}.md"
    log(f"Recipe: {rec.display} | model {served} | port {port} | artifacts {outdir}")

    warnings: list[str] = []
    if args.eval_limit > 0 or ":" in args.eval_tasks:
        warnings.append(f"lm-eval ran with sample limits (default {args.eval_limit}, per task/subtask; "
                        f"tasks: {args.eval_tasks}); scores are comparative samples, "
                        "not full-benchmark numbers.")

    # Make Ctrl+C / SIGTERM run atexit handlers (stops the workload).
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda s, f: sys.exit(128 + s))

    if args.cleanup:
        if args.skip_run:
            log("--cleanup: ignored with --skip-run (won't delete weights an external instance may be using).")
        else:
            preexisting_models = hf_cached_models()
            log(f"--cleanup: {len(preexisting_models)} HF model(s) already cached; "
                "models downloaded for this run will be deleted at exit.")
            atexit.register(cleanup_downloaded_models, preexisting_models)

    workload = Workload(sparkrun, rec, outdir / "sparkrun.log")
    if args.skip_run:
        log("--skip-run: benchmarking an externally-managed instance (won't launch or stop it).")
    else:
        workload.start()
    wait_for_ready(base_url, args.ready_timeout)
    warmup(base_url, served)

    # Trust the running server over the recipe: registry recipes often omit
    # max_model_len, and the ladder must not exceed the real context window.
    server_len = probe_server_max_len(base_url)
    if server_len:
        if max_model_len is None:
            log(f"Server reports max_model_len={server_len} (recipe does not set one).")
            max_model_len = server_len
        elif server_len < max_model_len:
            warnings.append(f"Recipe max_model_len={max_model_len} but the server reports "
                            f"{server_len}; using the server value.")
            max_model_len = server_len

    ladder_points = None
    eval_rows = None
    eval_failures: list[dict] = []
    bfcl_rows = None
    try:
        if not args.skip_speed:
            sizes, ladder_warnings = prompt_ladder(args.max_prompt, max_model_len,
                                                   args.output_tokens, args.steps)
            warnings += ladder_warnings
            log(f"Prompt ladder: {sizes}")
            ladder_points = [
                run_speed_point(base_url, served, size, 1, args.output_tokens,
                                args.request_timeout, args.seed, outdir)
                for size in sizes
            ]
            for p in ladder_points:
                if p["failed"]:
                    warnings.append(
                        f"Speed point {p['target_tokens']} tokens failed: {'; '.join(p['errors'])}")
        else:
            ladder_points, reuse_note = load_previous_speed(
                SCRIPT_DIR / "bench-results" / rec.results_name, outdir)
            if reuse_note:
                warnings.append(reuse_note)

        if not args.skip_eval:
            eval_rows = []
            for spec in [t.strip() for t in args.eval_tasks.split(",") if t.strip()]:
                task, sep, lim = spec.partition(":")
                limit = int(lim) if sep else args.eval_limit
                rows, err = run_lm_eval_task(task, base_url, served, model_id or served,
                                             limit, args.eval_concurrency, outdir)
                eval_rows += rows
                if err:
                    eval_failures.append(err)
                    log(f"  FAILED {task}: {err['reason']}")

        if args.with_bfcl:
            subsets = [s.strip() for s in args.bfcl_subsets.split(",") if s.strip()]
            bfcl_rows, bfcl_err = run_bfcl(base_url, served, subsets, args.bfcl_limit, outdir)
            if bfcl_err:
                eval_failures.append(bfcl_err)
                log(f"  FAILED bfcl: {bfcl_err['reason']}")
    finally:
        if not args.skip_run:
            workload.stop()
        write_report(report_path, {
            "args": args, "rec": rec, "recipe": recipe, "defaults": defaults,
            "model_id": model_id, "served": served, "base_url": base_url,
            "outdir": outdir, "host": host_info(),
            "ladder_points": ladder_points,
            "eval_rows": eval_rows, "eval_failures": eval_failures, "warnings": warnings,
            "bfcl_rows": bfcl_rows, "with_bfcl": args.with_bfcl,
            "duration_s": time.monotonic() - t_start,
        })


if __name__ == "__main__":
    main()
