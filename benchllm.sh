#!/usr/bin/env bash
# benchllm.sh — bootstrap for benchllm.py.
# Ensures uv + a virtualenv with pinned dependencies exist, then runs the benchmark.
#
# Usage: ./benchllm.sh --recipe <recipe.yaml | sparkrun-recipe-name> [options]   (see benchllm.py --help)
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

VENV="$SCRIPT_DIR/.benchllm-venv"
DEPS=(
  "lm-eval[api]==0.4.12"
  "transformers>=4.50"
  "requests>=2.32"
  "tiktoken>=0.8"
  "pyyaml>=6.0"
  "pandas>=2.2"
  "matplotlib>=3.8"
  "pillow>=10"
)

# BFCL tool-calling benchmark runs in its own venv: EvalScope + bfcl-eval pull heavy
# deps (torch) and their own transformers/pydantic pins that would clash with lm-eval.
# Built by default; pass --skip-bfcl to skip both this venv and the eval.
VENV_BFCL="$SCRIPT_DIR/.benchllm-bfcl-venv"
BFCL_DEPS=(
  "evalscope==1.2.0"
  "bfcl-eval==2025.10.27.1"
  "soundfile==0.14.0"   # bfcl-eval -> qwen_agent imports soundfile at load
)

if ! command -v uv >/dev/null 2>&1; then
  echo "benchllm: uv not found, installing..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

DEPS_HASH="$(printf '%s\n' "${DEPS[@]}" | sha256sum | cut -d' ' -f1)"
MARKER="$VENV/.deps-ok"

if [[ ! -f "$MARKER" || "$(cat "$MARKER" 2>/dev/null)" != "$DEPS_HASH" ]]; then
  echo "benchllm: building virtualenv (first run may take a few minutes)..."
  rm -rf "$VENV"
  uv venv --python 3.12 "$VENV"
  uv pip install --python "$VENV/bin/python" "${DEPS[@]}"
  printf '%s' "$DEPS_HASH" > "$MARKER"
fi

# Build the BFCL venv by default; skip only when the run opts out.
SKIP_BFCL=0
for arg in "$@"; do
  [[ "$arg" == "--skip-bfcl" ]] && SKIP_BFCL=1
done

if [[ "$SKIP_BFCL" == "0" ]]; then
  BFCL_HASH="$(printf '%s\n' "${BFCL_DEPS[@]}" | sha256sum | cut -d' ' -f1)"
  BFCL_MARKER="$VENV_BFCL/.deps-ok"
  if [[ ! -f "$BFCL_MARKER" || "$(cat "$BFCL_MARKER" 2>/dev/null)" != "$BFCL_HASH" ]]; then
    echo "benchllm: building BFCL virtualenv (first run downloads torch; slow — pass --skip-bfcl to skip)..."
    rm -rf "$VENV_BFCL"
    uv venv --python 3.12 "$VENV_BFCL"
    uv pip install --python "$VENV_BFCL/bin/python" "${BFCL_DEPS[@]}"
    printf '%s' "$BFCL_HASH" > "$BFCL_MARKER"
  fi
  export BENCHLLM_BFCL_PYTHON="$VENV_BFCL/bin/python"
fi

"$VENV/bin/python" "$SCRIPT_DIR/benchllm.py" "$@"
rc=$?

# --- Comparison PDF ---------------------------------------------------------
echo
echo "benchllm: generating comparison PDF..."
if "$VENV/bin/python" "$SCRIPT_DIR/benchllm-comparison.py" \
     --input-dir "$SCRIPT_DIR/benchmarks" --output "$SCRIPT_DIR/benchmarks/_Comparison.pdf"; then
  echo "benchllm: wrote $SCRIPT_DIR/benchmarks/_Comparison.pdf"
else
  echo "benchllm: WARNING - comparison PDF generation failed" >&2
fi

exit $rc
