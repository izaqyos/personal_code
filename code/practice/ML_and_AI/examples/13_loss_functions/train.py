#!/usr/bin/env python3
"""
Loss Functions Implementation and Comparison

Demonstrates all major loss functions.

Usage:
    python train.py
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================================
# REGRESSION LOSSES
# ============================================================================

def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Squared Error: (1/n) Σ(y - ŷ)²"""
    return np.mean((y_true - y_pred) ** 2)


def mae_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error: (1/n) Σ|y - ŷ|"""
    return np.mean(np.abs(y_true - y_pred))


def huber_loss(y_true: np.ndarray, y_pred: np.ndarray, delta: float = 1.0) -> float:
    """Huber Loss: MSE for small errors, MAE for large errors"""
    error = np.abs(y_true - y_pred)
    is_small = error <= delta
    small_error = 0.5 * error ** 2
    large_error = delta * error - 0.5 * delta ** 2
    return np.mean(np.where(is_small, small_error, large_error))


# ============================================================================
# CLASSIFICATION LOSSES
# ============================================================================

def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-7) -> float:
    """Binary Cross-Entropy: -[y·log(ŷ) + (1-y)·log(1-ŷ)]"""
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def cross_entropy(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-7) -> float:
    """Cross-Entropy for multiclass: -Σ yᵢ·log(ŷᵢ)"""
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=-1))


def focal_loss(y_true: np.ndarray, y_pred: np.ndarray, gamma: float = 2.0, eps: float = 1e-7) -> float:
    """Focal Loss: -αₜ(1-pₜ)^γ log(pₜ) - focuses on hard examples"""
    y_pred = np.clip(y_pred, eps, 1 - eps)
    pt = y_true * y_pred + (1 - y_true) * (1 - y_pred)
    focal_weight = (1 - pt) ** gamma
    bce = -y_true * np.log(y_pred) - (1 - y_true) * np.log(1 - y_pred)
    return np.mean(focal_weight * bce)


def demo_losses():
    """Demonstrate all loss functions."""
    print("\n" + "=" * 60)
    print("LOSS FUNCTIONS DEMO")
    print("=" * 60)
    
    # ===== REGRESSION LOSSES =====
    print("\n" + "-" * 40)
    print("REGRESSION LOSSES")
    print("-" * 40)
    
    y_true = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred = np.array([2.5, 0.0, 2.0, 8.0])
    
    print(f"\ny_true: {y_true}")
    print(f"y_pred: {y_pred}")
    print(f"errors: {y_true - y_pred}")
    
    print(f"\nMSE:   {mse_loss(y_true, y_pred):.4f}")
    print(f"MAE:   {mae_loss(y_true, y_pred):.4f}")
    print(f"Huber: {huber_loss(y_true, y_pred):.4f}")
    
    # With outlier
    print("\nWith outlier (y_pred[0] = 10.0):")
    y_pred_outlier = np.array([10.0, 0.0, 2.0, 8.0])
    print(f"MSE:   {mse_loss(y_true, y_pred_outlier):.4f} (affected by outlier)")
    print(f"MAE:   {mae_loss(y_true, y_pred_outlier):.4f} (less affected)")
    print(f"Huber: {huber_loss(y_true, y_pred_outlier):.4f} (robust)")
    
    # ===== CLASSIFICATION LOSSES =====
    print("\n" + "-" * 40)
    print("CLASSIFICATION LOSSES")
    print("-" * 40)
    
    # Binary classification
    y_true_binary = np.array([1, 0, 1, 1])
    y_pred_proba = np.array([0.9, 0.1, 0.8, 0.6])
    
    print(f"\nBinary Classification:")
    print(f"y_true: {y_true_binary}")
    print(f"y_pred: {y_pred_proba}")
    print(f"\nBCE Loss: {binary_cross_entropy(y_true_binary, y_pred_proba):.4f}")
    
    # Show confidence effect
    print("\nConfidence Effect on BCE:")
    for conf in [0.5, 0.7, 0.9, 0.99]:
        loss = binary_cross_entropy(np.array([1]), np.array([conf]))
        print(f"  P(y=1) = {conf}: BCE = {loss:.4f}")
    
    # Focal loss comparison
    print("\nFocal Loss (focuses on hard examples):")
    for conf in [0.5, 0.7, 0.9, 0.99]:
        bce = binary_cross_entropy(np.array([1]), np.array([conf]))
        focal = focal_loss(np.array([1]), np.array([conf]), gamma=2.0)
        print(f"  P(y=1) = {conf}: BCE = {bce:.4f}, Focal = {focal:.4f}")
    
    # ===== PYTORCH COMPARISON =====
    print("\n" + "-" * 40)
    print("PYTORCH IMPLEMENTATIONS")
    print("-" * 40)
    
    # Regression
    y_t = torch.tensor([3.0, -0.5, 2.0, 7.0])
    y_p = torch.tensor([2.5, 0.0, 2.0, 8.0])
    
    print(f"\nnn.MSELoss:      {nn.MSELoss()(y_p, y_t).item():.4f}")
    print(f"nn.L1Loss (MAE): {nn.L1Loss()(y_p, y_t).item():.4f}")
    print(f"nn.SmoothL1Loss: {nn.SmoothL1Loss()(y_p, y_t).item():.4f}")
    
    # Classification
    logits = torch.tensor([[2.0, 0.5, -1.0]])  # Raw scores
    target = torch.tensor([0])  # Class 0
    
    print(f"\nnn.CrossEntropyLoss: {nn.CrossEntropyLoss()(logits, target).item():.4f}")
    
    print("\nLoss functions demonstrated successfully!")


def main():
    demo_losses()


if __name__ == "__main__":
    main()
