#!/usr/bin/env python3
"""
Activation Functions Implementation and Visualization

Demonstrates all major activation functions and their gradients.

Usage:
    python train.py
"""

from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid: σ(x) = 1 / (1 + e^(-x))"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """Sigmoid derivative: σ(x) * (1 - σ(x))"""
    s = sigmoid(x)
    return s * (1 - s)


def tanh(x: np.ndarray) -> np.ndarray:
    """Tanh: (e^x - e^(-x)) / (e^x + e^(-x))"""
    return np.tanh(x)


def tanh_derivative(x: np.ndarray) -> np.ndarray:
    """Tanh derivative: 1 - tanh²(x)"""
    return 1 - np.tanh(x) ** 2


def relu(x: np.ndarray) -> np.ndarray:
    """ReLU: max(0, x)"""
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """ReLU derivative: 1 if x > 0 else 0"""
    return (x > 0).astype(float)


def leaky_relu(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Leaky ReLU: max(αx, x)"""
    return np.where(x > 0, x, alpha * x)


def leaky_relu_derivative(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Leaky ReLU derivative"""
    return np.where(x > 0, 1, alpha)


def gelu(x: np.ndarray) -> np.ndarray:
    """GELU: x * Φ(x) where Φ is CDF of standard normal"""
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


def softmax(x: np.ndarray) -> np.ndarray:
    """Softmax: e^xᵢ / Σe^xⱼ"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def demo_activations():
    """Demonstrate all activation functions."""
    print("\n" + "=" * 60)
    print("ACTIVATION FUNCTIONS DEMO")
    print("=" * 60)
    
    # Test values
    x = np.array([-3, -1, 0, 1, 3])
    
    activations = {
        "Sigmoid": (sigmoid, sigmoid_derivative),
        "Tanh": (tanh, tanh_derivative),
        "ReLU": (relu, relu_derivative),
        "Leaky ReLU": (leaky_relu, leaky_relu_derivative),
        "GELU": (gelu, None),
    }
    
    print(f"\nInput x: {x}")
    print("\n" + "-" * 60)
    
    for name, (func, deriv) in activations.items():
        output = func(x)
        print(f"\n{name}:")
        print(f"  f(x):  {output.round(4)}")
        if deriv:
            grad = deriv(x)
            print(f"  f'(x): {grad.round(4)}")
    
    # Softmax demo
    print("\n" + "-" * 60)
    print("SOFTMAX (for classification output)")
    print("-" * 60)
    
    logits = np.array([[2.0, 1.0, 0.1], [1.0, 3.0, 0.5]])
    probs = softmax(logits)
    
    print(f"\nLogits:\n{logits}")
    print(f"\nSoftmax probabilities:\n{probs.round(4)}")
    print(f"Sum per row: {probs.sum(axis=1).round(4)}")
    
    # Compare with PyTorch
    print("\n" + "-" * 60)
    print("PYTORCH COMPARISON")
    print("-" * 60)
    
    x_torch = torch.tensor([-3.0, -1.0, 0.0, 1.0, 3.0], requires_grad=True)
    
    pytorch_activations = {
        "torch.sigmoid": torch.sigmoid,
        "torch.tanh": torch.tanh,
        "F.relu": F.relu,
        "F.leaky_relu": lambda x: F.leaky_relu(x, 0.01),
        "F.gelu": F.gelu,
    }
    
    for name, func in pytorch_activations.items():
        out = func(x_torch)
        print(f"{name:<18}: {out.detach().numpy().round(4)}")
    
    # Training comparison
    print("\n" + "-" * 60)
    print("ACTIVATION COMPARISON IN TRAINING")
    print("-" * 60)
    print("Testing which activation converges faster on XOR problem...")
    
    from train_comparison import compare_activations
    compare_activations()
    
    print("\nActivation functions demonstrated successfully!")


def main():
    demo_activations()


if __name__ == "__main__":
    main()
