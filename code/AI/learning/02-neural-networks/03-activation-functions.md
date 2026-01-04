# Activation Functions

> Non-linear functions that give neural networks their power.

---

## Why Activation Functions?

Without non-linearity, stacked layers collapse to a single linear transformation:

```
Without activation:
z₁ = W₁x + b₁
z₂ = W₂z₁ + b₂ = W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂)
                                    = W'x + b'  ← Still linear!

With activation:
a₁ = f(W₁x + b₁)
a₂ = f(W₂a₁ + b₂)  ← Non-linear! Can approximate any function
```

---

## Activation Function Zoo

### Sigmoid

```
σ(z) = 1 / (1 + e⁻ᶻ)

Range: (0, 1)
Derivative: σ(z)(1 - σ(z))

         1 ────────────○○○○
           │         ○○
       0.5 │- - - -○- - - - -
           │      ○○
         0 ○○○○○○────────────
          -6    0    6
```

| Pros | Cons |
|------|------|
| Smooth gradient | Vanishing gradient (saturates) |
| Output in (0,1) | Not zero-centered |
| Probabilistic interpretation | Computationally expensive (exp) |

**Use case**: Output layer for binary classification

### Tanh

```
tanh(z) = (eᶻ - e⁻ᶻ) / (eᶻ + e⁻ᶻ) = 2σ(2z) - 1

Range: (-1, 1)
Derivative: 1 - tanh²(z)

         1 ────────────○○○○
           │         ○○
         0 │- - - -○- - - - -
           │      ○○
        -1 ○○○○○○────────────
          -6    0    6
```

| Pros | Cons |
|------|------|
| Zero-centered | Still saturates |
| Stronger gradients than sigmoid | Vanishing gradient |

**Use case**: Hidden layers (before ReLU era), RNNs

### ReLU (Rectified Linear Unit)

```
ReLU(z) = max(0, z)

Range: [0, ∞)
Derivative: 1 if z > 0, else 0

           │      ○
           │    ○○
           │  ○○
         0 ○○○────────
          -2  0  2
```

| Pros | Cons |
|------|------|
| No vanishing gradient (for z>0) | Dead neurons (z<0 always) |
| Computationally efficient | Not zero-centered |
| Sparse activation | Unbounded (can explode) |

**Use case**: Default for hidden layers in most networks

### Leaky ReLU

```
LeakyReLU(z) = max(αz, z)   where α ≈ 0.01

Range: (-∞, ∞)
Derivative: 1 if z > 0, else α

           │      ○
           │    ○○
         ○○○○○○────────
          -2  0  2
    (small negative slope)
```

**Fixes dead neuron problem** - always has gradient

### Parametric ReLU (PReLU)

Same as Leaky ReLU but α is learnable:
```python
PReLU(z) = max(αz, z)  # α learned during training
```

### ELU (Exponential Linear Unit)

```
ELU(z) = z if z > 0, else α(eᶻ - 1)

Range: (-α, ∞)

           │      ○
           │    ○○
       ○○○○○○○────────
    -α ----
          -2  0  2
   (smooth negative part)
```

| Pros | Cons |
|------|------|
| No dead neurons | Computationally expensive |
| Smooth everywhere | |
| Closer to zero mean | |

### SELU (Scaled ELU)

Self-normalizing - maintains mean≈0, variance≈1:
```
SELU(z) = λ × ELU(z, α)
# λ ≈ 1.0507, α ≈ 1.6733 (specific values for self-normalization)
```

### GELU (Gaussian Error Linear Unit)

```
GELU(z) = z × Φ(z)   where Φ is CDF of standard normal

Approximation: 0.5z(1 + tanh(√(2/π)(z + 0.044715z³)))
```

**Smooth version of ReLU** - used in Transformers (BERT, GPT)

### Swish / SiLU

```
Swish(z) = z × σ(z) = z × sigmoid(z)

Self-gated activation - smooth, non-monotonic
```

**Use case**: Modern CNNs, efficient networks

### Softmax

For multi-class output (converts logits to probabilities):

```
softmax(zᵢ) = eᶻⁱ / Σⱼeᶻʲ

Properties:
- Output sums to 1
- All outputs in (0, 1)
- Preserves ranking

Example:
z = [2.0, 1.0, 0.1]
softmax(z) = [0.659, 0.242, 0.099]
```

---

## Comparison Chart

```
                  Sigmoid    Tanh      ReLU     Leaky    GELU
Range             (0,1)     (-1,1)    [0,∞)    (-∞,∞)   (-0.17,∞)
Zero-centered     No        Yes       No       ~Yes     ~Yes
Saturates         Yes       Yes       No       No       No
Dead neurons      -         -         Yes      No       No
Computation       Slow      Slow      Fast     Fast     Medium
Modern use        Output    RNN       Default  Common   Transformers
```

---

## Implementation

```python
import numpy as np
import torch
import torch.nn as nn

# NumPy implementations
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def tanh(z):
    return np.tanh(z)

def relu(z):
    return np.maximum(0, z)

def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

def elu(z, alpha=1.0):
    return np.where(z > 0, z, alpha * (np.exp(z) - 1))

def gelu(z):
    return 0.5 * z * (1 + np.tanh(np.sqrt(2/np.pi) * (z + 0.044715 * z**3)))

def swish(z):
    return z * sigmoid(z)

def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=-1, keepdims=True)


# PyTorch
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)

        # Activation options
        self.relu = nn.ReLU()
        self.leaky_relu = nn.LeakyReLU(0.01)
        self.elu = nn.ELU()
        self.gelu = nn.GELU()
        self.silu = nn.SiLU()  # Swish

    def forward(self, x):
        x = self.gelu(self.fc1(x))
        x = self.gelu(self.fc2(x))
        x = self.fc3(x)  # No activation, use CrossEntropyLoss
        return x
```

---

## Choosing Activation Functions

```
┌─────────────────────────────────────────────────────────────┐
│                    Decision Guide                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Hidden Layers:                                              │
│  ├── Default choice ──────────────────── ReLU               │
│  ├── If dead neurons are problem ──────── Leaky ReLU / ELU  │
│  ├── Transformer architectures ────────── GELU              │
│  └── Self-normalizing networks ────────── SELU              │
│                                                              │
│  Output Layer:                                               │
│  ├── Binary classification ────────────── Sigmoid           │
│  ├── Multi-class classification ───────── Softmax           │
│  ├── Regression (unbounded) ───────────── None (linear)     │
│  └── Regression (bounded [0,1]) ───────── Sigmoid           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Exercises

1. **Visualize**: Plot all activation functions and their derivatives
2. **Compare**: Train MNIST with ReLU vs Leaky ReLU vs GELU. Compare convergence
3. **Dead neurons**: Create scenario where ReLU neurons die, show Leaky ReLU fixes it
4. **Implement**: Write GELU from scratch, verify against PyTorch
5. **Explore**: Why does GELU work well for Transformers? Research and explain

---

## Key Takeaways

- Activation functions introduce non-linearity (essential!)
- ReLU is the default for hidden layers - fast and effective
- Leaky ReLU/ELU fix the dead neuron problem
- GELU is preferred for Transformers
- Sigmoid/softmax for output layers (probabilities)
- Match activation to your architecture and problem

---

## Next Steps

→ Continue to [04-cnns.md](./04-cnns.md)
