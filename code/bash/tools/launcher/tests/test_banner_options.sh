#!/usr/bin/env bash
# Verifies that the daily timer menu now exposes 6 options and accepts banner choices.

set -e

LAUNCHER="$(cd "$(dirname "$0")/.." && pwd)/launcher.sh"
PASS=0
FAIL=0

assert_grep() {
	local pattern="$1"
	local description="$2"
	if grep -q -F -- "$pattern" "$LAUNCHER"; then
		echo "PASS: $description"
		PASS=$((PASS + 1))
	else
		echo "FAIL: $description (pattern: $pattern)"
		FAIL=$((FAIL + 1))
	fi
}

assert_grep "Start Meeting (CLI + Banner)" "Menu shows CLI + Banner option"
assert_grep "Start Meeting (CLI + Banner + Text)" "Menu shows CLI + Banner + Text option"
assert_grep "Enter your choice [0-6]" "Prompt range updated to 0-6"
assert_grep "main.py --mode cli --team imagine_dragons -b" "Banner option invokes -b"
assert_grep "Enter banner text:" "Banner+Text option prompts for text"
assert_grep "--banner-fields sprint,sprint_week,champion,dod,next_event --banner-text" "Banner+Text option passes both flags"

echo ""
echo "Total: $((PASS + FAIL)) tests, $PASS passed, $FAIL failed"
exit $FAIL
