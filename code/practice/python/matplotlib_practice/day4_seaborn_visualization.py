#!/usr/bin/env python3
"""
Day 4: Seaborn Statistical Visualization

Seaborn is a statistical visualization library built on matplotlib.
It provides:
- Beautiful default styles
- Statistical plot types (distributions, relationships, categories)
- Integration with Pandas DataFrames
- Automatic estimation and uncertainty visualization
- Faceting for multi-plot grids

WHY SEABORN?
- High-level interface = less code for complex plots
- Automatic statistics (mean, CI, regression lines)
- Consistent, publication-ready aesthetics
- Great for exploratory data analysis
- Works seamlessly with pandas DataFrames

INSTRUCTIONS:
1. Complete each exercise by filling in the TODO sections
2. Run the script to see your plots
3. Check day4_seaborn_visualization_answers.py if stuck
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

os.makedirs('output', exist_ok=True)


def exercise_1_distribution_plots():
    """
    Exercise 1: Visualize distributions.
    
    TODO:
    1. Create a histogram with KDE (kernel density estimate) overlay
    2. Create a KDE plot only
    3. Create a rug plot showing individual observations
    4. Create a box plot
    5. Create a violin plot
    
    HINTS:
    - sns.histplot(data, kde=True)
    - sns.kdeplot(data)
    - sns.rugplot(data)
    - sns.boxplot(x=..., data=...)
    - sns.violinplot(x=..., y=..., data=...)
    """
    print("\n" + "="*60)
    print("Exercise 1: Distribution Plots")
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
    
    # TODO: Histogram with KDE on axes[0, 0]
    # sns.histplot(data, kde=True, ax=axes[0, 0])
    # axes[0, 0].set_title('Histogram with KDE')
    
    # TODO: KDE plot on axes[0, 1]
    # sns.kdeplot(data, ax=axes[0, 1])
    # axes[0, 1].set_title('KDE Plot')
    
    # TODO: Histogram with rug on axes[0, 2]
    # sns.histplot(data, ax=axes[0, 2])
    # sns.rugplot(data, ax=axes[0, 2])
    # axes[0, 2].set_title('Histogram with Rug')
    
    # TODO: Box plot by group on axes[1, 0]
    # sns.boxplot(x='group', y='value', data=df, ax=axes[1, 0])
    
    # TODO: Violin plot by group on axes[1, 1]
    # sns.violinplot(x='group', y='value', data=df, ax=axes[1, 1])
    
    # TODO: Overlaid KDEs by group on axes[1, 2]
    # for group in ['A', 'B', 'C']:
    #     sns.kdeplot(df[df['group']==group]['value'], label=group, ax=axes[1, 2])
    
    plt.tight_layout()
    # plt.savefig('output/day4_ex1_distributions.png', dpi=150)
    # plt.show()
    
    print("Exercise 1: Not implemented yet - fill in the TODOs!")


def exercise_2_relationship_plots():
    """
    Exercise 2: Visualize relationships between variables.
    
    TODO:
    1. Create a scatter plot with regression line (regplot)
    2. Create a scatter plot colored by category (scatterplot with hue)
    3. Create a pair plot showing all pairwise relationships
    4. Create a joint plot with marginal distributions
    
    HINTS:
    - sns.regplot(x=..., y=..., data=...)
    - sns.scatterplot(x=..., y=..., hue=..., data=...)
    - sns.pairplot(data, hue=...)
    - sns.jointplot(x=..., y=..., data=..., kind='scatter')
    """
    print("\n" + "="*60)
    print("Exercise 2: Relationship Plots")
    print("="*60)
    
    np.random.seed(42)
    n = 100
    df = pd.DataFrame({
        'x': np.random.randn(n) * 10 + 50,
        'y': lambda df: df['x'] * 1.5 + np.random.randn(n) * 5,
        'category': np.random.choice(['A', 'B', 'C'], n),
        'size': np.random.randint(10, 100, n)
    }.items())
    
    # Recreate df properly
    x = np.random.randn(n) * 10 + 50
    df = pd.DataFrame({
        'x': x,
        'y': x * 1.5 + np.random.randn(n) * 5,
        'category': np.random.choice(['A', 'B', 'C'], n),
        'size': np.random.randint(10, 100, n)
    })
    
    # TODO: Regression plot
    # fig, ax = plt.subplots(figsize=(10, 6))
    # sns.regplot(x='x', y='y', data=df, ax=ax)
    # plt.title('Regression Plot')
    # plt.savefig('output/day4_ex2_regplot.png', dpi=150)
    # plt.show()
    
    # TODO: Scatter plot with hue
    # fig, ax = plt.subplots(figsize=(10, 6))
    # sns.scatterplot(x='x', y='y', hue='category', size='size', data=df, ax=ax)
    # plt.title('Scatter with Hue')
    # plt.savefig('output/day4_ex2_scatter.png', dpi=150)
    # plt.show()
    
    # TODO: Pair plot (uses entire figure)
    # pair_data = df[['x', 'y', 'size', 'category']]
    # g = sns.pairplot(pair_data, hue='category')
    # g.fig.suptitle('Pair Plot', y=1.02)
    # plt.savefig('output/day4_ex2_pairplot.png', dpi=150)
    # plt.show()
    
    # TODO: Joint plot
    # g = sns.jointplot(x='x', y='y', data=df, kind='scatter')
    # plt.savefig('output/day4_ex2_jointplot.png', dpi=150)
    # plt.show()
    
    print("Exercise 2: Not implemented yet - fill in the TODOs!")


def exercise_3_categorical_plots():
    """
    Exercise 3: Visualize categorical data.
    
    TODO:
    1. Create a count plot (bar chart of counts)
    2. Create a bar plot with error bars (mean + CI)
    3. Create a point plot (line connecting means)
    4. Create a swarm plot (scatter with no overlap)
    5. Create a strip plot (jittered scatter)
    
    HINTS:
    - sns.countplot(x=..., data=...)
    - sns.barplot(x=..., y=..., data=..., ci=95)
    - sns.pointplot(x=..., y=..., hue=..., data=...)
    - sns.swarmplot(x=..., y=..., data=...)
    - sns.stripplot(x=..., y=..., data=..., jitter=True)
    """
    print("\n" + "="*60)
    print("Exercise 3: Categorical Plots")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame({
        'day': np.repeat(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], 20),
        'sales': np.random.randint(50, 150, 100) + np.tile([0, 10, 20, 30, 40], 20),
        'region': np.tile(['North', 'South'], 50)
    })
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # TODO: Count plot on axes[0, 0]
    # sns.countplot(x='day', data=df, ax=axes[0, 0])
    # axes[0, 0].set_title('Count Plot')
    
    # TODO: Bar plot with CI on axes[0, 1]
    # sns.barplot(x='day', y='sales', data=df, ax=axes[0, 1])
    # axes[0, 1].set_title('Bar Plot (Mean + CI)')
    
    # TODO: Point plot with hue on axes[0, 2]
    # sns.pointplot(x='day', y='sales', hue='region', data=df, ax=axes[0, 2])
    # axes[0, 2].set_title('Point Plot')
    
    # TODO: Swarm plot on axes[1, 0]
    # sns.swarmplot(x='day', y='sales', data=df, ax=axes[1, 0], size=3)
    # axes[1, 0].set_title('Swarm Plot')
    
    # TODO: Strip plot on axes[1, 1]
    # sns.stripplot(x='day', y='sales', data=df, ax=axes[1, 1], jitter=True, alpha=0.5)
    # axes[1, 1].set_title('Strip Plot')
    
    # TODO: Combined box + swarm on axes[1, 2]
    # sns.boxplot(x='day', y='sales', data=df, ax=axes[1, 2])
    # sns.swarmplot(x='day', y='sales', data=df, ax=axes[1, 2], color='black', size=3)
    # axes[1, 2].set_title('Box + Swarm')
    
    plt.tight_layout()
    # plt.savefig('output/day4_ex3_categorical.png', dpi=150)
    # plt.show()
    
    print("Exercise 3: Not implemented yet - fill in the TODOs!")


def exercise_4_heatmaps_clustering():
    """
    Exercise 4: Heatmaps and clustered heatmaps.
    
    TODO:
    1. Create a correlation heatmap with annotations
    2. Create a clustered heatmap (clustermap)
    3. Customize colormap and center point
    
    HINTS:
    - df.corr() for correlation matrix
    - sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    - sns.clustermap(data, cmap=..., standard_scale=1)
    """
    print("\n" + "="*60)
    print("Exercise 4: Heatmaps")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame(np.random.randn(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
    df['B'] = df['A'] * 0.8 + np.random.randn(10) * 0.2  # Correlated
    df['C'] = -df['A'] * 0.6 + np.random.randn(10) * 0.3  # Anti-correlated
    
    # TODO: Correlation heatmap
    # fig, ax = plt.subplots(figsize=(10, 8))
    # corr = df.corr()
    # sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
    # plt.title('Correlation Heatmap')
    # plt.savefig('output/day4_ex4_heatmap.png', dpi=150)
    # plt.show()
    
    # TODO: Clustered heatmap
    # Create larger dataset for clustering
    data = pd.DataFrame(np.random.randn(20, 8), columns=[f'Var_{i}' for i in range(8)])
    # g = sns.clustermap(data, cmap='viridis', standard_scale=1)
    # g.fig.suptitle('Clustered Heatmap', y=1.02)
    # plt.savefig('output/day4_ex4_clustermap.png', dpi=150)
    # plt.show()
    
    print("Exercise 4: Not implemented yet - fill in the TODOs!")


def exercise_5_faceting():
    """
    Exercise 5: Create multi-plot grids with FacetGrid.
    
    TODO:
    1. Use FacetGrid to create plots split by one variable (col)
    2. Use FacetGrid to create plots split by two variables (row and col)
    3. Use catplot for categorical faceting
    4. Use relplot for relational faceting
    
    HINTS:
    - g = sns.FacetGrid(df, col='var'); g.map(sns.histplot, 'value')
    - sns.catplot(x=..., y=..., col=..., row=..., data=..., kind='box')
    - sns.relplot(x=..., y=..., col=..., data=..., kind='scatter')
    """
    print("\n" + "="*60)
    print("Exercise 5: Faceting")
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
    
    # TODO: FacetGrid with one column variable
    # g = sns.FacetGrid(df, col='category', height=4)
    # g.map(sns.histplot, 'value')
    # g.fig.suptitle('Faceted by Category', y=1.02)
    # plt.savefig('output/day4_ex5_facet_col.png', dpi=150)
    # plt.show()
    
    # TODO: FacetGrid with row and col
    # g = sns.FacetGrid(df, row='type', col='category', height=4)
    # g.map(sns.scatterplot, 'x', 'y')
    # plt.savefig('output/day4_ex5_facet_grid.png', dpi=150)
    # plt.show()
    
    # TODO: catplot
    # g = sns.catplot(x='category', y='value', col='type', data=df, kind='box')
    # plt.savefig('output/day4_ex5_catplot.png', dpi=150)
    # plt.show()
    
    # TODO: relplot
    # g = sns.relplot(x='x', y='y', col='category', hue='type', data=df)
    # plt.savefig('output/day4_ex5_relplot.png', dpi=150)
    # plt.show()
    
    print("Exercise 5: Not implemented yet - fill in the TODOs!")


def exercise_6_styling():
    """
    Exercise 6: Apply themes and customize appearance.
    
    TODO:
    1. Try different themes: whitegrid, darkgrid, white, dark, ticks
    2. Set color palettes: deep, muted, pastel, bright, dark, colorblind
    3. Use custom color palette
    4. Adjust figure aesthetics with set_context
    
    HINTS:
    - sns.set_theme(style='darkgrid', palette='deep')
    - sns.set_palette('colorblind')
    - sns.color_palette('husl', 8)
    - sns.set_context('talk')  # paper, notebook, talk, poster
    """
    print("\n" + "="*60)
    print("Exercise 6: Styling")
    print("="*60)
    
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 100)
    })
    
    themes = ['whitegrid', 'darkgrid', 'white', 'dark']
    
    # TODO: Create subplot for each theme
    # fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    # for ax, theme in zip(axes.flat, themes):
    #     sns.set_theme(style=theme)
    #     sns.scatterplot(x='x', y='y', hue='category', data=df, ax=ax)
    #     ax.set_title(f'Theme: {theme}')
    # plt.tight_layout()
    # plt.savefig('output/day4_ex6_themes.png', dpi=150)
    # plt.show()
    
    # TODO: Try different palettes
    # palettes = ['deep', 'muted', 'pastel', 'colorblind']
    # fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    # for ax, palette in zip(axes.flat, palettes):
    #     sns.set_palette(palette)
    #     sns.barplot(x='category', y='x', data=df, ax=ax)
    #     ax.set_title(f'Palette: {palette}')
    # plt.tight_layout()
    # plt.savefig('output/day4_ex6_palettes.png', dpi=150)
    # plt.show()
    
    # Reset to default
    sns.set_theme()
    
    print("Exercise 6: Not implemented yet - fill in the TODOs!")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 4: SEABORN STATISTICAL VISUALIZATION")
    print("="*60)
    print("\nSeaborn makes statistical visualization beautiful and easy.")
    print("Complete each exercise by filling in the TODO sections.")
    
    exercise_1_distribution_plots()
    exercise_2_relationship_plots()
    exercise_3_categorical_plots()
    exercise_4_heatmaps_clustering()
    exercise_5_faceting()
    exercise_6_styling()
    
    print("\n" + "="*60)
    print("Complete the TODOs and run again to see plots!")
    print("="*60)


if __name__ == "__main__":
    main()
