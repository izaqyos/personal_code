# Multi-Head Attention

Parallel attention with multiple representation subspaces.

## Concepts Covered

- **Multiple Heads**: Parallel attention computations
- **Head Splitting**: Divide embedding into heads
- **Concatenation**: Merge head outputs
- **Different Subspaces**: Each head learns different patterns

## The Math

### Multi-Head Attention
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O

where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

### Dimension Split
```
d_model = 512, num_heads = 8
d_head = d_model / num_heads = 64
```

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Different Perspectives**: Each head can focus on different aspects
2. **Efficient**: Same total computation as single head (d_head × num_heads = d_model)
3. **Head Specialization**: Some heads focus on syntax, others on semantics
4. **Standard Config**: 8-32 heads in modern transformers
