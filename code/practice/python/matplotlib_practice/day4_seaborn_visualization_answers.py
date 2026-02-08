#!/usr/bin/env python3
"""
Day 4: Seaborn Statistical Visualization - ANSWERS

Complete solutions for all Day 4 exercises.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

os.makedirs('output', exist_ok=True)


def exercise_1_distribution_plots():
    """Exercise 1: Visualize distributions."""
    print("\n" + "="*60)
    print("Exercise 1: Distribution Plots - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    data = np.random.normal(loc=50, scale=15, size=200)
    df = pd.DataFrame({
        'value': np.concatenate([
            np.random.normal(40, 10, 100),
            np.random.normal(60, 15, 100),
            np.random.normal(50, 8, 100)
        ]),
        'group': ['A']*100 + ['B']*100 + ['C']*100
    })
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    sns.histplot(data, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title('Histogram with KDE')
    
    sns.kdeplot(data, ax=axes[0, 1])
    axes[0, 1].set_title('KDE Plot')
    
    sns.histplot(data, ax=axes[0, 2])
    sns.rugplot(data, ax=axes[0, 2])
    axes[0, 2].set_title('Histogram with Rug')
    
    sns.boxplot(x='group', y='value', data=df, ax=axes[1, 0])
    axes[1, 0].set_title('Box Plot')
    
    sns.violinplot(x='group', y='value', data=df, ax=axes[1, 1])
    axes[1, 1].set_title('Violin Plot')
    
    for group in ['A', 'B', 'C']:
        sns.kdeplot(df[df['group']==group]['value'], label=group, ax=axes[1, 2])
    axes[1, 2].set_title('Overlaid KDEs')
    axes[1, 2].legend()
    
    plt.tight_layout()
    plt.savefig('output/day4_ex1_distributions.png', dpi=150)
    print("✓ Saved: output/day4_ex1_distributions.png")
    plt.show()


def exercise_2_relationship_plots():
    """Exercise 2: Visualize relationships."""
    print("\n" + "="*60)
    print("Exercise 2: Relationship Plots - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    n = 100
    x = np.random.randn(n) * 10 + 50
    df = pd.DataFrame({
        'x': x,
        'y': x * 1.5 + np.random.randn(n) * 5,
        'category': np.random.choice(['A', 'B', 'C'], n),
        'size': np.random.randint(10, 100, n)
    })
    
    # Regression plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='x', y='y', data=df, ax=ax)
    plt.title('Regression Plot')
    plt.savefig('output/day4_ex2_regplot.png', dpi=150)
    print("✓ Saved: output/day4_ex2_regplot.png")
    plt.show()
    
    # Scatter with hue
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='x', y='y', hue='category', size='size', data=df, ax=ax)
    plt.title('Scatter with Hue')
    plt.savefig('output/day4_ex2_scatter.png', dpi=150)
    print("✓ Saved: output/day4_ex2_scatter.png")
    plt.show()
    
    # Pair plot
    pair_data = df[['x', 'y', 'size', 'category']]
    g = sns.pairplot(pair_data, hue='category')
    g.figure.suptitle('Pair Plot', y=1.02)
    plt.savefig('output/day4_ex2_pairplot.png', dpi=150)
    print("✓ Saved: output/day4_ex2_pairplot.png")
    plt.show()
    
    # Joint plot
    g = sns.jointplot(x='x', y='y', data=df, kind='scatter')
    plt.savefig('output/day4_ex2_jointplot.png', dpi=150)
    print("✓ Saved: output/day4_ex2_jointplot.png")
    plt.show()


def exercise_3_categorical_plots():
    """Exercise 3: Visualize categorical data."""
    print("\n" + "="*60)
    print("Exercise 3: Categorical Plots - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame({
        'day': np.repeat(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 20),
        'sales': np.random.randint(50, 150, 100) + np.tile([0, 10, 20, 30, 40], 20),
        'region': np.tile(['North', 'South'], 50)
    })
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    sns.countplot(x='day', data=df, ax=axes[0, 0])
    axes[0, 0].set_title('Count Plot')
    
    sns.barplot(x='day', y='sales', data=df, ax=axes[0, 1])
    axes[0, 1].set_title('Bar Plot (Mean + CI)')
    
    sns.pointplot(x='day', y='sales', hue='region', data=df, ax=axes[0, 2])
    axes[0, 2].set_title('Point Plot')
    
    sns.swarmplot(x='day', y='sales', data=df, ax=axes[1, 0], size=3)
    axes[1, 0].set_title('Swarm Plot')
    
    sns.stripplot(x='day', y='sales', data=df, ax=axes[1, 1], jitter=True, alpha=0.5)
    axes[1, 1].set_title('Strip Plot')
    
    sns.boxplot(x='day', y='sales', data=df, ax=axes[1, 2])
    sns.swarmplot(x='day', y='sales', data=df, ax=axes[1, 2], color='black', size=3)
    axes[1, 2].set_title('Box + Swarm')
    
    plt.tight_layout()
    plt.savefig('output/day4_ex3_categorical.png', dpi=150)
    print("✓ Saved: output/day4_ex3_categorical.png")
    plt.show()


def exercise_4_heatmaps_clustering():
    """Exercise 4: Heatmaps and clustered heatmaps."""
    print("\n" + "="*60)
    print("Exercise 4: Heatmaps - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame(np.random.randn(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
    df['B'] = df['A'] * 0.8 + np.random.randn(10) * 0.2
    df['C'] = -df['A'] * 0.6 + np.random.randn(10) * 0.3
    
    # Correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax, fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.savefig('output/day4_ex4_heatmap.png', dpi=150)
    print("✓ Saved: output/day4_ex4_heatmap.png")
    plt.show()
    
    # Clustered heatmap
    data = pd.DataFrame(np.random.randn(20, 8), columns=[f'Var_{i}' for i in range(8)])
    g = sns.clustermap(data, cmap='viridis', standard_scale=1)
    g.figure.suptitle('Clustered Heatmap', y=1.02)
    plt.savefig('output/day4_ex4_clustermap.png', dpi=150)
    print("✓ Saved: output/day4_ex4_clustermap.png")
    plt.show()


def exercise_5_faceting():
    """Exercise 5: Create multi-plot grids."""
    print("\n" + "="*60)
    print("Exercise 5: Faceting - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame({
        'value': np.concatenate([
            np.random.normal(50, 10, 50),
            np.random.normal(60, 15, 50),
            np.random.normal(55, 12, 50),
            np.random.normal(65, 8, 50)
        ]),
        'category': ['A']*50 + ['B']*50 + ['A']*50 + ['B']*50,
        'type': ['X']*100 + ['Y']*100,
        'x': np.random.randn(200) * 10 + 50
    })
    df['y'] = df['x'] * 0.8 + np.random.randn(200) * 5
    
    # FacetGrid with one column
    g = sns.FacetGrid(df, col='category', height=4)
    g.map(sns.histplot, 'value')
    g.figure.suptitle('Faceted by Category', y=1.02)
    plt.savefig('output/day4_ex5_facet_col.png', dpi=150)
    print("✓ Saved: output/day4_ex5_facet_col.png")
    plt.show()
    
    # FacetGrid with row and col
    g = sns.FacetGrid(df, row='type', col='category', height=4)
    g.map(sns.scatterplot, 'x', 'y')
    plt.savefig('output/day4_ex5_facet_grid.png', dpi=150)
    print("✓ Saved: output/day4_ex5_facet_grid.png")
    plt.show()
    
    # catplot
    g = sns.catplot(x='category', y='value', col='type', data=df, kind='box')
    plt.savefig('output/day4_ex5_catplot.png', dpi=150)
    print("✓ Saved: output/day4_ex5_catplot.png")
    plt.show()
    
    # relplot
    g = sns.relplot(x='x', y='y', col='category', hue='type', data=df)
    plt.savefig('output/day4_ex5_relplot.png', dpi=150)
    print("✓ Saved: output/day4_ex5_relplot.png")
    plt.show()


def exercise_6_styling():
    """Exercise 6: Apply themes and customize."""
    print("\n" + "="*60)
    print("Exercise 6: Styling - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 100)
    })
    
    themes = ['whitegrid', 'darkgrid', 'white', 'dark']
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, theme in zip(axes.flat, themes):
        sns.set_theme(style=theme)
        sns.scatterplot(x='x', y='y', hue='category', data=df, ax=ax)
        ax.set_title(f'Theme: {theme}')
    plt.tight_layout()
    plt.savefig('output/day4_ex6_themes.png', dpi=150)
    print("✓ Saved: output/day4_ex6_themes.png")
    plt.show()
    
    palettes = ['deep', 'muted', 'pastel', 'colorblind']
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, palette in zip(axes.flat, palettes):
        sns.set_palette(palette)
        sns.barplot(x='category', y='x', data=df, ax=ax)
        ax.set_title(f'Palette: {palette}')
    plt.tight_layout()
    plt.savefig('output/day4_ex6_palettes.png', dpi=150)
    print("✓ Saved: output/day4_ex6_palettes.png")
    plt.show()
    
    sns.set_theme()  # Reset


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 4: SEABORN VISUALIZATION - ANSWERS")
    print("="*60)
    
    exercise_1_distribution_plots()
    exercise_2_relationship_plots()
    exercise_3_categorical_plots()
    exercise_4_heatmaps_clustering()
    exercise_5_faceting()
    exercise_6_styling()
    
    print("\n✓ All exercises completed!")


if __name__ == "__main__":
    main()
