#!/usr/bin/env python3
"""
Word Embeddings Demo

Demonstrates nn.Embedding and similarity search.

Usage:
    python train.py
"""

from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class SimpleEmbedding:
    """Demonstrate embedding concepts."""
    
    def __init__(self, vocab_size: int, embed_dim: int):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
    
    def lookup(self, token_ids: list[int]) -> torch.Tensor:
        """Look up embeddings for token IDs."""
        ids = torch.tensor(token_ids)
        return self.embedding(ids)
    
    def similarity(self, vec1: torch.Tensor, vec2: torch.Tensor) -> float:
        """Compute cosine similarity."""
        cos = nn.CosineSimilarity(dim=0)
        return cos(vec1, vec2).item()


class SkipGram(nn.Module):
    """Simple Skip-gram model for Word2Vec."""
    
    def __init__(self, vocab_size: int, embed_dim: int):
        super().__init__()
        self.center_embeddings = nn.Embedding(vocab_size, embed_dim)
        self.context_embeddings = nn.Embedding(vocab_size, embed_dim)
    
    def forward(self, center: torch.Tensor, context: torch.Tensor) -> torch.Tensor:
        # center: (batch,), context: (batch,)
        center_embed = self.center_embeddings(center)  # (batch, embed_dim)
        context_embed = self.context_embeddings(context)  # (batch, embed_dim)
        
        # Dot product
        scores = (center_embed * context_embed).sum(dim=1)  # (batch,)
        return scores


def train_word2vec_demo():
    """Train a simple Word2Vec model."""
    print("\n" + "=" * 60)
    print("WORD EMBEDDINGS DEMO")
    print("=" * 60)
    
    # Simple vocabulary
    vocab = {
        "<PAD>": 0, "king": 1, "queen": 2, "man": 3, "woman": 4,
        "prince": 5, "princess": 6, "boy": 7, "girl": 8,
        "dog": 9, "cat": 10, "puppy": 11, "kitten": 12,
    }
    id_to_word = {v: k for k, v in vocab.items()}
    
    vocab_size = len(vocab)
    embed_dim = 16
    
    print(f"\nVocabulary: {list(vocab.keys())}")
    print(f"Vocab size: {vocab_size}")
    print(f"Embedding dim: {embed_dim}")
    
    # Create model
    model = SkipGram(vocab_size, embed_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    # Create training pairs (center, context)
    # Simulate pairs based on semantic relationships
    training_pairs = [
        # Royal words co-occur
        (vocab["king"], vocab["queen"]),
        (vocab["queen"], vocab["king"]),
        (vocab["prince"], vocab["princess"]),
        (vocab["princess"], vocab["prince"]),
        (vocab["king"], vocab["prince"]),
        (vocab["queen"], vocab["princess"]),
        
        # Gender pairs
        (vocab["man"], vocab["woman"]),
        (vocab["woman"], vocab["man"]),
        (vocab["boy"], vocab["girl"]),
        (vocab["girl"], vocab["boy"]),
        (vocab["man"], vocab["boy"]),
        (vocab["woman"], vocab["girl"]),
        
        # Animals
        (vocab["dog"], vocab["puppy"]),
        (vocab["cat"], vocab["kitten"]),
        (vocab["dog"], vocab["cat"]),
    ]
    
    # Repeat pairs for more training data
    training_pairs = training_pairs * 100
    
    print(f"\nTraining on {len(training_pairs)} pairs...")
    
    # Train
    for epoch in range(50):
        total_loss = 0
        np.random.shuffle(training_pairs)
        
        for center, context in training_pairs:
            optimizer.zero_grad()
            
            center_t = torch.tensor([center])
            context_t = torch.tensor([context])
            
            # Positive sample
            pos_score = model(center_t, context_t)
            
            # Negative sample (random word)
            neg_context = np.random.randint(1, vocab_size)
            neg_context_t = torch.tensor([neg_context])
            neg_score = model(center_t, neg_context_t)
            
            # Loss: maximize positive, minimize negative
            loss = -torch.log(torch.sigmoid(pos_score)) - torch.log(torch.sigmoid(-neg_score))
            loss = loss.mean()
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}: loss = {total_loss/len(training_pairs):.4f}")
    
    # Extract embeddings
    embeddings = model.center_embeddings.weight.detach()
    
    print("\n" + "-" * 40)
    print("SIMILARITY ANALYSIS")
    print("-" * 40)
    
    cos = nn.CosineSimilarity(dim=0)
    
    # Test pairs
    test_pairs = [
        ("king", "queen"),
        ("king", "man"),
        ("dog", "cat"),
        ("dog", "puppy"),
        ("king", "dog"),
    ]
    
    print("\nCosine Similarities:")
    for w1, w2 in test_pairs:
        id1, id2 = vocab[w1], vocab[w2]
        sim = cos(embeddings[id1], embeddings[id2]).item()
        print(f"  {w1:10} - {w2:10}: {sim:+.4f}")
    
    # Word analogy
    print("\n" + "-" * 40)
    print("WORD ANALOGY: king - man + woman = ?")
    print("-" * 40)
    
    # king - man + woman should be close to queen
    result_vec = embeddings[vocab["king"]] - embeddings[vocab["man"]] + embeddings[vocab["woman"]]
    
    # Find most similar word
    similarities = []
    for word, idx in vocab.items():
        if word in ["king", "man", "woman", "<PAD>"]:
            continue
        sim = cos(result_vec, embeddings[idx]).item()
        similarities.append((word, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 5 most similar:")
    for word, sim in similarities[:5]:
        print(f"  {word}: {sim:.4f}")
    
    # Show embedding vectors
    print("\n" + "-" * 40)
    print("EMBEDDING VECTORS (first 4 dims)")
    print("-" * 40)
    
    for word in ["king", "queen", "man", "woman", "dog"]:
        vec = embeddings[vocab[word]][:4].numpy()
        print(f"  {word:10}: {vec.round(3)}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save({
        "embeddings": embeddings,
        "vocab": vocab,
        "embed_dim": embed_dim,
    }, MODEL_DIR / "embeddings.pt")
    
    print(f"\nEmbeddings saved to: {MODEL_DIR / 'embeddings.pt'}")


def main():
    train_word2vec_demo()


if __name__ == "__main__":
    main()
