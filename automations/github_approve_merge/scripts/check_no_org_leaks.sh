#!/bin/bash
# Pre-commit guard: refuse to stage files that contain known organization-internal
# substrings. Install: ln -s ../../scripts/check_no_org_leaks.sh .git/hooks/pre-commit
#
# To run manually: scripts/check_no_org_leaks.sh
# To run on the entire working tree (not just staged): scripts/check_no_org_leaks.sh --all

set -euo pipefail

# Patterns that must never appear in tracked files. Add to this list when you
# learn about new organization-internal terms that could leak.
PATTERNS=(
  'perimeter-81'
  'perimeter81-'
  'platform-global-domain'
  'checkpoint\.com'
  'p81-'
  'saferx'
  'saferdock'
  'harmony-sase'
  'Check Point'
  'CheckPoint'
)

# Files to skip (intentional metadata about the guard itself).
SKIP_BASENAMES=(
  'check_no_org_leaks.sh'
  'SECURITY.md'
)

if [[ "${1:-}" == "--all" ]]; then
  CHANGED=$(git ls-files)
else
  CHANGED=$(git diff --cached --name-only --diff-filter=ACMR)
fi

if [[ -z "$CHANGED" ]]; then
  exit 0
fi

# Build the egrep alternation pattern.
PATTERN=$(printf '%s|' "${PATTERNS[@]}")
PATTERN=${PATTERN%|}

FAIL=0
while IFS= read -r f; do
  # Skip the guard's own files (they reference the patterns intentionally).
  base=$(basename "$f")
  skip=0
  for s in "${SKIP_BASENAMES[@]}"; do
    if [[ "$base" == "$s" ]]; then skip=1; break; fi
  done
  [[ $skip -eq 1 ]] && continue

  if [[ -f "$f" ]] && grep -E -n "$PATTERN" "$f" > /dev/null 2>&1; then
    echo "✗ $f contains an org-internal substring:" >&2
    grep -E -n --color=always "$PATTERN" "$f" >&2 || true
    FAIL=1
  fi
done <<< "$CHANGED"

if [[ $FAIL -eq 1 ]]; then
  echo "" >&2
  echo "Pre-commit blocked. Replace org-internal terms with the standard placeholders" >&2
  echo "(acme-org, widgets-service, api-gateway, me@example.com) and stage again." >&2
  exit 1
fi
