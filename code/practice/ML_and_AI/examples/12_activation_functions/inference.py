#!/usr/bin/env python3
"""Activation Functions Visualization and Analysis"""

import numpy as np


def visualize_activations():
    """Show activation functions and their properties."""
    print("\n" + "=" * 60)
    print("ACTIVATION FUNCTIONS REFERENCE")
    print("=" * 60)
    
    print("""
╔══════════════╦════════════╦═══════════════╦═══════════════════╗
║ Activation   ║ Range      ║ Gradient      ║ Best For          ║
╠══════════════╬════════════╬═══════════════╬═══════════════════╣
║ Sigmoid      ║ (0, 1)     ║ 0.25 max      ║ Binary output     ║
║ Tanh         ║ (-1, 1)    ║ 1.0 max       ║ Hidden (legacy)   ║
║ ReLU         ║ [0, ∞)     ║ 0 or 1        ║ Hidden (default)  ║
║ Leaky ReLU   ║ (-∞, ∞)    ║ α or 1        ║ Prevent dying     ║
║ GELU         ║ (-0.17, ∞) ║ Smooth        ║ Transformers      ║
║ Softmax      ║ (0, 1)     ║ -             ║ Multiclass output ║
╚══════════════╩════════════╩═══════════════╩═══════════════════╝
    """)
    
    print("\nFormulas:")
    print("-" * 60)
    print("Sigmoid:    σ(x) = 1 / (1 + e^(-x))")
    print("Tanh:       tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))")
    print("ReLU:       f(x) = max(0, x)")
    print("Leaky ReLU: f(x) = max(αx, x),  α ≈ 0.01")
    print("GELU:       f(x) = x · Φ(x),    Φ = standard normal CDF")
    print("Softmax:    f(xᵢ) = e^xᵢ / Σⱼe^xⱼ")
    
    print("\n" + "-" * 60)
    print("Sample Values (x = -2, -1, 0, 1, 2):")
    print("-" * 60)
    
    x = np.array([-2, -1, 0, 1, 2])
    
    print(f"x:          {x}")
    print(f"Sigmoid:    {(1 / (1 + np.exp(-x))).round(3)}")
    print(f"Tanh:       {np.tanh(x).round(3)}")
    print(f"ReLU:       {np.maximum(0, x)}")
    print(f"LeakyReLU:  {np.where(x > 0, x, 0.01 * x).round(3)}")
    
    print("\nWhen to Use What:")
    print("-" * 60)
    print("• Hidden layers: ReLU (fast, works well)")
    print("• Deep networks: Leaky ReLU or GELU (avoid dying neurons)")
    print("• Binary output: Sigmoid")
    print("• Multiclass output: Softmax")
    print("• Transformers: GELU (smoother gradients)")


if __name__ == "__main__":
    visualize_activations()
