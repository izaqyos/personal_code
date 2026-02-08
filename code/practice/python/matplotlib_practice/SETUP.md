# Setup Instructions

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run Day 1 exercises
python day1_basic_plots.py

# Deactivate when done
deactivate
```

## Initial Setup (Already Done!)

The virtual environment and dependencies have been installed:

```bash
# Virtual environment created
python3 -m venv venv

# Dependencies installed
source venv/bin/activate
pip install -r requirements.txt
```

## Installed Packages

- **matplotlib** (3.10.8) - Core plotting library
- **numpy** (2.4.2) - Numerical computing
- **pandas** (3.0.0) - Data manipulation
- **seaborn** (0.13.2) - Statistical visualization
- **scipy** (1.17.0) - Scientific computing

## Running Exercises

```bash
# Always activate venv first
source venv/bin/activate

# Run any day's exercises
python day1_basic_plots.py
python day2_customization.py
# ... etc

# Or run specific exercise
python -c "from day1_basic_plots import exercise_1_simple_line_plot; exercise_1_simple_line_plot()"
```

## Troubleshooting

### Import errors
Make sure the virtual environment is activated:
```bash
source venv/bin/activate
```

### Missing packages
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Output folder
The scripts will automatically create an `output/` folder for saved plots.

## VS Code Integration

To use this venv in VS Code:
1. Open Command Palette (Cmd+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose `./venv/bin/python`
