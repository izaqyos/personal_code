# File: pomodoro_timer.py

import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")

        # Set default times in seconds
        self.work_time = 25 * 60  # 25 minutes
        self.short_break_time = 5 * 60  # 5 minutes
        self.long_break_time = 15 * 60  # 15 minutes
        self.reps = 0
        self.running = False

        # Create UI elements
        self.timer_label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        self.time_display = tk.Label(root, text=self._format_time(self.work_time), font=("Helvetica", 48))
        self.time_display.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.session_label = tk.Label(root, text="Sessions: 0", font=("Helvetica", 12))
        self.session_label.pack(pady=10)

    def _format_time(self, seconds):
        """Format seconds into MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def start_timer(self):
        """Starts the Pomodoro timer."""
        if not self.running:
            self.running = True
            self.reps += 1
            if self.reps % 8 == 0:
                self.count_down(self.long_break_time)
            elif self.reps % 2 == 0:
                self.count_down(self.short_break_time)
            else:
                self.count_down(self.work_time)
        else:
            messagebox.showinfo("Pomodoro Timer", "Timer is already running!")

    def reset_timer(self):
        """Resets the timer."""
        self.running = False
        self.reps = 0
        self.time_display.config(text=self._format_time(self.work_time))
        self.session_label.config(text="Sessions: 0")

    def count_down(self, count):
        """Countdown function for the timer."""
        def timer_thread():
            while count > 0 and self.running:
                mins, secs = divmod(count, 60)
                time_str = f"{mins:02}:{secs:02}"
                self.time_display.config(text=time_str)
                self.root.update()
                time.sleep(1)
                count -= 1

            if self.running:
                self.complete_cycle()

        Thread(target=timer_thread).start()

    def complete_cycle(self):
        """Completes a Pomodoro cycle."""
        self.running = False
        completed_sessions = self.reps // 2
        self.session_label.config(text=f"Sessions: {completed_sessions}")
        messagebox.showinfo("Pomodoro Timer", "Time's up! Take a break or start the next session.")

# Set up the Tkinter root
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

