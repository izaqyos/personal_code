#!/bin/bash
#
# Script Launcher
# Interactive menu for frequently used scripts
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACKER_SCRIPT="/Users/yosii/work/git/personal_code/code/AI/cursor/tracking/cursor_tracker.py"
REMINDER_SCRIPT="/Users/yosii/work/CheckPoint/Jira/release/reminder_app/remind_champion.py"
REPO_CLEANER_DIR="/Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner"
REPO_CLEANER_CMD="repo-cleaner"
CONTEXT_GENERATOR_SCRIPT="/Users/yosii/work/context/generate_context.sh"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Clear screen function
clear_screen() {
    clear
}

# Show main menu
show_main_menu() {
    clear_screen
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║     SCRIPT LAUNCHER - MAIN MENU        ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}Select a script:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC} - Cursor Tracker"
    echo -e "  ${GREEN}2${NC} - Remind Champion"
    echo -e "  ${GREEN}3${NC} - Repo Cleaner"
    echo -e "  ${GREEN}4${NC} - Context Generator"
    echo ""
    echo -e "  ${YELLOW}0${NC} - Exit"
    echo ""
    echo -n "Enter choice [0-4]: "
}

# Show tracker submenu
show_tracker_menu() {
    clear_screen
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║        CURSOR TRACKER MENU             ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}Select an action:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC} - Show Status"
    echo -e "  ${GREEN}2${NC} - Set Usage (Sync with Dashboard)"
    echo -e "  ${GREEN}3${NC} - Add Usage (Incremental)"
    echo -e "  ${GREEN}4${NC} - View History"
    echo -e "  ${GREEN}5${NC} - Reset Counter"
    echo -e "  ${GREEN}6${NC} - Show Help"
    echo ""
    echo -e "  ${YELLOW}0${NC} - Back to Main Menu"
    echo ""
    echo -n "Enter choice [0-6]: "
}

# Show repo cleaner submenu
show_repo_cleaner_menu() {
    clear_screen
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║        REPO CLEANER MENU               ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}Select an action:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC} - Current Directory (Dry Run)"
    echo -e "  ${GREEN}2${NC} - Current Directory (Clean)"
    echo -e "  ${GREEN}3${NC} - Specific Directory (Dry Run)"
    echo -e "  ${GREEN}4${NC} - Specific Directory (Clean)"
    echo ""
    echo -e "  ${GREEN}5${NC} - View Cleanup History"
    echo -e "  ${GREEN}6${NC} - List Available Languages"
    echo ""
    echo -e "  ${YELLOW}0${NC} - Back to Main Menu"
    echo ""
    echo -n "Enter choice [0-6]: "
}

# Show context generator submenu
show_context_generator_menu() {
    clear_screen
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║      CONTEXT GENERATOR MENU            ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}Select an action:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC} - Generate Next Month's File"
    echo -e "  ${GREEN}2${NC} - Generate Current Month's File"
    echo -e "  ${GREEN}3${NC} - Generate Specific Month"
    echo -e "  ${GREEN}4${NC} - List Existing Files"
    echo -e "  ${GREEN}5${NC} - Show Help"
    echo ""
    echo -e "  ${YELLOW}0${NC} - Back to Main Menu"
    echo ""
    echo -n "Enter choice [0-5]: "
}

# Show reminder submenu
show_reminder_menu() {
    clear_screen
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║      REMIND CHAMPION MENU             ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}Select an action:${NC}"
    echo ""
    echo -e "  ${GREEN}1${NC} - Show Release Schedule"
    echo -e "  ${GREEN}2${NC} - Show DoD Schedule"
    echo -e "  ${GREEN}3${NC} - Show All Schedules"
    echo -e "  ${GREEN}4${NC} - Send DoD Reminder"
    echo -e "  ${GREEN}5${NC} - Send TL DoD Reminder"
    echo -e "  ${GREEN}6${NC} - Cron Mode (Auto-send)"
    echo -e "  ${GREEN}7${NC} - Validate Schedules"
    echo -e "  ${GREEN}8${NC} - View Reminder Log"
    echo -e "  ${GREEN}9${NC} - List Reminder Types"
    echo -e "  ${GREEN}10${NC} - List Team Members"
    echo -e "  ${GREEN}11${NC} - Check DoD for Date"
    echo ""
    echo -e "  ${YELLOW}0${NC} - Back to Main Menu"
    echo ""
    echo -n "Enter choice [0-11]: "
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
    # Check if repo-cleaner is installed
    if ! command -v "$REPO_CLEANER_CMD" &> /dev/null; then
        clear_screen
        echo -e "${YELLOW}Warning: repo-cleaner not found in PATH${NC}"
        echo ""
        echo "To install, run:"
        echo "  cd $REPO_CLEANER_DIR"
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
                "$REPO_CLEANER_CMD" -n
                echo ""
                echo -n "Press Enter to continue..."
                read
                ;;
            2)
                clear_screen
                echo -e "${GREEN}Cleaning current directory...${NC}"
                echo ""
                "$REPO_CLEANER_CMD"
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
                "$REPO_CLEANER_CMD" -t "$target_dir" -n
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
                "$REPO_CLEANER_CMD" -t "$target_dir"
                echo ""
                echo -n "Press Enter to continue..."
                read
                ;;
            5)
                clear_screen
                "$REPO_CLEANER_CMD" --history
                echo ""
                echo -n "Press Enter to continue..."
                read
                ;;
            6)
                clear_screen
                "$REPO_CLEANER_CMD" --list-languages
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
    
    if ! command -v "$REPO_CLEANER_CMD" &> /dev/null; then
        echo -e "${YELLOW}Warning: repo-cleaner not installed (install from $REPO_CLEANER_DIR)${NC}"
    fi

    if [ ! -f "$CONTEXT_GENERATOR_SCRIPT" ]; then
        echo -e "${YELLOW}Warning: generate_context.sh not found at $CONTEXT_GENERATOR_SCRIPT${NC}"
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

# Run main function
main

