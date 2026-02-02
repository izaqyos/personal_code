#!/usr/bin/env python3
"""
Exercise 1: Basic Line Plots
============================
Time: 15-20 minutes

Learn the fundamentals of matplotlib:
- Creating simple line plots
- Adding labels and titles
- Multiple lines on one plot
- Basic formatting

Run: python run_exercises.py 1
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA (use these in your exercises)
# ============================================================

# Time series data
days = np.arange(1, 31)  # 1 to 30
temperature = 20 + 10 * np.sin(days / 5) + np.random.randn(30) * 2
humidity = 60 + 20 * np.cos(days / 7) + np.random.randn(30) * 5

# Math functions
x = np.linspace(0, 2 * np.pi, 100)
sin_y = np.sin(x)
cos_y = np.cos(x)

# Stock-like data
stock_days = np.arange(1, 101)
stock_price = 100 + np.cumsum(np.random.randn(100) * 2)


# ============================================================
# EXERCISE 1.1: Your First Plot
# ============================================================

def exercise_1_simple_line():
    """
    Create a simple line plot of temperature over days.
    
    TODO:
    1. Create a figure with plt.figure()
    2. Plot temperature vs days using plt.plot()
    3. Add x-label: "Day"
    4. Add y-label: "Temperature (°C)"
    5. Add title: "Daily Temperature"
    6. Show the plot with plt.show()
    
    Expected: A simple line graph showing temperature fluctuation over 30 days
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 1.2: Multiple Lines
# ============================================================

def exercise_2_multiple_lines():
    """
    Plot sin(x) and cos(x) on the same figure.
    
    TODO:
    1. Plot sin(x) with a blue solid line, label it "sin(x)"
    2. Plot cos(x) with a red dashed line, label it "cos(x)"
    3. Add a legend using plt.legend()
    4. Add x-label: "x (radians)"
    5. Add y-label: "y"
    6. Add title: "Trigonometric Functions"
    7. Add a grid with plt.grid(True)
    
    Hints:
    - Use linestyle='--' for dashed
    - Use color='blue' or 'b' for blue
    - Use label='...' parameter in plot()
    
    Expected: Two overlapping wave patterns with a legend
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 1.3: Line Styles and Markers
# ============================================================

def exercise_3_styling():
    """
    Create a plot showcasing different line styles and markers.
    
    TODO: Plot the stock price data with:
    1. First 33 days: solid blue line with circle markers ('o')
    2. Days 34-66: dashed green line with square markers ('s')
    3. Days 67-100: dotted red line with triangle markers ('^')
    
    Hints:
    - Use slicing: stock_days[:33], stock_price[:33]
    - linewidth=2 makes lines thicker
    - markersize=4 controls marker size
    - markevery=5 shows marker every 5th point (less cluttered)
    
    Expected: A stock chart with three visually distinct segments
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 1.4: Figure Size and DPI
# ============================================================

def exercise_4_figure_customization():
    """
    Create a publication-quality figure with custom size.
    
    TODO:
    1. Create a figure with figsize=(10, 6) and dpi=100
    2. Plot temperature and humidity on the same axes
    3. Use different y-axis scales (temperature ~20-30, humidity ~40-80)
       Hint: You'll learn twin axes later, for now just plot both
    4. Add a title with fontsize=16
    5. Add labels with fontsize=12
    6. Save the figure as 'my_first_plot.png' using plt.savefig()
    7. Then show it
    
    Expected: A larger, cleaner looking plot saved to disk
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 1.5: Challenge - Line Plot Analysis
# ============================================================

def exercise_5_analysis_plot():
    """
    Create an analytical plot with mean line and standard deviation band.
    
    TODO:
    1. Plot the stock price as a blue line
    2. Calculate and plot the mean price as a horizontal red dashed line
    3. Calculate std and plot std band (mean ± std) as a shaded region
       Hint: Use plt.fill_between(x, lower, upper, alpha=0.3)
    4. Add annotations showing the max and min values
       Hint: Use plt.annotate() or just plt.text()
    5. Add appropriate labels, title, and legend
    
    Expected: A stock chart with statistical overlay showing mean and variance
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("1.1 Simple Line Plot", exercise_1_simple_line),
        ("1.2 Multiple Lines", exercise_2_multiple_lines),
        ("1.3 Line Styles", exercise_3_styling),
        ("1.4 Figure Customization", exercise_4_figure_customization),
        ("1.5 Analysis Plot", exercise_5_analysis_plot),
    ]
    
    for name, func in exercises:
        print(f"\n--- {name} ---")
        try:
            func()
            if interactive:
                input("Press Enter to continue...")
        except Exception as e:
            print(f"⚠️  Not implemented or error: {e}")


# ============================================================
# NOTES & INSIGHTS
# ============================================================

"""
What I learned:
- 

Key functions:
- plt.figure(figsize, dpi)
- plt.plot(x, y, color, linestyle, marker, label)
- plt.xlabel(), plt.ylabel(), plt.title()
- plt.legend(), plt.grid()
- plt.savefig(), plt.show()

Common gotchas:
- 

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
