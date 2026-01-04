# Transformer Architecture

> The complete architecture that revolutionized NLP and beyond.

---

## Overview

The Transformer uses stacked self-attention layers without recurrence:

```
                    ┌─────────────────────────────────────┐
                    │           TRANSFORMER               │
                    │                                     │
   Input ─────────→│   ENCODER          DECODER         │─────→ Output
                    │   ┌─────┐          ┌─────┐         │
                    │   │Block│×N        │Block│×N       │
                    │   └─────┘          └─────┘         │
                    │                                     │
                    └─────────────────────────────────────┘

Original paper: "Attention Is All You Need" (Vaswani et al., 2017)
```

---

## Encoder Block

```
                    ┌────────────────────────────┐
      Input ───────→│                            │
                    │   Multi-Head Self-Attention│
                    │             │               │
      ┌─────────────│─────────────┴──────────────│
      │             │         Add & Norm          │
      │             │             │               │
      │             │      Feed-Forward          │
      │             │             │               │
      └─────────────│─────────────┴──────────────│
                    │         Add & Norm          │
                    │             │               │
                    └─────────────┼───────────────┘
                                  ↓
                              Output

Each operation has a residual connection and layer norm
```

### Components

```
1. Multi-Head Self-Attention
   - Each position attends to all positions
   - Captures relationships between tokens

2. Position-wise Feed-Forward Network
   FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
   - Applied to each position separately
   - Typically: d_model → 4×d_model → d_model
   - Adds non-linearity

3. Add & Norm (Residual + LayerNorm)
   LayerNorm(x + Sublayer(x))
   - Residual: Helps gradients flow
   - LayerNorm: Stabilizes training
```

---

## Decoder Block

```
                    ┌────────────────────────────┐
      Input ───────→│                            │
                    │ Masked Self-Attention      │  ← Can't see future
                    │             │               │
                    │         Add & Norm          │
                    │             │               │
Encoder output ────→│ Cross-Attention            │  ← Attends to encoder
                    │             │               │
                    │         Add & Norm          │
                    │             │               │
                    │      Feed-Forward          │
                    │             │               │
                    │         Add & Norm          │
                    │             │               │
                    └─────────────┼───────────────┘
                                  ↓
                              Output
```

### Key Differences from Encoder

```
1. Masked Self-Attention
   - Causal mask prevents seeing future tokens
   - Enables autoregressive generation

2. Cross-Attention
   - Q from decoder, K/V from encoder
   - Allows decoder to use encoder representations
```

---

## Complete Architecture

```
INPUT                                              OUTPUT
  │                                                  │
  ↓                                                  ↓
┌─────────────────┐                      ┌─────────────────┐
│ Input Embedding │                      │Output Embedding │
│       +         │                      │       +         │
│ Pos Encoding    │                      │ Pos Encoding    │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
         ↓                                        ↓
┌─────────────────┐                      ┌─────────────────┐
│                 │                      │                 │
│   Encoder ×N    │────────────────────→│   Decoder ×N    │
│                 │    (K, V)            │                 │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
         ↓                                        ↓
    (optional)                           ┌─────────────────┐
                                         │     Linear      │
                                         │     Softmax     │
                                         └────────┬────────┘
                                                  │
                                                  ↓
                                            Probabilities

Original configuration:
- N = 6 layers (encoder and decoder)
- d_model = 512
- h = 8 heads
- d_ff = 2048 (feed-forward inner dimension)
```

---

## Encoder-Only (BERT)

```
Just the encoder stack:

Input → Embedding → [Encoder Block] × N → Representations

Use cases:
- Classification (use [CLS] token)
- Named Entity Recognition
- Sentence embeddings

Models: BERT, RoBERTa, ALBERT, DistilBERT
```

---

## Decoder-Only (GPT)

```
Just the decoder stack (without cross-attention):

Input → Embedding → [Decoder Block] × N → Next Token Prediction

Always autoregressive (masked self-attention)

Use cases:
- Text generation
- Chat/dialogue
- Code completion

Models: GPT-2, GPT-3, GPT-4, LLaMA, Mistral
```

---

## Encoder-Decoder (T5, BART)

```
Full architecture for sequence-to-sequence:

Input → Encoder → Representations
                         ↓
Output → Decoder → Generation (cross-attending to encoder)

Use cases:
- Translation
- Summarization
- Question answering

Models: T5, BART, mT5, FLAN-T5
```

---

## Implementation

### Complete Transformer Block

```python
import torch
import torch.nn as nn
import math

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()

        # Multi-head attention
        self.attention = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )

        # Feed-forward network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )

        # Layer norms
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Self-attention with residual
        attn_out, _ = self.attention(x, x, x, attn_mask=mask)
        x = self.norm1(x + self.dropout(attn_out))

        # FFN with residual
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)

        return x


class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model=512, num_heads=8,
                 num_layers=6, d_ff=2048, max_len=512, dropout=0.1):
        super().__init__()

        self.d_model = d_model

        # Embeddings
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])

        # Output
        self.norm = nn.LayerNorm(d_model)
        self.output = nn.Linear(d_model, vocab_size)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch_size, seq_len = x.shape

        # Embeddings
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
        x = self.token_embedding(x) * math.sqrt(self.d_model)
        x = x + self.position_embedding(positions)
        x = self.dropout(x)

        # Transformer blocks
        for block in self.blocks:
            x = block(x, mask)

        x = self.norm(x)
        logits = self.output(x)

        return logits


# Usage
model = Transformer(
    vocab_size=50000,
    d_model=512,
    num_heads=8,
    num_layers=6,
    d_ff=2048
)

# Input tokens
tokens = torch.randint(0, 50000, (2, 100))  # [batch, seq]

# Causal mask for decoder
seq_len = tokens.size(1)
causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()

# Forward pass
logits = model(tokens, mask=causal_mask)  # [batch, seq, vocab]
```

---

## Pre-Norm vs Post-Norm

```
Original (Post-Norm):           Modern (Pre-Norm):
x → Sublayer → Add → Norm      x → Norm → Sublayer → Add
    ↑________________|              ↑_______________|

Pre-norm is more stable for deep models
Used in GPT-2+, LLaMA, etc.
```

```python
# Pre-norm implementation
def forward(self, x):
    x = x + self.attention(self.norm1(x))
    x = x + self.ffn(self.norm2(x))
    return x
```

---

## Training Details

```
Optimizer: Adam with warmup
- β₁ = 0.9, β₂ = 0.98, ε = 10⁻⁹

Learning rate schedule:
lr = d_model^(-0.5) × min(step^(-0.5), step × warmup^(-1.5))

Label smoothing: 0.1

Dropout: 0.1 (attention, FFN, embeddings)

Batch size: Large (thousands of tokens per batch)
```

---

## Exercises

1. **Implement**: Build full encoder-decoder Transformer from scratch
2. **Compare**: Train encoder-only vs decoder-only on classification
3. **Ablation**: Remove components (residuals, LayerNorm) and observe effects
4. **Scale**: Train models with 2, 4, 8, 12 layers. Plot validation loss
5. **Visualize**: Plot attention patterns across all layers and heads

---

## Key Takeaways

- Transformer = Self-Attention + FFN + Residuals + LayerNorm
- Encoder: bidirectional, good for understanding
- Decoder: autoregressive, good for generation
- Encoder-Decoder: sequence-to-sequence tasks
- Pre-norm is more stable than post-norm
- The architecture scales extremely well

---

## Next Steps

→ Continue to [07-residual-connections.md](./07-residual-connections.md)
