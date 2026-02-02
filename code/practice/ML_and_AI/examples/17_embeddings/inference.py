#!/usr/bin/env python3
"""Embeddings Inference and Similarity Search"""

from pathlib import Path
import torch
import torch.nn as nn

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


def load_embeddings():
    data = torch.load(MODEL_DIR / "embeddings.pt", weights_only=False)
    return data["embeddings"], data["vocab"], data["embed_dim"]


def find_similar(word: str, embeddings: torch.Tensor, vocab: dict, top_k: int = 5) -> list:
    """Find most similar words."""
    if word not in vocab:
        return []
    
    id_to_word = {v: k for k, v in vocab.items()}
    word_vec = embeddings[vocab[word]]
    
    cos = nn.CosineSimilarity(dim=0)
    similarities = []
    
    for w, idx in vocab.items():
        if w == word or w == "<PAD>":
            continue
        sim = cos(word_vec, embeddings[idx]).item()
        similarities.append((w, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


def demo_embeddings():
    print("\n" + "=" * 60)
    print("EMBEDDINGS INFERENCE DEMO")
    print("=" * 60)
    
    try:
        embeddings, vocab, embed_dim = load_embeddings()
    except FileNotFoundError:
        print("Embeddings not found. Run train.py first.")
        return
    
    print(f"Vocab size: {len(vocab)}")
    print(f"Embedding dim: {embed_dim}")
    
    # Similarity search
    print("\n" + "-" * 60)
    print("SIMILARITY SEARCH")
    print("-" * 60)
    
    for query in ["king", "dog", "boy"]:
        print(f"\nMost similar to '{query}':")
        similar = find_similar(query, embeddings, vocab)
        for word, sim in similar:
            print(f"  {word}: {sim:.4f}")
    
    # Embedding arithmetic
    print("\n" + "-" * 60)
    print("EMBEDDING ARITHMETIC")
    print("-" * 60)
    
    print("""
    Famous Word2Vec examples:
    - king - man + woman ≈ queen
    - paris - france + italy ≈ rome
    - bigger - big + small ≈ smaller
    
    The embedding space captures semantic relationships!
    """)


if __name__ == "__main__":
    demo_embeddings()
