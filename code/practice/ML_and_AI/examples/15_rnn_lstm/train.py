#!/usr/bin/env python3
"""
RNN/LSTM Training for Sequence Classification

Demonstrates LSTM for sentiment analysis.

Usage:
    python train.py
    python train.py --hidden-size 64 --epochs 20
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


class TextDataset(Dataset):
    """Simple text dataset for sentiment analysis."""
    
    def __init__(self, texts: list[str], labels: list[int], vocab: dict[str, int], max_len: int = 50):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx].lower().split()
        # Convert to indices
        indices = [self.vocab.get(w, self.vocab["<UNK>"]) for w in text[:self.max_len]]
        return torch.tensor(indices), torch.tensor(self.labels[idx])


def collate_fn(batch):
    """Pad sequences to same length."""
    texts, labels = zip(*batch)
    texts_padded = pad_sequence(texts, batch_first=True, padding_value=0)
    return texts_padded, torch.stack(labels)


class LSTMClassifier(nn.Module):
    """LSTM for text classification."""
    
    def __init__(self, vocab_size: int, embed_dim: int, hidden_size: int, num_classes: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_size, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, num_classes)  # *2 for bidirectional
    
    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # Concatenate forward and backward hidden states
        hidden_cat = torch.cat((hidden[-2], hidden[-1]), dim=1)
        out = self.fc(hidden_cat)
        return out


def build_vocab(texts: list[str], min_freq: int = 1) -> dict[str, int]:
    """Build vocabulary from texts."""
    word_counts = {}
    for text in texts:
        for word in text.lower().split():
            word_counts[word] = word_counts.get(word, 0) + 1
    
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, count in word_counts.items():
        if count >= min_freq:
            vocab[word] = len(vocab)
    
    return vocab


def train_model(
    hidden_size: int = 32,
    embed_dim: int = 50,
    epochs: int = 20,
    lr: float = 0.001,
    batch_size: int = 16,
) -> dict:
    """Train LSTM model."""
    print("\n" + "=" * 60)
    print("Training LSTM for Sentiment Classification")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(DATA_DIR / "sentiment.csv")
    
    # Map labels
    label_map = {"positive": 2, "neutral": 1, "negative": 0}
    df["label"] = df["sentiment"].map(label_map)
    
    texts = df["text"].tolist()
    labels = df["label"].tolist()
    
    print(f"\nDataset: {len(texts)} samples")
    print(f"Classes: {list(label_map.keys())}")
    
    # Build vocabulary
    vocab = build_vocab(texts)
    print(f"Vocabulary size: {len(vocab)}")
    
    # Split data
    split_idx = int(0.8 * len(texts))
    train_texts, test_texts = texts[:split_idx], texts[split_idx:]
    train_labels, test_labels = labels[:split_idx], labels[split_idx:]
    
    # Create datasets
    train_dataset = TextDataset(train_texts, train_labels, vocab)
    test_dataset = TextDataset(test_texts, test_labels, vocab)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, collate_fn=collate_fn)
    
    # Model
    model = LSTMClassifier(
        vocab_size=len(vocab),
        embed_dim=embed_dim,
        hidden_size=hidden_size,
        num_classes=3,
    )
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    print(f"\nArchitecture:")
    print(f"  Embedding: {len(vocab)} -> {embed_dim}")
    print(f"  LSTM: {embed_dim} -> {hidden_size} (bidirectional)")
    print(f"  FC: {hidden_size * 2} -> 3")
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Total params: {total_params:,}")
    
    # Training
    print("\n" + "-" * 40)
    print("TRAINING")
    print("-" * 40)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Evaluate
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_x, batch_y in test_loader:
                outputs = model(batch_x)
                _, predicted = torch.max(outputs, 1)
                total += batch_y.size(0)
                correct += (predicted == batch_y).sum().item()
        
        accuracy = correct / total if total > 0 else 0
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1:2d}: loss={total_loss/len(train_loader):.4f}, acc={accuracy:.4f}")
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Final Test Accuracy: {accuracy:.4f}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_DIR / "model.pt")
    torch.save({
        "vocab": vocab,
        "hidden_size": hidden_size,
        "embed_dim": embed_dim,
        "label_map": label_map,
    }, MODEL_DIR / "config.pt")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.pt'}")
    
    return {"model": model, "accuracy": accuracy}


def main():
    parser = argparse.ArgumentParser(description="Train LSTM")
    parser.add_argument("--hidden-size", type=int, default=32)
    parser.add_argument("--embed-dim", type=int, default=50)
    parser.add_argument("--epochs", type=int, default=20)
    
    args = parser.parse_args()
    train_model(hidden_size=args.hidden_size, embed_dim=args.embed_dim, epochs=args.epochs)


if __name__ == "__main__":
    main()
