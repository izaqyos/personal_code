#!/usr/bin/env python3
"""
Matplotlib Practice Exercises - Runner/Harness
===============================================

Usage:
    python run_exercises.py                    # Run all exercises
    python run_exercises.py 1                  # Run exercise 1 only
    python run_exercises.py 1 2 3              # Run exercises 1, 2, and 3
    python run_exercises.py --list             # List all exercises
    python run_exercises.py --interactive      # Run in interactive mode (pauses between plots)

Each exercise has multiple parts. Implement the TODOs and run to see your plots.
"""

import sys
import argparse
import importlib
from pathlib import Path

# Exercise modules and their descriptions
EXERCISES = {
    1: ("ex01_basic_line_plots", "Basic Line Plots - plt.plot(), labels, titles"),
    2: ("ex02_subplots_layouts", "Subplots & Layouts - fig, ax, gridspec"),
    3: ("ex03_bar_scatter", "Bar Charts & Scatter Plots"),
    4: ("ex04_histograms_distributions", "Histograms & Distribution Plots"),
    5: ("ex05_customization_styling", "Customization & Styling - colors, markers, legends"),
    6: ("ex06_annotations_text", "Annotations, Text & Arrows"),
    7: ("ex07_advanced_plots", "Advanced Plots - heatmaps, 3D, contours"),
}


def list_exercises():
    """Print available exercises"""
    print("\n" + "=" * 60)
    print("MATPLOTLIB PRACTICE EXERCISES")
    print("=" * 60)
    for num, (module, desc) in EXERCISES.items():
        print(f"  {num}. {desc}")
        print(f"     File: {module}.py")
    print("=" * 60 + "\n")


def run_exercise(num: int, interactive: bool = False):
    """Run a specific exercise module"""
    if num not in EXERCISES:
        print(f"❌ Exercise {num} not found. Use --list to see available exercises.")
        return False
    
    module_name, desc = EXERCISES[num]
    print(f"\n{'=' * 60}")
    print(f"EXERCISE {num}: {desc}")
    print(f"{'=' * 60}\n")
    
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'run_all'):
            module.run_all(interactive=interactive)
        else:
            print(f"⚠️  Module {module_name} missing run_all() function")
            return False
    except ImportError as e:
        print(f"❌ Could not import {module_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running exercise: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run matplotlib practice exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'exercises', 
        nargs='*', 
        type=int,
        help="Exercise numbers to run (default: all)"
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help="List all available exercises"
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help="Run in interactive mode (pauses between plots)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_exercises()
        return
    
    # Determine which exercises to run
    if args.exercises:
        exercise_nums = args.exercises
    else:
        exercise_nums = list(EXERCISES.keys())
    
    print("\n" + "=" * 60)
    print("MATPLOTLIB PRACTICE SESSION")
    print("=" * 60)
    print(f"Running exercises: {exercise_nums}")
    print("Tip: Close each plot window to proceed to the next one")
    print("=" * 60)
    
    success_count = 0
    for num in exercise_nums:
        if run_exercise(num, interactive=args.interactive):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"SESSION COMPLETE: {success_count}/{len(exercise_nums)} exercises ran")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
