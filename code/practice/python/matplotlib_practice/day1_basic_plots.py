#!/usr/bin/env python3
"""
Day 1: Matplotlib Basics - Line, Scatter, and Bar Plots

Learn the fundamentals of matplotlib plotting including:
- Creating figures and axes
- Line plots with customization
- Scatter plots
- Bar charts (vertical and horizontal)
- Labels, titles, and legends

INSTRUCTIONS:
1. Complete each exercise by filling in the TODO sections
2. Run the script to see your plots
3. Check day1_basic_plots_answers.py if you get stuck
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory
os.makedirs('output', exist_ok=True)


def exercise_1_simple_line_plot():
    """
    Exercise 1: Create a simple line plot of a sine wave.
    
    TODO:
    1. Create x values from 0 to 10 with 100 points using np.linspace()
    2. Calculate y = sin(x)
    3. Create a figure with figsize=(10, 6)
    4. Plot the line
    5. Add a title: 'Simple Sine Wave'
    6. Add x and y axis labels
    7. Save the plot to 'output/day1_ex1_simple_line.png'
    """
    print("\n" + "="*60)
    print("Exercise 1: Simple Line Plot")
    print("="*60)
    
    # TODO: Create x values (0 to 10, 100 points)
    x = None  # Use np.linspace()
    
    # TODO: Calculate y = sin(x)
    y = None  # Use np.sin()
    
    # TODO: Create figure
    # plt.figure(...)
    
    # TODO: Plot the line
    # plt.plot(...)
    
    # TODO: Add title and labels
    # plt.title(...)
    # plt.xlabel(...)
    # plt.ylabel(...)
    
    # TODO: Save and show
    # plt.savefig('output/day1_ex1_simple_line.png', dpi=150)
    # plt.show()
    
    print("Exercise 1: Not implemented yet - fill in the TODOs!")


def exercise_2_multiple_lines():
    """
    Exercise 2: Plot multiple lines with different styles.
    
    TODO:
    1. Create x from 0 to 10 (100 points)
    2. Create three y arrays: sin(x), cos(x), sin(x)*exp(-x/10)
    3. Plot all three lines with:
       - Different colors (blue, red, green)
       - Different linestyles (solid, dashed, dotted)
       - Labels for legend
    4. Add a legend in the upper right corner
    5. Save to 'output/day1_ex2_multiple_lines.png'
    
    HINTS:
    - Use linewidth=2 for thicker lines
    - linestyle options: '-', '--', ':', '-.'
    - np.exp() for exponential
    """
    print("\n" + "="*60)
    print("Exercise 2: Multiple Lines with Styles")
    print("="*60)
    
    # TODO: Create x values
    x = None
    
    # TODO: Create y values for three functions
    y1 = None  # sin(x)
    y2 = None  # cos(x)
    y3 = None  # sin(x) * exp(-x/10) - damped sine wave
    
    # TODO: Create figure
    
    # TODO: Plot three lines with different styles
    # plt.plot(x, y1, label='sin(x)', ...)
    # plt.plot(x, y2, label='cos(x)', ...)
    # plt.plot(x, y3, label='damped sin(x)', ...)
    
    # TODO: Add title, labels, legend, grid
    
    # TODO: Save and show
    
    print("Exercise 2: Not implemented yet - fill in the TODOs!")


def exercise_3_scatter_plot():
    """
    Exercise 3: Create scatter plots with customization.
    
    TODO:
    1. Generate random data:
       - n = 100 points
       - x = random normal distribution
       - y = 2*x + noise (random normal * 0.5)
    2. Create a scatter plot with:
       - Variable colors based on random values
       - Variable sizes based on random values (multiply by 1000)
       - Alpha transparency = 0.6
       - Use 'viridis' colormap
    3. Add a colorbar
    4. Save to 'output/day1_ex3_scatter.png'
    
    HINTS:
    - np.random.seed(42) for reproducibility
    - np.random.randn(n) for normal distribution
    - plt.scatter(x, y, c=colors, s=sizes, cmap='viridis')
    - plt.colorbar() to add colorbar
    """
    print("\n" + "="*60)
    print("Exercise 3: Scatter Plots")
    print("="*60)
    
    np.random.seed(42)  # For reproducibility
    n = 100
    
    # TODO: Generate x (random normal)
    x = None
    
    # TODO: Generate y = 2*x + noise
    y = None
    
    # TODO: Generate colors and sizes (random values)
    colors = None
    sizes = None
    
    # TODO: Create figure and scatter plot
    
    # TODO: Add colorbar, title, labels
    
    # TODO: Save and show
    
    print("Exercise 3: Not implemented yet - fill in the TODOs!")


def exercise_4_bar_charts():
    """
    Exercise 4: Create vertical and horizontal bar charts.
    
    TODO:
    1. Use this data:
       categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
       values = [85, 72, 68, 55, 48]
    2. Create a figure with 2 subplots side by side (1 row, 2 columns)
    3. Left subplot: Vertical bar chart
    4. Right subplot: Horizontal bar chart (use plt.barh())
    5. Add value labels on top of each bar
    6. Save to 'output/day1_ex4_bar_charts.png'
    
    HINTS:
    - fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    - ax1.bar(categories, values) for vertical
    - ax2.barh(categories, values) for horizontal
    - ax.text(x, y, str(value)) for labels
    """
    print("\n" + "="*60)
    print("Exercise 4: Bar Charts")
    print("="*60)
    
    categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
    values = [85, 72, 68, 55, 48]
    
    # TODO: Create subplots (1 row, 2 columns)
    # fig, (ax1, ax2) = plt.subplots(...)
    
    # TODO: Vertical bar chart on ax1
    
    # TODO: Horizontal bar chart on ax2
    
    # TODO: Add titles, labels, value annotations
    
    # TODO: Save and show
    
    print("Exercise 4: Not implemented yet - fill in the TODOs!")


def exercise_5_grouped_bar_chart():
    """
    Exercise 5: Create a grouped bar chart for comparison.
    
    TODO:
    1. Use this data:
       quarters = ['Q1', 'Q2', 'Q3', 'Q4']
       product_a = [23, 28, 31, 35]
       product_b = [18, 22, 25, 29]
       product_c = [15, 19, 23, 27]
    2. Create grouped bars where each quarter shows 3 products
    3. Use different colors for each product
    4. Add a legend
    5. Save to 'output/day1_ex5_grouped_bar.png'
    
    HINTS:
    - x = np.arange(len(quarters))  # Label locations
    - width = 0.25  # Width of bars
    - ax.bar(x - width, product_a, width, label='Product A')
    - ax.bar(x, product_b, width, label='Product B')
    - ax.bar(x + width, product_c, width, label='Product C')
    """
    print("\n" + "="*60)
    print("Exercise 5: Grouped Bar Chart")
    print("="*60)
    
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    product_a = [23, 28, 31, 35]
    product_b = [18, 22, 25, 29]
    product_c = [15, 19, 23, 27]
    
    # TODO: Create x positions and set bar width
    x = None
    width = 0.25
    
    # TODO: Create figure and axes
    
    # TODO: Create three bar groups (offset by width)
    
    # TODO: Set x-tick labels to quarters
    # ax.set_xticks(x)
    # ax.set_xticklabels(quarters)
    
    # TODO: Add title, labels, legend
    
    # TODO: Save and show
    
    print("Exercise 5: Not implemented yet - fill in the TODOs!")


def exercise_6_combined_plot():
    """
    Exercise 6: Combine line and scatter plots.
    
    TODO:
    1. Create "actual data" with noise:
       - x from 0 to 10 (50 points)
       - y_trend = 2*x + 5 (the trend line)
       - y_actual = y_trend + random noise (normal * 3)
    2. Plot scatter points for actual data
    3. Plot dashed red line for trend
    4. Add legend showing both
    5. Save to 'output/day1_ex6_combined.png'
    
    HINTS:
    - plt.scatter() for points
    - plt.plot(x, y, 'r--') for red dashed line
    - Use alpha for transparency on scatter
    """
    print("\n" + "="*60)
    print("Exercise 6: Combined Line and Scatter Plot")
    print("="*60)
    
    np.random.seed(42)
    
    # TODO: Create x values (0 to 10, 50 points)
    x = None
    
    # TODO: Create trend line y = 2x + 5
    y_trend = None
    
    # TODO: Create actual data with noise
    y_actual = None
    
    # TODO: Create figure
    
    # TODO: Scatter plot for actual data
    
    # TODO: Line plot for trend
    
    # TODO: Add title, labels, legend
    
    # TODO: Save and show
    
    print("Exercise 6: Not implemented yet - fill in the TODOs!")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 1: MATPLOTLIB BASICS")
    print("="*60)
    print("\nComplete each exercise by filling in the TODO sections.")
    print("Check day1_basic_plots_answers.py for solutions.")
    
    exercise_1_simple_line_plot()
    exercise_2_multiple_lines()
    exercise_3_scatter_plot()
    exercise_4_bar_charts()
    exercise_5_grouped_bar_chart()
    exercise_6_combined_plot()
    
    print("\n" + "="*60)
    print("Complete the TODOs and run again to see your plots!")
    print("="*60)


if __name__ == "__main__":
    main()
