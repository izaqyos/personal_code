#!/usr/bin/env python3
"""LSTM Inference Script"""

from pathlib import Path
import torch
import torch.nn as nn

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_size, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, num_classes)
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        hidden_cat = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(hidden_cat)


def load_model():
    config = torch.load(MODEL_DIR / "config.pt", weights_only=False)
    model = LSTMClassifier(
        vocab_size=len(config["vocab"]),
        embed_dim=config["embed_dim"],
        hidden_size=config["hidden_size"],
        num_classes=3,
    )
    model.load_state_dict(torch.load(MODEL_DIR / "model.pt", weights_only=True))
    model.eval()
    return model, config


def predict(text: str, model, config) -> str:
    vocab = config["vocab"]
    label_map = config["label_map"]
    inv_label_map = {v: k for k, v in label_map.items()}
    
    words = text.lower().split()
    indices = [vocab.get(w, vocab["<UNK>"]) for w in words]
    x = torch.tensor([indices])
    
    with torch.no_grad():
        output = model(x)
        pred = torch.argmax(output, dim=1).item()
    
    return inv_label_map[pred]


def demo_predictions():
    print("\n" + "=" * 60)
    print("LSTM INFERENCE DEMO")
    print("=" * 60)
    
    try:
        model, config = load_model()
    except FileNotFoundError:
        print("Model not found. Run train.py first.")
        return
    
    print(f"Vocabulary size: {len(config['vocab'])}")
    print(f"Hidden size: {config['hidden_size']}")
    
    # Show LSTM internals
    print("\n" + "-" * 60)
    print("LSTM ARCHITECTURE")
    print("-" * 60)
    print("""
    LSTM Cell:
    ┌─────────────────────────────────────────────┐
    │                                             │
    │  x_t ──┬──[Forget]──*─────────────────┐    │
    │        │            │                 │    │
    │        ├──[Input]───*──┐              │    │
    │        │               │              │    │
    │        └──[Candidate]──┴──+──> C_t ───┤    │
    │                           │           │    │
    │  h_{t-1}                  │    tanh   │    │
    │     │                     │     │     │    │
    │     └───[Output]──────────┴─────*─> h_t   │
    │                                           │
    └─────────────────────────────────────────────┘
    """)
    
    # Sample predictions
    samples = [
        "This product is excellent and amazing",
        "Terrible quality, very disappointed",
        "It's okay, nothing special",
        "Best purchase ever, highly recommend",
        "Worst experience, do not buy",
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for text in samples:
        sentiment = predict(text, model, config)
        print(f"  '{text[:40]}...' -> {sentiment.upper()}")


if __name__ == "__main__":
    demo_predictions()
