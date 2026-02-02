#!/usr/bin/env python3
"""
Gradient Descent Implementation from Scratch

Demonstrates batch, SGD, and mini-batch gradient descent on linear regression.

Usage:
    python train.py
    python train.py --variant sgd --lr 0.01 --epochs 100
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def generate_data(n_samples: int = 100, noise: float = 10.0) -> tuple[np.ndarray, np.ndarray]:
    """Generate synthetic linear data."""
    np.random.seed(42)
    X = np.random.randn(n_samples, 2)  # 2 features
    true_weights = np.array([3.0, -2.0])
    true_bias = 5.0
    y = X @ true_weights + true_bias + np.random.randn(n_samples) * noise
    return X, y


def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Squared Error."""
    return np.mean((y_true - y_pred) ** 2)


def compute_gradients(X: np.ndarray, y: np.ndarray, weights: np.ndarray, bias: float) -> tuple[np.ndarray, float]:
    """Compute gradients of MSE loss."""
    n = len(y)
    y_pred = X @ weights + bias
    error = y_pred - y
    
    dw = (2 / n) * X.T @ error
    db = (2 / n) * np.sum(error)
    
    return dw, db


def batch_gradient_descent(
    X: np.ndarray, y: np.ndarray,
    lr: float = 0.01, epochs: int = 100,
) -> tuple[np.ndarray, float, list]:
    """Batch Gradient Descent."""
    weights = np.zeros(X.shape[1])
    bias = 0.0
    losses = []
    
    for epoch in range(epochs):
        dw, db = compute_gradients(X, y, weights, bias)
        weights -= lr * dw
        bias -= lr * db
        
        loss = mse_loss(y, X @ weights + bias)
        losses.append(loss)
    
    return weights, bias, losses


def sgd(
    X: np.ndarray, y: np.ndarray,
    lr: float = 0.01, epochs: int = 100,
) -> tuple[np.ndarray, float, list]:
    """Stochastic Gradient Descent."""
    weights = np.zeros(X.shape[1])
    bias = 0.0
    losses = []
    n = len(y)
    
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        
        for i in indices:
            xi = X[i:i+1]
            yi = y[i:i+1]
            
            dw, db = compute_gradients(xi, yi, weights, bias)
            weights -= lr * dw
            bias -= lr * db
        
        loss = mse_loss(y, X @ weights + bias)
        losses.append(loss)
    
    return weights, bias, losses


def mini_batch_gd(
    X: np.ndarray, y: np.ndarray,
    lr: float = 0.01, epochs: int = 100, batch_size: int = 16,
) -> tuple[np.ndarray, float, list]:
    """Mini-batch Gradient Descent."""
    weights = np.zeros(X.shape[1])
    bias = 0.0
    losses = []
    n = len(y)
    
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            batch_idx = indices[start:end]
            
            xi = X[batch_idx]
            yi = y[batch_idx]
            
            dw, db = compute_gradients(xi, yi, weights, bias)
            weights -= lr * dw
            bias -= lr * db
        
        loss = mse_loss(y, X @ weights + bias)
        losses.append(loss)
    
    return weights, bias, losses


def momentum_gd(
    X: np.ndarray, y: np.ndarray,
    lr: float = 0.01, epochs: int = 100, beta: float = 0.9,
) -> tuple[np.ndarray, float, list]:
    """Gradient Descent with Momentum."""
    weights = np.zeros(X.shape[1])
    bias = 0.0
    losses = []
    
    vw = np.zeros_like(weights)
    vb = 0.0
    
    for epoch in range(epochs):
        dw, db = compute_gradients(X, y, weights, bias)
        
        vw = beta * vw + lr * dw
        vb = beta * vb + lr * db
        
        weights -= vw
        bias -= vb
        
        loss = mse_loss(y, X @ weights + bias)
        losses.append(loss)
    
    return weights, bias, losses


def train_model(
    variant: str = "batch",
    lr: float = 0.01,
    epochs: int = 100,
    batch_size: int = 16,
) -> dict:
    """Train using gradient descent."""
    print(f"\n{'='*60}")
    print(f"GRADIENT DESCENT ({variant.upper()})")
    print(f"{'='*60}")
    
    X, y = generate_data(n_samples=200)
    print(f"\nDataset: {len(X)} samples, {X.shape[1]} features")
    print(f"True weights: [3.0, -2.0], bias: 5.0")
    print(f"Learning rate: {lr}, Epochs: {epochs}")
    
    # Train
    if variant == "batch":
        weights, bias, losses = batch_gradient_descent(X, y, lr, epochs)
    elif variant == "sgd":
        weights, bias, losses = sgd(X, y, lr, epochs)
    elif variant == "mini_batch":
        weights, bias, losses = mini_batch_gd(X, y, lr, epochs, batch_size)
    elif variant == "momentum":
        weights, bias, losses = momentum_gd(X, y, lr, epochs)
    else:
        raise ValueError(f"Unknown variant: {variant}")
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Learned weights: {weights.round(4)}")
    print(f"Learned bias:    {bias:.4f}")
    print(f"Final loss:      {losses[-1]:.4f}")
    
    # Loss progression
    print("\n" + "-" * 40)
    print("LOSS PROGRESSION")
    print("-" * 40)
    
    checkpoints = [0, epochs//4, epochs//2, 3*epochs//4, epochs-1]
    for i in checkpoints:
        bar = "█" * int((1 - losses[i]/losses[0]) * 30)
        print(f"Epoch {i+1:4d}: loss={losses[i]:8.4f} {bar}")
    
    # Compare variants
    print("\n" + "-" * 40)
    print("VARIANT COMPARISON (same epochs)")
    print("-" * 40)
    
    variants = {
        "Batch": batch_gradient_descent(X, y, lr, epochs),
        "SGD": sgd(X, y, lr/10, epochs),  # Lower LR for SGD
        "Mini-batch": mini_batch_gd(X, y, lr, epochs),
        "Momentum": momentum_gd(X, y, lr, epochs),
    }
    
    for name, (w, b, l) in variants.items():
        print(f"{name:<12}: final_loss={l[-1]:8.4f}, weights={w.round(2)}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump({"weights": weights, "bias": bias}, MODEL_DIR / "model.joblib")
    joblib.dump(losses, MODEL_DIR / "losses.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"weights": weights, "bias": bias, "losses": losses}


def main():
    parser = argparse.ArgumentParser(description="Gradient Descent Demo")
    parser.add_argument("--variant", type=str, default="batch",
                       choices=["batch", "sgd", "mini_batch", "momentum"])
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    
    args = parser.parse_args()
    train_model(variant=args.variant, lr=args.lr, epochs=args.epochs, batch_size=args.batch_size)


if __name__ == "__main__":
    main()
