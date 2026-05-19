#!/bin/bash
# Aggregate test runner for the launcher.sh test suite.
# Runs every test_*.sh file in this directory and reports a single summary.
# Exits non-zero if any sub-suite fails.
#
# Usage: bash run_all.sh

set -u

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
BOLD=$'\033[1m'
NC=$'\033[0m'

failures=0
suites=0

for suite in "$TESTS_DIR"/test_*.sh; do
    [ -f "$suite" ] || continue
    ((suites++))
    name=$(basename "$suite")
    echo ""
    echo "${BOLD}=== Running $name ===${NC}"
    if bash "$suite"; then
        echo "${GREEN}$name passed${NC}"
    else
        echo "${RED}$name FAILED${NC}"
        ((failures++))
    fi
done

echo ""
echo "${BOLD}=== Suite summary ===${NC}"
echo "Suites run:    $suites"
if [ "$failures" -eq 0 ]; then
    echo "${GREEN}All suites passed ✓${NC}"
    exit 0
fi
echo "${RED}Failed suites: $failures${NC}"
exit 1
