# Data Visualization & Scientific Computing Practice

A comprehensive 5-day learning path covering matplotlib and its scientific Python ecosystem.

## Quick Start

```bash
cd matplotlib_practice

# Activate virtual environment
source venv/bin/activate

# Run any practice file
python day1_basic_plots.py

# Check answers when needed
python day1_basic_plots_answers.py

# Deactivate when done
deactivate
```

## Learning Path

### Day 1: Matplotlib Basics
Core plotting fundamentals.

| Topic | What You'll Learn |
|-------|-------------------|
| Line plots | `plt.plot()`, styles, colors |
| Scatter plots | `plt.scatter()`, sizes, colormaps |
| Bar charts | `plt.bar()`, `plt.barh()`, grouped |
| Labels & legends | `plt.title()`, `plt.xlabel()`, `plt.legend()` |

**Files**: `day1_basic_plots.py` → `day1_basic_plots_answers.py`

---

### Day 2: NumPy Fundamentals
The foundation of numerical computing.

| Topic | What You'll Learn |
|-------|-------------------|
| Array creation | `np.array()`, `np.zeros()`, `np.linspace()` |
| Indexing/slicing | `arr[0]`, `arr[1:3]`, `arr[:, 0]` |
| Vectorized ops | Element-wise operations, broadcasting |
| Aggregation | `sum()`, `mean()`, `std()`, axis operations |

**Files**: `day2_numpy_fundamentals.py` → `day2_numpy_fundamentals_answers.py`

---

### Day 3: Pandas Essentials
Data manipulation and analysis.

| Topic | What You'll Learn |
|-------|-------------------|
| DataFrames | Creation, selection, filtering |
| Data manipulation | Adding columns, sorting, transforming |
| GroupBy | Aggregation, split-apply-combine |
| Missing data | `isnull()`, `fillna()`, `dropna()` |
| Merging | `merge()`, `concat()`, joins |

**Files**: `day3_pandas_essentials.py` → `day3_pandas_essentials_answers.py`

---

### Day 4: Seaborn Visualization
Statistical visualization made beautiful.

| Topic | What You'll Learn |
|-------|-------------------|
| Distributions | `histplot()`, `kdeplot()`, `boxplot()`, `violinplot()` |
| Relationships | `regplot()`, `scatterplot()`, `pairplot()` |
| Categorical | `countplot()`, `barplot()`, `swarmplot()` |
| Heatmaps | `heatmap()`, `clustermap()` |
| Faceting | `FacetGrid`, `catplot()`, `relplot()` |

**Files**: `day4_seaborn_visualization.py` → `day4_seaborn_visualization_answers.py`

---

### Day 5: SciPy Scientific Computing
Advanced scientific capabilities.

| Topic | What You'll Learn |
|-------|-------------------|
| Statistics | Distributions, t-tests, correlations, ANOVA |
| Optimization | Minimization, root finding, curve fitting |
| Interpolation | Linear, cubic, splines |
| Signal processing | Filters, FFT, peak detection |
| Integration | Definite integrals, ODE solving |

**Files**: `day5_scipy_scientific.py` → `day5_scipy_scientific_answers.py`

---

## Library Explanations

### NumPy (Numerical Python)
**Purpose**: Fast array operations and numerical computing.

```python
import numpy as np

# 100x faster than Python lists for numerical operations
arr = np.array([1, 2, 3, 4, 5])
arr * 2  # Element-wise: [2, 4, 6, 8, 10]
```

**Key features**: N-dimensional arrays, broadcasting, vectorized operations, linear algebra.

---

### Pandas (Panel Data)
**Purpose**: Data manipulation and analysis with labeled data.

```python
import pandas as pd

# SQL-like operations on tabular data
df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
df[df['age'] > 25]  # Filter: just Bob
df.groupby('name').mean()  # Aggregation
```

**Key features**: DataFrames, missing data handling, groupby, merge/join, time series.

---

### Seaborn
**Purpose**: Statistical visualization with beautiful defaults.

```python
import seaborn as sns

# One line for publication-ready plots
sns.boxplot(x='category', y='value', data=df)
sns.regplot(x='x', y='y', data=df)  # Automatic regression line
```

**Key features**: Built-in statistics, automatic estimation, faceting, themes.

---

### SciPy (Scientific Python)
**Purpose**: Advanced scientific algorithms.

```python
from scipy import stats, optimize

# Statistical tests
stats.ttest_ind(group_a, group_b)

# Curve fitting
optimize.curve_fit(func, x, y)
```

**Key features**: Statistics, optimization, interpolation, signal processing, integration.

---

## How to Practice

1. **Open the practice file** (e.g., `day1_basic_plots.py`)
2. **Read the docstrings** - they explain the concept and give hints
3. **Fill in the TODOs** - replace `None` with your code
4. **Run the script** to test your solutions
5. **Compare with answers** if stuck

### Example TODO Structure

```python
def exercise_1_simple_line_plot():
    """
    Exercise 1: Create a simple line plot.
    
    TODO:
    1. Create x values from 0 to 10 with 100 points
    2. Calculate y = sin(x)
    ...
    
    HINTS:
    - np.linspace(start, stop, num_points)
    - np.sin(x)
    """
    # TODO: Create x values
    x = None  # ← Replace with np.linspace(0, 10, 100)
    
    # TODO: Calculate y
    y = None  # ← Replace with np.sin(x)
```

---

## Progress Tracker

- [ ] Day 1: Matplotlib Basics (6 exercises)
- [ ] Day 2: NumPy Fundamentals (6 exercises)
- [ ] Day 3: Pandas Essentials (6 exercises)
- [ ] Day 4: Seaborn Visualization (6 exercises)
- [ ] Day 5: SciPy Scientific (6 exercises)

**Total: 30 exercises**

---

## Output

All plots are saved to the `output/` folder when you run the answer scripts.

---

## Resources

- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [NumPy User Guide](https://numpy.org/doc/stable/user/index.html)
- [Pandas Getting Started](https://pandas.pydata.org/docs/getting_started/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [SciPy Lectures](https://scipy-lectures.org/)
