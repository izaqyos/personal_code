#!/usr/bin/env python3
"""
Exercise 5: Customization and Styling
======================================
Time: 20-25 minutes

Master visual aesthetics:
- Colors and colormaps
- Markers and line styles
- Legends and labels
- Themes and style sheets
- Custom tick formatting

Run: python run_exercises.py 5
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-x/10)

# Multi-series data
np.random.seed(42)
years = np.arange(2015, 2025)
products = ['Product A', 'Product B', 'Product C', 'Product D']
sales = np.random.randint(50, 150, (4, 10))


# ============================================================
# EXERCISE 5.1: Color Exploration
# ============================================================

def exercise_1_colors():
    """
    Explore different ways to specify colors in matplotlib.
    
    TODO:
    1. Create a figure with 6 subplots (2 rows, 3 columns)
    2. Each subplot should show the same sin wave but with different color specs:
       - Named color: 'royalblue'
       - Hex color: '#FF6B6B'
       - RGB tuple: (0.2, 0.8, 0.2)
       - RGBA with alpha: (1.0, 0.5, 0.0, 0.5)
       - Colormap color: plt.cm.viridis(0.6)
       - CSS4 color: pick from mcolors.CSS4_COLORS
    3. Title each subplot with the color specification used
    
    Expected: Same plot in 6 different colors
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 5.2: Line Styles and Markers
# ============================================================

def exercise_2_line_markers():
    """
    Create a reference chart of line styles and markers.
    
    TODO:
    1. Create a figure with 2 subplots (side by side)
    2. Left subplot - Line styles:
       - Plot 4 horizontal lines at y=1, 2, 3, 4
       - Use styles: solid '-', dashed '--', dotted ':', dashdot '-.'
       - Label each with the style code
    3. Right subplot - Markers:
       - Plot 8 points showing different markers
       - Use: 'o', 's', '^', 'D', 'v', '<', '>', 'p'
       - Label each marker
    4. Make this a useful reference you can consult later
    
    Expected: A reference chart for styles and markers
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 5.3: Custom Legend
# ============================================================

def exercise_3_legend():
    """
    Create plots with customized legends.
    
    TODO:
    1. Plot all 4 products' sales data over years
    2. Customize the legend:
       - Position: outside the plot (bbox_to_anchor)
       - Multiple columns (ncol=2)
       - Custom title: "Products"
       - Frame with rounded corners (fancybox=True)
       - Semi-transparent background (framealpha=0.8)
    3. Add a second "artist" to legend (custom entry)
       - e.g., a dashed line indicating "Target" 
       - Hint: create a Line2D object for custom legend entry
    
    Hints:
    - from matplotlib.lines import Line2D
    - legend_elements = [Line2D([0], [0], color='red', linestyle='--', label='Target')]
    - ax.legend(handles=handles + legend_elements, ...)
    
    Expected: Multi-line plot with fancy legend outside plot area
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 5.4: Styles and Themes
# ============================================================

def exercise_4_styles():
    """
    Compare different matplotlib styles.
    
    TODO:
    1. Create a 2x3 subplot figure
    2. Each subplot uses a different style:
       - 'default'
       - 'seaborn-v0_8'
       - 'ggplot'
       - 'dark_background'
       - 'bmh'
       - 'fivethirtyeight'
    3. Plot the same data (y1 and y2) in each
    4. Title each with the style name
    
    Hints:
    - Use plt.style.context(style_name) as a context manager
    - with plt.style.context('ggplot'):
          ax.plot(...)
    
    Expected: Same plots rendered in 6 different visual styles
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 5.5: Custom Tick Formatting
# ============================================================

def exercise_5_ticks():
    """
    Customize axis ticks and formatting.
    
    TODO:
    1. Create a plot of y3 (damped oscillation)
    2. Customize x-axis:
       - Set major ticks at every π (0, π, 2π, 3π)
       - Set minor ticks at every π/2
       - Format labels as multiples of π (e.g., "2π" not "6.28")
       Hint: Use ax.xaxis.set_major_locator() and set_major_formatter()
    3. Customize y-axis:
       - Set major ticks at every 0.5
       - Format as percentages (multiply by 100, add %)
    4. Add grid on major ticks only
    
    Hints:
    - from matplotlib.ticker import MultipleLocator, FuncFormatter
    - ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    
    Expected: Plot with custom π-based x-axis and percentage y-axis
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 5.6: Challenge - Publication-Ready Figure
# ============================================================

def exercise_6_publication():
    """
    Create a publication-quality figure with all best practices.
    
    TODO:
    1. Create a figure with these specifications:
       - Size: (8, 6) inches - good for journals
       - DPI: 300 (publication quality)
    2. Plot the 4 products' sales over years with:
       - Distinct colors from a colorblind-friendly palette
       - Different line styles for b&w printing
       - Markers at data points
    3. Add professional touches:
       - Title with proper capitalization
       - Axis labels with units
       - Legend with proper placement
       - Grid (subtle, gray)
       - Tight layout
    4. Customize fonts:
       - Use plt.rcParams to set font family and sizes
       - Title: 14pt, bold
       - Axis labels: 12pt
       - Tick labels: 10pt
       - Legend: 10pt
    5. Add figure annotation (e.g., "Figure 1" or source note)
    6. Save as PNG (300 DPI) and PDF (vector)
    
    Expected: A figure ready for publication/presentation
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("5.1 Color Exploration", exercise_1_colors),
        ("5.2 Lines and Markers", exercise_2_line_markers),
        ("5.3 Custom Legend", exercise_3_legend),
        ("5.4 Styles and Themes", exercise_4_styles),
        ("5.5 Custom Ticks", exercise_5_ticks),
        ("5.6 Publication Figure", exercise_6_publication),
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

Color specifications:
- Named: 'red', 'royalblue', 'salmon'
- Hex: '#FF6B6B'
- RGB tuple: (0.2, 0.8, 0.2)
- RGBA: (1.0, 0.5, 0.0, 0.5)
- Colormap: plt.cm.viridis(0.6)

Useful colormaps:
- Sequential: viridis, plasma, magma
- Diverging: coolwarm, RdBu
- Qualitative: Set1, Set2, tab10

Style sheets:
- plt.style.use('ggplot')  # permanent
- with plt.style.context('...'):  # temporary

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
