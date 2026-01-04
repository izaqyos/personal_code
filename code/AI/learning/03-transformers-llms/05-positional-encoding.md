# Positional Encoding

> How Transformers know word order without recurrence.

---

## The Problem

Self-attention is permutation invariant - order doesn't matter:

```
Attention("dog bites man") = Attention("man bites dog")

Without position info:
"The cat sat on the mat" and "mat the on sat cat The"
produce identical attention patterns!

We need to inject position information somehow.
```

---

## Solution: Add Position Information

```
Input:    token embeddings + position embeddings

x_final = Embedding(token) + PositionalEncoding(position)

Token:     [0.2, -0.1, 0.3, ...]   ← What word
Position:  [0.1,  0.2, 0.0, ...]   ← Where in sequence
─────────────────────────────────
Sum:       [0.3,  0.1, 0.3, ...]   ← Combined representation
```

---

## Sinusoidal Positional Encoding (Original Transformer)

Fixed mathematical function, no learned parameters:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

Where:
- pos: position in sequence (0, 1, 2, ...)
- i: dimension index (0, 1, ..., d_model/2 - 1)
- d_model: embedding dimension
```

### Visual Intuition

```
Position 0:  [sin(0), cos(0), sin(0), cos(0), ...]
Position 1:  [sin(1/10000^0), cos(1/10000^0), sin(1/10000^(2/d)), ...]
Position 2:  [sin(2/10000^0), cos(2/10000^0), sin(2/10000^(2/d)), ...]

Different dimensions oscillate at different frequencies:
Dim 0-1:    Fast oscillation  ∿∿∿∿∿∿∿∿
Dim 2-3:    Medium           ∿∿∿∿
Dim 4-5:    Slower          ∿∿
...
High dims:  Very slow       ∿

Like binary representation, but continuous!
Position in binary: 0, 1, 10, 11, 100, ...
Sinusoidal gives smooth interpolation
```

### Why This Works

```
Key property: PE(pos+k) can be represented as linear function of PE(pos)

[sin(pos+k)]   [cos(k)  sin(k)] [sin(pos)]
[cos(pos+k)] = [-sin(k) cos(k)] [cos(pos)]

Relative positions can be learned as linear transformations!
```

---

## Learned Positional Embeddings (BERT, GPT-2)

Simply learn an embedding for each position:

```python
# Learned positional embedding
position_embedding = nn.Embedding(max_seq_len, d_model)

positions = torch.arange(seq_len)  # [0, 1, 2, ..., seq_len-1]
pos_embed = position_embedding(positions)  # [seq_len, d_model]
```

### Comparison

| Method | Pros | Cons |
|--------|------|------|
| **Sinusoidal** | Extrapolates to longer sequences | Fixed, can't adapt |
| **Learned** | Adapts to data | Fixed max length |

---

## Rotary Position Embedding (RoPE)

Modern approach used in LLaMA, Mistral, etc.:

```
Instead of adding position, rotate the embedding vectors:

q_rotated = rotate(q, position)
k_rotated = rotate(k, position)

Attention: q_rotated · k_rotated = f(q, k, relative_position)

Key insight: Rotation preserves vector norms and makes
attention depend on RELATIVE position, not absolute!
```

### RoPE Mathematics

```
For 2D case:
      [cos(mθ)  -sin(mθ)] [q₁]
Rₘ = [sin(mθ)   cos(mθ)] [q₂]

Where m = position, θ = base angle

When computing attention:
(Rₘq) · (Rₙk) depends on (m-n), not m and n separately!
```

---

## ALiBi (Attention with Linear Biases)

Used in BLOOM and other models:

```
Instead of adding to embeddings, subtract from attention scores:

attention_score = q·k - m × |i-j|

Where:
- i, j: positions of query and key
- m: head-specific slope

Closer positions → higher scores
Further positions → penalized (but linearly, not cut off)
```

```
Example attention bias (one head):
        pos 0   pos 1   pos 2   pos 3
pos 0 [  0.0   -0.5    -1.0    -1.5  ]
pos 1 [ -0.5    0.0    -0.5    -1.0  ]
pos 2 [ -1.0   -0.5     0.0    -0.5  ]
pos 3 [ -1.5   -1.0    -0.5     0.0  ]
```

---

## Implementation

### Sinusoidal

```python
import torch
import math

class SinusoidalPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        # Create position encoding matrix
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()

        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)  # [1, max_len, d_model]
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x: [batch, seq_len, d_model]
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)
```

### Learned

```python
class LearnedPositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.position_embedding = nn.Embedding(max_len, d_model)

    def forward(self, x):
        # x: [batch, seq_len, d_model]
        seq_len = x.size(1)
        positions = torch.arange(seq_len, device=x.device)
        pos_embed = self.position_embedding(positions)
        return self.dropout(x + pos_embed)
```

### RoPE

```python
class RotaryPositionalEncoding(nn.Module):
    def __init__(self, dim, max_seq_len=2048, base=10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer('inv_freq', inv_freq)

        t = torch.arange(max_seq_len)
        freqs = torch.einsum('i,j->ij', t, inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer('cos', emb.cos())
        self.register_buffer('sin', emb.sin())

    def rotate_half(self, x):
        x1, x2 = x[..., :x.shape[-1]//2], x[..., x.shape[-1]//2:]
        return torch.cat((-x2, x1), dim=-1)

    def forward(self, q, k, seq_len):
        cos = self.cos[:seq_len]
        sin = self.sin[:seq_len]

        q_embed = (q * cos) + (self.rotate_half(q) * sin)
        k_embed = (k * cos) + (self.rotate_half(k) * sin)

        return q_embed, k_embed
```

---

## Visualizing Positional Encodings

```python
import matplotlib.pyplot as plt

def visualize_positional_encoding(pe, max_pos=100):
    """
    pe: [max_len, d_model]
    """
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(pe[:max_pos, :64].numpy(), aspect='auto', cmap='RdBu')
    plt.xlabel('Dimension')
    plt.ylabel('Position')
    plt.title('Positional Encoding (first 64 dims)')
    plt.colorbar()

    plt.subplot(1, 2, 2)
    for i in [0, 1, 2, 3]:
        plt.plot(pe[:max_pos, i].numpy(), label=f'dim {i}')
    plt.xlabel('Position')
    plt.ylabel('Value')
    plt.title('First 4 dimensions')
    plt.legend()

    plt.tight_layout()
    plt.show()
```

---

## Exercises

1. **Implement**: All three types of positional encoding from scratch
2. **Visualize**: Plot sinusoidal encodings, verify frequency patterns
3. **Extrapolation**: Test sinusoidal vs learned on sequences longer than training
4. **RoPE**: Verify that RoPE attention depends only on relative position
5. **Compare**: Train same model with different encodings, compare performance

---

## Key Takeaways

- Transformers need explicit position information
- Sinusoidal: mathematical, extrapolates, no learning
- Learned: flexible, limited to max length
- RoPE: rotates embeddings, captures relative position
- ALiBi: linear bias in attention, good extrapolation
- Choice depends on use case and required sequence length

---

## Next Steps

→ Continue to [06-transformer-architecture.md](./06-transformer-architecture.md)
