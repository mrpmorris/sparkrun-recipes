#!/usr/bin/env bash
# benchllm-all.sh — run benchllm.sh across a set of recipes.
#
# The set of recipes to benchmark comes from two sources, in this order:
#   1. models.yaml (next to this script): every `name:` entry under `models:`
#      (registry recipe names, e.g. @eugr/some-recipe). Curate it with
#      `sparkrun list --json`. Expected to hold only recipes that fit this
#      single-GB10 box (TP == 1 / min_nodes 1 or no numeric TP); nothing here
#      re-filters by TP.
#   2. Every *.yaml / *.yml file in the recipes/ folder (next to this script) —
#      local recipe files, run by path. Drop a recipe file in there to include
#      it without touching models.yaml.
#
# Either source may be empty; the run proceeds as long as at least one recipe
# is found across both.
#
# Every recipe is run with --cleanup so HF models downloaded for a run are
# deleted when it finishes (models already cached at startup are kept) — the
# whole catalog can be benchmarked even though it wouldn't fit on the SSD.
#
# Recipes whose report (benchmarks/<stem>.md) already exists are skipped, so
# re-running the batch just fills in what's missing. Pass --force to re-run
# everything regardless.
#
# Any extra arguments are passed straight through to benchllm.sh, e.g.:
#   ./benchllm-all.sh --skip-eval
#   ./benchllm-all.sh --force --skip-eval
#   ./benchllm-all.sh --with-bfcl --eval-limit 50
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

BENCHLLM="$SCRIPT_DIR/benchllm.sh"
[[ -x "$BENCHLLM" ]] || { echo "benchllm-all: $BENCHLLM not found or not executable" >&2; exit 1; }

MODELS_YAML="${MODELS_YAML:-$SCRIPT_DIR/models.yaml}"
RECIPES_DIR="${RECIPES_DIR:-$SCRIPT_DIR/recipes}"

# --- Build the list of recipes to run -------------------------------------
recipes=()

# 1. Registry recipe names from models.yaml. Lines look like:
#      models:
#        - name: @eugr/some-recipe
#          enabled: true
#          model: ...
#    A block with `enabled: false` is skipped (default is enabled). Comments
#    (#...) and blank lines are ignored; values may be quoted. The awk walks
#    per `- name:` block so it can pair each name with its own enabled flag.
if [[ -f "$MODELS_YAML" ]]; then
  while IFS= read -r name; do
    [[ -n "$name" ]] && recipes+=("$name")
  done < <(awk '
    function flush() { if (name != "" && enabled != "false") print name; name=""; enabled="" }
    /^[[:space:]]*-[[:space:]]*name:/ {
      flush(); v=$0; sub(/^[[:space:]]*-[[:space:]]*name:[[:space:]]*/,"",v)
      sub(/#.*/,"",v); gsub(/[\042\047]/,"",v); gsub(/[[:space:]]+$/,"",v); name=v }
    /^[[:space:]]*enabled:[[:space:]]*/ {
      v=$0; sub(/^[[:space:]]*enabled:[[:space:]]*/,"",v)
      sub(/#.*/,"",v); gsub(/[\042\047[:space:]]/,"",v); enabled=tolower(v) }
    END { flush() }
  ' "$MODELS_YAML")
else
  echo "benchllm-all: models file not found (skipping): $MODELS_YAML" >&2
fi

# 2. Local recipe files in the recipes/ folder.
if [[ -d "$RECIPES_DIR" ]]; then
  shopt -s nullglob
  for f in "$RECIPES_DIR"/*.yaml "$RECIPES_DIR"/*.yml; do
    recipes+=("$f")
  done
  shopt -u nullglob
fi

if [[ ${#recipes[@]} -eq 0 ]]; then
  echo "benchllm-all: no recipes found in $MODELS_YAML or $RECIPES_DIR." >&2
  exit 1
fi

echo "benchllm-all: ${#recipes[@]} recipe(s) to benchmark:"
printf '  - %s\n' "${recipes[@]}"
echo

# --- Ensure no stale workload is holding the box between models -----------
# A sparkrun serve that crashes (or a Ctrl-C'd run) leaves its container up as
# a `sleep infinity` shell, still holding unified memory. If the next model
# launches into that, it can't fit its KV cache and the driver then polls a
# dead endpoint for its whole watchdog timeout ("...waiting for endpoint").
# Tearing down between models keeps every run starting from a clean box.
SPARKRUN="${SPARKRUN:-sparkrun}"
BENCHLLM_TEARDOWN="${BENCHLLM_TEARDOWN:-1}"
teardown_workloads() {
  [[ "$BENCHLLM_TEARDOWN" == "1" ]] || return 0
  echo "benchllm-all: tearing down any running sparkrun workloads..."
  # Best-effort: never let cleanup failure abort the batch (set -e is active).
  "$SPARKRUN" stop --all >/dev/null 2>&1 || true
}

teardown_workloads   # clean slate before the first recipe

# --- Run each recipe, continuing past failures -----------------------------
declare -a ok_list=() fail_list=()
for recipe in "${recipes[@]}"; do
  echo "============================================================"
  echo "benchllm-all: >>> $recipe"
  echo "============================================================"
  if "$BENCHLLM" --recipe "$recipe" --cleanup "$@"; then
    ok_list+=("$recipe")
  else
    rc=$?
    echo "benchllm-all: !!! $recipe FAILED (exit $rc)" >&2
    fail_list+=("$recipe")
  fi
  # Always tear down this recipe's workload before the next one launches, so a
  # crashed or killed serve can't poison the following model's memory budget.
  teardown_workloads
  echo
done

# --- Summary ---------------------------------------------------------------
echo "============================================================"
echo "benchllm-all: summary — ${#ok_list[@]} ok, ${#fail_list[@]} failed"
echo "============================================================"
[[ ${#ok_list[@]}   -gt 0 ]] && printf '  ok    %s\n' "${ok_list[@]}"
[[ ${#fail_list[@]} -gt 0 ]] && printf '  FAIL  %s\n' "${fail_list[@]}"

[[ ${#fail_list[@]} -eq 0 ]]
