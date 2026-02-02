#!/usr/bin/env python3
"""
Exercise 6: Annotations and Text
=================================
Time: 15-20 minutes

Add informative text to plots:
- Text placement
- Arrows and annotations
- Mathematical expressions (LaTeX)
- Text boxes

Run: python run_exercises.py 6
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10)

# Find key points
max_idx = np.argmax(y)
min_idx = np.argmin(y)
zero_crossings = np.where(np.diff(np.signbit(y)))[0]

# Financial data
days = np.arange(1, 101)
np.random.seed(42)
stock = 100 + np.cumsum(np.random.randn(100) * 2)
crash_idx = 45  # Simulated crash
stock[crash_idx:crash_idx+10] -= 15


# ============================================================
# EXERCISE 6.1: Basic Text Annotation
# ============================================================

def exercise_1_basic_text():
    """
    Add text labels to key points on a plot.
    
    TODO:
    1. Plot y = sin(x) * exp(-x/10)
    2. Add text label at the maximum point
       - Use plt.text(x, y, 'text') or ax.text()
       - Include the max value in the label
    3. Add text label at the minimum point
    4. Mark zero crossings with vertical dashed lines
    5. Add a title and axis labels
    
    Hints:
    - x_max, y_max = x[max_idx], y[max_idx]
    - plt.text(x_max, y_max, f'Max: {y_max:.2f}')
    - Adjust position with offsets to avoid overlapping the point
    
    Expected: Plot with labeled maximum and minimum points
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 6.2: Annotate with Arrows
# ============================================================

def exercise_2_arrows():
    """
    Use annotations with arrows pointing to features.
    
    TODO:
    1. Plot the stock price data
    2. Annotate the crash point with an arrow:
       - Text: "Market Crash"
       - Arrow pointing from text to the data point
       - Use plt.annotate() with arrowprops
    3. Annotate the all-time high
    4. Annotate the recovery point (after crash)
    5. Customize arrow styles:
       - Use different arrow styles for each annotation
       - arrowprops={'arrowstyle': '->', 'color': 'red'}
       - arrowprops={'arrowstyle': 'fancy', 'fc': 'blue'}
    
    Hints:
    - plt.annotate('text', xy=(x, y), xytext=(x_text, y_text),
                   arrowprops=dict(arrowstyle='->', color='red'))
    
    Expected: Stock chart with arrow annotations at key events
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 6.3: Text Box Annotations
# ============================================================

def exercise_3_textbox():
    """
    Add styled text boxes to plots.
    
    TODO:
    1. Plot y = sin(x) * exp(-x/10)
    2. Add a text box with statistics:
       - "Statistics"
       - "Max: X.XX"
       - "Min: X.XX"
       - "Mean: X.XX"
    3. Style the text box:
       - Background color (facecolor)
       - Border (edgecolor)
       - Rounded corners (boxstyle='round')
       - Alpha/transparency
    4. Position the box in the upper right corner
       Hint: Use transform=ax.transAxes for relative positioning
    
    Hints:
    - props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    - ax.text(0.95, 0.95, text, transform=ax.transAxes, 
              verticalalignment='top', bbox=props)
    
    Expected: Plot with a styled statistics box
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 6.4: LaTeX Mathematical Expressions
# ============================================================

def exercise_4_latex():
    """
    Add mathematical expressions using LaTeX.
    
    TODO:
    1. Plot y = sin(x) * e^(-x/10)
    2. Add the equation as a title using LaTeX:
       r'$y = \sin(x) \cdot e^{-x/10}$'
    3. Add annotations with LaTeX:
       - At max: r'$\frac{dy}{dx} = 0$'
       - Add integral annotation: r'$\int_0^{10} f(x)dx = ...$'
         Calculate the actual integral value
    4. Add axis labels with units using LaTeX:
       - x-axis: r'$x$ (radians)'
       - y-axis: r'$y = f(x)$'
    
    Hints:
    - Raw strings r'...' are needed for LaTeX
    - np.trapz(y, x) gives approximate integral
    - Use math mode $ ... $ for inline math
    
    Expected: Plot with beautiful mathematical annotations
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 6.5: Multi-Line Annotations
# ============================================================

def exercise_5_multiline():
    """
    Create complex multi-line annotations.
    
    TODO:
    1. Create a figure with the stock data
    2. Add a detailed annotation box explaining the crash:
       - Title: "Market Crash Analysis"
       - Bullet points:
         * Date: Day 45
         * Drop: X%
         * Recovery: X days
       - Use proper formatting (newlines, alignment)
    3. Add a separate "Key" or legend-like text box
       explaining any markers/colors used
    4. Add a footer note with data source
       Position at bottom of figure
    
    Expected: Annotated chart suitable for a report
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 6.6: Challenge - Infographic Style
# ============================================================

def exercise_6_infographic():
    """
    Create an infographic-style annotated figure.
    
    TODO:
    1. Create a large figure (12, 8)
    2. Plot the damped oscillation
    3. Add multiple callout boxes:
       - "Initial Amplitude" pointing to first peak
       - "Decay Rate" with arrow showing envelope
       - "Zero Crossing" at first crossing
       - "Damping Time" showing where amplitude halves
    4. Style like an infographic:
       - Use colors from a consistent palette
       - Add icons or shapes (circles, rectangles)
       - Use different font sizes for hierarchy
    5. Add a title banner at top
    6. Add a footer with additional info
    
    This is open-ended - be creative!
    
    Expected: An attractive, self-explanatory visualization
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("6.1 Basic Text", exercise_1_basic_text),
        ("6.2 Arrows", exercise_2_arrows),
        ("6.3 Text Boxes", exercise_3_textbox),
        ("6.4 LaTeX", exercise_4_latex),
        ("6.5 Multi-Line", exercise_5_multiline),
        ("6.6 Infographic", exercise_6_infographic),
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
- ax.text(x, y, s, **kwargs)
- ax.annotate(s, xy, xytext, arrowprops)
- ax.set_title(r'$LaTeX$')

Positioning:
- Data coordinates: default
- Axes coordinates: transform=ax.transAxes (0-1 range)
- Figure coordinates: transform=fig.transFigure

Arrow styles:
- '->', '<-', '<->', 'fancy', 'simple', 'wedge'

Useful bbox styles:
- 'round', 'square', 'circle', 'rarrow', 'larrow'

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
