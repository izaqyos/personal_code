#!/usr/bin/env bash
# Presenter demo: walks through the tool step by step, pausing between steps.
#
#   demo/present.sh            mock LLM (offline, deterministic) — safest for a live talk
#   demo/present.sh --live     real Claude Code headless review in step 8
#   demo/present.sh --auto     no pauses (rehearsal / CI)
#
# The talking points for each step are in docs/presenter_guide.pdf.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIVE=0; AUTO=0
for a in "$@"; do
  case "$a" in --live) LIVE=1 ;; --auto) AUTO=1 ;; *) echo "unknown arg $a"; exit 2 ;; esac
done
WORK="${DEMO_DIR:-${TMPDIR:-/tmp}/aireview-present}"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[ -x "$PY" ] || PY="python3"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
ar() { (cd "$WORK" && "$PY" -m aireview "$@"); }

step() {
  printf '\n\033[1;36m━━ STEP %s ━━ %s\033[0m\n' "$1" "$2"
}
say() { printf '\033[2m  » %s\033[0m\n' "$*"; }
run() { printf '\033[1;33m$ %s\033[0m\n' "$*"; }
pause() { [ "$AUTO" = 1 ] || { printf '\n\033[2m[enter]\033[0m'; read -r _; }; }
summary() {  # summarize report.json: kept per severity + dropped reasons
  "$PY" - "$1" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
print(f"  status={d['status']}  counts={d['counts']}")
for f in d["findings"]:
    loc = f"{f['file']}:{f['line']}" if f.get("file") and f.get("line") else (f.get("file") or "PR-level")
    print(f"  {f['severity']:<7} {f['rule']:<9} {f['source']:<4} {loc:<45} {f['title'][:60]}")
if d["dropped"]:
    print("  -- dropped by validation --")
    for x in d["dropped"]:
        f = x["finding"]
        print(f"  ✗ {str(f.get('rule','?')):<9} {x['reason']}")
EOF
}

rm -rf "$WORK"

step 0 "The problem"
say "Devs use different agents (Claude Code, Cursor, Copilot). No API keys locally, so no RAG."
say "Goal: one review standard, everywhere — local before push, and CI on every PR."
pause

step 1 "A team repo with a PR to review"
"$PY" "$ROOT/demo/setup_demo_repo.py" "$WORK" >/dev/null
run "git log --oneline --all"; git -C "$WORK" log --oneline --all
run "git diff --stat main...feature/invoices"; git -C "$WORK" diff --stat main...feature/invoices
pause

step 2 "What's wrong with this PR (spot it yourself first)"
run "sed -n 13,26p src/routes/invoices.ts"; sed -n 13,26p "$WORK/src/routes/invoices.ts"
run "git diff main -- src/app.ts | grep '^+app'"; git -C "$WORK" diff main -- src/app.ts | grep '^+app' || true
pause

step 3 "The kit installed in the repo (aireview install)"
run "find .ai-review .claude .cursor .github AGENTS.md CLAUDE.md -type f"
(cd "$WORK" && find .ai-review .claude .cursor .github AGENTS.md CLAUDE.md -type f -not -path '*/out/*' | sort)
say "Adapters are thin pointers. Example — the Claude Code /ai-review command:"
run "sed -n 7,12p .claude/commands/ai-review.md"; sed -n 7,12p "$WORK/.claude/commands/ai-review.md"
pause

step 4 "The LLM wiki: rules with IDs + a routing table"
run "grep -A3 '^### SEC-002' .ai-review/wiki/security/authz.md"
grep -A3 '^### SEC-002' "$WORK/.ai-review/wiki/security/authz.md"
run "sed -n '/## Routing/,/^## Rule/p' .ai-review/wiki/index.md"
sed -n '/## Routing/,/^## Rule ID/p' "$WORK/.ai-review/wiki/index.md" | sed '$d'
run "aireview wiki-lint"; ar wiki-lint
pause

step 5 "Routing: which rules apply to THIS diff"
run "aireview route src/routes/invoices.ts migrations/002_drop_legacy_email.sql"
ar route src/routes/invoices.ts migrations/002_drop_legacy_email.sql
pause

step 6 "Deterministic checks — no LLM, cheap, repeatable"
run "aireview checks --base main --quiet --gate advisory"
ar checks --base main --quiet --gate advisory 2>/dev/null || true
summary "$WORK/.ai-review/out/report.json"
pause

step 7 "The context bundle the agent reads"
run "aireview context --base main"; ar context --base main
run "grep -E '^(# AI review|## (Review procedure|Output schema|Changed files|Test coverage|Deterministic|Routed wiki|PR description|Diff)|### wiki/|=== )' .ai-review/out/context.md"
grep -E '^(# AI review|## (Review procedure|Output schema|Changed files|Test coverage|Deterministic|Routed wiki|PR description|Diff)|### wiki/|=== )' "$WORK/.ai-review/out/context.md"
say "Trusted part: procedure, schema, tool results, wiki. Untrusted part: PR text + diff."
pause

if [ "$LIVE" = 1 ]; then
  step 8 "LLM review — real Claude Code headless (read-only tools)"
  run "aireview run --runner claude --base main --quiet"
  set +e; ar run --runner claude --base main --quiet; rc=$?; set -e
else
  step 8 "LLM review — mock model output (includes deliberate mistakes)"
  run "grep -c '\"rule\"' demo/mock_llm_response.md"
  echo "  $(grep -c '"rule"' "$ROOT/demo/mock_llm_response.md") findings proposed by the 'model'"
  run "aireview run --runner mock --mock-response demo/mock_llm_response.md --base main --quiet"
  set +e; ar run --runner mock --mock-response "$ROOT/demo/mock_llm_response.md" --base main --quiet; rc=$?; set -e
fi
pause

step 9 "Validation: the LLM is an untrusted proposer"
summary "$WORK/.ai-review/out/report.json"
pause

step 10 "The report + the gate"
run "head -12 .ai-review/out/report.md"; head -12 "$WORK/.ai-review/out/report.md"
echo; echo "  gate exit code: $rc  (config gate=blocker → 1 blocks the merge)"
pause

step 11 "Human override (label) — the tool advises, people decide"
run "aireview validate --base main --findings .ai-review/out/findings.raw.json --labels ai-review-override"
set +e
ar validate --base main --findings .ai-review/out/findings.raw.json --labels ai-review-override \
  --out-dir .ai-review/out/override --quiet; orc=$?
set -e
echo "  exit code with override label: $orc"
pause

step 12 "Same thing inside a dev's own agent"
say "export PATH=\"$ROOT/.venv/bin:\$PATH\"; cd $WORK && claude   →   /ai-review main"
say "Cursor: /ai-review command · Copilot: ai-review prompt · Codex: AGENTS.md"
say "CI: .github/workflows/ai-review.yml runs 'aireview run --runner claude' and comments on the PR."
echo
echo "Demo repo: $WORK   Full report: $WORK/.ai-review/out/report.md"
