#!/usr/bin/env python3
"""
Exercise 3: Bar Charts and Scatter Plots
=========================================
Time: 20-25 minutes

Create effective categorical and relationship plots:
- Vertical and horizontal bar charts
- Grouped and stacked bars
- Scatter plots with size and color encoding
- Adding error bars

Run: python run_exercises.py 3
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

# Sales data by quarter
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
sales_2023 = [150, 180, 220, 280]
sales_2024 = [170, 210, 250, 310]
sales_errors = [15, 20, 18, 25]  # Standard deviation

# Product categories
categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
revenue = [45000, 32000, 28000, 15000, 22000]
growth = [12, -3, 8, 2, 15]  # Percentage growth

# Scatter data: Hours studied vs Exam score
np.random.seed(42)
hours_studied = np.random.uniform(1, 10, 50)
exam_scores = 40 + 5 * hours_studied + np.random.randn(50) * 8
study_groups = np.random.choice(['A', 'B', 'C'], 50)

# City data for bubble chart
cities = ['NYC', 'LA', 'Chicago', 'Houston', 'Phoenix']
population = [8.3, 4.0, 2.7, 2.3, 1.6]  # millions
area = [302, 469, 227, 670, 517]  # sq miles
median_income = [63, 62, 58, 53, 55]  # thousands


# ============================================================
# EXERCISE 3.1: Basic Bar Chart
# ============================================================

def exercise_1_basic_bar():
    """
    Create a simple vertical bar chart of revenue by category.
    
    TODO:
    1. Create a figure with figsize=(10, 6)
    2. Create a bar chart using plt.bar(categories, revenue)
    3. Add a title: "Revenue by Product Category"
    4. Add y-label: "Revenue ($)"
    5. Color bars based on whether growth is positive (green) or negative (red)
       Hint: colors = ['green' if g > 0 else 'red' for g in growth]
    6. Add value labels on top of each bar
       Hint: Use plt.text() or ax.bar_label()
    
    Expected: A bar chart with colored bars and value labels
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 3.2: Grouped Bar Chart
# ============================================================

def exercise_2_grouped_bars():
    """
    Compare 2023 vs 2024 sales with grouped bars.
    
    TODO:
    1. Create a figure
    2. Create grouped bars:
       - Set bar width (e.g., 0.35)
       - Calculate x positions for each group
       - Plot 2023 bars at x positions
       - Plot 2024 bars at x + bar_width positions
    3. Set x-tick labels to quarters
    4. Add legend to distinguish years
    5. Add title and labels
    
    Hints:
    - x = np.arange(len(quarters))
    - First bar: plt.bar(x - width/2, sales_2023, width, label='2023')
    - Second bar: plt.bar(x + width/2, sales_2024, width, label='2024')
    - plt.xticks(x, quarters)
    
    Expected: Side-by-side bars comparing two years
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 3.3: Horizontal Bar with Error Bars
# ============================================================

def exercise_3_horizontal_bars():
    """
    Create a horizontal bar chart with error bars.
    
    TODO:
    1. Create a horizontal bar chart of sales_2024 by quarter
       Hint: Use plt.barh() instead of plt.bar()
    2. Add error bars showing sales_errors
       Hint: Use xerr parameter in barh()
    3. Sort bars by value (largest at top)
    4. Add a vertical line at the mean value
       Hint: plt.axvline(mean_value, color='red', linestyle='--')
    5. Add title and appropriate labels
    
    Expected: Horizontal bars with error bars and a reference line
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 3.4: Basic Scatter Plot
# ============================================================

def exercise_4_scatter():
    """
    Create a scatter plot showing study hours vs exam scores.
    
    TODO:
    1. Create a scatter plot of hours_studied vs exam_scores
    2. Color points by study_groups (A, B, C)
       Hint: Create a color map dict or use numeric encoding
    3. Add a trend line:
       - Use np.polyfit(hours_studied, exam_scores, 1) for linear fit
       - Plot the line with np.polyval()
    4. Add legend showing group colors
    5. Add title: "Study Hours vs Exam Performance"
    6. Add axis labels
    
    Expected: Colored scatter plot with trend line
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 3.5: Bubble Chart
# ============================================================

def exercise_5_bubble():
    """
    Create a bubble chart for city data.
    
    TODO:
    1. Create a scatter plot where:
       - x = area (sq miles)
       - y = median_income (thousands)
       - size = population * 100 (for visibility)
       - color = population (use a colormap)
    2. Add a colorbar showing population scale
    3. Annotate each bubble with the city name
       Hint: Use plt.annotate() for each city
    4. Add title: "City Comparison: Area, Income, and Population"
    5. Add axis labels
    
    Hints:
    - plt.scatter(..., s=sizes, c=colors, cmap='viridis', alpha=0.6)
    - plt.colorbar(label='Population (millions)')
    
    Expected: Bubble chart with labeled cities and colorbar
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 3.6: Challenge - Stacked Bar with Annotations
# ============================================================

def exercise_6_stacked():
    """
    Create a stacked bar chart showing composition.
    
    Scenario: Sales breakdown by channel (Online, Store, Wholesale)
    
    Data:
    channels = ['Online', 'Store', 'Wholesale']
    Q1 = [60, 70, 20]
    Q2 = [80, 75, 25]
    Q3 = [100, 80, 40]
    Q4 = [130, 100, 50]
    
    TODO:
    1. Create a stacked bar chart (one bar per quarter, stacked by channel)
       Hint: Use bottom parameter to stack
       - First: plt.bar(quarters, online_data)
       - Second: plt.bar(quarters, store_data, bottom=online_data)
       - Third: plt.bar(quarters, wholesale_data, bottom=online+store)
    2. Add percentage labels inside each segment
    3. Add total value on top of each bar
    4. Add legend
    5. Add title: "Quarterly Sales by Channel"
    
    Expected: Stacked bars showing composition with annotations
    """
    # Data for this exercise
    channels = ['Online', 'Store', 'Wholesale']
    q_data = {
        'Q1': [60, 70, 20],
        'Q2': [80, 75, 25],
        'Q3': [100, 80, 40],
        'Q4': [130, 100, 50]
    }
    
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("3.1 Basic Bar Chart", exercise_1_basic_bar),
        ("3.2 Grouped Bars", exercise_2_grouped_bars),
        ("3.3 Horizontal Bars", exercise_3_horizontal_bars),
        ("3.4 Scatter Plot", exercise_4_scatter),
        ("3.5 Bubble Chart", exercise_5_bubble),
        ("3.6 Stacked Bars", exercise_6_stacked),
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
- plt.bar(x, height, width, bottom, color, label)
- plt.barh(y, width, height, left, ...)  # horizontal
- plt.scatter(x, y, s=sizes, c=colors, cmap, alpha)
- ax.bar_label(container)  # auto-label bars

Tips:
- Grouped bars: offset x positions by bar width
- Stacked bars: use bottom parameter
- Bubble chart: scatter with size encoding

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
