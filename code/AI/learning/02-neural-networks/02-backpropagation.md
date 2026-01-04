# Backpropagation

> The algorithm that makes deep learning possible - computing gradients efficiently.

---

## Overview

Backpropagation computes gradients of the loss with respect to every parameter in the network using the chain rule.

```
Forward Pass:  Input ──→ Layer 1 ──→ Layer 2 ──→ ... ──→ Output ──→ Loss
                                                                       │
Backward Pass: ∂L/∂W₁ ←── ∂L/∂W₂ ←── ... ←───────────────────────────←┘
```

---

## The Chain Rule

For composite functions, derivatives multiply:

```
If y = f(g(x)), then:

dy/dx = (dy/dg) × (dg/dx) = f'(g(x)) × g'(x)

Example:
y = (3x + 2)²
g(x) = 3x + 2
f(g) = g²

dy/dx = 2g × 3 = 2(3x + 2) × 3 = 6(3x + 2)
```

---

## Computational Graph

Visualize computations as a directed graph:

```
Simple example: L = (wx + b - y)²

       x ─────────┐
                  ├──→ [×] ──→ [+] ──→ [-] ──→ [²] ──→ L
       w ─────────┘      │      │
                         │      │
       b ────────────────┘      │
                                │
       y ───────────────────────┘

Forward: Compute left to right
Backward: Compute gradients right to left
```

---

## Backprop Step by Step

### Example: Single Neuron

```
Forward:
z = wx + b
a = σ(z)        # sigmoid activation
L = -(y log(a) + (1-y) log(1-a))   # binary cross-entropy

Backward (using chain rule):

∂L/∂a = -y/a + (1-y)/(1-a)

∂L/∂z = ∂L/∂a × ∂a/∂z
      = (-y/a + (1-y)/(1-a)) × σ(z)(1-σ(z))
      = a - y   (simplifies nicely!)

∂L/∂w = ∂L/∂z × ∂z/∂w = (a - y) × x

∂L/∂b = ∂L/∂z × ∂z/∂b = (a - y) × 1

∂L/∂x = ∂L/∂z × ∂z/∂x = (a - y) × w   (for deeper layers)
```

### Multi-Layer Network

```
Layer l:
  Input:  a⁽ˡ⁻¹⁾
  Linear: z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
  Output: a⁽ˡ⁾ = f(z⁽ˡ⁾)

Backprop equations:

δ⁽ˡ⁾ = ∂L/∂z⁽ˡ⁾   # "error" at layer l

δ⁽L⁾ = ∇ₐL ⊙ f'(z⁽L⁾)    # Output layer

δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾ᵀ δ⁽ˡ⁺¹⁾) ⊙ f'(z⁽ˡ⁾)   # Hidden layers

∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾ (a⁽ˡ⁻¹⁾)ᵀ    # Weight gradients

∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾             # Bias gradients
```

---

## Visual Walkthrough

```
Network:  x → [W₁, b₁] → ReLU → [W₂, b₂] → Softmax → Loss

FORWARD:
x = [1, 2]
z₁ = W₁x + b₁ = [0.5, -0.3]
a₁ = ReLU(z₁) = [0.5, 0]
z₂ = W₂a₁ + b₂ = [0.2, 0.8]
a₂ = softmax(z₂) = [0.35, 0.65]
L = -log(0.35) = 1.05  (if true class is 0)

BACKWARD:
δ₂ = a₂ - y = [0.35-1, 0.65-0] = [-0.65, 0.65]
∂L/∂W₂ = δ₂ ⊗ a₁ᵀ
∂L/∂b₂ = δ₂

δ₁ = (W₂ᵀ δ₂) ⊙ ReLU'(z₁)
    = [?, ?] ⊙ [1, 0]  # ReLU'=0 where z₁<0
∂L/∂W₁ = δ₁ ⊗ xᵀ
∂L/∂b₁ = δ₁
```

---

## Automatic Differentiation

Modern frameworks compute gradients automatically:

### PyTorch Autograd

```python
import torch

# Create tensors with gradient tracking
x = torch.tensor([1.0, 2.0], requires_grad=True)
w = torch.tensor([[0.5, 0.3], [0.2, 0.4]], requires_grad=True)
b = torch.tensor([0.1, 0.1], requires_grad=True)

# Forward pass (builds computational graph)
z = x @ w + b
a = torch.relu(z)
loss = a.sum()

# Backward pass (computes all gradients)
loss.backward()

# Access gradients
print(f"∂L/∂w = {w.grad}")
print(f"∂L/∂b = {b.grad}")
print(f"∂L/∂x = {x.grad}")
```

### How Autograd Works

```python
# Each tensor operation creates a node in the graph
#
#   x ──┐
#       ├── MatMul ──┐
#   w ──┘            │
#                    ├── Add ── ReLU ── Sum ── loss
#   b ───────────────┘
#
# backward() traverses graph in reverse, computing gradients
```

---

## Common Issues

### Vanishing Gradients

```
Deep networks with sigmoid/tanh:
∂σ/∂z = σ(1-σ) ≤ 0.25

After many layers:
∂L/∂W₁ = (0.25)^L × ... → 0

Solutions:
- ReLU activation (gradient = 1 for positive)
- Batch normalization
- Residual connections
- Better initialization
```

### Exploding Gradients

```
Gradients grow exponentially:
∂L/∂W₁ = (large)^L × ... → ∞

Solutions:
- Gradient clipping: clip(grad, -max_norm, max_norm)
- Weight regularization
- Careful initialization
```

### Dead ReLU

```
If z < 0, ReLU(z) = 0 and gradient = 0
Neuron never updates → "dead"

Solutions:
- Leaky ReLU: max(0.01z, z)
- ELU, GELU activations
- Careful initialization
```

---

## Implementation from Scratch

```python
import numpy as np

class Layer:
    def forward(self, x):
        raise NotImplementedError

    def backward(self, grad_output):
        raise NotImplementedError

class Linear(Layer):
    def __init__(self, in_features, out_features):
        self.W = np.random.randn(in_features, out_features) * 0.01
        self.b = np.zeros((1, out_features))
        self.grad_W = None
        self.grad_b = None

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, grad_output):
        self.grad_W = self.x.T @ grad_output
        self.grad_b = np.sum(grad_output, axis=0, keepdims=True)
        return grad_output @ self.W.T

class ReLU(Layer):
    def forward(self, x):
        self.mask = (x > 0)
        return x * self.mask

    def backward(self, grad_output):
        return grad_output * self.mask

class Softmax(Layer):
    def forward(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.output = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self.output

    def backward(self, y_true):
        # Combined with cross-entropy loss
        return (self.output - y_true) / y_true.shape[0]

# Network
layers = [
    Linear(784, 256),
    ReLU(),
    Linear(256, 10),
    Softmax()
]

# Forward
x = input_data
for layer in layers:
    x = layer.forward(x)

# Backward
grad = layers[-1].backward(y_true)
for layer in reversed(layers[:-1]):
    grad = layer.backward(grad)

# Update
for layer in layers:
    if hasattr(layer, 'grad_W'):
        layer.W -= lr * layer.grad_W
        layer.b -= lr * layer.grad_b
```

---

## Gradient Checking

Verify gradients numerically:

```python
def gradient_check(f, x, analytic_grad, epsilon=1e-5):
    """
    f: function that computes loss
    x: parameters
    analytic_grad: gradient from backprop
    """
    numeric_grad = np.zeros_like(x)

    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += epsilon
        x_minus = x.copy()
        x_minus[i] -= epsilon

        numeric_grad[i] = (f(x_plus) - f(x_minus)) / (2 * epsilon)

    # Compare
    diff = np.linalg.norm(numeric_grad - analytic_grad)
    diff /= np.linalg.norm(numeric_grad) + np.linalg.norm(analytic_grad)

    print(f"Relative difference: {diff}")
    # Should be < 1e-5 for correct implementation
```

---

## Exercises

1. **Derive**: Work out backprop for 2-layer network with ReLU by hand
2. **Implement**: Build computational graph with automatic differentiation
3. **Debug**: Implement gradient checking for your MLP
4. **Visualize**: Plot gradient magnitudes per layer during training
5. **Experiment**: Compare training with/without gradient clipping

---

## Key Takeaways

- Backpropagation uses chain rule to compute gradients efficiently
- Forward pass: compute and cache intermediate values
- Backward pass: propagate gradients from loss to inputs
- Vanishing/exploding gradients are key challenges
- Modern frameworks handle this automatically (autograd)

---

## Next Steps

→ Continue to [03-activation-functions.md](./03-activation-functions.md)
