# Matplotlib Chart Patterns

## Overview

Common patterns for creating publication-quality charts with matplotlib.

---

## 1. Basic Setup

```python
import matplotlib.pyplot as plt
import numpy as np

# Style options
plt.style.use('seaborn-v0_8-whitegrid')  # Clean grid background
# plt.style.use('ggplot')                 # R-style
# plt.style.use('dark_background')        # Dark theme
```

---

## 2. Bar Chart

```python
def plot_bar_chart(names: list, values: list, title: str):
    """Create a bar chart with value labels."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bars
    bars = ax.bar(names, values, color='steelblue', edgecolor='black', linewidth=0.5)
    
    # Add value labels on top of bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.annotate(
            f'{value}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points above bar
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=10, fontweight='bold'
        )
    
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
```

---

## 3. Sorted Bar Chart

```python
# Sort data by value (descending)
sorted_data = sorted(zip(names, values, colors), key=lambda x: x[1], reverse=True)
names, values, colors = zip(*sorted_data)

bars = ax.bar(names, values, color=colors)
```

---

## 4. Grouped Bar Chart (Multiple Series)

```python
def plot_grouped_bars(categories: list, series: dict):
    """
    Create grouped bar chart.
    
    Args:
        categories: ["Q1", "Q2", "Q3", "Q4"]
        series: {"Product A": [10, 20, 15, 25], "Product B": [8, 15, 12, 20]}
    """
    x = np.arange(len(categories))
    width = 0.8 / len(series)  # Divide available space
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for i, (label, values) in enumerate(series.items()):
        offset = (i - len(series)/2 + 0.5) * width
        bars = ax.bar(x + offset, values, width, label=label, alpha=0.8)
        
        # Add value labels
        for bar, value in zip(bars, values):
            if value > 0:
                ax.annotate(
                    f'{value}',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8
                )
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

---

## 5. Pie Chart

```python
def plot_pie_chart(labels: list, values: list, title: str):
    """Create a pie chart with percentages."""
    # Filter out zeros
    filtered = [(l, v) for l, v in zip(labels, values) if v > 0]
    if not filtered:
        print("No data to display")
        return
    
    labels, values = zip(*filtered)
    total = sum(values)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*total)})',
        startangle=90,
        explode=[0.02] * len(values),  # Slight separation
        shadow=True
    )
    
    # Style the percentage labels
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax.set_title(f'{title}\n(Total: {total})', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
```

---

## 6. Adding Text Annotations

```python
# Text box in corner
ax.text(
    0.98, 0.98,                    # x, y position (0-1 in axes coords)
    f'Total: {total}',
    transform=ax.transAxes,         # Use axes coordinates
    ha='right', va='top',
    fontsize=11,
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
)
```

---

## 7. Saving Figures

```python
# PNG (raster, good for web)
plt.savefig('chart.png', dpi=150, bbox_inches='tight')

# PDF (vector, good for print)
plt.savefig('chart.pdf', bbox_inches='tight')

# SVG (vector, good for editing)
plt.savefig('chart.svg', bbox_inches='tight')

# Always close after saving
plt.close()
```

---

## 8. Subplots

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

# First subplot
axes[0].bar(x, y1)
axes[0].set_title('Chart 1')

# Second subplot
axes[1].pie(values)
axes[1].set_title('Chart 2')

plt.tight_layout()
plt.show()
```

---

## 9. Custom Colors

```python
# Named colors
color = 'steelblue'

# Hex colors
color = '#1f77b4'

# RGB tuple (0-1 scale)
color = (0.12, 0.47, 0.71)

# Color palette (matplotlib default)
colors = plt.cm.tab10.colors[:5]  # First 5 colors

# Custom palette
COLORS = {
    "user1": "#17becf",  # Cyan
    "user2": "#1f77b4",  # Blue
    "user3": "#ff7f0e",  # Orange
}
```

---

## 10. Real Example: Code Review Visualization

```python
def plot_bar_chart(data: dict, period: str = "full_2025", save_path: str = None):
    """Create a bar chart for code reviews by team member."""
    if data is None or not data.get("reviews"):
        print("⚠️ No data to display")
        return
    
    reviews = data["reviews"]
    names = [r["display_name"] for r in reviews]
    counts = [r.get(period, 0) for r in reviews]
    colors = [COLORS.get(r["github_username"], "#333333") for r in reviews]
    
    # Sort by count descending
    sorted_data = sorted(zip(names, counts, colors), key=lambda x: x[1], reverse=True)
    names, counts, colors = zip(*sorted_data)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(names, counts, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar, count in zip(bars, counts):
        ax.annotate(f'{count}',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Team Member', fontsize=12)
    ax.set_ylabel('Number of Code Reviews', fontsize=12)
    ax.set_title(f'Code Reviews - {period}', fontsize=14, fontweight='bold')
    
    # Total annotation
    ax.text(0.98, 0.98, f'Total: {sum(counts)}', transform=ax.transAxes,
            ha='right', va='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Overlapping labels | Use `rotation=45, ha='right'` |
| Clipped labels | Use `bbox_inches='tight'` when saving |
| Too many categories | Use horizontal bars or truncate names |
| Memory leak | Always call `plt.close()` after saving |

---

## See Also

- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- `~/work/CheckPoint/Jira/statistics/visualize_reviews.py` - Real example

---

**Created:** 2026-01-27  
**Source:** Code Review Statistics project
