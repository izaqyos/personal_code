#!/usr/bin/env python3
"""
Exercise 4: Histograms and Distribution Plots
==============================================
Time: 15-20 minutes

Visualize data distributions:
- Histograms with customization
- Density plots (KDE)
- Box plots and violin plots
- Comparing distributions

Run: python run_exercises.py 4
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

np.random.seed(42)

# Normal distributions
normal_data = np.random.randn(1000)
normal_shifted = np.random.randn(1000) + 2
bimodal_data = np.concatenate([np.random.randn(500) - 2, np.random.randn(500) + 2])

# Different distributions
uniform_data = np.random.uniform(-3, 3, 1000)
exponential_data = np.random.exponential(1, 1000)
poisson_data = np.random.poisson(5, 1000)

# Comparison groups
group_a = np.random.randn(200) * 1.5 + 5
group_b = np.random.randn(200) * 1.0 + 6
group_c = np.random.randn(200) * 2.0 + 4

# Response times (ms) - right-skewed
response_times = np.random.exponential(100, 500) + 50


# ============================================================
# EXERCISE 4.1: Basic Histogram
# ============================================================

def exercise_1_basic_histogram():
    """
    Create a histogram of the normal distribution.
    
    TODO:
    1. Create a figure with figsize=(10, 6)
    2. Plot a histogram of normal_data with:
       - 30 bins
       - Blue color with some transparency (alpha=0.7)
       - Black edge color for bars
    3. Add a vertical line at the mean
    4. Add vertical lines at mean ± std
    5. Add text annotation showing mean and std values
    6. Add title: "Normal Distribution (n=1000)"
    7. Add labels
    
    Expected: Histogram with statistical markers
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 4.2: Comparing Distributions
# ============================================================

def exercise_2_overlapping_histograms():
    """
    Compare two distributions on the same plot.
    
    TODO:
    1. Plot histograms of normal_data and normal_shifted
    2. Use transparency (alpha=0.5) so both are visible
    3. Use different colors (blue and orange)
    4. Add legend with labels: "Group 1" and "Group 2"
    5. Add title: "Comparison of Two Distributions"
    
    Bonus: Also plot using density=True to normalize
    
    Expected: Two overlapping semi-transparent histograms
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 4.3: Histogram with KDE
# ============================================================

def exercise_3_histogram_kde():
    """
    Create a histogram with a kernel density estimate overlay.
    
    TODO:
    1. Plot histogram of bimodal_data with density=True
       (density=True normalizes so area = 1)
    2. Calculate and plot a KDE (kernel density estimate)
       Simple approach: Use scipy.stats.gaussian_kde
       Or approximate with a smoothed line
    3. Show the bimodal nature clearly
    4. Add title: "Bimodal Distribution with KDE"
    
    Hints:
    - from scipy import stats
    - kde = stats.gaussian_kde(bimodal_data)
    - x_range = np.linspace(min, max, 200)
    - plt.plot(x_range, kde(x_range))
    
    Expected: Histogram with smooth curve overlay
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 4.4: Box Plots
# ============================================================

def exercise_4_boxplots():
    """
    Create box plots comparing multiple groups.
    
    TODO:
    1. Create a figure with two subplots (1 row, 2 columns)
    2. Left: Simple box plot of [group_a, group_b, group_c]
       - Use plt.boxplot() or ax.boxplot()
       - Label x-axis ticks as "A", "B", "C"
    3. Right: Horizontal box plot with additional styling
       - Show means (showmeans=True)
       - Show notches for confidence interval (notch=True)
       - Different box colors
    4. Add titles to each subplot
    
    Expected: Two styled box plot comparisons
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 4.5: Violin Plots
# ============================================================

def exercise_5_violin():
    """
    Create violin plots (box plots + KDE).
    
    TODO:
    1. Create violin plots of [group_a, group_b, group_c]
    2. Customize the violins:
       - Show quartile lines (showmedians=True)
       - Color each violin differently
    3. Overlay individual data points (optional but nice)
       Hint: Add scatter with jitter
    4. Add title: "Distribution Comparison: Violin Plots"
    5. Label x-axis ticks
    
    Hints:
    - ax.violinplot(data, showmedians=True)
    - For coloring: access parts = ax.violinplot(...), then parts['bodies']
    
    Expected: Three violin plots with customized styling
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 4.6: Challenge - Multi-Distribution Dashboard
# ============================================================

def exercise_6_distribution_dashboard():
    """
    Create a comprehensive distribution analysis dashboard.
    
    TODO:
    1. Create a 2x2 subplot figure
    2. Top-left: Histogram of response_times with log x-scale
       (response times are right-skewed)
    3. Top-right: Box plot of response_times showing outliers
    4. Bottom-left: Q-Q plot (quantile-quantile) vs normal
       Hint: from scipy import stats; stats.probplot(data, plot=ax)
    5. Bottom-right: ECDF (empirical cumulative distribution)
       Hint: sorted_data = np.sort(data)
             ecdf = np.arange(1, len(data)+1) / len(data)
             plt.step(sorted_data, ecdf)
    6. Add a main title: "Response Time Distribution Analysis"
    
    Expected: Four-panel analysis of a single variable
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("4.1 Basic Histogram", exercise_1_basic_histogram),
        ("4.2 Overlapping Histograms", exercise_2_overlapping_histograms),
        ("4.3 Histogram with KDE", exercise_3_histogram_kde),
        ("4.4 Box Plots", exercise_4_boxplots),
        ("4.5 Violin Plots", exercise_5_violin),
        ("4.6 Distribution Dashboard", exercise_6_distribution_dashboard),
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
- plt.hist(data, bins, density, alpha, color, edgecolor)
- plt.boxplot(data, labels, showmeans, notch)
- plt.violinplot(data, showmedians)

Important parameters:
- bins: number of bins or bin edges
- density=True: normalize to probability density
- alpha: transparency for overlapping

When to use each:
- Histogram: See full distribution shape
- Box plot: Compare medians and quartiles
- Violin: Compare distributions with shape info
- KDE: Smooth estimate of distribution

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
