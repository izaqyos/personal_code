#!/usr/bin/env python3
"""
Exercise 2: Subplots and Layouts
================================
Time: 20-25 minutes

Master figure layouts:
- Creating subplots with plt.subplots()
- The Figure and Axes objects
- GridSpec for complex layouts
- Sharing axes

Run: python run_exercises.py 2
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = x ** 2
y5 = np.exp(-x/5) * np.sin(x)
y6 = np.log(x + 1)

# Random data for different plot types
np.random.seed(42)
random_data = np.random.randn(1000)
scatter_x = np.random.randn(50)
scatter_y = scatter_x + np.random.randn(50) * 0.5


# ============================================================
# EXERCISE 2.1: Basic 2x2 Subplot Grid
# ============================================================

def exercise_1_basic_subplots():
    """
    Create a 2x2 grid of plots.
    
    TODO:
    1. Create a figure with 2x2 subplots using plt.subplots(2, 2)
    2. Top-left: Plot sin(x)
    3. Top-right: Plot cos(x)
    4. Bottom-left: Plot x^2
    5. Bottom-right: Plot exp(-x/5) * sin(x)
    6. Add a title to each subplot using ax.set_title()
    7. Use fig.tight_layout() to prevent overlap
    8. Show the plot
    
    Hints:
    - plt.subplots() returns (fig, axes) where axes is 2D array
    - Access subplots: axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]
    - Use ax.plot() instead of plt.plot()
    
    Expected: A 2x2 grid with four different function plots
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 2.2: Subplots with Shared Axes
# ============================================================

def exercise_2_shared_axes():
    """
    Create subplots that share the x-axis.
    
    TODO:
    1. Create 3 vertically stacked subplots (3 rows, 1 column)
    2. Share the x-axis between all subplots (sharex=True)
    3. Top: Plot sin(x) in blue
    4. Middle: Plot cos(x) in red
    5. Bottom: Plot sin(x) + cos(x) in green
    6. Only show x-label on the bottom subplot
    7. Add y-labels to each subplot
    8. Add a main title using fig.suptitle()
    
    Expected: Three stacked plots with aligned x-axes
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 2.3: Different Subplot Sizes with GridSpec
# ============================================================

def exercise_3_gridspec():
    """
    Create a complex layout with different sized subplots.
    
    Layout:
    +------------------+--------+
    |                  |        |
    |   Main Plot      |  Side  |
    |   (2x2 area)     |  Plot  |
    |                  |        |
    +--------+---------+--------+
    | Bottom | Bottom  | Bottom |
    |  Left  | Middle  | Right  |
    +--------+---------+--------+
    
    TODO:
    1. Create a figure with figsize=(12, 8)
    2. Use GridSpec to create a 3x3 grid
    3. Main plot spans rows 0-1, columns 0-1: Plot y5 (damped oscillation)
    4. Side plot spans rows 0-1, column 2: Plot histogram of random_data
    5. Bottom plots: three separate plots in row 2, columns 0, 1, 2
       - Bottom left: scatter plot
       - Bottom middle: y6 (log function)
       - Bottom right: bar chart with 5 random values
    6. Add titles to each subplot
    
    Hints:
    - from matplotlib.gridspec import GridSpec
    - fig.add_subplot(gs[0:2, 0:2]) spans 2 rows and 2 columns
    
    Expected: A dashboard-like layout with different sized plots
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 2.4: Inset Axes (Plot within a Plot)
# ============================================================

def exercise_4_inset():
    """
    Create a main plot with a zoomed inset.
    
    TODO:
    1. Create a figure and main axes
    2. Plot sin(x) * exp(-x/10) on the main axes (x from 0 to 10)
    3. Create an inset axes in the top-right corner
       Hint: Use ax.inset_axes([left, bottom, width, height]) 
       where values are fractions of the parent axes (e.g., [0.6, 0.6, 0.35, 0.35])
    4. In the inset, plot the same data but zoomed to x=[1, 3]
    5. Add a box around the zoomed region using ax.indicate_inset_zoom()
       Or manually draw a rectangle
    
    Expected: A full plot with a zoomed-in portion shown in corner
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 2.5: Challenge - Dashboard Layout
# ============================================================

def exercise_5_dashboard():
    """
    Create a multi-panel data dashboard.
    
    Scenario: You're creating a dashboard showing various metrics.
    
    TODO:
    1. Create a figure with figsize=(14, 10)
    2. Layout (use GridSpec):
       - Header row: One wide plot spanning full width (time series)
       - Middle row: Two equal plots (histogram left, scatter right)
       - Bottom row: Three equal plots (any three different visualizations)
    3. Add a main title with fig.suptitle("Data Dashboard", fontsize=16)
    4. Use consistent styling:
       - All axes should have titles
       - Use plt.style.context('seaborn-v0_8-whitegrid') or similar
       - Add grid to appropriate plots
    5. Save as 'dashboard.png'
    
    Expected: A professional-looking dashboard with 6 panels
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("2.1 Basic 2x2 Subplots", exercise_1_basic_subplots),
        ("2.2 Shared Axes", exercise_2_shared_axes),
        ("2.3 GridSpec Layout", exercise_3_gridspec),
        ("2.4 Inset Axes", exercise_4_inset),
        ("2.5 Dashboard", exercise_5_dashboard),
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

Key concepts:
- Figure vs Axes: Figure is the window, Axes is the actual plot
- plt.subplots(nrows, ncols) returns (fig, axes)
- ax.method() vs plt.method(): ax is explicit, plt uses "current" axes
- GridSpec allows non-uniform subplot sizes

Useful patterns:
- fig, axes = plt.subplots(2, 2, figsize=(10, 8))
- fig.tight_layout()  # Prevent overlapping
- fig.suptitle()  # Main title above all subplots

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
