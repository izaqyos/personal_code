#!/usr/bin/env python3
"""
Exercise 7: Advanced Plot Types
================================
Time: 25-30 minutes

Explore specialized visualizations:
- Heatmaps and colorbars
- Contour plots
- 3D plots
- Pie charts and polar plots
- Image display

Run: python run_exercises.py 7
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SAMPLE DATA
# ============================================================

# For heatmaps
np.random.seed(42)
correlation_matrix = np.random.rand(8, 8)
correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
np.fill_diagonal(correlation_matrix, 1)

# For contour plots
x_grid = np.linspace(-3, 3, 100)
y_grid = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x_grid, y_grid)
Z = np.sin(X) * np.cos(Y) * np.exp(-(X**2 + Y**2) / 10)

# For 3D
theta_3d = np.linspace(0, 4 * np.pi, 100)
z_3d = np.linspace(0, 2, 100)
r_3d = z_3d**2 + 1
x_3d = r_3d * np.sin(theta_3d)
y_3d = r_3d * np.cos(theta_3d)

# For pie chart
market_share = [35, 25, 20, 12, 8]
companies = ['Company A', 'Company B', 'Company C', 'Company D', 'Others']

# For polar
angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
values = [4, 3, 5, 2, 4, 5, 3, 4]  # Radar chart values

# For image
image_data = np.random.rand(100, 100)
image_rgb = np.random.rand(50, 50, 3)


# ============================================================
# EXERCISE 7.1: Heatmap
# ============================================================

def exercise_1_heatmap():
    """
    Create a heatmap of the correlation matrix.
    
    TODO:
    1. Create a figure with figsize=(10, 8)
    2. Use plt.imshow() or ax.imshow() to display correlation_matrix
    3. Add a colorbar with appropriate label
    4. Add labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
       on both axes
    5. Annotate each cell with its value (rounded to 2 decimals)
       Hint: Use nested loops and ax.text()
    6. Use a diverging colormap (e.g., 'coolwarm')
    7. Set vmin=-1, vmax=1 for correlation range
    
    Hints:
    - ax.set_xticks(range(8))
    - ax.set_xticklabels(['A', 'B', ...])
    - For annotations: ax.text(j, i, f'{val:.2f}', ha='center', va='center')
    
    Expected: A labeled correlation heatmap with cell values
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.2: Contour Plot
# ============================================================

def exercise_2_contour():
    """
    Create filled contour plots.
    
    TODO:
    1. Create a figure with 2 subplots side by side
    2. Left: Contour lines only
       - Use ax.contour(X, Y, Z, levels=15)
       - Add contour labels using ax.clabel()
    3. Right: Filled contours
       - Use ax.contourf(X, Y, Z, levels=15, cmap='viridis')
       - Add a colorbar
    4. Add titles: "Contour Lines" and "Filled Contours"
    5. Label axes as 'x' and 'y'
    
    Expected: Two contour visualizations of the same data
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.3: 3D Line Plot
# ============================================================

def exercise_3_3d_line():
    """
    Create a 3D spiral plot.
    
    TODO:
    1. Create a figure with a 3D axes
       Hint: fig = plt.figure(); ax = fig.add_subplot(111, projection='3d')
    2. Plot the 3D spiral using ax.plot3D(x_3d, y_3d, z_3d)
    3. Color the line by height (z value)
       Alternative: Use ax.scatter3D for colored points
    4. Add labels: 'X', 'Y', 'Z'
    5. Add title: "3D Spiral"
    6. Adjust viewing angle: ax.view_init(elev=30, azim=45)
    
    Expected: A colorful 3D spiral that can be rotated interactively
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.4: 3D Surface Plot
# ============================================================

def exercise_4_3d_surface():
    """
    Create a 3D surface plot.
    
    TODO:
    1. Create a figure with a 3D axes
    2. Plot Z as a surface: ax.plot_surface(X, Y, Z, cmap='coolwarm')
    3. Add a colorbar
    4. Customize:
       - Transparency: alpha=0.8
       - Edge color: edgecolor='none' for smooth
       - Or edgecolor='black', linewidth=0.5 for wireframe look
    5. Add contour projection on the bottom
       Hint: ax.contourf(X, Y, Z, zdir='z', offset=-1, cmap='coolwarm')
    6. Set axis limits and labels
    
    Expected: A beautiful 3D surface with contour base
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.5: Pie Chart
# ============================================================

def exercise_5_pie():
    """
    Create an enhanced pie chart.
    
    TODO:
    1. Create a basic pie chart of market_share with companies labels
    2. Enhance it:
       - Explode the largest slice (first one)
       - Show percentages: autopct='%1.1f%%'
       - Add a shadow
       - Start angle: startangle=90
    3. Make it a donut chart:
       - Draw a white circle in the center
       Hint: circle = plt.Circle((0,0), 0.5, color='white')
             ax.add_artist(circle)
    4. Add center text showing total or title
    
    Expected: A professional-looking donut chart
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.6: Radar/Spider Chart
# ============================================================

def exercise_6_radar():
    """
    Create a radar (spider) chart.
    
    TODO:
    1. Create a polar axes: fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    2. Plot the radar chart:
       - Categories: ['Speed', 'Power', 'Defense', 'Magic', 'Luck', 'HP', 'MP', 'Stamina']
       - Values: values (from sample data)
       - Close the polygon by appending first value
    3. Fill the area with color and alpha
    4. Add a second data series for comparison
       values2 = [3, 4, 3, 5, 2, 4, 4, 3]
    5. Add legend
    6. Add title
    
    Hints:
    - angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
    - angles = np.concatenate((angles, [angles[0]]))  # close polygon
    - values = values + [values[0]]  # close polygon
    
    Expected: A radar chart comparing two entities
    """
    # YOUR CODE HERE
    pass


# ============================================================
# EXERCISE 7.7: Challenge - Multi-Type Dashboard
# ============================================================

def exercise_7_dashboard():
    """
    Create a dashboard combining multiple plot types.
    
    TODO:
    1. Create a 2x3 figure with different plot types:
       - (0,0): Heatmap (small version)
       - (0,1): Contour plot
       - (0,2): Pie chart
       - (1,0): 3D surface (use projection='3d')
       - (1,1): Polar/radar chart
       - (1,2): Your choice - be creative!
    2. Use consistent styling:
       - Same colormap family
       - Consistent fonts
    3. Add a main title
    4. Make it look professional
    
    This requires GridSpec since 3D and polar need special projections.
    
    Hints:
    - gs = fig.add_gridspec(2, 3)
    - ax1 = fig.add_subplot(gs[0, 0])  # regular
    - ax5 = fig.add_subplot(gs[1, 1], projection='polar')
    
    Expected: A diverse, visually cohesive dashboard
    """
    # YOUR CODE HERE
    pass


# ============================================================
# RUNNER
# ============================================================

def run_all(interactive=False):
    """Run all exercises in this module"""
    exercises = [
        ("7.1 Heatmap", exercise_1_heatmap),
        ("7.2 Contour Plot", exercise_2_contour),
        ("7.3 3D Line", exercise_3_3d_line),
        ("7.4 3D Surface", exercise_4_3d_surface),
        ("7.5 Pie/Donut Chart", exercise_5_pie),
        ("7.6 Radar Chart", exercise_6_radar),
        ("7.7 Multi-Type Dashboard", exercise_7_dashboard),
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
- ax.imshow(): display matrix as image/heatmap
- ax.contour(), ax.contourf(): contour lines/filled
- ax.plot3D(), ax.scatter3D(): 3D line/scatter
- ax.plot_surface(): 3D surface
- ax.pie(): pie chart
- Polar projection for radar charts

3D basics:
- from mpl_toolkits.mplot3d import Axes3D
- ax = fig.add_subplot(111, projection='3d')
- ax.view_init(elev, azim)

Questions:
- 
"""

if __name__ == "__main__":
    run_all(interactive=True)
