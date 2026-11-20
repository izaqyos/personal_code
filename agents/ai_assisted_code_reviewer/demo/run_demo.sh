#!/usr/bin/env bash
# AI review demo on a mock TS/Express service with a deliberately bad PR.
#
#   demo/run_demo.sh            offline: mock LLM response, shows validation + gate
#   demo/run_demo.sh --live     real review via Claude Code headless (claude -p)
#   demo/run_demo.sh --setup    only build the demo repo, then review interactively:
#                                 cd <repo> && claude   →   /ai-review
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-mock}"
WORK="${DEMO_DIR:-${TMPDIR:-/tmp}/aireview-demo}"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[ -x "$PY" ] || PY="python3"
AIREVIEW=("$PY" -m aireview)
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

bold() { printf '\n\033[1m%s\033[0m\n' "$*"; }

rm -rf "$WORK"
bold "1) Building demo repo at $WORK"
"$PY" "$ROOT/demo/setup_demo_repo.py" "$WORK" >/dev/null
git -C "$WORK" log --oneline --all
git -C "$WORK" diff --stat main...feature/invoices

bold "2) Wiki lint"
(cd "$WORK" && "${AIREVIEW[@]}" wiki-lint)

bold "3) Routing: which wiki pages apply to this diff"
(cd "$WORK" && "${AIREVIEW[@]}" context --base main)

case "$MODE" in
  --setup|setup)
    bold "Ready. Review it interactively in Claude Code:"
    echo "  export PATH=\"$ROOT/.venv/bin:\$PATH\"   # so the agent can call 'aireview'"
    echo "  cd $WORK && claude"
    echo "  > /ai-review main"
    exit 0 ;;
  --live|live)
    bold "4) LLM review: Claude Code headless (read-only tools)"
    set +e
    (cd "$WORK" && "${AIREVIEW[@]}" run --runner claude --base main)
    rc=$? ;;
  *)
    bold "4) LLM review: mock runner (canned model output incl. bad findings)"
    set +e
    (cd "$WORK" && "${AIREVIEW[@]}" run --runner mock --mock-response "$ROOT/demo/mock_llm_response.md" --base main)
    rc=$? ;;
esac
set -e

bold "5) Gate exit code: $rc  (1 = blocked; config gate=blocker)"
echo "Report: $WORK/.ai-review/out/report.md   JSON: $WORK/.ai-review/out/report.json"

bold "6) Same PR with the override label → passes the gate with a warning"
(cd "$WORK" && "${AIREVIEW[@]}" validate --base main --findings .ai-review/out/findings.raw.json \
   --labels ai-review-override --out-dir .ai-review/out/override --quiet) && echo "exit 0 (overridden)"
