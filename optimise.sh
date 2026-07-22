#!/usr/bin/env bash
# Optimise a sparkrun recipe for single-stream generation speed.
# Usage: ./optimise.sh --recipe <filename>   (see optimise.py --help)
set -euo pipefail
cd "$(dirname "$0")"
# sparkrun installs to ~/.local/bin, which non-login shells may not have
export PATH="$HOME/.local/bin:$PATH"
exec python3 optimise.py "$@"
