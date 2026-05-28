#!/bin/bash
#
# Script Launcher
# Interactive menu for frequently used scripts
#

LAUNCHER_VERSION="1.2.0"

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
EMOJI_GENERATOR_DIR="/Users/yosii/work/git/personal_code/code/python/emoji_generator"
EMOJI_GENERATOR_VENV="$EMOJI_GENERATOR_DIR/.venv"
NUGGETS_DIR="/Users/yosii/work/git/personal_code/code/python/knowledge/oneliners"
BACKUP_AGENT_SCRIPT="/Users/yosii/work/git/personal_code/agents/backup/backup_agent.py"
BACKUP_VENV="/Users/yosii/work/git/git_backup/yosi_general_venv"
GITHUB_MERGER_DIR="/Users/yosii/work/git/personal_code/automations/github_approve_merge"
GITHUB_MERGER_VENV="$GITHUB_MERGER_DIR/.venv"

# Colors for output (using $'...' for proper escape interpretation)
GREEN=$'\033[0;32m'
BLUE=$'\033[0;34m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
MAGENTA=$'\033[0;35m'
NC=$'\033[0m' # No Color
BOLD=$'\033[1m'

# Sprint-scoped reminder types: read from remind_champion.py (REMINDER_TEMPLATES minus DoD).
print_release_reminder_types_for_prompt() {
	echo -e "${BOLD}Reminder Types:${NC}"
	if [ ! -f "$REMINDER_SCRIPT" ]; then
		echo -e "  ${YELLOW}(remind_champion.py not found)${NC}"
		echo ""
		return 1
	fi
	local tsv ec
	tsv=$(python3 "$REMINDER_SCRIPT" --list-release-reminder-types-tsv 2>/dev/null)
	ec=$?
	if [ "$ec" -ne 0 ] || [ -z "$tsv" ]; then
		echo -e "  ${YELLOW}(Could not load types — try: python3 \"\$REMINDER_SCRIPT\" --list-release-reminder-types-tsv)${NC}"
		echo ""
		return 1
	fi
	local line key summary
	while IFS= read -r line || [ -n "$line" ]; do
		[ -z "$line" ] && continue
		key="${line%%$'\t'*}"
		summary="${line#*$'\t'}"
		printf "  ${GREEN}%-22s${NC} - %s\n" "$key" "$summary"
	done <<< "$tsv"
	echo ""
	echo -e "  ${BOLD}(DoD:${NC} menu ${GREEN}[4]${NC} / ${GREEN}[5]${NC}; full templates: ${GREEN}python3${NC} \"\$REMINDER_SCRIPT\" --list-types)"
	echo ""
}

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
	print_menu_item "7" "Emoji Generator"
	print_menu_item "8" "Backup Manager"
	print_menu_item "9" "GitHub PR Merger"
	print_box_empty
	print_box_separator
	print_box_empty
	print_menu_item "0" "Exit" "$YELLOW"
	print_box_empty
	print_box_bottom
	echo ""
	printf "   ${BOLD}➜ Enter your choice [0-9]: ${NC}"
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
	echo -e "${BOLD}${CYAN}║  ${GREEN}[15]${CYAN}  Send Team Message (Unicast DMs)          ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[16]${CYAN}  Send Heads-Up (heads_up, pick sprint)   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[17]${CYAN}  Send DoD Heads-Up (next week's DoD)     ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}   ← Back to Main Menu                     ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-17]: ${NC}"
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
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Start Meeting (CLI + Banner)            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Start Meeting (CLI + Banner + Text)     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Start Meeting (Web UI)                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  View Meeting History                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  View History (Custom Range)            ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-6]: ${NC}"
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
			print_release_reminder_types_for_prompt
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
			print_release_reminder_types_for_prompt
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
		15)
			clear_screen
			echo -e "${CYAN}Send Team Message (Unicast DMs)${NC}"
			echo ""
			echo -e "${BOLD}Sends a message as individual DMs to each team member.${NC}"
			echo ""
			echo -n "Enter message: "
			read team_msg
			if [ -z "$team_msg" ]; then
				echo "Error: No message provided"
				sleep 2
				continue
			fi
			echo ""
			echo -e "Recipients:"
			echo -e "  ${GREEN}[1]${NC}  Team members only (default)"
			echo -e "  ${GREEN}[2]${NC}  Team members + Tech Leads (Yocheved, Guy)"
			echo -e "  ${GREEN}[3]${NC}  Cherry-pick specific people"
			echo ""
			echo -n "Choose [1-3]: "
			read recipient_choice
			recipient_choice=${recipient_choice:-1}

			local extra_flags=""
			case "$recipient_choice" in
			2)
				extra_flags="--include-tls"
				;;
			3)
				echo -n "Enter names (comma-separated, e.g. chen,muhe): "
				read only_names
				if [ -z "$only_names" ]; then
					echo "Error: No names provided"
					sleep 2
					continue
				fi
				extra_flags="--only $only_names"
				;;
			esac

			echo ""
			echo -e "${YELLOW}Dry-run first? (Y/n): ${NC}"
			read dry_first
			if [[ ! "$dry_first" =~ ^[Nn]$ ]]; then
				python3 "$REMINDER_SCRIPT" --dry-run --send-team "$team_msg" $extra_flags
				echo ""
				echo -e "${YELLOW}Send for real now? (y/N): ${NC}"
				read confirm_send
				if [[ "$confirm_send" =~ ^[Yy]$ ]]; then
					echo ""
					python3 "$REMINDER_SCRIPT" --send-team "$team_msg" $extra_flags
				else
					echo "Send cancelled."
				fi
			else
				python3 "$REMINDER_SCRIPT" --send-team "$team_msg" $extra_flags
			fi
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
		16)
			clear_screen
			echo -e "${CYAN}Send Heads-Up Reminder${NC} ${BOLD}(reminder type: heads_up)${NC}"
			echo ""
			print_release_reminder_types_for_prompt
			echo -n "Enter sprint (e.g., Q2-S1 or 26.Q2.2): "
			read sprint_hu
			if [ -z "$sprint_hu" ]; then
				echo "Error: No sprint provided"
				sleep 2
				continue
			fi
			echo ""
			echo -e "Will run: ${BOLD}python3 remind_champion.py ${sprint_hu} heads_up${NC}"
			echo ""
			echo -e "${YELLOW}Dry-run first? (Y/n): ${NC}"
			read dry_first
			if [[ ! "$dry_first" =~ ^[Nn]$ ]]; then
				python3 "$REMINDER_SCRIPT" --dry-run "$sprint_hu" heads_up
				echo ""
				echo -e "${YELLOW}Send for real now? (y/N): ${NC}"
				read confirm_send
				if [[ "$confirm_send" =~ ^[Yy]$ ]]; then
					echo ""
					python3 "$REMINDER_SCRIPT" "$sprint_hu" heads_up
				else
					echo "Send cancelled."
				fi
			else
				python3 "$REMINDER_SCRIPT" "$sprint_hu" heads_up
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		17)
			clear_screen
			echo -e "${CYAN}Send DoD Heads-Up${NC} ${BOLD}(next week's DoD champion)${NC}"
			echo ""
			echo -e "Will run: ${BOLD}python3 remind_champion.py --dod-heads-up${NC}"
			echo ""
			echo -e "${BOLD}Mode:${NC}"
			echo -e "  ${GREEN}[1]${NC} Dry-run (preview only, no Slack)"
			echo -e "  ${GREEN}[2]${NC} Test (real Slack DM, redirected to yosi_test)"
			echo -e "  ${GREEN}[3]${NC} Test + Dry-run (verify test banner without sending)"
			echo -e "  ${GREEN}[4]${NC} REAL send (to next week's DoD champion)"
			echo -e "  ${YELLOW}[0]${NC} Cancel"
			echo ""
			echo -n "Choose mode [0-4]: "
			read dod_hu_mode
			echo ""
			case "$dod_hu_mode" in
			1)
				python3 "$REMINDER_SCRIPT" --dry-run --dod-heads-up
				;;
			2)
				python3 "$REMINDER_SCRIPT" --test --dod-heads-up
				;;
			3)
				python3 "$REMINDER_SCRIPT" --test --dry-run --dod-heads-up
				;;
			4)
				echo -e "${YELLOW}This will send a REAL Slack DM to next week's DoD champion.${NC}"
				echo -n "Are you sure? (y/N): "
				read confirm_dod_hu
				if [[ "$confirm_dod_hu" =~ ^[Yy]$ ]]; then
					python3 "$REMINDER_SCRIPT" --dod-heads-up
				else
					echo "Send cancelled."
				fi
				;;
			0)
				echo "Cancelled."
				;;
			*)
				echo -e "${YELLOW}Invalid choice.${NC}"
				;;
			esac
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
			echo -e "${CYAN}Starting Daily Standup (CLI + Banner)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode cli --team imagine_dragons -b
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -n "Enter banner text: "
			read banner_text
			echo ""
			echo -e "${CYAN}Starting Daily Standup (CLI + Banner + Text)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			if [ -z "$banner_text" ]; then
				python main.py --mode cli --team imagine_dragons -b
			else
				python main.py --mode cli --team imagine_dragons -b --banner-text "$banner_text"
			fi
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
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
		5)
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
		6)
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
			echo -e "${RED}Invalid choice. Please try again.${NC}"
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

# Show emoji generator submenu
show_emoji_generator_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║          🎨 EMOJI GENERATOR MENU                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Search Emoji (One-shot Query)           ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Interactive Mode (REPL)                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  List All Emojis                         ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Add New Emoji (Edit YAML)               ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-4]: ${NC}"
}

# Emoji generator menu handler
handle_emoji_generator_menu() {
	# Check if venv exists
	if [ ! -d "$EMOJI_GENERATOR_VENV" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Emoji Generator venv not found${NC}"
		echo ""
		echo "To set up, run:"
		echo "  cd $EMOJI_GENERATOR_DIR"
		echo "  python3 -m venv .venv"
		echo "  source .venv/bin/activate"
		echo "  pip install -e ."
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_emoji_generator_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			echo -n "Enter search query: "
			read query
			if [ -z "$query" ]; then
				echo "Error: No query provided"
				sleep 2
				continue
			fi
			echo ""
			cd "$EMOJI_GENERATOR_DIR"
			source "$EMOJI_GENERATOR_VENV/bin/activate"
			devmoji "$query"
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Starting Emoji Generator (Interactive Mode)...${NC}"
			echo ""
			cd "$EMOJI_GENERATOR_DIR"
			source "$EMOJI_GENERATOR_VENV/bin/activate"
			devmoji --repl
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			cd "$EMOJI_GENERATOR_DIR"
			source "$EMOJI_GENERATOR_VENV/bin/activate"
			devmoji --list
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			local yaml_file="$EMOJI_GENERATOR_DIR/emoji_generator/data/emojis.yaml"
			echo -e "${CYAN}Opening emojis.yaml in editor...${NC}"
			echo ""
			${EDITOR:-vim} "$yaml_file"
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

# Show GitHub PR merger submenu
show_github_merger_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║          🔀 GITHUB PR MERGER MENU               ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Auth Status                              ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Auth Login (Browser)                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Dry-Run (Preview Classifications)       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Run (Approve + Merge)                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Cleanup Old Logs (GC)                   ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-5]: ${NC}"
}

# GitHub PR merger menu handler
handle_github_merger_menu() {
	if [ ! -d "$GITHUB_MERGER_DIR" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: GitHub PR Merger dir not found at $GITHUB_MERGER_DIR${NC}"
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	if ! command -v uv >/dev/null 2>&1; then
		clear_screen
		echo -e "${YELLOW}Warning: 'uv' not found in PATH. Install from https://docs.astral.sh/uv/${NC}"
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_github_merger_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			cd "$GITHUB_MERGER_DIR"
			uv run gh-approve-merge auth status
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Opening browser for GitHub login...${NC}"
			echo -e "${YELLOW}Sign in to github.com (SSO included). Session saved on success.${NC}"
			echo ""
			cd "$GITHUB_MERGER_DIR"
			uv run gh-approve-merge auth login
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3 | 4)
			local dry_flag=""
			local mode_label="Run (REAL)"
			if [ "$choice" = "3" ]; then
				dry_flag="--dry-run"
				mode_label="Dry-Run"
			fi
			clear_screen
			echo -e "${CYAN}${mode_label}: GitHub PR Merger${NC}"
			echo ""
			echo -e "${BOLD}Input:${NC}"
			echo -e "  ${GREEN}[1]${NC}  Paste URLs (space-separated)"
			echo -e "  ${GREEN}[2]${NC}  Path to file (one URL per line)"
			echo ""
			echo -n "Choose [1-2]: "
			read input_mode
			local extra_args=""
			case "$input_mode" in
			1)
				echo -n "Enter PR URLs (space-separated): "
				read pr_urls
				if [ -z "$pr_urls" ]; then
					echo "Error: No URLs provided"
					sleep 2
					continue
				fi
				extra_args="$pr_urls"
				;;
			2)
				echo -n "Enter path to URL file: "
				read pr_file
				if [ -z "$pr_file" ] || [ ! -f "$pr_file" ]; then
					echo "Error: File not found"
					sleep 2
					continue
				fi
				extra_args="--file $pr_file"
				;;
			*)
				echo "Invalid choice."
				sleep 1
				continue
				;;
			esac
			echo ""
			echo -e "${YELLOW}Redact PR slugs in logs (for shareable artifacts)? (y/N): ${NC}"
			read redact
			local redact_flag=""
			if [[ "$redact" =~ ^[Yy]$ ]]; then
				redact_flag="--redact-logs"
			fi
			echo ""
			cd "$GITHUB_MERGER_DIR"
			uv run gh-approve-merge run $dry_flag $redact_flag $extra_args
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -e "${CYAN}Cleaning up old run logs (retention sweep)...${NC}"
			echo ""
			cd "$GITHUB_MERGER_DIR"
			uv run gh-approve-merge gc
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

# Show backup manager submenu
show_backup_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║           💾 BACKUP MANAGER MENU                ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  System Status (Health Check)            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Run Git Backup (dotfiles + repos)       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Run OneDrive Backup                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Run Obsidian Checkpoint                 ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Run All Backups                         ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  LaunchAgent Status                      ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[7]${CYAN}  View Backup Logs                        ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[8]${CYAN}  Show Config Summary                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[9]${CYAN}  Validate Config Paths                   ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-9]: ${NC}"
}

# Backup manager menu handler
handle_backup_menu() {
	if [ ! -f "$BACKUP_AGENT_SCRIPT" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Backup agent not found at $BACKUP_AGENT_SCRIPT${NC}"
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	local backup_python="$BACKUP_VENV/bin/python"
	if [ ! -f "$backup_python" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Backup venv not found at $BACKUP_VENV${NC}"
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_backup_menu
		read choice

		case "$choice" in
		1)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" status
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${YELLOW}Run as dry-run first? (Y/n): ${NC}"
			read dry_first
			if [[ ! "$dry_first" =~ ^[Nn]$ ]]; then
				"$backup_python" "$BACKUP_AGENT_SCRIPT" run git --dry-run
				echo ""
				echo -e "${YELLOW}Run for real now? (y/N): ${NC}"
				read confirm
				if [[ "$confirm" =~ ^[Yy]$ ]]; then
					echo ""
					"$backup_python" "$BACKUP_AGENT_SCRIPT" run git
				fi
			else
				"$backup_python" "$BACKUP_AGENT_SCRIPT" run git
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" run onedrive
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" run checkpoint
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -e "${YELLOW}This will run ALL backups. Continue? (y/N): ${NC}"
			read confirm
			if [[ "$confirm" =~ ^[Yy]$ ]]; then
				"$backup_python" "$BACKUP_AGENT_SCRIPT" run all
			else
				echo "Cancelled."
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" launchctl status
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		7)
			clear_screen
			echo -e "${CYAN}Which job logs to view?${NC}"
			echo ""
			echo -e "  ${GREEN}[1]${NC}  Git Backup"
			echo -e "  ${GREEN}[2]${NC}  OneDrive Backup"
			echo -e "  ${GREEN}[3]${NC}  Obsidian Checkpoint"
			echo ""
			echo -n "Choice [1-3]: "
			read log_choice
			local job_name=""
			case "$log_choice" in
			1) job_name="gitbackup" ;;
			2) job_name="onedrive" ;;
			3) job_name="checkpoint" ;;
			*)
				echo "Invalid choice."
				sleep 1
				continue
				;;
			esac
			echo ""
			"$backup_python" "$BACKUP_AGENT_SCRIPT" launchctl logs "$job_name"
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		8)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" config show
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		9)
			clear_screen
			"$backup_python" "$BACKUP_AGENT_SCRIPT" config validate
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

	if [ ! -d "$EMOJI_GENERATOR_VENV" ]; then
		echo -e "${YELLOW}Warning: Emoji Generator venv not found at $EMOJI_GENERATOR_VENV${NC}"
	fi

	if [ ! -f "$BACKUP_AGENT_SCRIPT" ]; then
		echo -e "${YELLOW}Warning: Backup agent not found at $BACKUP_AGENT_SCRIPT${NC}"
	fi

	if [ ! -d "$GITHUB_MERGER_DIR" ]; then
		echo -e "${YELLOW}Warning: GitHub PR Merger dir not found at $GITHUB_MERGER_DIR${NC}"
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
		7)
			handle_emoji_generator_menu
			;;
		8)
			handle_backup_menu
			;;
		9)
			handle_github_merger_menu
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
	case "${1:-}" in
	--version | -v)
		echo "launcher.sh v${LAUNCHER_VERSION}"
		exit 0
		;;
	esac
	main
fi
