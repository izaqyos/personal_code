#!/usr/bin/env python3
"""Gradient Descent Inference Script"""

from pathlib import Path
import joblib
import numpy as np

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


def load_model():
    model = joblib.load(MODEL_DIR / "model.joblib")
    losses = joblib.load(MODEL_DIR / "losses.joblib")
    return model["weights"], model["bias"], losses


def demo_predictions():
    print("\n" + "=" * 60)
    print("GRADIENT DESCENT INFERENCE DEMO")
    print("=" * 60)
    
    weights, bias, losses = load_model()
    
    print(f"\nLearned Parameters:")
    print(f"  Weights: {weights}")
    print(f"  Bias:    {bias:.4f}")
    
    print(f"\nTraining Summary:")
    print(f"  Initial loss: {losses[0]:.4f}")
    print(f"  Final loss:   {losses[-1]:.4f}")
    print(f"  Improvement:  {(1 - losses[-1]/losses[0])*100:.1f}%")
    
    # Predictions
    print("\n" + "-" * 60)
    print("Sample Predictions: y = w₁x₁ + w₂x₂ + b")
    print("-" * 60)
    
    samples = [
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [2.0, -1.0],
    ]
    
    for x in samples:
        y_pred = np.dot(weights, x) + bias
        print(f"  x={x} -> y_pred={y_pred:.2f}")
    
    print("\nTrue function: y = 3x₁ - 2x₂ + 5")


if __name__ == "__main__":
    demo_predictions()
