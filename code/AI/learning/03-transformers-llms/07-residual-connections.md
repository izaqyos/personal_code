# Residual Connections

> Skip connections that enable training of very deep networks.

---

## The Problem with Deep Networks

As networks get deeper, training becomes harder:

```
Layer 1 → Layer 2 → Layer 3 → ... → Layer 100

Problems:
1. Vanishing gradients: ∂L/∂W₁ → 0
2. Degradation: Adding layers makes accuracy WORSE
3. Optimization difficulty: Loss landscape becomes complex

Counterintuitive: Deeper network ≠ Better performance
```

---

## Residual Learning

Key insight from ResNet (2015): Learn the residual, not the full transformation.

```
Standard:           Residual:
x → F(x)            x → F(x) + x
                          ↓
                    Learn F(x) = H(x) - x
                    Instead of H(x) directly

If identity is optimal, F(x) can just become 0!
```

### Visual Comparison

```
Standard Block:                 Residual Block:
     │                              │
     ↓                              │
  ┌─────┐                          │
  │ F(x)│                          │
  └──┬──┘                    ┌─────┴─────┐
     │                       │           │
     ↓                       ↓           │
  output                  ┌─────┐        │
                          │ F(x)│        │
                          └──┬──┘        │
                             │           │
                             ↓           │
                           ┌─┴─┐         │
                           │ + │←────────┘
                           └─┬─┘
                             │
                             ↓
                          output
```

---

## Why Residuals Work

### 1. Gradient Flow

```
Without residual:
∂L/∂x = ∂L/∂F(x) × ∂F(x)/∂x

Chain of products can vanish!

With residual:
y = F(x) + x
∂L/∂x = ∂L/∂y × (∂F(x)/∂x + 1)
                          ↑
                    Always at least 1!

Gradient has a "highway" to flow backward
```

### 2. Ensemble Effect

```
Residual networks can be viewed as ensembles:

Layer outputs:
y₁ = F₁(x) + x
y₂ = F₂(y₁) + y₁ = F₂(F₁(x) + x) + F₁(x) + x

Expanding: exponentially many paths!

   x
   ├── F₁(x)
   ├── x (skip)
   │    ├── F₂(F₁(x) + x)
   │    └── F₁(x) + x (skip)
   ...

Like averaging many shallow networks
```

### 3. Identity Baseline

```
If identity is optimal (no transformation needed):
- Standard network must learn complex identity mapping
- Residual network just sets F(x) ≈ 0

Much easier to learn "do nothing" with residuals!
```

---

## Residual Connection in Transformers

```
In each Transformer block:

1. Self-Attention with residual:
   x = x + Attention(x)

2. FFN with residual:
   x = x + FFN(x)

Information can flow through many layers unchanged,
while each layer adds its contribution.
```

### With Layer Normalization

```
Post-norm (original):           Pre-norm (modern):
x₁ = LayerNorm(x + Attn(x))    x₁ = x + Attn(LayerNorm(x))
x₂ = LayerNorm(x₁ + FFN(x₁))   x₂ = x₁ + FFN(LayerNorm(x₁))

Pre-norm puts identity path OUTSIDE normalization:
- Cleaner gradient flow
- More stable training
- Used in GPT-2+, LLaMA
```

---

## Implementation

### Basic Residual Block

```python
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return x + self.ffn(x)  # Residual connection
```

### Pre-norm Transformer Block

```python
class PreNormTransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()

        self.attn = nn.MultiheadAttention(d_model, num_heads, dropout, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        # Pre-norm: normalize before sublayer
        normed = self.norm1(x)
        attn_out, _ = self.attn(normed, normed, normed, attn_mask=mask)
        x = x + attn_out  # Residual

        normed = self.norm2(x)
        x = x + self.ffn(normed)  # Residual

        return x
```

### Deep Network with Residuals

```python
class DeepResidualNetwork(nn.Module):
    def __init__(self, d_model, d_ff, num_layers, dropout=0.1):
        super().__init__()

        self.layers = nn.ModuleList([
            ResidualBlock(d_model, d_ff, dropout)
            for _ in range(num_layers)
        ])

        self.norm = nn.LayerNorm(d_model)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return self.norm(x)

# Can train 100+ layers!
model = DeepResidualNetwork(d_model=512, d_ff=2048, num_layers=100)
```

---

## Scaling Factor

For very deep networks, scale residual contributions:

```python
class ScaledResidualBlock(nn.Module):
    def __init__(self, d_model, d_ff, num_layers, dropout=0.1):
        super().__init__()
        self.ffn = nn.Sequential(...)

        # Scale by 1/√num_layers (DeepNorm style)
        self.scale = 1.0 / math.sqrt(num_layers)

    def forward(self, x):
        return x + self.scale * self.ffn(x)
```

---

## Residual Stream View

Modern interpretation: residual stream as shared memory

```
         Token 1    Token 2    Token 3
            │          │          │
    x₀ ─────┼──────────┼──────────┼───── Initial embeddings
            │          │          │
Layer 1     │←─────────│←─────────│ Read from stream
reads →    [Attention reads, writes back]
writes →    │──────────│──────────│ Add to stream
            │          │          │
Layer 2     │←─────────│←─────────│
reads →    [FFN reads, writes back]
writes →    │──────────│──────────│
            │          │          │
    ...    │          │          │
            │          │          │
   Final    ↓          ↓          ↓
           out₁       out₂       out₃

Each layer reads from and writes to a "residual stream"
All layers have access to original + all previous contributions
```

---

## Exercises

1. **Ablation**: Train models with and without residuals. Compare gradient norms
2. **Depth**: Train 10, 50, 100 layer networks. How deep can you go with residuals?
3. **Scaling**: Experiment with different residual scaling factors
4. **Visualize**: Plot activation magnitudes through layers with/without residuals
5. **Pre vs Post**: Compare pre-norm vs post-norm training stability

---

## Key Takeaways

- Residuals add identity shortcut: y = F(x) + x
- Enable gradient flow in very deep networks
- Make "do nothing" easy to learn (just set F(x) ≈ 0)
- Create ensemble-like behavior (exponential paths)
- Pre-norm is more stable than post-norm
- "Residual stream" interpretation: shared memory across layers

---

## Next Steps

→ Continue to [08-llm-layers.md](./08-llm-layers.md)
