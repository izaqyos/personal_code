# Attention Mechanism

The core mechanism behind transformers.

## Concepts Covered

- **Query, Key, Value**: The three projections
- **Scaled Dot-Product**: Attention formula
- **Attention Weights**: Soft selection of values
- **Self-Attention**: Sequence attending to itself

## The Math

### Attention Formula
```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) V
```

Where:
- Q = Query matrix (what to look for)
- K = Key matrix (what's available)
- V = Value matrix (what to retrieve)
- d_k = Key dimension (for scaling)

## Why Scaling?

Without √d_k, dot products grow large with dimension, causing softmax to produce near-one-hot distributions with vanishing gradients.

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Parallelizable**: Unlike RNNs, all positions computed at once
2. **Long-Range**: Direct connections between any positions
3. **Interpretable**: Attention weights show what model focuses on
4. **Scalable**: O(n²) complexity, but efficient on GPUs
