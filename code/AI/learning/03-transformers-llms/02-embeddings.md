# Embeddings

> Dense vector representations that capture meaning.

---

## Overview

Embeddings map discrete tokens to continuous vectors where similar items are close together.

```
Token IDs:  [15496, 11, 703, 389]  # "Hello, how are"
                ↓
Embedding:  [[0.12, -0.34, 0.56, ...],   # 768-dim vector for "Hello"
             [0.89, 0.23, -0.11, ...],   # 768-dim vector for ","
             [0.45, 0.67, 0.12, ...],    # 768-dim vector for "how"
             [-0.23, 0.45, 0.89, ...]]   # 768-dim vector for "are"

Result: [batch_size, sequence_length, embedding_dim]
```

---

## Why Embeddings?

### One-Hot Encoding Problem

```
Vocabulary: ["cat", "dog", "car", "truck"]

One-hot:
cat   = [1, 0, 0, 0]
dog   = [0, 1, 0, 0]
car   = [0, 0, 1, 0]
truck = [0, 0, 0, 1]

Problems:
1. High dimensional (vocab_size dim)
2. All pairs equally distant: dist(cat, dog) = dist(cat, car) = √2
3. No semantic relationships
```

### Embeddings Solution

```
Learned embeddings:
cat   = [0.8, 0.1, 0.3, -0.2, ...]   ┐
dog   = [0.7, 0.2, 0.4, -0.1, ...]   ┤ Animals cluster together
car   = [-0.3, 0.9, 0.1, 0.6, ...]   ┐
truck = [-0.2, 0.8, 0.2, 0.7, ...]   ┤ Vehicles cluster together

dist(cat, dog) < dist(cat, car)  ✓
```

---

## Word2Vec (Historical Context)

Revolutionary 2013 paper showing embeddings capture semantics:

### Skip-gram

Predict context words from center word:

```
"The quick brown fox jumps"
Center: "brown"
Context: ["The", "quick", "fox", "jumps"]

Train: P(quick | brown), P(fox | brown), ...
```

### CBOW (Continuous Bag of Words)

Predict center word from context:

```
Context: ["The", "quick", "fox", "jumps"]
Center: "brown"

Train: P(brown | context)
```

### Famous Result: Semantic Arithmetic

```
king - man + woman ≈ queen

vec("king") - vec("man") + vec("woman") ≈ vec("queen")

The "royal" direction is preserved when gender changes!
```

---

## Token Embeddings in Transformers

### Embedding Layer

```python
import torch.nn as nn

class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        # Lookup table: vocab_size × embed_dim
        self.embedding = nn.Embedding(vocab_size, embed_dim)

    def forward(self, token_ids):
        # token_ids: [batch, seq_len]
        # output: [batch, seq_len, embed_dim]
        return self.embedding(token_ids)

# Example
embed = TokenEmbedding(vocab_size=50000, embed_dim=768)
tokens = torch.tensor([[101, 2054, 2003]])  # [CLS] What is
embeddings = embed(tokens)  # [1, 3, 768]
```

### What Gets Embedded?

```
For each token position:

1. Token embedding:    lookup(token_id) → [embed_dim]
2. Position embedding: lookup(position) → [embed_dim]  (or computed)
3. (Optional) Segment embedding: lookup(segment_id) → [embed_dim]

Final: token_embed + position_embed (+ segment_embed)
```

---

## Embedding Dimensions

| Model | Embedding Dim | Vocab Size |
|-------|---------------|------------|
| Word2Vec | 100-300 | ~3M |
| BERT-base | 768 | 30,522 |
| BERT-large | 1024 | 30,522 |
| GPT-2 | 768-1600 | 50,257 |
| GPT-3 | 12,288 | 50,257 |
| GPT-4 | ~12,000+ | ~100,000 |

---

## Sentence/Document Embeddings

Get single vector for entire text:

### Mean Pooling

```python
def mean_pooling(embeddings, attention_mask):
    """Average all token embeddings (excluding padding)"""
    mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size())
    sum_embeddings = torch.sum(embeddings * mask_expanded, dim=1)
    sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
    return sum_embeddings / sum_mask
```

### [CLS] Token (BERT-style)

```python
# First token [CLS] represents whole sequence
sentence_embedding = output[0][:, 0, :]  # [batch, embed_dim]
```

### Sentence Transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = ["This is a sentence", "Each sentence becomes a vector"]
embeddings = model.encode(sentences)
# embeddings.shape = (2, 384)

# Similarity search
from sklearn.metrics.pairwise import cosine_similarity
sim = cosine_similarity([embeddings[0]], [embeddings[1]])
```

---

## Implementation

### Using Hugging Face

```python
from transformers import AutoModel, AutoTokenizer
import torch

# Load model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Tokenize
text = "Machine learning is fascinating"
inputs = tokenizer(text, return_tensors="pt", padding=True)

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)

# Token embeddings
token_embeddings = outputs.last_hidden_state  # [1, seq_len, 768]

# Sentence embedding (mean pooling)
attention_mask = inputs['attention_mask']
sentence_embedding = mean_pooling(token_embeddings, attention_mask)
```

### OpenAI Embeddings API

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)

embedding = response.data[0].embedding  # List of 1536 floats
```

---

## Embedding Visualization

### t-SNE / UMAP

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Reduce dimensionality for visualization
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

# Plot
plt.figure(figsize=(12, 8))
for i, word in enumerate(words):
    x, y = embeddings_2d[i]
    plt.scatter(x, y)
    plt.annotate(word, xy=(x, y))
plt.show()
```

```
Visualization shows clusters:
         technology●   ●computer
                  ●software

    king●
        ●queen
            ●prince

                cat●  ●dog
                  ●pet
```

---

## Similarity Metrics

### Cosine Similarity

```
cos(A, B) = (A · B) / (||A|| × ||B||)

Range: [-1, 1]
1 = identical direction
0 = orthogonal
-1 = opposite direction

Most common for embeddings
```

### Euclidean Distance

```
dist(A, B) = √(Σ(Aᵢ - Bᵢ)²)

Lower = more similar
Sensitive to magnitude
```

### Dot Product

```
A · B = Σ(Aᵢ × Bᵢ)

Used in attention mechanism
Depends on both direction AND magnitude
```

---

## Applications

### Semantic Search

```python
# Encode query and documents
query_embed = model.encode("How to train a neural network?")
doc_embeds = model.encode(documents)

# Find most similar
similarities = cosine_similarity([query_embed], doc_embeds)[0]
top_indices = similarities.argsort()[-5:][::-1]
```

### Clustering

```python
from sklearn.cluster import KMeans

embeddings = model.encode(texts)
kmeans = KMeans(n_clusters=5)
clusters = kmeans.fit_predict(embeddings)
```

### Recommendation Systems

```
User embedding + Item embeddings → Nearest neighbors
```

---

## Exercises

1. **Implement**: Build Word2Vec skip-gram from scratch
2. **Visualize**: Create t-SNE plot of word embeddings, find clusters
3. **Semantic Search**: Build simple document search with embeddings
4. **Arithmetic**: Verify word analogies (king-man+woman=queen)
5. **Compare**: Sentence embeddings from BERT vs dedicated models

---

## Key Takeaways

- Embeddings map discrete tokens to continuous vectors
- Similar items cluster together in embedding space
- Position embeddings add sequence information
- Sentence embeddings enable semantic search
- Cosine similarity is the standard metric
- Modern embeddings are learned, not hand-crafted

---

## Next Steps

→ Continue to [03-attention-mechanism.md](./03-attention-mechanism.md)
