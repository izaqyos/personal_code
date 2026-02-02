# Word Embeddings

Dense vector representations of words/tokens.

## Concepts Covered

- **Embedding Layer**: Lookup table (token ID -> vector)
- **Word2Vec**: Skip-gram and CBOW training
- **Similarity**: Cosine similarity between vectors
- **Visualization**: t-SNE/PCA projections

## The Math

### Embedding Lookup
```
E[token_id] = vector of shape (embed_dim,)
```

### Cosine Similarity
```
sim(a, b) = (a · b) / (||a|| × ||b||)
```

### Word2Vec Skip-gram
```
P(context | center) = softmax(E_context · E_center)
```

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Dense vs Sparse**: Embeddings are dense, one-hot is sparse
2. **Learned**: Embeddings are learned during training
3. **Semantic Meaning**: Similar words have similar vectors
4. **Transfer Learning**: Pre-trained embeddings (GloVe, FastText)
