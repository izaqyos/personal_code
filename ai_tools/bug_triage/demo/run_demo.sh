#!/usr/bin/env bash
# Triage the ready-made demo bugs: demo/run_demo.sh [never|on-disagreement|always]
# Needs Ollama with gemma4:12b; the final tier (on escalation) needs the claude CLI.
# If the tiers can't decide (the judge fails twice, or the final tier fails), it asks you to pick the team.
# DEMO_MODEL=no-such-model demo/run_demo.sh  makes the judge fail, to show that path.
set -euo pipefail
cd "$(dirname "$0")/.."
final="${1:-on-disagreement}"
model="${DEMO_MODEL:-gemma4:12b}"
for f in demo/0*.json; do
  echo "=== $f: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["title"])' "$f")"
  # stderr stays on the terminal: the human prompt is written there (stdout is the JSON)
  uv run --quiet bug-triage triage --file "$f" --final "$final" --model "$model" | python3 demo/show.py
  echo
done
