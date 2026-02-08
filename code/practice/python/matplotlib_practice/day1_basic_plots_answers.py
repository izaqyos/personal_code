#!/usr/bin/env python3
"""
Day 1: Matplotlib Basics - ANSWERS

Complete solutions for all Day 1 exercises.
Compare with your implementations in day1_basic_plots.py
"""

import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')
os.makedirs('output', exist_ok=True)


def exercise_1_simple_line_plot():
    """Exercise 1: Create a simple line plot."""
    print("\n" + "="*60)
    print("Exercise 1: Simple Line Plot - ANSWER")
    print("="*60)
    
    # Create x values from 0 to 10 with 100 points
    x = np.linspace(0, 10, 100)
    
    # Calculate y = sin(x)
    y = np.sin(x)
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot the line
    plt.plot(x, y)
    
    # Add title and labels
    plt.title('Simple Sine Wave', fontsize=16, fontweight='bold')
    plt.xlabel('X axis', fontsize=12)
    plt.ylabel('Y axis', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Save and show
    plt.tight_layout()
    plt.savefig('output/day1_ex1_simple_line.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex1_simple_line.png")
    plt.show()


def exercise_2_multiple_lines():
    """Exercise 2: Plot multiple lines with different styles."""
    print("\n" + "="*60)
    print("Exercise 2: Multiple Lines - ANSWER")
    print("="*60)
    
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.exp(-x/10)
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(x, y1, label='sin(x)', linewidth=2, color='blue')
    plt.plot(x, y2, label='cos(x)', linewidth=2, color='red', linestyle='--')
    plt.plot(x, y3, label='damped sin(x)', linewidth=2, color='green', linestyle=':')
    
    plt.title('Multiple Trigonometric Functions', fontsize=16, fontweight='bold')
    plt.xlabel('X axis', fontsize=12)
    plt.ylabel('Y axis', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/day1_ex2_multiple_lines.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex2_multiple_lines.png")
    plt.show()


def exercise_3_scatter_plot():
    """Exercise 3: Create scatter plots with customization."""
    print("\n" + "="*60)
    print("Exercise 3: Scatter Plot - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    n = 100
    
    x = np.random.randn(n)
    y = 2 * x + np.random.randn(n) * 0.5
    colors = np.random.rand(n)
    sizes = 1000 * np.random.rand(n)
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, 
                         cmap='viridis', edgecolors='black', linewidth=0.5)
    
    plt.title('Scatter Plot with Variable Size and Color', fontsize=16, fontweight='bold')
    plt.xlabel('X values', fontsize=12)
    plt.ylabel('Y values', fontsize=12)
    plt.colorbar(scatter, label='Color scale')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/day1_ex3_scatter.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex3_scatter.png")
    plt.show()


def exercise_4_bar_charts():
    """Exercise 4: Vertical and horizontal bar charts."""
    print("\n" + "="*60)
    print("Exercise 4: Bar Charts - ANSWER")
    print("="*60)
    
    categories = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
    values = [85, 72, 68, 55, 48]
    colors_list = ['#3776ab', '#f7df1e', '#007396', '#00599c', '#00add8']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Vertical bar chart
    ax1.bar(categories, values, color=colors_list, edgecolor='black', linewidth=1.5)
    ax1.set_title('Programming Language Popularity (Vertical)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Language', fontsize=12)
    ax1.set_ylabel('Popularity Score', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(values):
        ax1.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
    
    # Horizontal bar chart
    ax2.barh(categories, values, color=colors_list, edgecolor='black', linewidth=1.5)
    ax2.set_title('Programming Language Popularity (Horizontal)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Popularity Score', fontsize=12)
    ax2.set_ylabel('Language', fontsize=12)
    ax2.grid(axis='x', alpha=0.3)
    
    for i, v in enumerate(values):
        ax2.text(v + 1, i, str(v), ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/day1_ex4_bar_charts.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex4_bar_charts.png")
    plt.show()


def exercise_5_grouped_bar_chart():
    """Exercise 5: Grouped bar chart for comparison."""
    print("\n" + "="*60)
    print("Exercise 5: Grouped Bar Chart - ANSWER")
    print("="*60)
    
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    product_a = [23, 28, 31, 35]
    product_b = [18, 22, 25, 29]
    product_c = [15, 19, 23, 27]
    
    x = np.arange(len(quarters))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars1 = ax.bar(x - width, product_a, width, label='Product A', color='#ff6b6b')
    bars2 = ax.bar(x, product_b, width, label='Product B', color='#4ecdc4')
    bars3 = ax.bar(x + width, product_c, width, label='Product C', color='#45b7d1')
    
    ax.set_title('Quarterly Sales Comparison', fontsize=16, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Sales (in thousands)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height}', ha='center', va='bottom', fontsize=9)
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    plt.tight_layout()
    plt.savefig('output/day1_ex5_grouped_bar.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex5_grouped_bar.png")
    plt.show()


def exercise_6_combined_plot():
    """Exercise 6: Combine line and scatter plots."""
    print("\n" + "="*60)
    print("Exercise 6: Combined Plot - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    
    x = np.linspace(0, 10, 50)
    y_trend = 2 * x + 5
    y_actual = y_trend + np.random.randn(50) * 3
    
    plt.figure(figsize=(12, 6))
    
    plt.scatter(x, y_actual, alpha=0.6, s=50, color='blue', 
               label='Actual Data', edgecolors='black', linewidth=0.5)
    plt.plot(x, y_trend, 'r--', linewidth=2, label='Trend Line')
    
    plt.title('Sales Data with Trend Line', fontsize=16, fontweight='bold')
    plt.xlabel('Time (months)', fontsize=12)
    plt.ylabel('Sales ($1000s)', fontsize=12)
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/day1_ex6_combined.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved: output/day1_ex6_combined.png")
    plt.show()


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 1: MATPLOTLIB BASICS - ANSWERS")
    print("="*60)
    
    exercise_1_simple_line_plot()
    exercise_2_multiple_lines()
    exercise_3_scatter_plot()
    exercise_4_bar_charts()
    exercise_5_grouped_bar_chart()
    exercise_6_combined_plot()
    
    print("\n" + "="*60)
    print("✓ All Day 1 exercises completed!")
    print("="*60)


if __name__ == "__main__":
    main()
