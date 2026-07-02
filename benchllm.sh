#!/usr/bin/env bash
# benchllm.sh — bootstrap for benchllm.py.
# Ensures uv + a virtualenv with pinned dependencies exist, then runs the benchmark.
#
# Usage: ./benchllm.sh --recipe <recipe.yaml> [options]   (see benchllm.py --help)
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"

VENV="$SCRIPT_DIR/.benchllm-venv"
DEPS=(
  "lm-eval[api]==0.4.12"
  "requests>=2.32"
  "tiktoken>=0.8"
  "pyyaml>=6.0"
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

exec "$VENV/bin/python" "$SCRIPT_DIR/benchllm.py" "$@"
