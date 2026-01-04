# Attention Mechanism

> The core innovation that enables Transformers to process sequences effectively.

---

## Overview

Attention allows models to focus on relevant parts of the input when producing each output.

```
Input:  "The cat sat on the mat"
Query:  "What sat?"

Without attention: Process left-to-right, hope context is remembered
With attention:    Directly attend to "cat" when answering

         "The"  "cat"  "sat"  "on"  "the"  "mat"
           ↓     ↓↓↓    ↓      ↓      ↓      ↓
Weights:  0.05  0.70  0.15   0.03   0.02   0.05
                 ↑↑↑
           Most attention on "cat"
```

---

## Intuition: Query, Key, Value

Think of attention like a search engine:

```
Query (Q): What am I looking for?
Keys (K):  Labels on each item (what does each item contain?)
Values (V): The actual content of each item

Process:
1. Compare query to all keys (how relevant is each item?)
2. Get attention weights (probability distribution)
3. Weighted sum of values (aggregate relevant content)

Example - Answering "Who sat?":
Query:  "Who sat?" → vector q
Keys:   ["The", "cat", "sat", ...] → vectors k₁, k₂, k₃, ...
Values: [embed(The), embed(cat), embed(sat), ...] → v₁, v₂, v₃, ...

Similarity: q·k₂ is high (cat is relevant to "who")
Output: Mainly v₂ (cat's representation)
```

---

## Scaled Dot-Product Attention

The fundamental attention operation:

```
                    ┌─────────────────┐
                    │   MatMul(Q, Kᵀ) │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Scale (÷√dₖ)  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     Softmax     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   MatMul(·, V)  │
                    └────────┬────────┘
                             ↓
                         Attention

Attention(Q, K, V) = softmax(QKᵀ / √dₖ) × V
```

### Why Scale by √dₖ?

```
When dₖ is large, dot products can be very large,
pushing softmax into saturation (gradients → 0)

Example:
dₖ = 64, q and k are random unit vectors
E[q·k] = 0, but Var[q·k] = dₖ = 64

Scaling: q·k / √64 = q·k / 8
Keeps variance ≈ 1, softmax stays in good range
```

---

## Step-by-Step Example

```
Input: ["I", "love", "cats"]
Embeddings (dim=4 for simplicity):
x₁ = [1, 0, 1, 0]  # "I"
x₂ = [0, 1, 1, 0]  # "love"
x₃ = [1, 1, 0, 1]  # "cats"

Weight matrices (learned):
Wq, Wk, Wv each 4×4

Step 1: Compute Q, K, V
Q = X × Wq  →  q₁, q₂, q₃  (each 1×4)
K = X × Wk  →  k₁, k₂, k₃
V = X × Wv  →  v₁, v₂, v₃

Step 2: Compute attention scores (Q × Kᵀ)
         k₁   k₂   k₃
    q₁ [ 2.1  1.3  0.8 ]
    q₂ [ 1.5  2.4  1.1 ]
    q₃ [ 0.9  1.2  2.3 ]

Step 3: Scale by √dₖ = √4 = 2
         k₁   k₂   k₃
    q₁ [ 1.05 0.65 0.40 ]
    q₂ [ 0.75 1.20 0.55 ]
    q₃ [ 0.45 0.60 1.15 ]

Step 4: Softmax (row-wise)
         k₁    k₂    k₃
    q₁ [ 0.47  0.31  0.22 ]
    q₂ [ 0.28  0.45  0.27 ]
    q₃ [ 0.23  0.27  0.50 ]

Step 5: Weighted sum of values
out₁ = 0.47×v₁ + 0.31×v₂ + 0.22×v₃
out₂ = 0.28×v₁ + 0.45×v₂ + 0.27×v₃
out₃ = 0.23×v₁ + 0.27×v₂ + 0.50×v₃
```

---

## Self-Attention

When Q, K, V all come from the same sequence:

```
Self-Attention: Each position attends to all positions (including itself)

"The cat sat on the mat"
     ↓
Every word can "look at" every other word

Attention for "sat":
- Attends to "cat" (subject)
- Attends to "mat" (prepositional phrase)
- Attends to "on" (connects them)
```

### Attention Patterns

```
Visualizing attention weights (for one head):

         The  cat  sat  on  the  mat
The     [███  ░░░  ░░░  ░░░  ░░░  ░░░]  # "The" attends to itself
cat     [░░░  ███  ░░░  ░░░  ░░░  ░░░]  # "cat" attends to itself
sat     [░░░  ███  ██░  ░░░  ░░░  ░░░]  # "sat" attends to "cat", "sat"
on      [░░░  ░░░  ██░  ███  ░░░  ░░░]  # "on" attends to "sat", "on"
the     [███  ░░░  ░░░  ░░░  ███  ░░░]  # "the" attends to "The", "the"
mat     [░░░  ░░░  ░░░  ███  ░░░  ███]  # "mat" attends to "on", "mat"

█ = high attention, ░ = low attention
```

---

## Cross-Attention

When Q comes from one sequence, K and V from another:

```
Machine Translation:

Encoder input:  "Je t'aime"  → K, V
Decoder query:  "I love ___" → Q

When generating "you":
Q from decoder position 3
K, V from encoder ("Je", "t'", "aime")
Attends heavily to "t'" (the "you" in French)
```

---

## Causal (Masked) Attention

For autoregressive models (GPT), prevent looking at future tokens:

```
Standard attention:          Causal attention:
         t₁  t₂  t₃  t₄           t₁  t₂  t₃  t₄
    t₁ [ ✓   ✓   ✓   ✓ ]     t₁ [ ✓   ✗   ✗   ✗ ]
    t₂ [ ✓   ✓   ✓   ✓ ]     t₂ [ ✓   ✓   ✗   ✗ ]
    t₃ [ ✓   ✓   ✓   ✓ ]     t₃ [ ✓   ✓   ✓   ✗ ]
    t₄ [ ✓   ✓   ✓   ✓ ]     t₄ [ ✓   ✓   ✓   ✓ ]

Implemented by setting masked positions to -∞ before softmax
softmax(-∞) = 0 → No attention to future positions
```

---

## Implementation

### NumPy

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: [batch, seq_len_q, d_k]
    K: [batch, seq_len_k, d_k]
    V: [batch, seq_len_k, d_v]
    mask: [batch, seq_len_q, seq_len_k]
    """
    d_k = K.shape[-1]

    # Compute attention scores
    scores = np.matmul(Q, K.transpose(0, 2, 1)) / np.sqrt(d_k)

    # Apply mask (for causal attention)
    if mask is not None:
        scores = np.where(mask, scores, -1e9)

    # Softmax
    attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)

    # Weighted sum
    output = np.matmul(attention_weights, V)

    return output, attention_weights
```

### PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k, dropout=0.1):
        super().__init__()
        self.d_k = d_k
        self.dropout = nn.Dropout(dropout)

    def forward(self, Q, K, V, mask=None):
        # Q, K, V: [batch, heads, seq_len, d_k]

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        output = torch.matmul(attention_weights, V)

        return output, attention_weights
```

---

## Visualizing Attention

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_attention(attention_weights, tokens_q, tokens_kv):
    """
    attention_weights: [seq_q, seq_kv]
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        attention_weights,
        xticklabels=tokens_kv,
        yticklabels=tokens_q,
        cmap='Blues',
        annot=True,
        fmt='.2f'
    )
    plt.xlabel('Keys')
    plt.ylabel('Queries')
    plt.title('Attention Weights')
    plt.show()
```

---

## Exercises

1. **Implement**: Build scaled dot-product attention from scratch
2. **Visualize**: Plot attention weights for a sentence, interpret patterns
3. **Masking**: Implement and verify causal masking works correctly
4. **Compare**: Self-attention vs Cross-attention on translation task
5. **Debug**: What happens if you forget to scale by √dₖ?

---

## Key Takeaways

- Attention computes weighted combinations based on relevance
- Query-Key-Value paradigm: query asks, keys answer, values provide content
- Scaling prevents softmax saturation
- Self-attention: sequence attends to itself
- Cross-attention: one sequence attends to another
- Causal masking enables autoregressive generation

---

## Next Steps

→ Continue to [04-multi-head-attention.md](./04-multi-head-attention.md)
