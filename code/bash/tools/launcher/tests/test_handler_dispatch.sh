#!/bin/bash
# Handler dispatch tests.
#
# Strategy: drop a fake `python3` stub at the front of PATH. The stub logs its
# argv to $STUB_LOG and exits 0. We then drive handle_reminder_menu via stdin
# to exercise specific menu paths and assert the recorded argv matches what we
# expect — proving the case branches build the right command.
#
# Run with: bash test_handler_dispatch.sh

set -u

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$TESTS_DIR/../launcher.sh"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
NC=$'\033[0m'

# ----------------------------------------------------------------------------
# Stub setup
# ----------------------------------------------------------------------------

STUB_DIR="$(mktemp -d)"
trap 'rm -rf "$STUB_DIR"' EXIT

cat >"$STUB_DIR/python3" <<'STUB'
#!/bin/bash
# Records its argv (one arg per line, blank-line separated per call) to $STUB_LOG.
# Strips the leading script-path arg so tests can match on flags/positional only.
shift   # drop script path (e.g. .../remind_champion.py)
printf '%s\n' "$@" >>"$STUB_LOG"
echo "---" >>"$STUB_LOG"
exit 0
STUB
chmod +x "$STUB_DIR/python3"

export PATH="$STUB_DIR:$PATH"

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

assert_log_contains() {
    local name="$1" needle="$2"
    ((TESTS_RUN++))
    if grep -qxF -e "$needle" "$STUB_LOG"; then
        ((TESTS_PASSED++))
        echo -e "${GREEN}✓ PASS${NC}: $name"
    else
        ((TESTS_FAILED++))
        echo -e "${RED}✗ FAIL${NC}: $name"
        echo "  expected line: $needle"
        echo "  actual log:"
        sed 's/^/    /' "$STUB_LOG"
    fi
}

assert_log_missing() {
    local name="$1" needle="$2"
    ((TESTS_RUN++))
    if grep -qxF -e "$needle" "$STUB_LOG"; then
        ((TESTS_FAILED++))
        echo -e "${RED}✗ FAIL${NC}: $name (unexpected line present: $needle)"
    else
        ((TESTS_PASSED++))
        echo -e "${GREEN}✓ PASS${NC}: $name"
    fi
}

run_handler() {
    # $1: stdin content (lines fed to read)
    # Sources the launcher fresh per invocation so handler state cannot leak.
    STUB_LOG="$STUB_DIR/log_$$_$TESTS_RUN.txt"
    : >"$STUB_LOG"
    export STUB_LOG
    bash -c "
        source '$LAUNCHER' 2>/dev/null
        handle_reminder_menu
    " <<<"$1" >/dev/null 2>&1 || true
}

# ----------------------------------------------------------------------------
# Case 17 — DoD Heads-Up dispatcher
# ----------------------------------------------------------------------------

# Mode 1: dry-run preview
run_handler "17
1

0
"
assert_log_contains "case 17 mode 1 sends --dry-run" "--dry-run"
assert_log_contains "case 17 mode 1 sends --dod-heads-up" "--dod-heads-up"
assert_log_missing  "case 17 mode 1 omits --test"        "--test"

# Mode 2: test redirect
run_handler "17
2

0
"
assert_log_contains "case 17 mode 2 sends --test"        "--test"
assert_log_contains "case 17 mode 2 sends --dod-heads-up" "--dod-heads-up"
assert_log_missing  "case 17 mode 2 omits --dry-run"     "--dry-run"

# Mode 3: test + dry-run
run_handler "17
3

0
"
assert_log_contains "case 17 mode 3 sends --test"        "--test"
assert_log_contains "case 17 mode 3 sends --dry-run"     "--dry-run"
assert_log_contains "case 17 mode 3 sends --dod-heads-up" "--dod-heads-up"

# Mode 4 with confirmation declined: must NOT call python3
run_handler "17
4
n

0
"
assert_log_missing "case 17 mode 4 declined makes no call" "--dod-heads-up"

# Mode 4 with confirmation y: real send (no --dry-run, no --test)
run_handler "17
4
y

0
"
assert_log_contains "case 17 mode 4 confirmed sends --dod-heads-up" "--dod-heads-up"
assert_log_missing  "case 17 mode 4 confirmed omits --dry-run"      "--dry-run"
assert_log_missing  "case 17 mode 4 confirmed omits --test"         "--test"

# ----------------------------------------------------------------------------
# Sanity — case 1 (Show Release Schedule) calls --schedule
# ----------------------------------------------------------------------------

run_handler "1

0
"
assert_log_contains "case 1 sends --schedule" "--schedule"

# ----------------------------------------------------------------------------
# Sanity — case 4 (Send DoD Reminder) calls --dod-reminder
# ----------------------------------------------------------------------------

run_handler "4

0
"
assert_log_contains "case 4 sends --dod-reminder" "--dod-reminder"

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------

echo ""
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
[ "$TESTS_FAILED" -eq 0 ]
