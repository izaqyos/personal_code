# File: pomodoro_timer.py

import time
from threading import Thread

class PomodoroTimer:
    def __init__(self, work_time=25*60, short_break_time=5*60, long_break_time=15*60):
        self.work_time = work_time
        self.short_break_time = short_break_time
        self.long_break_time = long_break_time
        self.reps = 0
        self.running = False
        self.on_complete = None  # Callback to notify on cycle completion

    def start_cycle(self):
        """Starts a new Pomodoro cycle."""
        self.running = True
        self.reps += 1
        if self.reps % 8 == 0:
            self.count_down(self.long_break_time)
        elif self.reps % 2 == 0:
            self.count_down(self.short_break_time)
        else:
            self.count_down(self.work_time)

    def reset_cycle(self):
        """Resets the Pomodoro cycle."""
        self.running = False
        self.reps = 0

    def count_down(self, count):
        """Simulate countdown without blocking, for UI testing."""
        while count > 0 and self.running:
            time.sleep(1)
            count -= 1
        if self.running:
            self.running = False
            if self.on_complete:
                self.on_complete()  # Notify cycle completion

# Below is the UI class that interacts with Tkinter

import tkinter as tk
from tkinter import messagebox

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")

        # Initialize the timer with callback to update UI
        self.timer = PomodoroTimer()
        self.timer.on_complete = self.complete_cycle

        # UI Elements
        self.timer_label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        self.time_display = tk.Label(root, text="25:00", font=("Helvetica", 48))
        self.time_display.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.session_label = tk.Label(root, text="Sessions: 0", font=("Helvetica", 12))
        self.session_label.pack(pady=10)

    def start_timer(self):
        """Starts the Pomodoro timer and updates the display."""
        if not self.timer.running:
            self.timer.start_cycle()
            self.update_display(self.timer.work_time)
        else:
            messagebox.showinfo("Pomodoro Timer", "Timer is already running!")

    def reset_timer(self):
        """Resets the timer and updates the display."""
        self.timer.reset_cycle()
        self.time_display.config(text="25:00")
        self.session_label.config(text="Sessions: 0")

    def update_display(self, time_left):
        """Updates the display with the remaining time."""
        minutes, seconds = divmod(time_left, 60)
        self.time_display.config(text=f"{minutes:02}:{seconds:02}")

    def complete_cycle(self):
        """Updates the session count and notifies the user on completion."""
        completed_sessions = self.timer.reps // 2
        self.session_label.config(text=f"Sessions: {completed_sessions}")
        messagebox.showinfo("Pomodoro Timer", "Time's up! Take a break or start the next session.")

# To run the UI, you can initialize the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
