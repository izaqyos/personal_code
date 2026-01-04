# LLM Layers and Architecture

> The complete anatomy of modern Large Language Models.

---

## Overview

Modern LLMs (GPT-4, Claude, LLaMA, etc.) are decoder-only Transformers with specific architectural choices:

```
┌─────────────────────────────────────────────────────┐
│                    LLM Architecture                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Input IDs → Token Embedding                        │
│              + Positional Encoding (RoPE)           │
│                      ↓                              │
│  ┌─────────────────────────────────────────────┐   │
│  │            Decoder Block (×N)                │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │ RMSNorm                               │  │   │
│  │  │ Grouped Query Attention (Causal)      │  │   │
│  │  │ + Residual                            │  │   │
│  │  ├───────────────────────────────────────┤  │   │
│  │  │ RMSNorm                               │  │   │
│  │  │ SwiGLU Feed-Forward                   │  │   │
│  │  │ + Residual                            │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
│                      ↓                              │
│  RMSNorm                                            │
│  Linear → Logits                                    │
│                      ↓                              │
│  Output: Next Token Probabilities                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Layer-by-Layer Breakdown

### 1. Token Embedding Layer

```python
class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)

    def forward(self, x):
        return self.embedding(x)

# Typical sizes:
# vocab_size: 32k-100k+
# embed_dim: 4096-12288
```

```
Token "Hello" → ID 15496 → lookup → [0.12, -0.34, ..., 0.56]
                                    ↑ 4096+ dimensional vector
```

### 2. Positional Encoding (RoPE)

Most modern LLMs use Rotary Position Embeddings:

```python
class RotaryEmbedding(nn.Module):
    def __init__(self, dim, base=10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, positions):
        freqs = torch.outer(positions, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        return emb.cos(), emb.sin()

    def apply_rotary(self, x, cos, sin):
        # Rotate x using precomputed cos and sin
        x_rotated = (x * cos) + (self._rotate_half(x) * sin)
        return x_rotated
```

### 3. RMSNorm (Pre-Normalization)

Simpler and faster than LayerNorm:

```python
class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        # No mean subtraction, just RMS normalization
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        return (x / rms) * self.weight

# LayerNorm:  (x - mean) / std * γ + β
# RMSNorm:    x / RMS(x) * γ  (no mean, no β)
```

### 4. Attention Variants

#### Multi-Head Attention (MHA)
```
Original: Separate Q, K, V projections per head
Q: [batch, heads, seq, head_dim]
K: [batch, heads, seq, head_dim]
V: [batch, heads, seq, head_dim]
```

#### Multi-Query Attention (MQA)
```
All heads share same K, V (Google PaLM)
Q: [batch, heads, seq, head_dim]
K: [batch, 1, seq, head_dim]  ← Shared
V: [batch, 1, seq, head_dim]  ← Shared

Much smaller KV cache, faster inference
```

#### Grouped Query Attention (GQA)
```
Groups of heads share K, V (LLaMA 2, Mistral)
Q: [batch, heads, seq, head_dim]
K: [batch, num_kv_heads, seq, head_dim]  ← Shared within groups
V: [batch, num_kv_heads, seq, head_dim]

Balance between MHA (quality) and MQA (speed)
```

```python
class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model, num_heads, num_kv_heads):
        super().__init__()
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = d_model // num_heads
        self.num_groups = num_heads // num_kv_heads

        self.q_proj = nn.Linear(d_model, num_heads * self.head_dim)
        self.k_proj = nn.Linear(d_model, num_kv_heads * self.head_dim)
        self.v_proj = nn.Linear(d_model, num_kv_heads * self.head_dim)
        self.o_proj = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, L, _ = x.shape

        q = self.q_proj(x).view(B, L, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(B, L, self.num_kv_heads, self.head_dim)
        v = self.v_proj(x).view(B, L, self.num_kv_heads, self.head_dim)

        # Repeat KV for each group
        k = k.repeat_interleave(self.num_groups, dim=2)
        v = v.repeat_interleave(self.num_groups, dim=2)

        # Standard attention from here...
```

### 5. Feed-Forward Network (SwiGLU)

Modern LLMs use gated variants:

```python
class SwiGLU(nn.Module):
    """
    SwiGLU: Swish-Gated Linear Unit
    Used in LLaMA, PaLM, etc.
    """
    def __init__(self, d_model, d_ff):
        super().__init__()
        # Note: d_ff is typically 8/3 * d_model for SwiGLU
        self.w1 = nn.Linear(d_model, d_ff, bias=False)  # Gate
        self.w2 = nn.Linear(d_ff, d_model, bias=False)  # Down
        self.w3 = nn.Linear(d_model, d_ff, bias=False)  # Up

    def forward(self, x):
        # SwiGLU(x) = (Swish(xW1) ⊙ xW3) W2
        return self.w2(F.silu(self.w1(x)) * self.w3(x))

# Original FFN:     ReLU(xW1)W2
# GELU FFN:        GELU(xW1)W2
# SwiGLU:          Swish(xW1) ⊙ xW3 then W2 (gated)
```

### 6. Output Layer

```python
class LMHead(nn.Module):
    def __init__(self, d_model, vocab_size):
        super().__init__()
        self.norm = RMSNorm(d_model)
        self.linear = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, x):
        x = self.norm(x)
        logits = self.linear(x)
        return logits

# Often weight-tied with embedding:
# lm_head.linear.weight = token_embedding.weight
```

---

## Complete LLM Implementation

```python
class LLM(nn.Module):
    def __init__(
        self,
        vocab_size=32000,
        d_model=4096,
        num_layers=32,
        num_heads=32,
        num_kv_heads=8,
        d_ff=11008,  # 8/3 * d_model for SwiGLU
        max_seq_len=4096,
        dropout=0.0,
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.rotary = RotaryEmbedding(d_model // num_heads)

        self.layers = nn.ModuleList([
            DecoderBlock(d_model, num_heads, num_kv_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])

        self.norm = RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

        # Weight tying
        self.lm_head.weight = self.token_embedding.weight

    def forward(self, input_ids, attention_mask=None):
        B, L = input_ids.shape

        # Embeddings
        x = self.token_embedding(input_ids)

        # Positional encoding
        positions = torch.arange(L, device=input_ids.device)
        cos, sin = self.rotary(positions)

        # Causal mask
        causal_mask = torch.triu(torch.ones(L, L), diagonal=1).bool()
        causal_mask = causal_mask.to(input_ids.device)

        # Decoder layers
        for layer in self.layers:
            x = layer(x, cos, sin, causal_mask, attention_mask)

        # Output
        x = self.norm(x)
        logits = self.lm_head(x)

        return logits


class DecoderBlock(nn.Module):
    def __init__(self, d_model, num_heads, num_kv_heads, d_ff, dropout):
        super().__init__()
        self.attn_norm = RMSNorm(d_model)
        self.attention = GroupedQueryAttention(d_model, num_heads, num_kv_heads)
        self.ffn_norm = RMSNorm(d_model)
        self.ffn = SwiGLU(d_model, d_ff)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, cos, sin, causal_mask, attention_mask=None):
        # Pre-norm attention + residual
        residual = x
        x = self.attn_norm(x)
        x = self.attention(x, cos, sin, causal_mask, attention_mask)
        x = residual + self.dropout(x)

        # Pre-norm FFN + residual
        residual = x
        x = self.ffn_norm(x)
        x = self.ffn(x)
        x = residual + self.dropout(x)

        return x
```

---

## Model Sizes and Configurations

| Model | Params | d_model | Layers | Heads | KV Heads | FFN | Context |
|-------|--------|---------|--------|-------|----------|-----|---------|
| LLaMA 7B | 7B | 4096 | 32 | 32 | 32 | 11008 | 4k |
| LLaMA 13B | 13B | 5120 | 40 | 40 | 40 | 13824 | 4k |
| LLaMA 70B | 70B | 8192 | 80 | 64 | 8 | 28672 | 4k |
| Mistral 7B | 7B | 4096 | 32 | 32 | 8 | 14336 | 32k |
| GPT-3 | 175B | 12288 | 96 | 96 | 96 | 49152 | 4k |

---

## KV Cache for Inference

During generation, cache computed K and V to avoid recomputation:

```python
class CachedAttention(nn.Module):
    def forward(self, x, cos, sin, mask, kv_cache=None, use_cache=True):
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        # Apply RoPE to Q and K
        q, k = self.apply_rotary(q, k, cos, sin)

        if kv_cache is not None:
            # Append to cache
            k = torch.cat([kv_cache[0], k], dim=2)
            v = torch.cat([kv_cache[1], v], dim=2)

        if use_cache:
            new_cache = (k, v)
        else:
            new_cache = None

        # Attention computation...
        output = attention(q, k, v, mask)

        return output, new_cache
```

```
Without cache (quadratic):
Step 1: Compute Q,K,V for token 1
Step 2: Compute Q,K,V for tokens 1,2
Step 3: Compute Q,K,V for tokens 1,2,3
...

With cache (linear):
Step 1: Compute Q,K,V for token 1, cache K,V
Step 2: Compute Q,K,V for token 2 only, concat with cache
Step 3: Compute Q,K,V for token 3 only, concat with cache
...
```

---

## Exercises

1. **Implement**: Build a mini LLM with all modern components (RoPE, GQA, SwiGLU)
2. **Profile**: Compare memory usage of MHA vs MQA vs GQA
3. **KV Cache**: Implement KV caching, measure speedup during generation
4. **Ablation**: Compare LayerNorm vs RMSNorm training stability
5. **Scale**: Estimate FLOPs for different model sizes

---

## Key Takeaways

- Modern LLMs: decoder-only, pre-norm, RoPE, GQA, SwiGLU
- RMSNorm: simpler, faster than LayerNorm
- GQA: balance between quality (MHA) and speed (MQA)
- SwiGLU: gated FFN with better performance
- KV cache: essential for efficient inference
- Weight tying: embedding and output share weights

---

## Track Complete!

You've completed the Transformers & LLMs track. Next:
→ Continue to [04-advanced-models/01-vjepa.md](../04-advanced-models/01-vjepa.md)
