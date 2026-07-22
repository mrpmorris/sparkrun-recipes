#!/usr/bin/env python3
"""Optimise a sparkrun recipe for single-stream generation speed.

Usage:
    ./Optimise.sh --recipe <filename-or-recipe-name>

Resolves the recipe from recipes/ (or via `sparkrun export recipe` for
registry recipes), then tunes its parameters by relaunching the workload
with overrides and benchmarking a ~1k-token prompt against the server.

Each iteration prints TTPT (total time per generated token, ms) and TPS
(generated tokens per second). Enumerated parameters are swept over all
supported values; numeric parameters are searched by binary splitting.
The best configuration is written to recipes/<name>--optimised.yaml and
a before/after summary is printed.

Beware: every iteration restarts the model. For large models that means
~10+ minutes of weight loading per iteration, so a full run can take
hours. Use --params to restrict which parameters are tuned, or
--dry-run to preview the plan.
"""

import argparse
import copy
import json
import os
import random
import subprocess
import sys
import time
import urllib.error
import urllib.request

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_DIR = os.path.join(SCRIPT_DIR, "recipes")

# Parameters with known enumerations: every supported value is tried.
# Unsupported values on a given build simply fail to launch and are skipped.
ENUM_PARAMS = {
    "attention_backend": ["flashinfer", "flash_attn", "triton"],
    "moe_backend": ["marlin", "triton", "cutlass"],
    "kv_cache_dtype": ["auto", "fp8"],
}

# name: (low, high, type, resolution, max_evals)
NUMERIC_PARAMS = {
    "gpu_memory_utilization": (0.70, 0.92, float, 0.02, 5),
    "max_num_seqs": (1, 64, int, 4, 5),
    "max_num_batched_tokens": (2048, 32768, int, 2048, 5),
    "num_speculative_tokens": (1, 24, int, 2, 5),  # inside speculative_config
}

# Never tuned: identity/capability settings, not performance knobs
# (max_model_len is deliberately excluded so the optimised recipe never
# loses context length).
UNTUNABLE = {
    "host", "port", "served_model_name", "model", "quantization",
    "max_model_len", "tensor_parallel", "pipeline_parallel",
    "load_format", "reasoning_parser", "tool_call_parser",
    "generation_config", "speculative_config",
}

WORDS = (
    "the of and to in a is that for it as was with be by on not he this are "
    "or his from at which but have an they you were her all she there would "
    "their we him been has when who will no more if out so said what its "
    "about into than them can only other time new some could these two may "
    "first then do any like my now over such our man me even most made "
    "after also did many before must through back years where much your way "
    "well down should because each just those people how too little state "
    "good very make world still own see men work long get here between both "
    "life being under never day same another know while last might us great "
    "old year off come since against go came right used take three"
).split()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run_cmd(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


# ----------------------------------------------------------------- recipe IO

def resolve_recipe(name):
    """Return (recipe_dict, yaml_path). Falls back to sparkrun export."""
    candidates = [
        name,
        os.path.join(RECIPES_DIR, name),
        os.path.join(RECIPES_DIR, name + ".yaml"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            with open(path) as f:
                return yaml.safe_load(f), os.path.abspath(path)

    log(f"'{name}' not found in {RECIPES_DIR}; trying sparkrun export recipe")
    base = name[:-5] if name.endswith(".yaml") else name
    r = run_cmd(["sparkrun", "export", "recipe", base])
    if r.returncode != 0:
        sys.exit(f"error: cannot resolve recipe '{name}':\n{r.stderr.strip()}")
    recipe = yaml.safe_load(r.stdout)
    # materialise it so sparkrun run has a file to launch
    path = os.path.join(RECIPES_DIR, os.path.basename(base) + ".yaml")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(r.stdout)
        log(f"exported registry recipe to {path}")
    return recipe, os.path.abspath(path)


def optimised_path(recipe_path):
    d, fname = os.path.split(recipe_path)
    stem = fname[:-5] if fname.endswith(".yaml") else fname
    return os.path.join(RECIPES_DIR, stem + "--optimised.yaml")


def write_optimised(recipe, overrides, out_path):
    out = copy.deepcopy(recipe)
    defaults = out.setdefault("defaults", {})
    for key, value in overrides.items():
        if key == "num_speculative_tokens":
            spec = json.loads(defaults["speculative_config"])
            spec["num_speculative_tokens"] = value
            defaults["speculative_config"] = json.dumps(
                spec, separators=(",", ":"))
        else:
            defaults[key] = value
    note = f"Auto-tuned by Optimise.py on {time.strftime('%Y-%m-%d')}"
    meta = out.setdefault("metadata", {})
    meta["description"] = (meta.get("description", "").rstrip(". ")
                           + f". {note}.").lstrip(". ")
    with open(out_path, "w") as f:
        yaml.safe_dump(out, f, sort_keys=False, width=100)


# ------------------------------------------------------------ server control

def stop_all():
    run_cmd(["sparkrun", "stop", "--all"])


def launch(recipe_path, overrides, port):
    args = ["sparkrun", "run", recipe_path, "--solo", "--no-follow",
            "--port", str(port)]
    for key, value in overrides.items():
        args += ["-o", f"{key}={value}"]
    r = run_cmd(args)
    if r.returncode != 0:
        log(f"  launch failed: {(r.stderr or r.stdout).strip()[-300:]}")
        return False
    return True


def wait_healthy(host, port, timeout):
    url = f"http://{host}:{port}/v1/models"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(10)
    return False


# ------------------------------------------------------------------ benchmark

def make_prompt(n_tokens, seed):
    rng = random.Random(seed)
    words = rng.choices(WORDS, k=int(n_tokens))
    return "Continue this text:\n" + " ".join(words)


def one_request(host, port, model, prompt_tokens, max_tokens, seed, timeout):
    body = json.dumps({
        "model": model,
        "prompt": make_prompt(prompt_tokens, seed),
        "max_tokens": max_tokens,
        "temperature": 0,
        "ignore_eos": True,
    }).encode()
    req = urllib.request.Request(
        f"http://{host}:{port}/v1/completions", data=body,
        headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    elapsed = time.monotonic() - t0
    usage = data["usage"]
    ctok = usage["completion_tokens"]
    if not ctok:
        return None
    return {
        "elapsed": elapsed,
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": ctok,
        "ttpt_ms": elapsed / ctok * 1000.0,
        "tps": ctok / elapsed,
    }


def benchmark(host, port, model, prompt_tokens, max_tokens, runs,
              timeout=600):
    """Warmup + N timed runs. Returns dict with median ttpt/tps, or None."""
    try:
        one_request(host, port, model, prompt_tokens, max_tokens,
                    seed=int(time.time()), timeout=timeout)  # warmup
        results = []
        for i in range(runs):
            r = one_request(host, port, model, prompt_tokens, max_tokens,
                            seed=int(time.time()) * 1000 + i, timeout=timeout)
            if r:
                log(f"    run {i + 1}/{runs}: prompt={r['prompt_tokens']}t "
                    f"gen={r['completion_tokens']}t "
                    f"TTPT={r['ttpt_ms']:.2f}ms TPS={r['tps']:.2f}")
                results.append(r)
    except Exception as exc:
        log(f"    benchmark error: {exc}")
        return None
    if not results:
        return None
    results.sort(key=lambda r: r["tps"])
    mid = results[len(results) // 2]
    return {"ttpt_ms": mid["ttpt_ms"], "tps": mid["tps"]}


# ------------------------------------------------------------------ tuning

class Tuner:
    def __init__(self, args, recipe, recipe_path, model, defaults):
        self.args = args
        self.recipe = recipe
        self.recipe_path = recipe_path
        self.model = model
        self.defaults = defaults
        self.cache = {}     # frozenset(config.items()) -> result-or-None
        self.evals = 0

    def evaluate(self, config, label):
        key = frozenset(config.items())
        if key in self.cache:
            log(f"  {label}: cached "
                + self.fmt(self.cache[key]))
            return self.cache[key]
        self.evals += 1
        log(f"  [{self.evals}] {label}: restarting server ...")
        stop_all()
        result = None
        overrides = self.expand(config)
        if launch(self.recipe_path, overrides, self.args.port):
            if wait_healthy(self.args.host, self.args.port,
                            self.args.health_timeout):
                result = benchmark(
                    self.args.host, self.args.port, self.model,
                    self.args.prompt_tokens, self.args.max_tokens,
                    self.args.runs)
            else:
                log("    server did not become healthy in time")
        log(f"  [{self.evals}] {label}: " + self.fmt(result))
        self.cache[key] = result
        return result

    def expand(self, config):
        """Translate virtual params (num_speculative_tokens) to overrides."""
        overrides = {}
        for key, value in config.items():
            if key == "num_speculative_tokens":
                spec = json.loads(self.defaults["speculative_config"])
                spec["num_speculative_tokens"] = value
                overrides["speculative_config"] = json.dumps(
                    spec, separators=(",", ":"))
            else:
                overrides[key] = value
        return overrides

    @staticmethod
    def fmt(result):
        if result is None:
            return "FAILED"
        return f"TTPT={result['ttpt_ms']:.2f}ms TPS={result['tps']:.2f}"

    # -- parameter discovery ------------------------------------------------

    def tunable_params(self):
        enums, numerics = [], []
        for key in self.defaults:
            if key in UNTUNABLE:
                continue
            if key in ENUM_PARAMS:
                enums.append(key)
            elif key in NUMERIC_PARAMS:
                numerics.append(key)
        if "speculative_config" in self.defaults:
            try:
                spec = json.loads(self.defaults["speculative_config"])
                if "num_speculative_tokens" in spec:
                    numerics.append("num_speculative_tokens")
            except (ValueError, TypeError):
                pass
        if self.args.params:
            wanted = {p.strip() for p in self.args.params.split(",")}
            enums = [p for p in enums if p in wanted]
            numerics = [p for p in numerics if p in wanted]
        return enums, numerics

    def current_value(self, param):
        if param == "num_speculative_tokens":
            return json.loads(
                self.defaults["speculative_config"])["num_speculative_tokens"]
        return self.defaults[param]

    # -- search strategies --------------------------------------------------

    def sweep_enum(self, param, best_config):
        current = self.defaults.get(param)
        best_val, best = current, self.evaluate(best_config, f"{param}={current}")
        for value in ENUM_PARAMS[param]:
            if value == current:
                continue
            result = self.evaluate({**best_config, param: value},
                                   f"{param}={value}")
            if result and (best is None or result["tps"] > best["tps"]):
                best_val, best = value, result
        return best_val, best

    def split_numeric(self, param, best_config):
        lo, hi, typ, resolution, max_evals = NUMERIC_PARAMS[param]
        current = typ(self.current_value(param))

        tested = {}

        def norm(v):
            v = max(lo, min(hi, v))
            return round(v, 2) if typ is float else int(round(v))

        def ev(v):
            v = norm(v)
            if v not in tested:
                result = self.evaluate({**best_config, param: v},
                                       f"{param}={v}")
                tested[v] = result["tps"] if result else None
            return tested[v]

        for v in dict.fromkeys([current, lo, hi]):  # dedupe, keep order
            ev(v)

        while len(tested) < max_evals:
            good = sorted(v for v, s in tested.items() if s is not None)
            if not good:
                break
            best_pt = max(good, key=lambda v: tested[v])
            idx = good.index(best_pt)
            gaps = []
            if idx > 0:
                gaps.append((good[idx - 1], best_pt))
            if idx < len(good) - 1:
                gaps.append((best_pt, good[idx + 1]))
            gaps = [(a, b) for a, b in gaps if (b - a) > resolution]
            if not gaps:
                break
            a, b = max(gaps, key=lambda g: g[1] - g[0])
            mid = norm((a + b) / 2)
            if mid in tested:
                break
            ev(mid)

        good = {v: s for v, s in tested.items() if s is not None}
        if not good:
            return current, None
        best_val = max(good, key=good.get)
        return best_val, {"tps": good[best_val],
                          "ttpt_ms": 1000.0 / good[best_val]}


# ----------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recipe", required=True,
                    help="recipe filename in recipes/, a path, or a registry recipe name")
    ap.add_argument("--prompt-tokens", type=int, default=1000)
    ap.add_argument("--max-tokens", type=int, default=256,
                    help="tokens generated per benchmark request")
    ap.add_argument("--runs", type=int, default=3,
                    help="timed requests per configuration (median is used)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--health-timeout", type=int, default=1800,
                    help="seconds to wait for the server after each restart")
    ap.add_argument("--params",
                    help="comma-separated list restricting which parameters are tuned")
    ap.add_argument("--dry-run", action="store_true",
                    help="show the tuning plan without running anything")
    ap.add_argument("--measure-only", action="store_true",
                    help="benchmark an already-running server and exit (no restarts)")
    args = ap.parse_args()

    recipe, recipe_path = resolve_recipe(args.recipe)
    defaults = recipe.get("defaults", {})
    model = defaults.get("served_model_name") or recipe["model"]
    log(f"recipe: {recipe_path}")
    log(f"model:  {model}")

    tuner = Tuner(args, recipe, recipe_path, model, defaults)

    if args.measure_only:
        result = benchmark(args.host, args.port, model, args.prompt_tokens,
                           args.max_tokens, args.runs)
        if result is None:
            sys.exit("error: benchmark failed — is the server running?")
        log(f"result: {Tuner.fmt(result)}")
        return

    enums, numerics = tuner.tunable_params()
    if not enums and not numerics:
        sys.exit("error: no tunable parameters found in this recipe's defaults")

    log("tuning plan (coordinate descent, one parameter at a time):")
    total = 1
    for p in enums:
        n = len(ENUM_PARAMS[p])
        total += n - 1
        log(f"  enum    {p}: all of {ENUM_PARAMS[p]}")
    for p in numerics:
        lo, hi, _, _, max_evals = NUMERIC_PARAMS[p]
        total += max_evals - 1
        log(f"  numeric {p}: binary split in [{lo}, {hi}], "
            f"<= {max_evals} evals")
    log(f"worst case ~{total} server restarts; large models load slowly, "
        f"so budget ~10-15 min per restart")
    if args.dry_run:
        return

    try:
        best_config = {}
        log("=== baseline ===")
        baseline = tuner.evaluate({}, "baseline")
        if baseline is None:
            sys.exit("error: baseline launch/benchmark failed — fix the "
                     "recipe before optimising")
        best = baseline

        for param in enums + numerics:
            log(f"=== tuning {param} ===")
            if param in ENUM_PARAMS:
                value, result = tuner.sweep_enum(param, best_config)
            else:
                value, result = tuner.split_numeric(param, best_config)
            if result and result["tps"] > best["tps"]:
                best = result
            if value != tuner.current_value(param):
                best_config[param] = value
            log(f"=== {param} -> {value} ({Tuner.fmt(result)}) ===")
    finally:
        log("stopping workload")
        stop_all()

    out_path = optimised_path(recipe_path)
    write_optimised(recipe, best_config, out_path)

    print()
    log(f"optimised recipe written: {out_path}")
    log(f"changed settings: {best_config if best_config else '(none - baseline was best)'}")
    log(f"before: TTPT={baseline['ttpt_ms']:.2f}ms TPS={baseline['tps']:.2f}")
    log(f"after:  TTPT={best['ttpt_ms']:.2f}ms TPS={best['tps']:.2f} "
        f"({(best['tps'] / baseline['tps'] - 1) * 100:+.1f}% TPS)")


if __name__ == "__main__":
    main()
