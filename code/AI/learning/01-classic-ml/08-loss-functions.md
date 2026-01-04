# Loss Functions

> How we measure model performance and guide optimization.

---

## Overview

Loss functions (also called cost functions or objective functions) quantify how wrong our predictions are. The goal of training is to minimize loss.

```
Input → Model → Prediction (ŷ) ─┐
                                ├─→ Loss → Optimize
Ground Truth (y) ──────────────┘
```

---

## Regression Loss Functions

### Mean Squared Error (MSE) / L2 Loss

```
MSE = (1/n) × Σ(yᵢ - ŷᵢ)²

Properties:
- Penalizes large errors heavily (quadratic)
- Differentiable everywhere
- Sensitive to outliers
- Units are squared
```

```
Error:  -3   -2   -1    0    1    2    3
MSE:     9    4    1    0    1    4    9
         ▃▃▃ ▂▂  ▁    ·    ▁  ▂▂ ▃▃▃
```

### Mean Absolute Error (MAE) / L1 Loss

```
MAE = (1/n) × Σ|yᵢ - ŷᵢ|

Properties:
- Linear penalty
- Robust to outliers
- Not differentiable at 0
- Same units as y
```

```
Error:  -3   -2   -1    0    1    2    3
MAE:     3    2    1    0    1    2    3
        ▃▃▃ ▂▂▂ ▁▁▁   ·   ▁▁▁ ▂▂▂ ▃▃▃
```

### Huber Loss (Smooth L1)

Best of both worlds:

```
         ⎧ 0.5 × (y - ŷ)²           if |y - ŷ| ≤ δ
Huber = ⎨
         ⎩ δ × |y - ŷ| - 0.5 × δ²   otherwise

- Quadratic near zero (smooth gradient)
- Linear for large errors (robust to outliers)
- δ controls transition point
```

```
        MSE (sensitive)    Huber           MAE (robust)
        │     /\           │   __/\__      │    /\
   Loss │   /    \         │  /      \     │   /  \
        │ /        \       │ /        \    │  /    \
        │/          \      │/          \   │ /      \
        └────────────      └────────────   └────────────
                               Error
```

### Comparison

```python
import numpy as np

y_true = np.array([1, 2, 3, 10])  # Note: 10 is outlier
y_pred = np.array([1.1, 2.2, 2.8, 3])

mse = np.mean((y_true - y_pred)**2)   # 12.3 (dominated by outlier)
mae = np.mean(np.abs(y_true - y_pred)) # 1.8 (more robust)
```

---

## Classification Loss Functions

### Binary Cross-Entropy (Log Loss)

```
BCE = -(1/n) × Σ[yᵢ log(p̂ᵢ) + (1-yᵢ) log(1-p̂ᵢ)]

Where:
- yᵢ ∈ {0, 1}: true label
- p̂ᵢ ∈ (0, 1): predicted probability

Properties:
- Heavily penalizes confident wrong predictions
- Requires probabilities, not raw scores
```

```
When y=1:                    When y=0:
Cost │                       Cost │
     │\                           │         /
     │ \                          │        /
     │  \__                       │    __/
     │     \_____                 │___/
     └──────────── p̂             └──────────── p̂
     0            1              0            1
  "Wrong! High cost"          "Wrong! High cost"
```

### Categorical Cross-Entropy

For multi-class classification:

```
CCE = -(1/n) × Σᵢ Σⱼ yᵢⱼ log(p̂ᵢⱼ)

Where:
- yᵢⱼ: one-hot encoded label (1 for true class, 0 otherwise)
- p̂ᵢⱼ: predicted probability for class j
- Sum over all classes j for each sample i
```

### Sparse Categorical Cross-Entropy

Same as CCE but takes integer labels instead of one-hot:

```python
# Categorical CE (one-hot labels)
y_true = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# Sparse Categorical CE (integer labels)
y_true = [0, 1, 2]  # Same meaning, less memory
```

### Hinge Loss (SVM)

```
Hinge = (1/n) × Σ max(0, 1 - yᵢ × ŷᵢ)

Where yᵢ ∈ {-1, +1}

Properties:
- Zero loss for correct predictions with margin ≥ 1
- Linear penalty for violations
- Basis of SVM
```

```
         │\
    Loss │ \
         │  \
         │   \______
         └──────────────── yᵢ × ŷᵢ
         0    1
       (margin)
```

---

## Specialized Loss Functions

### Focal Loss (Imbalanced Classification)

Down-weight easy examples, focus on hard ones:

```
FL = -α × (1 - p̂)^γ × log(p̂)   (for positive class)

γ = focusing parameter (typically 2)
- When p̂ is high (easy example): (1-p̂)^γ is small → low loss
- When p̂ is low (hard example): (1-p̂)^γ is large → high loss
```

### KL Divergence

Measure difference between probability distributions:

```
KL(P || Q) = Σ P(x) log(P(x) / Q(x))

Used in:
- VAEs
- Knowledge distillation
- Regularization
```

### Contrastive Loss (Metric Learning)

Pull similar pairs together, push dissimilar apart:

```
L = (1-y) × 0.5 × D² + y × 0.5 × max(0, margin - D)²

Where:
- y = 0 for similar pairs
- y = 1 for dissimilar pairs
- D = distance between embeddings
```

### Triplet Loss

Anchor, positive, negative triplets:

```
L = max(0, D(anchor, positive) - D(anchor, negative) + margin)

Goal: D(a,p) + margin < D(a,n)
```

---

## Loss Function Selection Guide

| Task | Loss Function | Notes |
|------|---------------|-------|
| Regression | MSE | Default, sensitive to outliers |
| Regression (outliers) | MAE or Huber | More robust |
| Binary Classification | Binary CE | Use with sigmoid |
| Multi-class | Categorical CE | Use with softmax |
| Imbalanced Classes | Focal Loss | Focus on hard examples |
| Ranking/Retrieval | Triplet Loss | Learn embeddings |
| SVM | Hinge Loss | Margin-based |

---

## Implementation

### NumPy

```python
import numpy as np

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred)**2)

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def binary_cross_entropy(y_true, y_pred, eps=1e-15):
    y_pred = np.clip(y_pred, eps, 1 - eps)  # Prevent log(0)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

def categorical_cross_entropy(y_true, y_pred, eps=1e-15):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
```

### PyTorch

```python
import torch.nn as nn

# Regression
mse_loss = nn.MSELoss()
mae_loss = nn.L1Loss()
huber_loss = nn.SmoothL1Loss()

# Classification (expects logits, applies softmax internally)
ce_loss = nn.CrossEntropyLoss()  # Combines LogSoftmax + NLLLoss

# Binary (expects logits)
bce_logits = nn.BCEWithLogitsLoss()

# Binary (expects probabilities)
bce = nn.BCELoss()

# Usage
loss = ce_loss(predictions, targets)
loss.backward()
```

---

## Exercises

1. **Compare**: Train regression with MSE vs MAE on data with outliers
2. **Implement**: Code focal loss from scratch
3. **Visualize**: Plot loss curves for BCE with different predicted probabilities
4. **Experiment**: Try different γ values for focal loss on imbalanced data
5. **Custom**: Design a loss function that penalizes underestimation more than overestimation

---

## Key Takeaways

- MSE penalizes large errors quadratically, MAE linearly
- Huber loss combines benefits of both
- Cross-entropy is standard for classification
- Focal loss helps with class imbalance
- Always match loss function to task requirements
- Numerical stability matters (clip predictions before log)

---

## Track Complete!

You've completed the Classic ML track. Next:
→ Continue to [02-neural-networks/01-perceptrons-basics.md](../02-neural-networks/01-perceptrons-basics.md)
