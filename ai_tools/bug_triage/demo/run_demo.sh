#!/usr/bin/env bash
# Triage the ready-made demo bugs: demo/run_demo.sh [never|on-disagreement|always]
# Needs Ollama with gemma4:12b; the final tier (on escalation) needs the claude CLI.
set -euo pipefail
cd "$(dirname "$0")/.."
final="${1:-on-disagreement}"
for f in demo/0*.json; do
  echo "=== $f: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["title"])' "$f")"
  uv run bug-triage triage --file "$f" --final "$final" 2>/dev/null | python3 demo/show.py
  echo
done
