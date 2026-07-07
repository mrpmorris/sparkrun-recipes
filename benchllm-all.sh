#!/usr/bin/env bash
# benchllm-all.sh — run benchllm.sh across every valid recipe.
#
# Targets:
#   1. Every *.yaml recipe file in this script's folder.
#   2. Every built-in recipe from `sparkrun list` whose TP column is `1`
#      or is not a number (e.g. `-`). Recipes needing TP > 1 are skipped
#      because this box is a single GB10 (tensor parallel > 1 won't fit).
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

# --- Build the list of recipes to run -------------------------------------
recipes=()

# 1. Local YAML recipes in this folder.
shopt -s nullglob
for f in "$SCRIPT_DIR"/*.yaml "$SCRIPT_DIR"/*.yml; do
  recipes+=("$f")
done
shopt -u nullglob

# 2. Built-in recipes with TP == 1 or TP not a number.
if command -v sparkrun >/dev/null 2>&1; then
  while IFS= read -r name; do
    [[ -n "$name" ]] && recipes+=("$name")
  done < <(sparkrun list 2>/dev/null \
             | awk '/^@/ { if ($3 == "1" || $3 !~ /^[0-9]+$/) print $1 }')
else
  echo "benchllm-all: WARNING — sparkrun not on PATH; skipping built-in recipes." >&2
fi

# Drop transitional recipes: on this box they wedge sglang's scheduler on the
# lm-eval step (models endpoint stays up, generation dies). Skip anything whose
# name contains @sparkrun-transitional.
filtered=()
for r in "${recipes[@]}"; do
  if [[ "$r" == *@sparkrun-transitional* ]]; then
    echo "benchllm-all: skipping transitional recipe: $r" >&2
  else
    filtered+=("$r")
  fi
done
recipes=("${filtered[@]+"${filtered[@]}"}")

if [[ ${#recipes[@]} -eq 0 ]]; then
  echo "benchllm-all: no recipes found." >&2
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

# --- Comparison PDF ---------------------------------------------------------
echo
echo "benchllm-all: generating comparison PDF..."
if "$SCRIPT_DIR/.benchllm-venv/bin/python" "$SCRIPT_DIR/benchllm-comparison.py" \
     --input-dir "$SCRIPT_DIR/benchmarks" --output "$SCRIPT_DIR/benchmarks/_Comparison.pdf"; then
  echo "benchllm-all: wrote $SCRIPT_DIR/benchmarks/_Comparison.pdf"
else
  echo "benchllm-all: WARNING - comparison PDF generation failed" >&2
fi

[[ ${#fail_list[@]} -eq 0 ]]
