#!/usr/bin/env bash
# generate-comparison.sh — build benchmarks/_Comparison.pdf from benchmarks/*.md
# on demand. (This used to run automatically after every benchllm.sh benchmark;
# it is now manual-only.)
#
# Usage: ./generate-comparison.sh
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

VENV="$SCRIPT_DIR/.benchllm-venv"

# Same venv benchllm.sh builds; bootstrap it here too so this script works
# standalone (same deps + hash marker, so the two scripts share one venv).
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

if ! command -v uv >/dev/null 2>&1; then
  echo "generate-comparison: uv not found, installing..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

DEPS_HASH="$(printf '%s\n' "${DEPS[@]}" | sha256sum | cut -d' ' -f1)"
MARKER="$VENV/.deps-ok"

if [[ ! -f "$MARKER" || "$(cat "$MARKER" 2>/dev/null)" != "$DEPS_HASH" ]]; then
  echo "generate-comparison: building virtualenv (first run may take a few minutes)..."
  rm -rf "$VENV"
  uv venv --python 3.12 "$VENV"
  uv pip install --python "$VENV/bin/python" "${DEPS[@]}"
  printf '%s' "$DEPS_HASH" > "$MARKER"
fi

"$VENV/bin/python" "$SCRIPT_DIR/benchllm-comparison.py" \
  --input-dir "$SCRIPT_DIR/benchmarks" --output "$SCRIPT_DIR/benchmarks/_Comparison.pdf"
echo "generate-comparison: wrote $SCRIPT_DIR/benchmarks/_Comparison.pdf"
