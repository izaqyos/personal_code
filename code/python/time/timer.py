import sys
import time
import argparse

def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        time_left = f"{mins:02}:{secs:02}"
        print(f"\rTime left: {time_left}", end="")
        time.sleep(1)
        total_seconds -= 1
    print("\rTime left: 00:00 - Time's up!     ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Countdown Timer")
    parser.add_argument("minutes", type=int, help="Countdown duration in minutes")
    args = parser.parse_args()
    
    print(f"Starting countdown for {args.minutes} minute(s)...")
    countdown(args.minutes)

