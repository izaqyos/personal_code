# Attention Mechanism Implementation

This repository contains a PyTorch implementation of the attention mechanism as described in the paper ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762) by Vaswani et al. The implementation includes:

1. **Scaled Dot-Product Attention**
2. **Multi-Head Attention**
3. **Self-Attention**

## Core Concepts

### Scaled Dot-Product Attention

The core attention mechanism computes:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

Where:
- **Q** (Query): What we're looking for
- **K** (Key): What we match against
- **V** (Value): What we retrieve
- **d_k**: Dimension of the key vectors

The scaling factor `1/sqrt(d_k)` prevents the dot products from growing too large in magnitude, which would push the softmax function into regions with extremely small gradients.

### Multi-Head Attention

Instead of performing a single attention function, multi-head attention performs attention multiple times in parallel:

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_O
where head_i = Attention(Q * W_q_i, K * W_k_i, V * W_v_i)
```

This allows the model to attend to information from different representation subspaces at different positions.

### Self-Attention

In self-attention, the queries, keys, and values all come from the same source. This allows each position in a sequence to attend to all positions in the sequence, capturing the relationships between different words.

## Running the Code

To run the code and see the attention mechanism in action:

```bash
python attention.py
```

This will:
1. Run unit tests for all three attention types
2. Create a visualization of attention weights that will be saved as 'attention_visualization.png'

## Requirements

- PyTorch
- NumPy
- Matplotlib

## Extending the Implementation

This implementation can be extended by:

1. Adding positional encoding
2. Implementing a full Transformer block (with feed-forward networks and layer normalization)
3. Building a complete encoder or decoder stack

## Performance Considerations

- The current implementation processes each attention head sequentially. For better performance, this could be parallelized.
- Time Complexity: O(n²) where n is the sequence length, which becomes a bottleneck for long sequences.
- Space Complexity: O(n²) for storing the attention matrix.

## Next Steps

After understanding attention, consider:
1. Building a full transformer encoder/decoder
2. Implementing input embeddings and positional encoding
3. Adding training pipeline with appropriate optimizers and learning rate schedules 