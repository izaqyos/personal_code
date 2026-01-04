#!/usr/bin/env python3
"""
Cursor AI Usage Tracker
Monitors your Cursor API usage and provides recommendations
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
MONTHLY_LIMIT = 1000
RESET_DAY = 1  # Day of month when limit resets
MAX_HISTORY_ENTRIES = 500  # Keep last N history entries
DATA_FILE = Path(__file__).parent / "usage_statistics.json"

# Model costs (in requests)
MODEL_COSTS = {
    "claude-4-opus": 4,
    "claude-4.1-opus": 4,
    "claude-4-sonnet": 1,
    "claude-4.5-sonnet": 1,
    "claude-4.5-haiku": 1,
    "claude-4.5-opus": 1,
    "composer-1": 1,
    "gemini": 1
}


def load_usage_data():
    """Load usage data from file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure history exists
            if "history" not in data:
                data["history"] = []
            return data
    return {"total_used": 0, "last_updated": None, "reset_date": None, "history": []}


def save_usage_data(data):
    """Save usage data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_next_reset_date():
    """Calculate next reset date (1st of next month)"""
    today = datetime.now()
    if today.day >= RESET_DAY:
        # Next month
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
    else:
        # This month
        next_month = today.month
        next_year = today.year
    
    return datetime(next_year, next_month, RESET_DAY)


def calculate_stats(used, reset_date):
    """Calculate usage statistics"""
    today = datetime.now()
    days_remaining = (reset_date - today).days + 1

    # Calculate period start (1st of current billing month)
    if reset_date.month > 1:
        period_start = datetime(reset_date.year, reset_date.month - 1, RESET_DAY)
    else:
        period_start = datetime(reset_date.year - 1, 12, RESET_DAY)

    days_in_period = (reset_date - period_start).days
    days_elapsed = days_in_period - days_remaining + 1
    
    remaining = MONTHLY_LIMIT - used
    daily_budget = MONTHLY_LIMIT / days_in_period
    used_today_budget = days_elapsed * daily_budget
    
    return {
        "remaining": remaining,
        "percentage_used": (used / MONTHLY_LIMIT) * 100,
        "days_remaining": days_remaining,
        "days_elapsed": days_elapsed,
        "daily_budget": daily_budget,
        "recommended_daily": remaining / days_remaining if days_remaining > 0 else 0,
        "on_track": used <= used_today_budget
    }


def get_status_emoji(percentage):
    """Get status emoji based on usage percentage"""
    if percentage < 50:
        return "🟢"
    elif percentage < 75:
        return "🟡"
    else:
        return "🔴"


def get_model_recommendation(remaining, days_remaining):
    """Recommend which models to use"""
    avg_remaining = remaining / days_remaining if days_remaining > 0 else 0
    
    if avg_remaining > 50:
        return "✅ Use any model comfortably"
    elif avg_remaining > 25:
        return "⚠️  Prefer standard models (1 req), limit premium usage"
    elif avg_remaining > 10:
        return "🚨 ONLY use standard models (1 req)"
    else:
        return "💀 CRITICAL: Use only for emergencies"


def update_usage(requests_to_add, model_name="standard"):
    """Update usage with new requests"""
    data = load_usage_data()
    reset_date = get_next_reset_date()
    now = datetime.now()

    # Check if we need to reset usage (but keep history)
    if data.get("reset_date"):
        last_reset = datetime.fromisoformat(data["reset_date"])
        if now >= last_reset:
            data["total_used"] = 0

    # Add new usage
    cost = MODEL_COSTS.get(model_name, 1)
    actual_cost = requests_to_add * cost
    data["total_used"] += actual_cost
    data["last_updated"] = now.isoformat()
    data["reset_date"] = reset_date.isoformat()

    # Add to history
    data["history"].append({
        "timestamp": now.isoformat(),
        "requests": requests_to_add,
        "model": model_name,
        "cost": actual_cost,
        "total_after": data["total_used"]
    })

    # Cleanup: keep only last N entries
    if len(data["history"]) > MAX_HISTORY_ENTRIES:
        data["history"] = data["history"][-MAX_HISTORY_ENTRIES:]

    save_usage_data(data)
    return data["total_used"]


def set_usage(total_requests):
    """Set usage to exact value from Cursor dashboard (non-incremental)"""
    data = load_usage_data()
    reset_date = get_next_reset_date()
    now = datetime.now()

    old_total = data.get("total_used", 0)
    data["total_used"] = total_requests
    data["last_updated"] = now.isoformat()
    data["reset_date"] = reset_date.isoformat()

    # Add to history
    data["history"].append({
        "timestamp": now.isoformat(),
        "requests": total_requests - old_total,
        "model": "sync",
        "cost": total_requests - old_total,
        "total_after": total_requests
    })

    # Cleanup: keep only last N entries
    if len(data["history"]) > MAX_HISTORY_ENTRIES:
        data["history"] = data["history"][-MAX_HISTORY_ENTRIES:]

    save_usage_data(data)
    return total_requests


def display_status():
    """Display current usage status"""
    data = load_usage_data()
    reset_date = get_next_reset_date()
    used = data.get("total_used", 0)
    last_updated = data.get("last_updated")

    # Check if we need to reset
    if data.get("reset_date"):
        last_reset = datetime.fromisoformat(data["reset_date"])
        if datetime.now() >= last_reset:
            used = 0
            data["total_used"] = 0
            data["reset_date"] = reset_date.isoformat()
            save_usage_data(data)

    stats = calculate_stats(used, reset_date)
    emoji = get_status_emoji(stats["percentage_used"])

    print("\n" + "="*60)
    print(f"  {emoji} CURSOR AI USAGE TRACKER {emoji}")
    print("="*60)

    # Last update info (shown first)
    print(f"\n🕐 LAST UPDATE")
    if last_updated:
        updated_dt = datetime.fromisoformat(last_updated)
        days_ago = (datetime.now() - updated_dt).days
        if days_ago == 0:
            age_str = "today"
        elif days_ago == 1:
            age_str = "yesterday"
        else:
            age_str = f"{days_ago} days ago"
        print(f"   {updated_dt.strftime('%B %d, %Y at %H:%M')} ({age_str})")
    else:
        print(f"   Never - no usage recorded yet")

    # Usage overview (shown second)
    print(f"\n📊 USAGE OVERVIEW")
    print(f"   Used:       {used:4d} / {MONTHLY_LIMIT} requests ({stats['percentage_used']:.1f}%)")
    print(f"   Remaining:  {stats['remaining']:4d} requests")

    # Progress bar
    bar_length = 40
    filled = int(bar_length * used / MONTHLY_LIMIT)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"   [{bar}]")

    print(f"\n📅 TIME")
    print(f"   Days elapsed:   {stats['days_elapsed']}")
    print(f"   Days remaining: {stats['days_remaining']}")
    print(f"   Resets on:      {reset_date.strftime('%B %d, %Y')}")

    print(f"\n🎯 BUDGET")
    print(f"   Original daily budget: {stats['daily_budget']:.1f} requests/day")
    print(f"   Adjusted daily budget: {stats['recommended_daily']:.1f} requests/day")

    status = "ON TRACK ✅" if stats["on_track"] else "OVER BUDGET ⚠️"
    print(f"   Status: {status}")

    print(f"\n💡 RECOMMENDATION")
    print(f"   {get_model_recommendation(stats['remaining'], stats['days_remaining'])}")

    # Hint to sync with real usage (shown last)
    print("\n" + "-"*60)
    print("📝 SYNC WITH REAL USAGE")
    print("   Check actual usage: https://cursor.com/dashboard?tab=usage")
    print("   Then run: python3 cursor_tracker.py set <total>")
    print("="*60 + "\n")


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add":
            if len(sys.argv) < 3:
                print("Usage: python cursor_tracker.py add <number> [model_name]")
                return

            requests = int(sys.argv[2])
            model = sys.argv[3] if len(sys.argv) > 3 else "standard"
            new_total = update_usage(requests, model)
            print(f"✅ Added {requests} requests using {model}")
            print(f"   New total: {new_total}")
            display_status()

        elif command == "set":
            if len(sys.argv) < 3:
                print("Usage: python cursor_tracker.py set <total>")
                print("  Set total usage to exact value from Cursor dashboard")
                return

            total = int(sys.argv[2])
            set_usage(total)
            print(f"✅ Set total usage to {total} (synced with dashboard)")
            display_status()

        elif command == "reset":
            data = {
                "total_used": 0,
                "last_updated": datetime.now().isoformat(),
                "reset_date": get_next_reset_date().isoformat(),
                "history": []
            }
            save_usage_data(data)
            print("✅ Usage reset to 0")
            display_status()

        elif command == "history":
            data = load_usage_data()
            history = data.get("history", [])
            if not history:
                print("\n📜 No history recorded yet.\n")
            else:
                print("\n" + "="*60)
                print("  📜 USAGE HISTORY")
                print("="*60)
                for entry in history[-10:]:  # Show last 10 entries
                    ts = datetime.fromisoformat(entry["timestamp"])
                    print(f"   {ts.strftime('%b %d %H:%M')} | +{entry['cost']:3d} req | {entry['model']:20s} | Total: {entry['total_after']}")
                if len(history) > 10:
                    print(f"   ... and {len(history) - 10} more entries")
                print("="*60 + "\n")

        elif command == "help":
            print("\nCursor Usage Tracker Commands:")
            print("  python cursor_tracker.py              - Show current status")
            print("  python cursor_tracker.py set N        - Set total to N (sync with dashboard)")
            print("  python cursor_tracker.py add N        - Add N requests to counter")
            print("  python cursor_tracker.py add N model  - Add N requests with specific model")
            print("  python cursor_tracker.py history      - Show usage history")
            print("  python cursor_tracker.py reset        - Reset counter to 0")
            print("  python cursor_tracker.py help         - Show this help\n")
        
        else:
            display_status()
    else:
        display_status()


if __name__ == "__main__":
    main()
