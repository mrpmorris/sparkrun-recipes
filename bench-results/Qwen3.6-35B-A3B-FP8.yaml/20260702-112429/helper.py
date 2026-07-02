import argparse, concurrent.futures, json, os, statistics, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests, yaml
try:
    import tiktoken
    ENC = tiktoken.get_encoding("o200k_base")
except Exception:
    ENC = None

def jdump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2), encoding="utf-8")

def parse_recipe(args):
    r = yaml.safe_load(Path(args.recipe).read_text(encoding="utf-8")) or {}
    d = r.get("defaults") or {}
    info = {"model": r.get("model"), "runtime": r.get("runtime"), "container": r.get("container"),
            "port": d.get("port", 8000), "host": d.get("host"),
            "max_model_len": d.get("max_model_len"), "gpu_memory_utilization": d.get("gpu_memory_utilization"),
            "max_num_batched_tokens": d.get("max_num_batched_tokens"), "max_num_seqs": d.get("max_num_seqs"),
            "kv_cache_dtype": d.get("kv_cache_dtype"), "attention_backend": d.get("attention_backend"),
            "tool_call_parser": d.get("tool_call_parser"), "reasoning_parser": d.get("reasoning_parser"),
            "speculative_config": d.get("speculative_config")}
    jdump(args.out, info)

def wait_model(args):
    url = args.base_url.rstrip("/") + "/v1/models"
    deadline = time.time() + args.timeout
    last_error, last_ids = None, []
    while time.time() < deadline:
        try:
            payload = requests.get(url, timeout=10).json()
            ids = [x.get("id") for x in payload.get("data", []) if isinstance(x, dict) and x.get("id")]
            last_ids = ids
            print(f"models: {ids}", flush=True)
            if args.model in ids:
                jdump(args.out, {"base_url": args.base_url, "expected_model": args.model, "matched_model": args.model, "models": ids, "raw": payload})
                return
        except Exception as ex:
            last_error = repr(ex)
            print(f"not ready: {last_error}", flush=True)
        time.sleep(args.poll)
    jdump(args.out, {"base_url": args.base_url, "expected_model": args.model, "matched_model": None, "models": last_ids, "last_error": last_error})
    raise SystemExit(1)

def pct(vals, p):
    vals = sorted(x for x in vals if x is not None)
    if not vals: return None
    k = (len(vals) - 1) * p / 100
    f, c = int(k), min(int(k) + 1, len(vals) - 1)
    return vals[f] if f == c else vals[f] + (vals[c] - vals[f]) * (k - f)

def est_tokens(text):
    return (len(ENC.encode(text)), "tiktoken_o200k_base") if ENC else (max(1, len(text.split())), "word_count")

def post_stream(base_url, payload):
    variants = [payload, {k:v for k,v in payload.items() if k != "ignore_eos"}, {k:v for k,v in payload.items() if k not in ("ignore_eos", "stream_options")}]
    last = None
    for body in variants:
        try:
            r = requests.post(base_url.rstrip("/") + "/v1/chat/completions", json=body, stream=True, timeout=900)
            if r.status_code < 400: return r
            last = f"{r.status_code}: {r.text[:1000]}"; r.close()
        except Exception as ex:
            last = repr(ex)
    raise RuntimeError(last)

def one_speed(i, base_url, model, input_words, max_tokens):
    prompt = "Benchmark prompt. " + ("word " * input_words) + f"\nRequest {i}. Continue with plain text until stopped."
    payload = {"model": model, "messages": [{"role":"user", "content":prompt}], "temperature":0, "max_tokens":max_tokens, "stream":True, "stream_options":{"include_usage":True}, "ignore_eos":True}
    start = time.perf_counter(); first = None; parts = []; usage = {}
    with post_stream(base_url, payload) as r:
        for line in r.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "): continue
            data = line[6:]
            if data == "[DONE]": break
            obj = json.loads(data)
            if obj.get("usage"): usage = obj["usage"]
            choices = obj.get("choices") or []
            if choices:
                chunk = ((choices[0].get("delta") or {}).get("content") or "")
                if chunk:
                    if first is None: first = time.perf_counter()
                    parts.append(chunk)
    end = time.perf_counter(); text = "".join(parts)
    toks = usage.get("completion_tokens"); estimated_by = None; estimated = False
    if toks is None:
        toks, estimated_by = est_tokens(text); estimated = True
    return {"request": i, "latency_s": end-start, "ttft_s": None if first is None else first-start, "completion_tokens": toks, "prompt_tokens": usage.get("prompt_tokens"), "total_tokens": usage.get("total_tokens"), "token_count_estimated": estimated, "estimated_by": estimated_by, "chars": len(text)}

def speed(args):
    base_url, model = os.environ["BASE_URL"], os.environ["MODEL"]
    start = time.perf_counter(); rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(one_speed, i, base_url, model, args.input_words, args.max_tokens) for i in range(args.requests)]
        for f in concurrent.futures.as_completed(futs):
            rows.append(f.result()); print(f"done {len(rows)}/{args.requests}", flush=True)
    wall = time.perf_counter() - start
    lats = [r["latency_s"] for r in rows]; ttfts = [r["ttft_s"] for r in rows if r["ttft_s"] is not None]
    out_toks = sum(r["completion_tokens"] for r in rows); estimated = any(r["token_count_estimated"] for r in rows)
    warnings = ["Server did not return completion_tokens for at least one request. Output tok/s is estimated."] if estimated else []
    summary = {"model": model, "base_url": base_url, "requests": args.requests, "concurrency": args.concurrency, "input_words": args.input_words, "max_tokens": args.max_tokens, "wall_time_s": wall, "output_tokens": out_toks, "output_tokens_per_s": out_toks / max(0.001, wall), "latency_mean_s": statistics.mean(lats), "latency_p50_s": pct(lats,50), "latency_p95_s": pct(lats,95), "ttft_mean_s": statistics.mean(ttfts) if ttfts else None, "ttft_p50_s": pct(ttfts,50), "ttft_p95_s": pct(ttfts,95), "token_count_estimated": estimated, "warnings": warnings, "results": sorted(rows, key=lambda x:x["request"])}
    jdump(args.out, summary); print(json.dumps(summary, indent=2))

def read_json(path):
    try: return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception: return None

def fmt(v):
    if v is None: return ""
    if isinstance(v, float): return f"{v:.4f}"
    if isinstance(v, bool): return "yes" if v else "no"
    return str(v).replace("\n", " ").replace("|", "\\|")

def table(headers, rows):
    if not rows: return "\n_None._\n"
    return "\n" + "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"]*len(headers)) + " |"] + ["| " + " | ".join(fmt(x) for x in r) + " |" for r in rows]) + "\n"

def report(args):
    out = Path(args.out_dir); recipe = Path(args.recipe); info = read_json(args.recipe_info) or {}
    speed_rows = []
    for name in ["speed-single.json", "speed-concurrency8.json"]:
        d = read_json(out/name)
        if d: speed_rows.append([name.replace("speed-", "").replace(".json", ""), d.get("requests"), d.get("concurrency"), d.get("output_tokens"), d.get("output_tokens_per_s"), d.get("ttft_mean_s"), d.get("ttft_p50_s"), d.get("ttft_p95_s"), d.get("latency_mean_s"), d.get("latency_p50_s"), d.get("latency_p95_s"), d.get("token_count_estimated")])
    lm_rows = []
    for p in sorted(out.glob("lm-eval*/**/results_*.json")):
        d = read_json(p) or {}; res = d.get("results", {})
        for task, metrics in sorted(res.items()):
            if isinstance(metrics, dict):
                for metric, val in sorted(metrics.items()):
                    if metric != "alias" and not metric.endswith("_stderr") and (isinstance(val, (int,float,str,bool)) or val is None):
                        lm_rows.append([task, metric, val, metrics.get(metric + "_stderr"), str(p.relative_to(out))])
    bcb_rows = []
    for pat in ["**/*pass_at_k.json", "**/*eval_results.json"]:
        for p in sorted(out.glob(pat)):
            d = read_json(p)
            if isinstance(d, dict):
                for k, v in sorted(d.items()):
                    if isinstance(v, (int,float,str,bool)) or v is None: bcb_rows.append([k, v, str(p.relative_to(out))])
                    elif isinstance(v, dict):
                        for k2, v2 in sorted(v.items()):
                            if isinstance(v2, (int,float,str,bool)) or v2 is None: bcb_rows.append([f"{k}.{k2}", v2, str(p.relative_to(out))])
    warns = []
    for f in [out/"speed-single.json", out/"speed-concurrency8.json"]:
        d = read_json(f)
        if d: warns += d.get("warnings") or []
    if not any((out/n).exists() for n in ["bigcodebench-evaluate-docker.log", "bigcodebench-evaluate-host.log", "bigcodebench-evaluate-gradio.log"]):
        warns.append("BigCodeBench code execution did not run. Pass@1 may be absent. Generated samples may exist.")
    files = [str(p.relative_to(out)) for p in sorted(out.rglob("*")) if p.is_file()]
    md = [f"# {recipe.name} benchmark results", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "", "## Run", table(["Key", "Value"], [["Recipe", str(recipe)], ["Model", info.get("model")], ["Runtime", info.get("runtime")], ["Container", info.get("container")], ["Base URL", args.base_url], ["Output dir", str(out)]]), "## Recipe settings", table(["Setting", "Value"], [[k,v] for k,v in info.items() if v is not None]), "## Speed", table(["Run", "Requests", "Concurrency", "Output tokens", "Output tok/s", "TTFT mean s", "TTFT p50 s", "TTFT p95 s", "Latency mean s", "Latency p50 s", "Latency p95 s", "Tokens estimated"], speed_rows), "## Intelligence, lm-eval", table(["Task", "Metric", "Value", "Stderr", "File"], lm_rows), "## Coding, BigCodeBench", table(["Metric", "Value", "File"], bcb_rows), "## Warnings", table(["Warning"], [[w] for w in sorted(set(warns))]), "## Output files", table(["File"], [[f] for f in files]), ""]
    Path(args.report).write_text("\n".join(md), encoding="utf-8"); print(args.report)

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("parse"); a.add_argument("--recipe", required=True); a.add_argument("--out", required=True); a.set_defaults(fn=parse_recipe)
    a = sub.add_parser("wait"); a.add_argument("--base-url", required=True); a.add_argument("--model", required=True); a.add_argument("--timeout", type=int, required=True); a.add_argument("--poll", type=int, required=True); a.add_argument("--out", required=True); a.set_defaults(fn=wait_model)
    a = sub.add_parser("speed"); a.add_argument("--requests", type=int, required=True); a.add_argument("--concurrency", type=int, required=True); a.add_argument("--input-words", type=int, default=1024); a.add_argument("--max-tokens", type=int, default=512); a.add_argument("--out", required=True); a.set_defaults(fn=speed)
    a = sub.add_parser("report"); a.add_argument("--recipe", required=True); a.add_argument("--recipe-info", required=True); a.add_argument("--base-url", required=True); a.add_argument("--out-dir", required=True); a.add_argument("--report", required=True); a.set_defaults(fn=report)
    args = p.parse_args(); args.fn(args)
if __name__ == "__main__": main()
