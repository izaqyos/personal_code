# Multi-Head Attention

> Multiple attention mechanisms running in parallel to capture different relationships.

---

## Why Multiple Heads?

Single attention head learns one type of relationship. Multi-head attention learns many:

```
Single Head:                    Multi-Head (8 heads):
- One attention pattern         - Head 1: Subject-verb relationships
- Limited expressiveness        - Head 2: Adjective-noun pairs
                                - Head 3: Coreference (pronouns)
                                - Head 4: Positional patterns
                                - Head 5: Syntactic dependencies
                                - Head 6: Semantic similarity
                                - Head 7: Punctuation patterns
                                - Head 8: Long-range dependencies

Each head can specialize!
```

---

## Architecture

```
Input X
   │
   ├──────────────┬──────────────┬──────────────┐
   ↓              ↓              ↓              ↓
 Head 1        Head 2        Head 3    ...   Head h
   │              │              │              │
   └──────────────┴──────────────┴──────────────┘
                       │
                       ↓
                   Concat
                       │
                       ↓
                Linear (Wᵒ)
                       │
                       ↓
                   Output

Each head: Attention(XWqⁱ, XWkⁱ, XWvⁱ)
```

---

## Mathematical Formulation

```
MultiHead(Q, K, V) = Concat(head₁, head₂, ..., headₕ) × Wᵒ

where headᵢ = Attention(QWqⁱ, KWkⁱ, VWvⁱ)

Dimensions:
- Input: d_model (e.g., 768)
- Per head: d_k = d_v = d_model / h (e.g., 768/12 = 64)
- Wqⁱ, Wkⁱ: [d_model × d_k]
- Wvⁱ: [d_model × d_v]
- Concat: [d_v × h] = [d_model]
- Wᵒ: [d_model × d_model]

Total parameters ≈ same as single large head
But much more expressive!
```

---

## Typical Configurations

| Model | d_model | Heads | d_k = d_v |
|-------|---------|-------|-----------|
| BERT-base | 768 | 12 | 64 |
| BERT-large | 1024 | 16 | 64 |
| GPT-2 | 768 | 12 | 64 |
| GPT-3 | 12288 | 96 | 128 |
| GPT-4 | ~12000 | ~120 | ~100 |

---

## Step-by-Step Example

```
Input: [batch=1, seq_len=3, d_model=8]
Heads: h=2
d_k = d_v = 8/2 = 4

Step 1: Project to Q, K, V for each head

Head 1:
Q₁ = X × Wq¹ → [1, 3, 4]
K₁ = X × Wk¹ → [1, 3, 4]
V₁ = X × Wv¹ → [1, 3, 4]

Head 2:
Q₂ = X × Wq² → [1, 3, 4]
K₂ = X × Wk² → [1, 3, 4]
V₂ = X × Wv² → [1, 3, 4]

Step 2: Compute attention for each head

head₁ = Attention(Q₁, K₁, V₁) → [1, 3, 4]
head₂ = Attention(Q₂, K₂, V₂) → [1, 3, 4]

Step 3: Concatenate

concat = [head₁, head₂] → [1, 3, 8]

Step 4: Final projection

output = concat × Wᵒ → [1, 3, 8]
```

---

## Efficient Implementation

Instead of h separate linear layers, use one large one and reshape:

```
# Naive (slow):
heads = []
for i in range(h):
    q = X @ Wq[i]
    k = X @ Wk[i]
    v = X @ Wv[i]
    heads.append(attention(q, k, v))
output = concat(heads) @ Wo

# Efficient:
# Single linear, then reshape to separate heads
Q = X @ Wq  # [batch, seq, d_model]
Q = Q.reshape(batch, seq, h, d_k).transpose(1, 2)  # [batch, h, seq, d_k]

# Now attention is batched across heads!
```

---

## Implementation

### PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # Combined projections for efficiency
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        self.dropout = nn.Dropout(dropout)

    def split_heads(self, x, batch_size):
        """Split the last dimension into (num_heads, d_k)"""
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(1, 2)  # [batch, heads, seq, d_k]

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        # Linear projections
        Q = self.W_q(query)  # [batch, seq_q, d_model]
        K = self.W_k(key)
        V = self.W_v(value)

        # Split into heads
        Q = self.split_heads(Q, batch_size)  # [batch, heads, seq_q, d_k]
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)

        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        context = torch.matmul(attention_weights, V)

        # Concatenate heads
        context = context.transpose(1, 2).contiguous()
        context = context.view(batch_size, -1, self.d_model)

        # Final linear
        output = self.W_o(context)

        return output, attention_weights


# Usage
mha = MultiHeadAttention(d_model=512, num_heads=8)
x = torch.randn(2, 10, 512)  # [batch, seq, d_model]
output, weights = mha(x, x, x)  # Self-attention
print(output.shape)  # [2, 10, 512]
print(weights.shape)  # [2, 8, 10, 10]
```

### Using PyTorch Built-in

```python
import torch.nn as nn

# Built-in multi-head attention
mha = nn.MultiheadAttention(
    embed_dim=512,
    num_heads=8,
    dropout=0.1,
    batch_first=True  # Important!
)

# Self-attention
output, attention_weights = mha(x, x, x)

# With mask (e.g., causal)
seq_len = x.size(1)
causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
output, weights = mha(x, x, x, attn_mask=causal_mask)
```

---

## Attention Head Specialization

Research shows heads learn different patterns:

```
Head Type        Pattern Example
─────────────────────────────────────────────
Positional       Attend to previous/next token
Syntactic        Subject→Verb, Det→Noun
Rare words       Attend to infrequent tokens
Separator        Attend to [SEP], punctuation
BOS/EOS          Attend to sequence boundaries
Vertical         Attend to same position
Diagonal         Attention follows diagonal
Block diagonal   Attend within phrases

Some heads become "attention sinks" in LLMs:
- First token gets lots of attention (parking spot for unused attention)
```

---

## Visualizing Multi-Head Attention

```python
def visualize_multihead_attention(attention_weights, tokens, num_heads=4):
    """
    attention_weights: [batch, heads, seq_q, seq_kv]
    """
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, num_heads, figsize=(4*num_heads, 4))

    for h in range(num_heads):
        ax = axes[h]
        im = ax.imshow(attention_weights[0, h].detach().numpy(), cmap='Blues')
        ax.set_xticks(range(len(tokens)))
        ax.set_yticks(range(len(tokens)))
        ax.set_xticklabels(tokens, rotation=45)
        ax.set_yticklabels(tokens)
        ax.set_title(f'Head {h+1}')

    plt.tight_layout()
    plt.show()
```

---

## Exercises

1. **Implement**: Build multi-head attention from scratch
2. **Visualize**: Plot attention patterns for all heads, identify specializations
3. **Ablation**: Train model with 1, 4, 8, 16 heads. Compare performance
4. **Efficiency**: Compare naive vs batched implementation speed
5. **Pruning**: Which heads can be removed with minimal performance loss?

---

## Key Takeaways

- Multiple heads learn diverse attention patterns
- Each head operates on smaller dimensions (d_model / h)
- Total parameters similar to single-head attention
- Efficient implementation batches across heads
- Heads specialize in different linguistic patterns
- Concatenation + projection combines all perspectives

---

## Next Steps

→ Continue to [05-positional-encoding.md](./05-positional-encoding.md)
