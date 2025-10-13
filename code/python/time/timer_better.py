import sys
import time
import argparse

def countdown(minutes):
    end_time = time.time() + minutes * 60
    while True:
        total_seconds = int(end_time - time.time())
        if total_seconds <= 0:
            break
        mins, secs = divmod(total_seconds, 60)
        time_left = f"{mins:02}:{secs:02}"
        print(f"\rTime left: {time_left}", end="")
        time.sleep(0.1)  # Sleep for a shorter duration to improve accuracy

    print("\rTime left: 00:00 - Time's up!     ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Countdown Timer")
    parser.add_argument("minutes", type=int, help="Countdown duration in minutes")
    args = parser.parse_args()
    
    print(f"Starting countdown for {args.minutes} minute(s)...")
    countdown(args.minutes)

