#!/bin/bash
# Smoke tests for every show_*_menu function in launcher.sh.
# Verifies each menu renders without errors and contains the expected option labels.
# Run with: bash test_menu_rendering.sh

set -u

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$TESTS_DIR/../launcher.sh"
source "$LAUNCHER" 2>/dev/null || true

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
NC=$'\033[0m'

# strip_ansi may already be defined by launcher.sh, but keep a local copy for safety.
_strip() { echo "$1" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g'; }

assert_contains() {
    local name="$1" haystack="$2" needle="$3"
    ((TESTS_RUN++))
    if echo "$haystack" | grep -qF "$needle"; then
        ((TESTS_PASSED++))
        echo -e "${GREEN}✓ PASS${NC}: $name"
    else
        ((TESTS_FAILED++))
        echo -e "${RED}✗ FAIL${NC}: $name (missing: $needle)"
    fi
}

assert_renders() {
    local name="$1" fn="$2"
    ((TESTS_RUN++))
    if "$fn" >/dev/null 2>&1; then
        ((TESTS_PASSED++))
        echo -e "${GREEN}✓ PASS${NC}: $name renders cleanly"
    else
        ((TESTS_FAILED++))
        echo -e "${RED}✗ FAIL${NC}: $name returned non-zero exit"
    fi
}

run_menu_checks() {
    local fn="$1"; shift
    local out
    out=$(_strip "$("$fn" 2>&1)")
    assert_renders "$fn" "$fn"
    while [ "$#" -gt 0 ]; do
        assert_contains "$fn contains '$1'" "$out" "$1"
        shift
    done
}

# Main menu — top-level entries
run_menu_checks show_main_menu \
    "MAIN MENU" \
    "Cursor Tracker" \
    "Remind Champion" \
    "Backup"

run_menu_checks show_tracker_menu \
    "TRACKER" \
    "[0]"

run_menu_checks show_repo_cleaner_menu \
    "REPO CLEANER" \
    "[0]"

run_menu_checks show_context_generator_menu \
    "CONTEXT" \
    "[0]"

# Reminder menu — make sure the new DoD heads-up entry is present
run_menu_checks show_reminder_menu \
    "REMIND CHAMPION MENU" \
    "[16]" \
    "Send Heads-Up" \
    "[17]" \
    "Send DoD Heads-Up" \
    "[0-17]"

run_menu_checks show_daily_timer_menu \
    "DAILY STANDUP TIMER" \
    "[0]"

run_menu_checks show_mcp_helper_menu \
    "MCP" \
    "[0]"

run_menu_checks show_emoji_generator_menu \
    "EMOJI" \
    "[0]"

run_menu_checks show_backup_menu \
    "BACKUP" \
    "[0]"

echo ""
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
[ "$TESTS_FAILED" -eq 0 ]
