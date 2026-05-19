#!/bin/bash
# Test suite for launcher.sh formatting and alignment helpers.
# Run with: bash test_formatting.sh

set -e

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$TESTS_DIR/../launcher.sh"
source "$LAUNCHER" 2>/dev/null || true

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors for test output
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
NC=$'\033[0m'

# ============================================================================
# Test helper functions
# ============================================================================

test_pass() {
    ((TESTS_PASSED++))
    echo -e "${GREEN}✓ PASS${NC}: $1"
}

test_fail() {
    ((TESTS_FAILED++))
    echo -e "${RED}✗ FAIL${NC}: $1"
    echo "  Expected: $2"
    echo "  Got:      $3"
}

run_test() {
    ((TESTS_RUN++))
    local name="$1"
    local expected="$2"
    local actual="$3"
    
    if [ "$expected" = "$actual" ]; then
        test_pass "$name"
    else
        test_fail "$name" "$expected" "$actual"
    fi
}

# ============================================================================
# Test: strip_ansi function
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing strip_ansi()"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Test 1: Strip simple color code
input="${GREEN}Hello${NC}"
expected="Hello"
actual=$(strip_ansi "$input")
run_test "strip_ansi: simple green color" "$expected" "$actual"

# Test 2: Strip multiple color codes
input="${RED}Red${NC} and ${BLUE}Blue${NC}"
expected="Red and Blue"
actual=$(strip_ansi "$input")
run_test "strip_ansi: multiple colors" "$expected" "$actual"

# Test 3: Strip bold
input="${BOLD}Bold Text${NC}"
expected="Bold Text"
actual=$(strip_ansi "$input")
run_test "strip_ansi: bold formatting" "$expected" "$actual"

# Test 4: No ANSI codes
input="Plain text"
expected="Plain text"
actual=$(strip_ansi "$input")
run_test "strip_ansi: plain text unchanged" "$expected" "$actual"

# Test 5: Complex nested codes
input="${BOLD}${CYAN}[${GREEN}1${CYAN}]${NC} Menu Item"
expected="[1] Menu Item"
actual=$(strip_ansi "$input")
run_test "strip_ansi: complex nested codes" "$expected" "$actual"

# ============================================================================
# Test: visible_length function
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing visible_length()"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Test 1: Plain text length
input="Hello World"
expected="11"
actual=$(visible_length "$input")
run_test "visible_length: plain text" "$expected" "$actual"

# Test 2: Colored text length (should ignore ANSI)
input="${GREEN}Hello${NC}"
expected="5"
actual=$(visible_length "$input")
run_test "visible_length: colored text" "$expected" "$actual"

# Test 3: Menu item with colors
input="${GREEN}[1]${NC}  Cursor Tracker"
expected="19"
actual=$(visible_length "$input")
run_test "visible_length: menu item" "$expected" "$actual"

# Test 4: Empty string
input=""
expected="0"
actual=$(visible_length "$input")
run_test "visible_length: empty string" "$expected" "$actual"

# ============================================================================
# Test: pad_right function
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing pad_right()"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Test 1: Pad plain text
input="Hello"
result=$(pad_right "$input" 10)
result_len=$(visible_length "$result")
run_test "pad_right: plain text to 10 chars" "10" "$result_len"

# Test 2: Pad colored text
input="${GREEN}Hi${NC}"
result=$(pad_right "$input" 10)
result_len=$(visible_length "$result")
run_test "pad_right: colored text to 10 chars" "10" "$result_len"

# Test 3: Text already at target width
input="Exactly10!"
result=$(pad_right "$input" 10)
result_len=$(visible_length "$result")
run_test "pad_right: text at exact width" "10" "$result_len"

# Test 4: Text longer than target (no truncation, just return as-is)
input="This is longer than 10"
result=$(pad_right "$input" 10)
result_len=$(visible_length "$result")
run_test "pad_right: text longer than target (no truncation)" "22" "$result_len"

# ============================================================================
# Test: pad_center function
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing pad_center()"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Test 1: Center plain text
input="Hello"
result=$(pad_center "$input" 11)
result_len=$(visible_length "$result")
run_test "pad_center: plain text width" "11" "$result_len"

# Test 2: Verify centering (check spaces on each side)
input="Hi"
result=$(pad_center "$input" 10)
expected="    Hi    "
run_test "pad_center: equal padding" "$expected" "$result"

# Test 3: Center colored text
input="${GREEN}OK${NC}"
result=$(pad_center "$input" 10)
result_len=$(visible_length "$result")
run_test "pad_center: colored text width" "10" "$result_len"

# ============================================================================
# Test: Box line functions output correct width
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing box line functions (140-char width)"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Test 1: print_box_top is 140 chars
result=$(print_box_top)
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_top: exactly 140 chars" "140" "$result_len"

# Test 2: print_box_bottom is 140 chars
result=$(print_box_bottom)
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_bottom: exactly 140 chars" "140" "$result_len"

# Test 3: print_box_separator is 140 chars
result=$(print_box_separator)
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_separator: exactly 140 chars" "140" "$result_len"

# Test 4: print_box_empty is 140 chars
result=$(print_box_empty)
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_empty: exactly 140 chars" "140" "$result_len"

# Test 5: print_box_line with plain text is 140 chars
result=$(print_box_line "Test content")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_line: plain text exactly 140 chars" "140" "$result_len"

# Test 6: print_box_line centered is 140 chars
result=$(print_box_line "Centered Text" "center")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_box_line: centered exactly 140 chars" "140" "$result_len"

# Test 7: print_menu_item is 140 chars
result=$(print_menu_item "1" "Menu Item Label")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_menu_item: exactly 140 chars" "140" "$result_len"

# Test 8: print_menu_item with different color is 140 chars
result=$(print_menu_item "0" "Exit" "$YELLOW")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_menu_item: yellow key exactly 140 chars" "140" "$result_len"

# Test 9: print_nugget_line is 140 chars
result=$(print_nugget_line "Python" "$GREEN" "Use list comprehensions for concise code.")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_nugget_line: exactly 140 chars" "140" "$result_len"

# Test 10: print_nugget_line continuation is 140 chars
result=$(print_nugget_line "" "" "This is a continuation line" "true")
result_stripped=$(strip_ansi "$result")
result_len=${#result_stripped}
run_test "print_nugget_line: continuation exactly 140 chars" "140" "$result_len"

# ============================================================================
# Test: Full menu output alignment
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing full menu alignment (all lines = 140 chars)"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Capture menu output and verify each line
all_lines_correct=true
wrong_lines=0

while IFS= read -r line; do
    if [ -z "$line" ]; then
        continue
    fi
    stripped=$(echo "$line" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g')
    len=${#stripped}

    # Skip lines that strip to empty (e.g. clear_screen ANSI-only output)
    if [ "$len" -eq 0 ]; then
        continue
    fi

    # Skip the prompt line (doesn't need to be 140)
    if [[ "$stripped" == *"Enter your choice"* ]]; then
        continue
    fi

    if [ "$len" -ne 140 ]; then
        all_lines_correct=false
        ((wrong_lines++))
        echo -e "${RED}  Line length $len (expected 140): ${stripped:0:50}...${NC}"
    fi
done < <(show_main_menu 2>/dev/null)

if [ "$all_lines_correct" = true ]; then
    ((TESTS_PASSED++))
    echo -e "${GREEN}✓ PASS${NC}: All menu lines are exactly 140 characters"
else
    ((TESTS_FAILED++))
    echo -e "${RED}✗ FAIL${NC}: $wrong_lines lines have incorrect width"
fi
((TESTS_RUN++))

# ============================================================================
# Test: Border alignment consistency
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Testing border character alignment"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Verify all lines start with ║ and end with ║ (except top/bottom)
all_borders_correct=true

while IFS= read -r line; do
    if [ -z "$line" ]; then
        continue
    fi
    stripped=$(echo "$line" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g')
    
    # Skip prompt and empty lines
    if [[ "$stripped" == *"Enter your choice"* ]] || [ -z "$stripped" ]; then
        continue
    fi
    
    first_char="${stripped:0:1}"
    last_char="${stripped: -1}"
    
    # Check that box lines have proper borders
    if [[ "$first_char" == "║" ]] && [[ "$last_char" != "║" ]]; then
        all_borders_correct=false
        echo -e "${RED}  Missing right border: ${stripped:0:50}...${NC}"
    fi
    if [[ "$first_char" == "╔" ]] && [[ "$last_char" != "╗" ]]; then
        all_borders_correct=false
        echo -e "${RED}  Missing top-right corner: ${stripped:0:50}...${NC}"
    fi
    if [[ "$first_char" == "╚" ]] && [[ "$last_char" != "╝" ]]; then
        all_borders_correct=false
        echo -e "${RED}  Missing bottom-right corner: ${stripped:0:50}...${NC}"
    fi
    if [[ "$first_char" == "╠" ]] && [[ "$last_char" != "╣" ]]; then
        all_borders_correct=false
        echo -e "${RED}  Missing separator right: ${stripped:0:50}...${NC}"
    fi
done < <(show_main_menu 2>/dev/null)

if [ "$all_borders_correct" = true ]; then
    ((TESTS_PASSED++))
    echo -e "${GREEN}✓ PASS${NC}: All border characters properly aligned"
else
    ((TESTS_FAILED++))
    echo -e "${RED}✗ FAIL${NC}: Border alignment issues detected"
fi
((TESTS_RUN++))

# ============================================================================
# Summary
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Test Summary"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
