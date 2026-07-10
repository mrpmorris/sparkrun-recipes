# Work instructions: get the failed benchllm benchmarks working

Audience: an agent working on sparky1 in `/home/mrpmorris/sparkrun-recipes`.
Every failure below was root-caused from logs on 2026-07-10; follow the playbooks in order.
Do the tasks ONE AT A TIME, top to bottom. Never run two benchmarks at the same time.

---

## Ground rules

1. **Work directory:** everything happens in `/home/mrpmorris/sparkrun-recipes`.
2. **Run a benchmark:** `./benchllm.sh --recipe <local-yaml-or-@registry/name> --cleanup`
   - A recipe is SKIPPED if `benchmarks/<stem>.md` already exists. Add `--force` to re-run
     (or delete that one `.md` file — never delete anything else).
   - `<stem>` for a local file `foo.yaml` is `foo`. For `@eugr/x` it is `eugr__x`.
3. **Registry recipes are read-only.** To change one, export it to a local file first:
   ```
   ~/.local/bin/sparkrun export recipe @eugr/NAME > eugr__NAME.yaml
   ```
   Then edit the local file and run `./benchllm.sh --recipe eugr__NAME.yaml --force --cleanup`.
   Name the file exactly `<builder>__<name>.yaml` so results land under the same stem.
4. **Fast iteration flags** (a full run takes 30–90+ min):
   - Server-starts-at-all check: `--skip-bfcl --skip-eval --max-prompt 1024 --steps 1`
   - BFCL only (for the GLM crash): `--skip-eval --skip-speed`
   - Cap a slow task: `--eval-tasks "gsm8k:100,humaneval:0,mbpp:0"` (N = sample cap, 0 = full)
   - Other useful flags: `--eval-concurrency N` (default 4), `--ready-timeout S` (default 3600).
   After a fix works, do one final FULL run (default flags + `--force --cleanup`) so the
   report regenerates properly.
5. **Before every run, check memory.** This host runs `earlyoom`, which SIGTERMs the model
   server when MemAvailable ≤ 2% — the benchmark then fails with misleading errors.
   ```
   awk '/MemAvailable/ {printf "%.1f GiB available\n", $2/1048576}' /proc/meminfo
   docker ps        # must show no leftover benchmark containers
   ```
   Need ≥ 80 GiB available before starting. While a run is loading a model, watch:
   ```
   tail -f /var/log/syslog | grep earlyoom
   ```
   If you ever see `earlyoom ... sending SIGTERM`, the failure that follows is an
   out-of-memory kill, NOT a bug in the model/runtime — record that and stop tuning
   other knobs.
6. **Capturing a startup crash:** benchllm reads the server log from inside the container
   at `/tmp/sparkrun_serve.log` but does not save it. Until you apply patch A below, you can
   capture it manually while benchllm waits for the endpoint:
   ```
   docker ps --format '{{.Names}}' | grep _solo     # find the container
   docker exec <name> sh -c 'tail -f /tmp/sparkrun_serve.log' | tee /tmp/startup-capture.log
   ```
7. **Expected skips — do not chase these.** Tasks mmlu, arc_challenge and hellaswag need
   `echo+logprobs` on `/v1/completions`. The `atlas` and `llama-cpp` runtimes do not support
   that, so on those runtimes those 3 tasks always report
   "skipped: server does not support echo+logprobs". A fully healthy atlas/llama-cpp run =
   **3 task(s) completed** (gsm8k, humaneval, mbpp) + 3 skips. vLLM runs should reach 6/6.
8. Note: the batch ran with `--cleanup`, so model weights were deleted — first re-runs
   re-download (GLM ≈ 20 GB, gpt-oss-120b ≈ 65 GB, diffusion-gemma bf16 ≈ 50 GB).
9. Do not `git commit` or push anything. Do not edit files under `bench-results/`.

---

## Task 0 — three small benchllm.py patches (do these first)

**A. Persist the serve log on startup failures** (this is why two failures below have no
known root cause). Run `grep -n "StartupError" benchllm.py`, find the `except StartupError`
block that writes the FAILED report, and inside it — using the run-output-directory variable
already in scope there — add:
```python
(outdir / "serve-startup.log").write_text(read_serve_log(200_000) or "<serve log unavailable>", encoding="utf-8")
```
(Adjust `outdir` to the variable actually in scope.) Verify: run any still-broken recipe and
confirm `bench-results/<recipe>/<timestamp>/serve-startup.log` appears with vLLM output in it.

**B. Fix the TTFT=None crash** (broke the nemotron-3-puzzle speed test). In `run_speed_point`
(~line 615) this line crashes when the model streams no recognizable text deltas:
```python
        log(f"  ok={point['ok']} failed={point['failed']} "
            f"ttft_mean={point['ttft_mean_s']:.3f}s agg={point['aggregate_tok_s']:.1f} tok/s")
```
Replace with:
```python
        ttft_txt = f"{point['ttft_mean_s']:.3f}s" if point['ttft_mean_s'] is not None else "n/a"
        agg_txt = f"{point['aggregate_tok_s']:.1f}" if point['aggregate_tok_s'] is not None else "n/a"
        log(f"  ok={point['ok']} failed={point['failed']} ttft_mean={ttft_txt} agg={agg_txt} tok/s")
```

**C. Raise lm-eval retries** (helps Task 5's intermittent NaN 400s). In `run_lm_eval_task`
(~line 815) change `max_retries=3,` to `max_retries=8,`.

---

## Task 1 — the four diffusion-gemma recipes (recipe templating bug) — EASY

**Recipes:** `@eugr/diffusion-gemma-bf16`, `-bf16-thinking`, `-nvfp4`, `-nvfp4-thinking`
**Symptom:** `vllm serve: error: argument --diffusion-config/-dc: Value {{"canvas_length":256}} cannot be converted`
**Cause:** the recipe command contains `'{{"canvas_length":256}}'`. The doubled `{{ }}` is
never collapsed to single braces, so vLLM receives invalid JSON. Three arguments are affected:
`--diffusion-config`, `--override-generation-config`, `--default-chat-template-kwargs`.

**Steps (do bf16 first, then repeat for the other three):**
1. `~/.local/bin/sparkrun export recipe @eugr/diffusion-gemma-bf16 > eugr__diffusion-gemma-bf16.yaml`
2. Edit the file: in the `command:` block change every `{{` to `{` and `}}` to `}` **only inside
   the three quoted JSON arguments** (leave `{max_model_len}`-style single-brace placeholders alone).
3. Quick check: `./benchllm.sh --recipe eugr__diffusion-gemma-bf16.yaml --force --skip-bfcl --skip-eval --max-prompt 1024 --steps 1`
   - If sparkrun/benchllm errors while *rendering* the command (KeyError/ValueError mentioning
     `canvas_length`), the renderer does treat `{}` as placeholders. Fallback: move each JSON blob
     into `defaults:` (e.g. `diffusion_config: '{"canvas_length":256}'`) and reference it in the
     command as `--diffusion-config '{diffusion_config}'`.
4. When the server starts, run the full benchmark: `./benchllm.sh --recipe eugr__diffusion-gemma-bf16.yaml --force --cleanup`
5. Success = `benchmarks/eugr__diffusion-gemma-bf16.md` no longer says `Status: FAILED`.

---

## Task 2 — qwen__qwen3.6-27b-fp8-mtp-atlas (endpoint never ready) — EASY TO TRY

**Recipe:** local file `qwen__qwen3.6-27b-fp8-mtp-atlas.yaml`
**Symptom:** "model endpoint did not become ready in time" (1 h wait).
**Best lead:** its near-identical twin `unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml` DID start, and
the only structural difference is the twin sets an env var this recipe is missing. Also this
recipe's own description says "32k context" but the command passes `--max-seq-len 262144`.

**Steps, in order — test after each with the quick-check flags from Ground rule 4:**
1. Add to the yaml (top level, same as the unsloth twin):
   ```yaml
   env:
     ATLAS_KV_OVERCOMMIT: '1'
   ```
2. If still not ready: change `--max-seq-len 262144` to `--max-seq-len 32768` (matches its own
   description; 262k fp8 KV at util 0.90 may not fit without overcommit).
3. While it waits, capture the ATLAS startup log (Ground rule 6) — whatever it prints last is
   the real blocker; include it in your report.
4. On success run the full suite. Expected best case per Ground rule 7: 3 completed + 3 skips.

---

## Task 3 — nvidia__qwen3.6-27b-nvfp4-mtp-vllm (killed by earlyoom during load)

**Recipe:** local file `nvidia__qwen3.6-27b-nvfp4-mtp-vllm.yaml`
**Symptom:** report says "Engine core initialization failed", but syslog shows earlyoom
SIGTERM'd `VLLM::EngineCore` at 2026-07-09 01:05:19 — host memory exhaustion, not a vLLM bug.

**Steps:**
1. Confirm ≥ 80 GiB MemAvailable and no leftover containers (Ground rule 5), then simply
   re-run with `--force --cleanup` while watching the earlyoom tail. It may just pass on an
   idle machine.
2. If earlyoom fires again during load, lower the footprint in the yaml `defaults:` and retry
   after each single change:
   - `gpu_memory_utilization: 0.7` → `0.6`
   - `max_model_len: 262144` → `131072`
   - `max_num_batched_tokens: 16384` → `8192`
3. If it still dies, record the exact earlyoom syslog lines and stop — that means this config
   cannot fit alongside the host's 2% MemAvailable floor, and the decision belongs to Peter.

---

## Task 4 — unsloth deepseek-v4-flash-671b GGUF (killed by earlyoom mid-eval)

**Recipe:** local file `unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml`
**Symptom:** llama-server got SIGTERM twice at 03:07 (earlyoom, MemAvailable ≤ 2%); gsm8k then
failed with connection-refused. The quant is 90.9 GB and the recipe passes `--no-mmap`, which
loads all 90.9 GB as non-reclaimable anonymous memory → MemAvailable collapses.

**Steps:**
1. In the yaml, **delete the `--no-mmap` line**. With mmap (llama.cpp default) the weights are
   file-backed and reclaimable, so MemAvailable stays healthy and earlyoom stays quiet.
2. Re-run capped, this model decodes at only ~3–4 tok/s and full gsm8k would blow the 2 h
   eval watchdog anyway:
   ```
   ./benchllm.sh --recipe unsloth__deepseek-v4-flash-671b-gguf-udiq2m-llama-cpp.yaml \
     --force --cleanup --eval-concurrency 2 \
     --eval-tasks "mmlu:10,gsm8k:100,arc_challenge:0,hellaswag,humaneval:0,mbpp:100"
   ```
3. Watch the earlyoom tail throughout. Success per Ground rule 7 = gsm8k/humaneval/mbpp
   complete, 3 echo+logprobs skips are expected.
4. If decode is so slow even 100 samples exceeds 2 h, reduce further (gsm8k:50) and note the
   tok/s in your report.

---

## Task 5 — official__qwen3.6-27b-fp8-mtp-vllm (NaN logprobs → mmlu + arc failed)

**Recipe:** registry `@official/qwen3.6-27b-fp8-mtp-vllm` (export per Ground rule 3)
**Symptom:** HTTP 400 "Out of range float values are not JSON compliant: nan" on loglikelihood
(echo+logprobs) requests. Intermittent — hellaswag hit 77 of them and still passed via retries.
The non-MTP twin recipe passed 6/6, so the NaN comes from the MTP speculative config.

**Steps, in order:**
1. Patch C from Task 0 (max_retries 3→8) may alone be enough, since the NaN is intermittent.
   Re-run just the failing tasks first:
   `./benchllm.sh --recipe @official/qwen3.6-27b-fp8-mtp-vllm --force --skip-bfcl --skip-speed --eval-tasks "mmlu:10,arc_challenge:0"`
2. If NaN still kills them: export the recipe, and in `defaults:` change
   ```yaml
   speculative_config: '{"method": "mtp", "num_speculative_tokens": 2}'
   ```
   to
   ```yaml
   speculative_config: '{"method": "mtp", "num_speculative_tokens": 2, "disable_logprobs": false}'
   ```
   (vLLM's speculative config has a `disable_logprobs` switch controlling whether real
   logprobs are computed during spec decoding.) Re-run step 1's command against the local yaml.
3. If NaN persists after both: this vLLM build cannot produce valid logprobs under MTP.
   Document that mmlu/arc must be excluded for MTP recipes (the non-MTP twin already provides
   those scores) — do not keep tuning.
4. Finish with a full run so the report regenerates cleanly.

---

## Task 6 — unsloth__qwen3.6-27b-nvfp4-mtp-atlas (generation degrades under load)

**Recipe:** local file `unsloth__qwen3.6-27b-nvfp4-mtp-atlas.yaml`
**Symptom:** the server starts fine, but under sustained concurrent generation each request
gets slower (5 s → 36 s by sample ~300) until the client times out; gsm8k was killed at the 2 h
cap and humaneval/mbpp died on timeouts. Single requests still worked afterwards (the speed
ladder even completed a 257k-token prefill), so it is a concurrency/scheduler degradation.
The serve log shows repeated `finish_sequence: blocking response send failed (receiver dropped)`.

**Steps — one change at a time, testing with `--force --skip-bfcl --skip-speed --eval-tasks "gsm8k:100"`:**
1. No yaml change: add `--eval-concurrency 1`. If gsm8k now completes at a steady pace, the
   ATLAS scheduler mishandles concurrent generation — report that and run the full suite with
   `--eval-concurrency 1`.
2. If it still degrades: remove `--speculative` and `--num-drafts 1` from the yaml (the
   dropped-receiver warnings point at the speculative path).
3. If still degrading: change `--max-seq-len 262144` → `32768`.
4. If still degrading: remove `--enable-prefix-caching`.
5. Success = gsm8k:100 completes with per-request times that do NOT trend upward; then full run
   (expect 3 completed + 3 skips).

---

## Task 7 — eugr__glm-4.7-flash-awq (vLLM crash: AWQ + MLA prefill)

**Recipe:** registry `@eugr/glm-4.7-flash-awq` (export per Ground rule 3)
**Symptom:** ~10 s into the first BFCL request the engine dies:
`AttributeError: 'ColumnParallelLinear' object has no attribute 'weight'` in
`mla_attention.py:_compute_prefill_context` (`kv_c_normed.to(self.kv_b_proj.weight.dtype)`).
AWQ-quantized layers store `qweight`, not `weight`; the MLA chunked-prefill context path
assumes an unquantized `kv_b_proj`. This is a vLLM code bug in the `vllm-node` image build.

**Fast repro loop:** `./benchllm.sh --recipe <yaml> --force --skip-eval --skip-speed` — the
crash (or its absence) shows within seconds of the endpoint becoming ready. Follow the serve
log per Ground rule 6 to see whether the AttributeError still appears.

**Steps, in order:**
1. Export the recipe. In `defaults:` set `max_num_batched_tokens: 4096` → `32768` and
   `max_num_seqs: 64` → `8`. The crashing function only runs when a prefill is split into
   chunks; a bigger batched-token budget makes chunking (and the crash) far less likely for
   benchmark-sized prompts. Run the repro loop.
2. If it still crashes, additionally append `--enable-chunked-prefill=False` to the command
   block (if this vLLM build rejects that flag, remove it again — the serve log will show an
   argparse error immediately).
3. If it still crashes, the fix must come from a newer vLLM. Check whether the upstream fix
   exists: search the vLLM GitHub issues/commits for
   `ColumnParallelLinear object has no attribute 'weight'` + MLA + AWQ. If fixed upstream,
   report which commit/version is needed so Peter can rebuild the `vllm-node` image — do not
   rebuild images yourself.
4. Alternative worth one attempt: a different quantization of the same model. Search
   Hugging Face for a GLM-4.7-Flash checkpoint in FP8 or GPTQ; if one exists, copy the exported
   yaml under a NEW name, change `model:` (and drop AWQ-specific bits), and note it as a
   substitute recipe rather than a fix.

---

## Task 8 — eugr__openai-gpt-oss-120b (engine init failed, cause unknown)

**Recipe:** registry `@eugr/openai-gpt-oss-120b` (export per Ground rule 3)
**Symptom:** "Engine core initialization failed" during startup. The real traceback was never
saved (that is what Task 0 patch A fixes). No earlyoom/driver events in syslog for this one.
It uses an experimental MXFP4 build (`vllm-node-mxfp4` container, CUTLASS backend, FlashInfer
attention, fp8 KV).

**Steps:**
1. FIRST apply Task 0 patch A, then re-run the quick check
   (`--force --skip-bfcl --skip-eval --max-prompt 1024 --steps 1`) purely to capture
   `serve-startup.log`. Read the last ~100 lines; the branch below depends on the actual error.
2. Branch on what the log says (change ONE thing in the exported yaml per attempt):
   - CUDA out of memory → `gpu_memory_utilization: 0.8` → `0.7`, then `0.6`.
   - Error mentioning CUTLASS / mxfp4 kernels → change `--mxfp4-backend CUTLASS` to
     `--mxfp4-backend TRITON` (check `vllm serve --help` inside the container for valid
     values: `docker run --rm --entrypoint vllm <container-image> serve --help | grep -A3 mxfp4`).
   - Error mentioning FlashInfer → remove `--attention-backend FLASHINFER` and the
     `VLLM_USE_FLASHINFER_MOE_MXFP4_MXFP8` env line.
   - Error mentioning fp8 KV cache → remove `--kv-cache-dtype fp8`.
3. Whatever you find, paste the decisive traceback lines into your report — that log is the
   deliverable even if no flag combination works.

---

## Task 9 — official qwen3-vl-embedding-8b and qwen3-vl-reranker-8b — DO NOT FIX, RECLASSIFY

**Symptom:** HF download stalled ~12 s in; run hit the 2 h cap.
**But the real finding:** both recipes serve vLLM with `--runner pooling` — an
embedding/reranker server has NO `/v1/chat/completions` or text generation. benchllm's speed
test, lm-eval tasks and BFCL are all generative: **these two recipes can never produce results
with the current benchllm**, even after the download issue is fixed.

**Steps:**
1. Leave their FAILED report files in place so the batch keeps skipping them, and state in
   your report that they need either exclusion from the batch or a new embedding-benchmark
   mode in benchllm (Peter's decision).
2. Only if asked to fix the download stall anyway: pre-download with hf_transfer disabled,
   then re-run —
   ```
   HF_HUB_ENABLE_HF_TRANSFER=0 ~/.local/bin/hf download Qwen/Qwen3-VL-Embedding-8B
   ```
   (if `hf` is missing, use `.benchllm-venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-VL-Embedding-8B')"`).

---

## Task 10 — eugr__qwen3.5-397b-int4-autoround — DO NOT ATTEMPT

The weights are ~211 GB and sparkrun's own sizing shows 120.4 GB per-GPU needed vs 102.8 GB
usable, with 0 GB left for KV cache. It cannot fit on this 121 GB GB10, and the 2 h cap
expired before the download even finished. Leave its FAILED report in place; record
"impossible on this hardware" in your report.

---

## Task 11 — nvidia__nemotron-3-puzzle-75b speed test (benchllm bug, evals already passed)

All 6 eval tasks passed; only the speed ladder failed, via the TTFT=None crash fixed by
Task 0 patch B. Root cause of TTFT staying None: the model's stream contained no
`content`/`reasoning_content`/`reasoning` deltas that `stream_request` (~line 538) recognizes.

**Steps:**
1. Apply patch B, then: `./benchllm.sh --recipe nvidia__nemotron-3-puzzle-75b-a9b-nvfp4-vllm.yaml --force --skip-bfcl --skip-eval`
2. If the ladder now reports `ttft_mean=n/a`, the stream shape is still unrecognized: add a
   temporary debug print inside `stream_request`'s delta loop to dump `delta.keys()` for the
   first few chunks, run one speed point, and report which key carries the text (then add that
   key to the `if delta.get(...)` condition and remove the debug print).

---

## Reporting back

For each task, report: recipe, what you changed (exact yaml/py diff), the single command you
verified with, outcome (pass/fail + the relevant log lines), and the final report status line
from `benchmarks/<stem>.md` (e.g. "6 task(s) completed, 0 failed"). Flag anything where you
had to stop at a "decision belongs to Peter" step.
