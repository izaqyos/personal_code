# Emerging Architectures

> The cutting edge of AI model design.

---

## Overview

The field is rapidly evolving. This guide covers emerging architectures and techniques shaping the next generation of AI models.

---

## State Space Models (Mamba)

Challenge Transformers' quadratic attention:

### The Problem with Attention

```
Attention complexity: O(n²) in sequence length

Sequence: 1000 → 1,000,000 comparisons
Sequence: 100,000 → 10,000,000,000 comparisons

Memory: Must store all KV pairs
```

### State Space Models (SSMs)

```
RNN-like recurrence with efficient parallel training:

h_t = A × h_{t-1} + B × x_t    (state update)
y_t = C × h_t + D × x_t        (output)

Key insight: Can be computed in parallel during training!
Complexity: O(n log n) instead of O(n²)
```

### Mamba Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mamba Block                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Input ─┬───→ Linear ─→ Conv1D ─→ SiLU ─→ SSM ─→ ×     │
│          │                                     ↑        │
│          └───→ Linear ─→ SiLU ─────────────────┘        │
│                                                 │        │
│                                              Output      │
│                                                          │
└─────────────────────────────────────────────────────────┘

Key innovations:
1. Input-dependent parameters (selective SSM)
2. Hardware-efficient implementation
3. Linear complexity in sequence length
```

```python
# Simplified Mamba-style selective scan
class SelectiveSSM(nn.Module):
    def __init__(self, d_model, d_state):
        super().__init__()
        self.A = nn.Parameter(torch.randn(d_state, d_state))
        self.B_proj = nn.Linear(d_model, d_state)
        self.C_proj = nn.Linear(d_model, d_state)
        self.D = nn.Parameter(torch.ones(d_model))

    def forward(self, x):
        # x: [batch, seq, d_model]
        B = self.B_proj(x)  # Input-dependent!
        C = self.C_proj(x)  # Input-dependent!

        # Selective scan (efficient parallel algorithm)
        h = selective_scan(x, self.A, B, C, self.D)
        return h
```

---

## Mixture of Experts (MoE)

Scale parameters without scaling compute:

```
┌─────────────────────────────────────────────────────────┐
│                   Mixture of Experts                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Input ──→ Router ──→ [Expert 1, Expert 2, ..., Expert N]
│              │                                           │
│              ↓                                           │
│    Gate weights: [0.7, 0.3, 0, 0, ..., 0]              │
│                    ↓    ↓                               │
│                 Expert 1  Expert 2                       │
│                    ↓      ↓                              │
│    Output = 0.7×E1(x) + 0.3×E2(x)                       │
│                                                          │
└─────────────────────────────────────────────────────────┘

Each token uses only top-k experts (typically k=2)
But total parameters = all experts (hundreds!)
```

### Implementation

```python
class MoELayer(nn.Module):
    def __init__(self, d_model, d_ff, num_experts, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        # Router (gate)
        self.router = nn.Linear(d_model, num_experts)

        # Experts (each is an FFN)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Linear(d_ff, d_model)
            )
            for _ in range(num_experts)
        ])

    def forward(self, x):
        # x: [batch, seq, d_model]
        batch, seq, d = x.shape

        # Route tokens to experts
        router_logits = self.router(x)  # [batch, seq, num_experts]
        router_probs = F.softmax(router_logits, dim=-1)

        # Select top-k experts per token
        top_k_probs, top_k_indices = router_probs.topk(self.top_k, dim=-1)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)

        # Compute expert outputs (simplified)
        output = torch.zeros_like(x)
        for i, expert in enumerate(self.experts):
            mask = (top_k_indices == i).any(dim=-1)
            if mask.any():
                expert_out = expert(x[mask])
                weight = top_k_probs[..., top_k_indices == i].sum(dim=-1)
                output[mask] += weight[mask].unsqueeze(-1) * expert_out

        return output
```

### MoE Models

| Model | Total Params | Active Params | Experts |
|-------|--------------|---------------|---------|
| Mixtral 8x7B | 47B | 13B | 8 |
| GPT-4 (rumored) | ~1.8T | ~220B | 8 |
| Switch Transformer | 1.6T | ~1.6B | 2048 |

---

## Retrieval-Augmented Generation (RAG)

Extend knowledge with external retrieval:

```
┌─────────────────────────────────────────────────────────┐
│                         RAG                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Query ──→ Embed ──→ Search ──→ Retrieved docs         │
│              │           ↓                               │
│              │      [doc1, doc2, doc3]                  │
│              │           ↓                               │
│              └──→ LLM([query, doc1, doc2, doc3])        │
│                           ↓                              │
│                      Response                            │
│                                                          │
└─────────────────────────────────────────────────────────┘

Benefits:
- Up-to-date information
- Verifiable sources
- Reduced hallucination
- Domain-specific knowledge
```

```python
class RAG:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def generate(self, query, top_k=3):
        # 1. Retrieve relevant documents
        docs = self.retriever.search(query, top_k=top_k)

        # 2. Format context
        context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(docs)])

        # 3. Generate with context
        prompt = f"""Use the following documents to answer the question.

{context}

Question: {query}
Answer:"""

        return self.llm.generate(prompt)
```

---

## KAN (Kolmogorov-Arnold Networks)

Learnable activation functions on edges:

```
Standard NN:             KAN:
Weights on edges         Learnable functions on edges
Fixed activations        No fixed activations

   x₁ ────w₁────┐          x₁ ────φ₁(x)────┐
                 ↓                          ↓
              [ReLU] ──→ y            φ₃(z₁)──→ y
                 ↑                          ↑
   x₂ ────w₂────┘          x₂ ────φ₂(x)────┘

φ are spline functions (learnable curves)
```

```python
# Simplified KAN layer concept
class KANLayer(nn.Module):
    def __init__(self, in_features, out_features, num_splines=10):
        super().__init__()
        # B-spline basis functions
        self.spline_weights = nn.Parameter(
            torch.randn(out_features, in_features, num_splines)
        )

    def forward(self, x):
        # Apply learnable spline functions instead of linear + activation
        spline_basis = compute_bspline_basis(x)  # [batch, in, num_splines]
        return torch.einsum('bin,oin->bo', spline_basis, self.spline_weights)
```

---

## Neural Architecture Search (NAS)

Let AI design AI architectures:

```
Search Space:                     Controller:
- Number of layers               (RNN or RL agent)
- Hidden sizes                        │
- Attention heads                     ↓
- Activation functions          Sample architecture
- Skip connections                    │
                                      ↓
                               Train & Evaluate
                                      │
                                      ↓
                               Update controller
                               (reinforce good designs)
```

---

## Efficient Attention Variants

### Flash Attention

```
Standard attention: O(n²) memory
Flash Attention: O(n) memory

Key insight: Fuse operations, avoid materializing full attention matrix
Implemented in CUDA, 2-4× faster
```

### Linear Attention

```
Standard: softmax(QKᵀ)V          O(n²)
Linear:   φ(Q)(φ(K)ᵀV)          O(n)

Approximate attention with kernel tricks
Trade accuracy for speed
```

### Sparse Attention

```
Instead of attending to all positions:

Sliding window: Attend to local neighbors
Dilated: Attend to every k-th position
Global: Some tokens attend everywhere

Reduces O(n²) to O(n × window_size)
```

---

## Test-Time Compute Scaling

Recent research shows scaling compute at inference:

```
Chain-of-Thought: More tokens = more "thinking"
Best-of-N: Generate multiple, select best
Tree Search: Explore multiple reasoning paths
Iterative Refinement: Improve answer over rounds

Key insight: Sometimes inference compute matters more than parameters
```

---

## Future Directions

### Neuromorphic Computing
```
- Event-driven (spiking neural networks)
- Massive parallelism
- Ultra-low power
```

### World Models
```
- Learn physics/dynamics of environment
- Plan in latent space
- Video prediction → understanding
```

### Constitutional AI
```
- Self-improvement with principles
- Reduce harmful outputs
- Scalable oversight
```

---

## Exercises

1. **Implement**: Build simple selective state space model
2. **MoE**: Add mixture of experts to transformer FFN
3. **RAG**: Build retrieval system with vector database
4. **Efficient**: Implement sliding window attention
5. **Research**: Read and summarize a recent architecture paper

---

## Key Takeaways

- State Space Models (Mamba): Linear complexity alternative to Transformers
- Mixture of Experts: Scale parameters without scaling compute
- RAG: External knowledge reduces hallucination
- KAN: Learnable activations on edges
- Flash Attention: Memory-efficient attention implementation
- The field evolves rapidly - stay curious!

---

## Track Complete!

Congratulations! You've completed the Advanced Models track.

For continued learning:
- Follow arXiv cs.LG and cs.CL
- Read papers from major labs (OpenAI, Anthropic, Google, Meta)
- Implement ideas from scratch
- Experiment and iterate!
