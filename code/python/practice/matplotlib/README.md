# Matplotlib Practice Exercises

A structured set of exercises to learn matplotlib from basics to advanced topics.

## Setup

The virtual environment is already created and dependencies are installed!

### Activate the environment:

```bash
# On macOS/Linux
source venv/bin/activate

# Or use the full path
./venv/bin/python3 run_exercises.py --list
```

### Dependencies installed:
- matplotlib 3.10.8
- numpy 2.4.1
- scipy 1.17.0

## Usage

### Option 1: Use the wrapper script (easiest - no activation needed!)

```bash
./run.sh --list              # List all exercises
./run.sh                     # Run all exercises
./run.sh 1                   # Run exercise 1
./run.sh 1 2 3               # Run multiple exercises
./run.sh 1 --interactive     # Interactive mode
```

### Option 2: Activate the virtual environment first

```bash
# Activate the virtual environment
source activate.sh
# or
source venv/bin/activate

# Then run exercises:
python run_exercises.py --list          # List all exercises
python run_exercises.py 1               # Run exercise 1
python ex01_basic_line_plots.py         # Run file directly
```

## Exercise Structure

Each exercise file (`ex01_*.py` through `ex07_*.py`) contains:
- **Sample data** at the top - ready to use
- **5-7 exercises** with clear TODO instructions
- **Helper functions** and hints
- **Notes section** at the bottom for your observations

## Exercises

1. **Basic Line Plots** (`ex01_basic_line_plots.py`)
   - Simple line plots, labels, titles
   - Multiple lines on one plot
   - Line styles and markers
   - Figure customization and saving

2. **Subplots & Layouts** (`ex02_subplots_layouts.py`)
   - Creating subplot grids
   - Shared axes
   - GridSpec for complex layouts
   - Inset axes

3. **Bar Charts & Scatter Plots** (`ex03_bar_scatter.py`)
   - Vertical and horizontal bars
   - Grouped and stacked bars
   - Scatter plots with encoding
   - Bubble charts

4. **Histograms & Distributions** (`ex04_histograms_distributions.py`)
   - Histograms with customization
   - Kernel density estimates (KDE)
   - Box plots and violin plots
   - Distribution comparisons

5. **Customization & Styling** (`ex05_customization_styling.py`)
   - Color specifications
   - Line styles and markers
   - Custom legends
   - Themes and style sheets
   - Tick formatting

6. **Annotations & Text** (`ex06_annotations_text.py`)
   - Text placement
   - Arrows and annotations
   - LaTeX mathematical expressions
   - Text boxes and callouts

7. **Advanced Plot Types** (`ex07_advanced_plots.py`)
   - Heatmaps and colorbars
   - Contour plots
   - 3D plots (lines, surfaces)
   - Pie/donut charts
   - Radar/spider charts

## Workflow

1. Open an exercise file (e.g., `ex01_basic_line_plots.py`)
2. Read the exercise description and TODO comments
3. Implement the function (replace `pass` with your code)
4. Run it: `python3 run_exercises.py 1`
5. View the plots and iterate
6. Add notes in the "NOTES & INSIGHTS" section

## Tips

- Start with Exercise 1 and work sequentially
- Each exercise builds on previous concepts
- Sample data is provided - focus on the matplotlib code
- Close plot windows to proceed to the next exercise
- Use `--interactive` flag to pause between plots
- Check the hints in comments if you get stuck

## Quick Test

```bash
# Activate the environment
source activate.sh

# Test that everything works
python -c "import matplotlib; import numpy; import scipy; print('✅ All dependencies installed!')"

# List exercises
python run_exercises.py --list
```

Happy plotting! 📊
