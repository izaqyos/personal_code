# Gradient Descent

> The optimization algorithm that powers machine learning.

---

## Overview

Gradient descent iteratively adjusts parameters to minimize a cost function by moving in the direction of steepest descent.

```
Cost J(θ)
    │
    │\
    │ \    Start here
    │  \   ↓
    │   ○───→───→───○  ← Minimum
    │                 \
    │                  \
    └────────────────────── θ

Update rule:
θ := θ - α × ∇J(θ)

Where:
- θ: parameters (weights)
- α: learning rate
- ∇J(θ): gradient (direction of steepest ascent)
```

---

## Intuition

Imagine rolling a ball down a hill:
- Ball naturally moves toward lowest point
- Gradient tells us which direction is "downhill"
- Learning rate controls step size

```
3D Loss Surface:

        Start ○
              \
    ______     \___
   /      \       ○ Local minimum
  /        \_____/
 /                \
/         ○        \
      Global minimum
```

---

## Types of Gradient Descent

### Batch Gradient Descent

Use entire dataset for each update:

```
for epoch in range(n_epochs):
    gradient = compute_gradient(X, y)  # All data
    θ = θ - α × gradient

Pros: Stable, converges smoothly
Cons: Slow for large datasets, memory-intensive
```

### Stochastic Gradient Descent (SGD)

Use one sample per update:

```
for epoch in range(n_epochs):
    shuffle(X, y)
    for i in range(n_samples):
        gradient = compute_gradient(X[i], y[i])  # Single sample
        θ = θ - α × gradient

Pros: Fast updates, can escape local minima
Cons: Noisy, may not converge smoothly
```

### Mini-batch Gradient Descent

Use small batches (best of both worlds):

```
for epoch in range(n_epochs):
    shuffle(X, y)
    for batch in batches(X, y, batch_size):
        gradient = compute_gradient(batch)  # Batch of 32-256
        θ = θ - α × gradient

Pros: Balance of stability and speed
Cons: Requires tuning batch size
```

```
Convergence comparison:

Batch:          SGD:            Mini-batch:
  ↘               ↙↘↗↘           ↘
    ↘           ↙    ↘↗          ↘ ↘
      ↘       ↙        ↘        ↘    ↘
        ↘   ↙            ○         ↘   ○
          ○
 Smooth       Noisy            Balanced
```

---

## Learning Rate

The most critical hyperparameter:

```
α too small:              α too large:           α just right:
    │\                        │    /              │\
    │ \                       │  /  \             │ \
    │  \                      │/    /             │  \
    │   ○─○─○─○              │  \ /               │   ○───○
    │                        │   ×                │       ↓
    └────────────            └────────            └──────○
    Very slow                Diverges!             Converges
```

### Learning Rate Schedules

Decay learning rate over time:

```python
# Step decay
α = α₀ × drop^floor(epoch / epochs_drop)

# Exponential decay
α = α₀ × e^(-kt)

# 1/t decay
α = α₀ / (1 + k×t)

# Cosine annealing
α = α_min + 0.5 × (α_max - α_min) × (1 + cos(πt/T))
```

---

## Momentum

Accelerate convergence by accumulating velocity:

```
Standard GD:               With Momentum:
  ↓                          ↓↓
  ↓                           ↓↓↓
  ↓                            ↓↓↓↓
  ↓                             →→→→→
  (slow in valleys)           (builds up speed)

Update rule:
v = β × v + α × ∇J(θ)    # β typically 0.9
θ = θ - v

Like a ball with momentum rolling downhill
```

---

## Advanced Optimizers

### RMSprop

Adapt learning rate per parameter:

```
cache = β × cache + (1-β) × gradient²
θ = θ - α × gradient / (√cache + ε)

- Parameters with large gradients get smaller updates
- Parameters with small gradients get larger updates
```

### Adam (Adaptive Moment Estimation)

Combines momentum + RMSprop:

```python
# Most popular optimizer
m = β₁ × m + (1-β₁) × gradient      # Momentum
v = β₂ × v + (1-β₂) × gradient²     # RMSprop

# Bias correction
m_hat = m / (1 - β₁^t)
v_hat = v / (1 - β₂^t)

θ = θ - α × m_hat / (√v_hat + ε)

Default: β₁=0.9, β₂=0.999, ε=1e-8
```

### Optimizer Comparison

| Optimizer | Pros | Cons |
|-----------|------|------|
| SGD | Simple, generalizes well | Slow, sensitive to LR |
| SGD+Momentum | Faster, smoother | Extra hyperparameter |
| RMSprop | Adaptive LR | May not converge |
| Adam | Fast, adaptive | May not generalize as well |
| AdamW | Adam + weight decay | Most popular default |

---

## Implementation

### From Scratch

```python
import numpy as np

class SGD:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocity = None

    def update(self, params, grads):
        if self.velocity is None:
            self.velocity = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            self.velocity[i] = self.momentum * self.velocity[i] + self.lr * g
            p -= self.velocity[i]

        return params


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = None
        self.v = None
        self.t = 0

    def update(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]

        self.t += 1

        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g**2

            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)

            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

        return params
```

### Using PyTorch

```python
import torch.optim as optim

# SGD with momentum
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Adam
optimizer = optim.Adam(model.parameters(), lr=0.001)

# AdamW (Adam with decoupled weight decay)
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# Training loop
for epoch in range(n_epochs):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()       # Clear gradients
        output = model(batch_x)     # Forward pass
        loss = criterion(output, batch_y)
        loss.backward()             # Compute gradients
        optimizer.step()            # Update parameters
```

---

## Common Issues and Solutions

### Problem: Vanishing/Exploding Gradients

```
Solution:
- Gradient clipping: clip gradients to max norm
- Better initialization (Xavier, He)
- Batch normalization
- Residual connections
```

### Problem: Stuck in Local Minima/Saddle Points

```
Solution:
- Momentum helps escape saddle points
- Learning rate warmup
- Stochastic noise (SGD naturally has this)
```

### Problem: Oscillation

```
Solution:
- Reduce learning rate
- Add momentum
- Use adaptive optimizers (Adam)
```

---

## Exercises

1. **Implement**: Code SGD, momentum, and Adam from scratch
2. **Visualize**: Plot optimization paths on a 2D loss surface (e.g., Rosenbrock)
3. **Compare**: Train same model with different optimizers. Plot loss curves
4. **Tune**: Grid search learning rates. What's the optimal range?
5. **Schedule**: Implement cosine annealing. Does it improve final accuracy?

---

## Key Takeaways

- Gradient descent minimizes loss by following the negative gradient
- Mini-batch SGD balances speed and stability
- Learning rate is the most important hyperparameter
- Momentum accelerates convergence
- Adam is a good default optimizer
- Learning rate schedules help fine-tune convergence

---

## Next Steps

→ Continue to [08-loss-functions.md](./08-loss-functions.md)
