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
#          model: ...
#    Comments (#...) and blank lines are ignored; values may be quoted.
if [[ -f "$MODELS_YAML" ]]; then
  while IFS= read -r name; do
    [[ -n "$name" ]] && recipes+=("$name")
  done < <(sed -E \
             -e 's/#.*$//' \
             -e '/^[[:space:]]*-[[:space:]]*name:[[:space:]]*/!d' \
             -e 's/^[[:space:]]*-[[:space:]]*name:[[:space:]]*//' \
             -e 's/^["'\'']//; s/["'\'']?[[:space:]]*$//' \
             "$MODELS_YAML")
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
  echo
done

# --- Summary ---------------------------------------------------------------
echo "============================================================"
echo "benchllm-all: summary — ${#ok_list[@]} ok, ${#fail_list[@]} failed"
echo "============================================================"
[[ ${#ok_list[@]}   -gt 0 ]] && printf '  ok    %s\n' "${ok_list[@]}"
[[ ${#fail_list[@]} -gt 0 ]] && printf '  FAIL  %s\n' "${fail_list[@]}"

[[ ${#fail_list[@]} -eq 0 ]]
