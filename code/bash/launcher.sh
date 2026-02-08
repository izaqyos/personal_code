#!/bin/bash
#
# Script Launcher
# Interactive menu for frequently used scripts
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACKER_SCRIPT="/Users/yosii/work/git/personal_code/code/AI/cursor/tracking/cursor_tracker.py"
REMINDER_SCRIPT="/Users/yosii/work/CheckPoint/Jira/release/reminder_app/remind_champion.py"
REPO_CLEANER_DIR="/Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner"
REPO_CLEANER_VENV="$REPO_CLEANER_DIR/.venv"
CONTEXT_GENERATOR_SCRIPT="/Users/yosii/work/context/tools/generate_context.sh"
DAILY_RUNNER_DIR="/Users/yosii/work/git/personal_code/code/python/tools/daily_runner"
DAILY_RUNNER_VENV="$DAILY_RUNNER_DIR/.venv"
MCP_HELPER_DIR="/Users/yosii/work/git/personal_code/code/python/tools/mcp_helper"
MCP_HELPER_VENV="$MCP_HELPER_DIR/.venv"
NUGGETS_DIR="/Users/yosii/work/git/personal_code/code/python/knowledge/oneliners"

# Colors for output (using $'...' for proper escape interpretation)
GREEN=$'\033[0;32m'
BLUE=$'\033[0;34m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
MAGENTA=$'\033[0;35m'
NC=$'\033[0m' # No Color
BOLD=$'\033[1m'

# Box width constants for 140-char layout
BOX_WIDTH=140
BOX_INNER=138
CONTENT_WIDTH=132 # BOX_INNER - 6 (3 padding each side)

# ============================================================================
# ANSI-aware string formatting functions
# ============================================================================

# Strip ANSI escape codes from a string to get visible text only
# Usage: stripped=$(strip_ansi "$colored_string")
strip_ansi() {
	local input="$1"
	# Remove all ANSI escape sequences (colors, formatting, cursor movement)
	echo -e "$input" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g'
}

# Get the visible length of a string (excluding ANSI codes, accounting for wide chars)
# Usage: len=$(visible_length "$colored_string")
visible_length() {
	local input="$1"
	local stripped
	stripped=$(strip_ansi "$input")

	# Try to use wc -m for proper multi-byte character counting
	# This handles emojis and wide characters better
	if command -v wc &>/dev/null; then
		# Use printf to avoid newline, then count display width
		# Note: This still won't be perfect for all emojis, but better than ${#stripped}
		local len
		len=$(printf "%s" "$stripped" | wc -m | tr -d ' ')
		echo "$len"
	else
		echo ${#stripped}
	fi
}

# Pad a string with spaces on the right to reach exact visible width
# Usage: padded=$(pad_right "$string" 50)
pad_right() {
	local content="$1"
	local target_width="$2"
	local vis_len
	vis_len=$(visible_length "$content")
	local padding=$((target_width - vis_len))

	if [ $padding -gt 0 ]; then
		printf "%s%*s" "$content" "$padding" ""
	else
		printf "%s" "$content"
	fi
}

# Pad a string with spaces on both sides to center it
# Usage: centered=$(pad_center "$string" 50)
pad_center() {
	local content="$1"
	local target_width="$2"
	local vis_len
	vis_len=$(visible_length "$content")
	local total_padding=$((target_width - vis_len))
	local pad_left=$((total_padding / 2))
	local pad_right=$((total_padding - pad_left))

	if [ $total_padding -gt 0 ]; then
		printf "%*s%s%*s" "$pad_left" "" "$content" "$pad_right" ""
	else
		printf "%s" "$content"
	fi
}

# Get a random programming nugget
# Python has double chance (2/6), others have 1/6 each
# Sets global variables: NUGGET_TAG, NUGGET_COLOR, NUGGET_LINE1, NUGGET_LINE2
get_random_nugget() {
	local lang_choice=$((RANDOM % 6))
	local lang_file=""

	NUGGET_TAG=""
	NUGGET_COLOR=""
	NUGGET_LINE1=""
	NUGGET_LINE2=""

	case $lang_choice in
	0 | 1) # Python gets 2/6 chance
		lang_file="python.json"
		NUGGET_TAG="Python"
		NUGGET_COLOR="${GREEN}"
		;;
	2)
		lang_file="bash.json"
		NUGGET_TAG="Bash"
		NUGGET_COLOR="${YELLOW}"
		;;
	3)
		lang_file="cpp.json"
		NUGGET_TAG="C++"
		NUGGET_COLOR="${BLUE}"
		;;
	4)
		lang_file="nodejs.json"
		NUGGET_TAG="Node.js"
		NUGGET_COLOR="${MAGENTA}"
		;;
	5)
		lang_file="javascript.json"
		NUGGET_TAG="JS"
		NUGGET_COLOR="${CYAN}"
		;;
	esac

	local json_path="${NUGGETS_DIR}/${lang_file}"

	# Check if file exists and jq is available
	if [ -f "$json_path" ] && command -v jq &>/dev/null; then
		local count=$(jq '.nuggets | length' "$json_path" 2>/dev/null)
		if [ -n "$count" ] && [ "$count" -gt 0 ]; then
			local idx=$((RANDOM % count))
			local nugget=$(jq -r ".nuggets[$idx]" "$json_path" 2>/dev/null)
			if [ -n "$nugget" ] && [ "$nugget" != "null" ]; then
				# Max chars for first line (after [Tag] ) - 140 char box
				# "   [Tag    ]  text..." = 3 + 9 + 2 + text = 14 + text
				# 138 inner - 14 = 124 chars for text on line 1
				local max_line1=118
				local max_line2=128 # Second line has more space (no tag, just 14 space indent)

				if [ ${#nugget} -le $max_line1 ]; then
					# Fits on one line
					NUGGET_LINE1="$nugget"
					NUGGET_LINE2=""
				else
					# Need to wrap - find a good break point
					local break_point=$max_line1
					# Try to break at a space
					while [ $break_point -gt 60 ] && [ "${nugget:$break_point:1}" != " " ]; do
						((break_point--))
					done
					if [ $break_point -le 60 ]; then
						break_point=$max_line1
					fi

					NUGGET_LINE1="${nugget:0:$break_point}"
					local remaining="${nugget:$break_point}"
					remaining="${remaining# }" # Trim leading space

					if [ ${#remaining} -gt $max_line2 ]; then
						NUGGET_LINE2="${remaining:0:$((max_line2 - 3))}..."
					else
						NUGGET_LINE2="$remaining"
					fi
				fi
				return
			fi
		fi
	fi

	# Fallback if no nuggets available
	NUGGET_LINE1="💡 Loading wisdom..."
	NUGGET_LINE2=""
}

# Clear screen function
clear_screen() {
	clear
}

# ============================================================================
# Box drawing functions (120-char wide, ANSI-aware)
# ============================================================================

# Inner width: 138 chars (140 - 2 for ║ borders)
BOX_INNER_WIDTH=138

# Print a line inside the box with proper padding
# Usage: print_box_line "content" [center]
print_box_line() {
	local content="$1"
	local align="${2:-left}" # left or center
	local padded

	if [ "$align" = "center" ]; then
		padded=$(pad_center "$content" $BOX_INNER_WIDTH)
	else
		# Left align with 3-char indent
		local indented="   $content"
		padded=$(pad_right "$indented" $BOX_INNER_WIDTH)
	fi

	printf "${BOLD}${CYAN}║${NC}%s${BOLD}${CYAN}║${NC}\n" "$padded"
}

# Print empty box line (138 spaces)
print_box_empty() {
	printf "${BOLD}${CYAN}║%138s║${NC}\n" ""
}

# Print box top border
print_box_top() {
	printf "${BOLD}${CYAN}╔"
	printf '═%.0s' {1..138}
	printf "╗${NC}\n"
}

# Print box bottom border
print_box_bottom() {
	printf "${BOLD}${CYAN}╚"
	printf '═%.0s' {1..138}
	printf "╝${NC}\n"
}

# Print box separator line
print_box_separator() {
	printf "${BOLD}${CYAN}╠"
	printf '═%.0s' {1..138}
	printf "╣${NC}\n"
}

# Print menu item with proper ANSI-aware padding
# Usage: print_menu_item "1" "Menu Label" [color]
print_menu_item() {
	local key="$1"
	local label="$2"
	local key_color="${3:-$GREEN}"

	# Build the content: "   [1]  Label"
	local content="   ${key_color}[${key}]${NC}  ${label}"
	local padded
	padded=$(pad_right "$content" $BOX_INNER_WIDTH)

	printf "${BOLD}${CYAN}║${NC}%s${BOLD}${CYAN}║${NC}\n" "$padded"
}

# Print nugget line with language tag
# Usage: print_nugget_line "$TAG" "$COLOR" "$TEXT" [is_continuation]
print_nugget_line() {
	local tag="$1"
	local color="$2"
	local text="$3"
	local is_continuation="${4:-false}"

	if [ "$is_continuation" = "true" ]; then
		# Continuation line: indent to align with first line text (14 spaces)
		local content="              ${text}"
		local padded
		padded=$(pad_right "$content" $BOX_INNER_WIDTH)
		printf "${BOLD}${CYAN}║${NC}%s${BOLD}${CYAN}║${NC}\n" "$padded"
	else
		# First line with tag: "   [Tag    ]  text"
		local plain_tag
		plain_tag=$(printf "[%-7s]" "$tag")
		local colored_tag="${color}${plain_tag}${NC}"

		# Build the full content line with colors
		local content="   ${colored_tag}  ${text}"

		# Pad to exact width using ANSI-aware function
		local padded
		padded=$(pad_right "$content" $BOX_INNER_WIDTH)

		printf "${BOLD}${CYAN}║${NC}%s${BOLD}${CYAN}║${NC}\n" "$padded"
	fi
}

# Show main menu
show_main_menu() {
	clear_screen
	local current_date=$(date "+%a %b %d, %Y")
	local current_time=$(date "+%H:%M:%S")

	# Get random nugget (sets NUGGET_TAG, NUGGET_COLOR, NUGGET_LINE1, NUGGET_LINE2)
	get_random_nugget

	echo ""
	print_box_top
	print_box_empty
	# Use >> instead of emoji to avoid display width issues
	print_box_line ">> YOSI's SCRIPT LAUNCHER - MAIN MENU <<" "center"
	print_box_line "${current_date}   │   ${current_time}" "center"
	print_box_empty
	print_box_separator
	print_box_empty

	# Print nugget line(s)
	print_nugget_line "$NUGGET_TAG" "$NUGGET_COLOR" "$NUGGET_LINE1"
	if [ -n "$NUGGET_LINE2" ]; then
		print_nugget_line "" "" "$NUGGET_LINE2" "true"
	fi

	print_box_empty
	print_box_separator
	print_box_empty
	print_menu_item "1" "Cursor Tracker"
	print_menu_item "2" "Remind Champion"
	print_menu_item "3" "Repo Cleaner"
	print_menu_item "4" "Context Generator"
	print_menu_item "5" "Daily Standup Timer"
	print_menu_item "6" "MCP Health Check"
	print_box_empty
	print_box_separator
	print_box_empty
	print_menu_item "0" "Exit" "$YELLOW"
	print_box_empty
	print_box_bottom
	echo ""
	printf "   ${BOLD}➜ Enter your choice [0-6]: ${NC}"
}

# Show tracker submenu
show_tracker_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║            📊 CURSOR TRACKER MENU               ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Show Status                              ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Set Usage (Sync with Dashboard)         ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Add Usage (Incremental)                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  View History                            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Reset Counter                           ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  Show Help                                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-6]: ${NC}"
}

# Show repo cleaner submenu
show_repo_cleaner_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║             🧹 REPO CLEANER MENU                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Current Directory (Dry Run)             ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Current Directory (Clean)               ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Specific Directory (Dry Run)            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Specific Directory (Clean)              ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  View Cleanup History                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  List Available Languages                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-6]: ${NC}"
}

# Show context generator submenu
show_context_generator_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║          📄 CONTEXT GENERATOR MENU              ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Generate Next Month's File              ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Generate Current Month's File           ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Generate Specific Month                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  List Existing Files                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Show Help                                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-5]: ${NC}"
}

# Show reminder submenu
show_reminder_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║           🔔 REMIND CHAMPION MENU               ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}   Show Release Schedule                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}   Show DoD Schedule                       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}   Show All Schedules                      ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}   Send DoD Reminder                       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}   Send TL DoD Reminder                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}   Cron Mode (Auto-send)                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[7]${CYAN}   Validate Schedules                      ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[8]${CYAN}   View Reminder Log                       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[9]${CYAN}   List Reminder Types                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[10]${CYAN}  List Team Members                       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[11]${CYAN}  Check DoD for Date                      ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[12]${CYAN}  Send Release Reminder                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[13]${CYAN}  Dry-Run Release Reminder                ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[14]${CYAN}  Send Execution Report                   ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}   ← Back to Main Menu                     ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-14]: ${NC}"
}

# Show daily timer submenu
show_daily_timer_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║         ⏱️  DAILY STANDUP TIMER MENU            ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Start Meeting (CLI)                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Start Meeting (Web UI)                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  View Meeting History                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  View History (Custom Range)            ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-4]: ${NC}"
}

# Tracker menu handler
handle_tracker_menu() {
	while true; do
		show_tracker_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			python3 "$TRACKER_SCRIPT"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Sync with Cursor Dashboard${NC}"
			echo "Check your usage at: https://cursor.com/dashboard?tab=usage"
			echo ""
			echo -n "Enter total usage from dashboard: "
			read total
			if [ -z "$total" ]; then
				echo "Error: No value provided"
				sleep 2
				continue
			fi
			python3 "$TRACKER_SCRIPT" set "$total"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -n "Enter number of requests to add: "
			read count
			if [ -z "$count" ]; then
				echo "Error: No count provided"
				sleep 2
				continue
			fi
			echo -n "Enter model name (or press Enter for 'standard'): "
			read model
			model=${model:-standard}
			python3 "$TRACKER_SCRIPT" add "$count" "$model"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			python3 "$TRACKER_SCRIPT" history
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -e "${YELLOW}Are you sure you want to reset the counter? (y/N): ${NC}"
			read confirm
			if [[ "$confirm" =~ ^[Yy]$ ]]; then
				python3 "$TRACKER_SCRIPT" reset
			else
				echo "Reset cancelled."
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			python3 "$TRACKER_SCRIPT" help
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Repo cleaner menu handler
handle_repo_cleaner_menu() {
	# Check if venv exists
	if [ ! -d "$REPO_CLEANER_VENV" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Repo Cleaner venv not found${NC}"
		echo ""
		echo "To set up, run:"
		echo "  cd $REPO_CLEANER_DIR"
		echo "  python3 -m venv .venv"
		echo "  source .venv/bin/activate"
		echo "  pip install -e ."
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_repo_cleaner_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			echo -e "${CYAN}Dry run on current directory...${NC}"
			echo ""
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner -n
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${GREEN}Cleaning current directory...${NC}"
			echo ""
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -n "Enter target directory path: "
			read target_dir
			if [ -z "$target_dir" ]; then
				echo "Error: No directory provided"
				sleep 2
				continue
			fi
			if [ ! -d "$target_dir" ]; then
				echo "Error: Directory does not exist"
				sleep 2
				continue
			fi
			echo ""
			echo -e "${CYAN}Dry run on: $target_dir${NC}"
			echo ""
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner -t "$target_dir" -n
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			echo -n "Enter target directory path: "
			read target_dir
			if [ -z "$target_dir" ]; then
				echo "Error: No directory provided"
				sleep 2
				continue
			fi
			if [ ! -d "$target_dir" ]; then
				echo "Error: Directory does not exist"
				sleep 2
				continue
			fi
			echo ""
			echo -e "${GREEN}Cleaning: $target_dir${NC}"
			echo ""
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner -t "$target_dir" --force
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner --history
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			cd "$REPO_CLEANER_DIR"
			source "$REPO_CLEANER_VENV/bin/activate"
			repo-cleaner --list-languages
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Context generator menu handler
handle_context_generator_menu() {
	while true; do
		show_context_generator_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			echo -e "${CYAN}Generating next month's context file...${NC}"
			echo ""
			"$CONTEXT_GENERATOR_SCRIPT"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Generating current month's context file...${NC}"
			echo ""
			"$CONTEXT_GENERATOR_SCRIPT" --current
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -n "Enter month (e.g., Jan, Feb, Mar): "
			read month
			if [ -z "$month" ]; then
				echo "Error: No month provided"
				sleep 2
				continue
			fi
			echo -n "Enter year (e.g., 2026): "
			read year
			if [ -z "$year" ]; then
				echo "Error: No year provided"
				sleep 2
				continue
			fi
			echo ""
			echo -e "${CYAN}Generating context file for $month $year...${NC}"
			echo ""
			"$CONTEXT_GENERATOR_SCRIPT" "$month" "$year"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			echo -e "${CYAN}Existing context files:${NC}"
			echo ""
			ls -la /Users/yosii/work/context/context_*
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			"$CONTEXT_GENERATOR_SCRIPT" --help
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Reminder menu handler
handle_reminder_menu() {
	while true; do
		show_reminder_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			python3 "$REMINDER_SCRIPT" --schedule
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			python3 "$REMINDER_SCRIPT" --dod-schedule
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			python3 "$REMINDER_SCRIPT" --show-all
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			python3 "$REMINDER_SCRIPT" --dod-reminder
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			python3 "$REMINDER_SCRIPT" --dod-tl-reminder
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			echo -e "${YELLOW}Run in test mode? (y/N): ${NC}"
			read test_mode
			if [[ "$test_mode" =~ ^[Yy]$ ]]; then
				python3 "$REMINDER_SCRIPT" --cron --test
			else
				python3 "$REMINDER_SCRIPT" --cron
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		7)
			clear_screen
			python3 "$REMINDER_SCRIPT" --validate
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		8)
			clear_screen
			echo -n "Number of entries to show (default 20): "
			read count
			count=${count:-20}
			python3 "$REMINDER_SCRIPT" --log "$count"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		9)
			clear_screen
			python3 "$REMINDER_SCRIPT" --list-types
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		10)
			clear_screen
			python3 "$REMINDER_SCRIPT" --list-team
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		11)
			clear_screen
			echo -n "Enter date (YYYY-MM-DD): "
			read date
			if [ -z "$date" ]; then
				echo "Error: No date provided"
				sleep 2
				continue
			fi
			python3 "$REMINDER_SCRIPT" --dod "$date"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		12)
			clear_screen
			echo -e "${CYAN}Send Release Reminder${NC}"
			echo ""
			echo -e "Reminder Types:"
			echo -e "  ${GREEN}risk_analysis${NC}       - Risk analysis reminder"
			echo -e "  ${GREEN}risk_analysis_final${NC} - Final risk analysis reminder"
			echo -e "  ${GREEN}dr_tomorrow${NC}         - DR is tomorrow reminder"
			echo -e "  ${GREEN}dr_today${NC}            - DR is today reminder"
			echo -e "  ${GREEN}prod_tomorrow${NC}       - Production is tomorrow reminder"
			echo -e "  ${GREEN}prod_today${NC}          - Production is today reminder"
			echo ""
			echo -n "Enter sprint (e.g., Q1-S1): "
			read sprint
			if [ -z "$sprint" ]; then
				echo "Error: No sprint provided"
				sleep 2
				continue
			fi
			echo -n "Enter reminder type: "
			read reminder_type
			if [ -z "$reminder_type" ]; then
				echo "Error: No reminder type provided"
				sleep 2
				continue
			fi
			echo ""
			echo -e "${YELLOW}Run in test mode? (y/N): ${NC}"
			read test_mode
			if [[ "$test_mode" =~ ^[Yy]$ ]]; then
				python3 "$REMINDER_SCRIPT" --test "$sprint" "$reminder_type"
			else
				python3 "$REMINDER_SCRIPT" "$sprint" "$reminder_type"
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		13)
			clear_screen
			echo -e "${CYAN}Dry-Run Release Reminder (Preview Only)${NC}"
			echo ""
			echo -e "Reminder Types:"
			echo -e "  ${GREEN}risk_analysis${NC}       - Risk analysis reminder"
			echo -e "  ${GREEN}risk_analysis_final${NC} - Final risk analysis reminder"
			echo -e "  ${GREEN}dr_tomorrow${NC}         - DR is tomorrow reminder"
			echo -e "  ${GREEN}dr_today${NC}            - DR is today reminder"
			echo -e "  ${GREEN}prod_tomorrow${NC}       - Production is tomorrow reminder"
			echo -e "  ${GREEN}prod_today${NC}          - Production is today reminder"
			echo ""
			echo -n "Enter sprint (e.g., Q1-S1): "
			read sprint
			if [ -z "$sprint" ]; then
				echo "Error: No sprint provided"
				sleep 2
				continue
			fi
			echo -n "Enter reminder type: "
			read reminder_type
			if [ -z "$reminder_type" ]; then
				echo "Error: No reminder type provided"
				sleep 2
				continue
			fi
			echo ""
			python3 "$REMINDER_SCRIPT" --dry-run "$sprint" "$reminder_type"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		14)
			clear_screen
			echo -e "${CYAN}Send Execution Report${NC}"
			echo ""
			echo -e "${BOLD}Usage Example:${NC}"
			echo -e "  ${DIM}cd /Users/yosii/work/CheckPoint/Jira/release/reminder_app${NC}"
			echo ""
			echo -e "  ${DIM}# Preview first:${NC}"
			echo -e "  ${DIM}python3 remind_champion.py --dry-run --send-report ../execution/2026/q1/reports/sprint3_execution_report_2026-01-23.json${NC}"
			echo ""
			echo -e "  ${DIM}# Send for real (will show preview + ask confirmation):${NC}"
			echo -e "  ${DIM}python3 remind_champion.py --send-report ../execution/2026/q1/reports/sprint3_execution_report_2026-01-23.json${NC}"
			echo ""
			echo -n "Enter path to execution report JSON: "
			read report_path
			if [ -z "$report_path" ]; then
				echo "Error: No report path provided"
				sleep 2
				continue
			fi
			echo ""
			echo -e "${YELLOW}Run in dry-run mode first? (Y/n): ${NC}"
			read dry_run_mode
			if [[ ! "$dry_run_mode" =~ ^[Nn]$ ]]; then
				python3 "$REMINDER_SCRIPT" --dry-run --send-report "$report_path"
				echo ""
				echo -e "${YELLOW}Send for real now? (y/N): ${NC}"
				read confirm_send
				if [[ "$confirm_send" =~ ^[Yy]$ ]]; then
					echo ""
					python3 "$REMINDER_SCRIPT" --send-report "$report_path"
				else
					echo "Send cancelled."
				fi
			else
				python3 "$REMINDER_SCRIPT" --send-report "$report_path"
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Daily timer menu handler
handle_daily_timer_menu() {
	# Check if venv exists
	if [ ! -d "$DAILY_RUNNER_VENV" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Daily Runner venv not found${NC}"
		echo ""
		echo "To set up, run:"
		echo "  cd $DAILY_RUNNER_DIR"
		echo "  python3 -m venv .venv"
		echo "  source .venv/bin/activate"
		echo "  pip install -e ."
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_daily_timer_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			echo -e "${CYAN}Starting Daily Standup (CLI mode)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode cli --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Starting Daily Standup (Web UI)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode ui --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -e "${CYAN}Meeting History (last 30 days):${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode history --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			echo -n "Enter number of days to show (default 30): "
			read days
			days=${days:-30}
			echo -n "Enter max entries to show (default 20): "
			read limit
			limit=${limit:-20}
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode history --team imagine_dragons --days "$days" --limit "$limit"
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Show MCP health check submenu
show_mcp_helper_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║          🔧 MCP HEALTH CHECK MENU               ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Quick Check (Token Validation)          ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Full Check (Token + Connection)         ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Check Specific Server                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  List Configured Servers                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Watch Mode (Continuous)                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  Auto-Refresh Atlassian Token            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[7]${CYAN}  Re-Authenticate Atlassian (Browser)     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[8]${CYAN}  Wipe & Re-Auth (Nuclear Option)         ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[9]${CYAN}  Cleanup Stale Processes (Auth Spam Fix) ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	echo -e "${BLUE}  ℹ️  Note: Token validation is the default (option 1).${NC}"
	echo -e "${BLUE}     Connection tests may show false negatives.${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-9]: ${NC}"
}

# MCP helper menu handler
handle_mcp_helper_menu() {
	# Check if venv exists
	if [ ! -d "$MCP_HELPER_VENV" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: MCP Helper venv not found${NC}"
		echo ""
		echo "To set up, run:"
		echo "  cd $MCP_HELPER_DIR"
		echo "  python3 -m venv .venv"
		echo "  source .venv/bin/activate"
		echo "  pip install -e ."
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_mcp_helper_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			echo -e "${CYAN}Running MCP Health Check (Token Validation)...${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Running Full MCP Health Check (with Connection Test)...${NC}"
			echo -e "${YELLOW}(Connection test spawns new processes - may show false negatives)${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check --with-mcp
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -e "${CYAN}Available servers:${NC}"
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health list-servers 2>/dev/null | grep -E "^\s+[a-zA-Z]" || echo "  github, slack, perimeter81-atlassian"
			deactivate
			echo ""
			echo -n "Enter server name: "
			read server_name
			if [ -z "$server_name" ]; then
				echo "Error: No server name provided"
				sleep 2
				cd - >/dev/null
				continue
			fi
			echo ""
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check --server "$server_name" -v
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			echo -e "${CYAN}Configured MCP Servers:${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health list-servers
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -n "Enter check interval in seconds (default 60): "
			read interval
			interval=${interval:-60}
			echo ""
			echo -e "${CYAN}Starting Watch Mode (Ctrl+C to stop)...${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check --watch --interval "$interval"
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			echo -e "${CYAN}Auto-refreshing Atlassian OAuth token...${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check --server perimeter81-atlassian --auto-refresh
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		7)
			clear_screen
			echo -e "${CYAN}Re-authenticating Atlassian (will open browser)...${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health check --server perimeter81-atlassian --reauth
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		8)
			clear_screen
			echo -e "${YELLOW}⚠️  WIPE & RE-AUTHENTICATE (Nuclear Option)${NC}"
			echo ""
			echo -e "${YELLOW}This will completely remove ALL OAuth tokens and force fresh authentication.${NC}"
			echo -e "${YELLOW}Use this when tokens are corrupted or in a bad state.${NC}"
			echo ""
			echo -e "Files that will be removed:"
			echo -e "  • Token files (*_tokens.json)"
			echo -e "  • Client registration (*_client_info.json)"
			echo -e "  • PKCE verifiers (*_code_verifier.txt)"
			echo -e "  • Lock files (*_lock.json)"
			echo ""
			echo -n "Enter server name (or press Enter for all Atlassian servers): "
			read server_name
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			if [ -z "$server_name" ]; then
				mcp-health wipe-reauth
			else
				mcp-health wipe-reauth -s "$server_name"
			fi
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		9)
			clear_screen
			echo -e "${CYAN}Cleanup Stale MCP Processes${NC}"
			echo ""
			echo -e "${YELLOW}This kills stale mcp-remote processes that cause auth popup spam.${NC}"
			echo -e "${YELLOW}Use when you see multiple browser tabs opening for OAuth.${NC}"
			echo ""
			cd "$MCP_HELPER_DIR"
			source "$MCP_HELPER_VENV/bin/activate"
			mcp-health cleanup
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Check if scripts exist
check_scripts() {
	if [ ! -f "$TRACKER_SCRIPT" ]; then
		echo -e "${YELLOW}Warning: cursor_tracker.py not found at $TRACKER_SCRIPT${NC}"
	fi

	if [ ! -f "$REMINDER_SCRIPT" ]; then
		echo -e "${YELLOW}Warning: remind_champion.py not found at $REMINDER_SCRIPT${NC}"
	fi

	if [ ! -d "$REPO_CLEANER_VENV" ]; then
		echo -e "${YELLOW}Warning: Repo Cleaner venv not found at $REPO_CLEANER_VENV${NC}"
	fi

	if [ ! -f "$CONTEXT_GENERATOR_SCRIPT" ]; then
		echo -e "${YELLOW}Warning: generate_context.sh not found at $CONTEXT_GENERATOR_SCRIPT${NC}"
	fi

	if [ ! -d "$DAILY_RUNNER_VENV" ]; then
		echo -e "${YELLOW}Warning: Daily Runner venv not found at $DAILY_RUNNER_VENV${NC}"
	fi

	if [ ! -d "$MCP_HELPER_VENV" ]; then
		echo -e "${YELLOW}Warning: MCP Helper venv not found at $MCP_HELPER_VENV${NC}"
	fi
}

# Main loop
main() {
	check_scripts

	while true; do
		show_main_menu
		read choice

		case "$choice" in
		1)
			if [ ! -f "$TRACKER_SCRIPT" ]; then
				echo -e "${YELLOW}Error: Tracker script not found!${NC}"
				sleep 2
				continue
			fi
			handle_tracker_menu
			;;
		2)
			if [ ! -f "$REMINDER_SCRIPT" ]; then
				echo -e "${YELLOW}Error: Reminder script not found!${NC}"
				sleep 2
				continue
			fi
			handle_reminder_menu
			;;
		3)
			handle_repo_cleaner_menu
			;;
		4)
			if [ ! -f "$CONTEXT_GENERATOR_SCRIPT" ]; then
				echo -e "${YELLOW}Error: Context generator script not found!${NC}"
				sleep 2
				continue
			fi
			handle_context_generator_menu
			;;
		5)
			handle_daily_timer_menu
			;;
		6)
			handle_mcp_helper_menu
			;;
		0)
			clear_screen
			echo -e "${GREEN}Goodbye!${NC}"
			exit 0
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}

# Run main function only if executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	main
fi
