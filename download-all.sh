#!/usr/bin/env bash
# download-all.sh — pre-download every model referenced by the benchmark set.
#
# Mirrors benchllm-all.sh's two recipe sources:
#   1. models.yaml — registry recipe entries (`- name:` blocks). Each block's
#      `model:` repo is fetched. A block whose `tp:` is numeric and > 1 is
#      skipped (needs multi-GPU tensor parallelism, can't run on this box).
#   2. recipes/*.yaml|*.yml — local recipe files (run by path in benchllm-all).
#      Each file's top-level `model:` is fetched, skipped if its
#      `tensor_parallel:` default is > 1. External speculative-decoding
#      drafters named in a `speculative_config:` line (e.g. DFlash) are ALSO
#      fetched, honouring a pinned `"revision"` when the config carries one —
#      without the pinned drafter revision those recipes fail to serve.
#
# Downloads are idempotent (hf skips files already in the local cache), and the
# script continues past individual failures, printing a summary at the end.
#
# NOTE ON DISK: benchllm-all.sh runs with --cleanup because the whole catalogue
# may not fit on the SSD at once. Downloading everything here can consume a lot
# of space — check `df -h ~` first. To fetch a subset, trim models.yaml (or set
# MODELS_YAML/RECIPES_DIR), or run `hf download <repo>` for one model.
#
# Usage:
#   ./download-all.sh                 # download everything referenced
#   ./download-all.sh --dry-run       # print the plan, download nothing
#   MODELS_YAML=... RECIPES_DIR=... ./download-all.sh
#
# Any other arguments are passed straight through to `hf download`, e.g.:
#   ./download-all.sh --max-workers 4
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

MODELS_YAML="${MODELS_YAML:-$SCRIPT_DIR/models.yaml}"
RECIPES_DIR="${RECIPES_DIR:-$SCRIPT_DIR/recipes}"

command -v hf >/dev/null 2>&1 || { echo "download-all: 'hf' not found on PATH" >&2; exit 1; }

# --- Parse args ------------------------------------------------------------
DRY_RUN=0
passthru=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    *)         passthru+=("$a") ;;
  esac
done

# --- Collect download specs ------------------------------------------------
# Each spec is "repo" or "repo<TAB>revision". Deduped later, order-preserving.
specs=()
add_spec() {  # $1=repo  [$2=revision]
  local repo="$1" rev="${2:-}"
  [[ -n "$repo" ]] || return 0
  if [[ -n "$rev" ]]; then specs+=("$repo"$'\t'"$rev"); else specs+=("$repo"); fi
}

# 1. models.yaml — walk `- name:` blocks; emit `model:` for tp <= 1.
if [[ -f "$MODELS_YAML" ]]; then
  while IFS= read -r repo; do add_spec "$repo"; done < <(awk '
    function flush() {
      if (model == "") { tp = ""; return }
      if (tp ~ /^[0-9]+$/ && tp + 0 > 1) {
        print "  skip (tp=" tp "): " model > "/dev/stderr"
      } else { print model }
      model = ""; tp = ""
    }
    /^[[:space:]]*-[[:space:]]*name:/ { flush() }
    /^[[:space:]]*model:[[:space:]]*/ {
      v = $0; sub(/^[[:space:]]*model:[[:space:]]*/, "", v)
      sub(/#.*/, "", v); gsub(/[\042\047]/, "", v); gsub(/[[:space:]]+$/, "", v)
      model = v
    }
    /^[[:space:]]*tp:[[:space:]]*/ {
      v = $0; sub(/^[[:space:]]*tp:[[:space:]]*/, "", v)
      sub(/#.*/, "", v); gsub(/[\042\047[:space:]]/, "", v)
      tp = v
    }
    END { flush() }
  ' "$MODELS_YAML")
else
  echo "download-all: models file not found (skipping): $MODELS_YAML" >&2
fi

# 2. recipes/ — top-level model: per file (+ external drafters), tp <= 1.
if [[ -d "$RECIPES_DIR" ]]; then
  shopt -s nullglob
  for f in "$RECIPES_DIR"/*.yaml "$RECIPES_DIR"/*.yml; do
    model=$(sed -nE 's/^[[:space:]]*model:[[:space:]]*//p' "$f" | head -n1 \
              | sed -E 's/#.*//; s/["'\'']//g; s/[[:space:]]+$//')
    tp=$(sed -nE 's/.*tensor_parallel:[[:space:]]*([0-9]+).*/\1/p' "$f" | head -n1)
    if [[ -n "$tp" && "$tp" -gt 1 ]]; then
      echo "  skip (tp=$tp): ${model:-?}  [$(basename "$f")]" >&2
    else
      add_spec "$model"
    fi
    # External drafters: pull `"model"`/`"revision"` out of speculative_config.
    while IFS= read -r line; do
      dmodel=$(sed -nE 's/.*"model"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/p' <<<"$line")
      drev=$(sed -nE 's/.*"revision"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/p' <<<"$line")
      [[ -n "$dmodel" ]] && add_spec "$dmodel" "$drev"
    done < <(grep -E 'speculative_config' "$f" 2>/dev/null || true)
  done
  shopt -u nullglob
fi

# Dedup, order-preserving.
if [[ ${#specs[@]} -gt 0 ]]; then
  mapfile -t specs < <(printf '%s\n' "${specs[@]}" | awk 'NF && !seen[$0]++')
fi
if [[ ${#specs[@]} -eq 0 ]]; then
  echo "download-all: nothing to download (no models found in $MODELS_YAML or $RECIPES_DIR)" >&2
  exit 1
fi

# --- Report the plan -------------------------------------------------------
echo "download-all: ${#specs[@]} unique download(s):"
for spec in "${specs[@]}"; do
  repo="${spec%%$'\t'*}"
  if [[ "$spec" == *$'\t'* ]]; then printf '  - %s @ %s\n' "$repo" "${spec#*$'\t'}"
  else printf '  - %s\n' "$repo"; fi
done
echo

if [[ $DRY_RUN -eq 1 ]]; then
  echo "download-all: --dry-run, nothing downloaded."
  exit 0
fi

# --- Download each, continuing past failures -------------------------------
declare -a ok_list=() fail_list=()
for spec in "${specs[@]}"; do
  repo="${spec%%$'\t'*}"
  rev=""; [[ "$spec" == *$'\t'* ]] && rev="${spec#*$'\t'}"
  label="$repo"; [[ -n "$rev" ]] && label="$repo @ $rev"
  cmd=(hf download "$repo")
  [[ -n "$rev" ]] && cmd+=(--revision "$rev")
  echo "============================================================"
  echo "download-all: >>> ${cmd[*]}"
  echo "============================================================"
  if "${cmd[@]}" ${passthru[@]+"${passthru[@]}"}; then
    ok_list+=("$label")
  else
    rc=$?
    echo "download-all: !!! $label FAILED (exit $rc)" >&2
    fail_list+=("$label")
  fi
  echo
done

# --- Summary ---------------------------------------------------------------
echo "============================================================"
echo "download-all: summary — ${#ok_list[@]} ok, ${#fail_list[@]} failed"
echo "============================================================"
[[ ${#ok_list[@]}   -gt 0 ]] && printf '  ok    %s\n' "${ok_list[@]}"
[[ ${#fail_list[@]} -gt 0 ]] && printf '  FAIL  %s\n' "${fail_list[@]}"

[[ ${#fail_list[@]} -eq 0 ]]
