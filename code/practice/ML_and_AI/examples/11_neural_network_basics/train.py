#!/usr/bin/env python3
"""
Neural Network from Scratch with PyTorch

Demonstrates MLP for classification.

Usage:
    python train.py
    python train.py --hidden-size 64 --epochs 50
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


class MLP(nn.Module):
    """Multi-Layer Perceptron."""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)


def train_model(
    hidden_size: int = 32,
    epochs: int = 100,
    lr: float = 0.01,
    batch_size: int = 16,
) -> dict:
    """Train neural network."""
    print(f"\n{'='*60}")
    print("Training NEURAL NETWORK (MLP)")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(DATA_DIR / "iris.csv")
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X = df[features].values
    y = df["species"].values
    
    # Encode and scale
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Convert to tensors
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.LongTensor(y_train)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.LongTensor(y_test)
    
    print(f"\nDataset: {len(X)} samples")
    print(f"Architecture: {len(features)} -> {hidden_size} -> {hidden_size} -> {len(le.classes_)}")
    print(f"Learning rate: {lr}, Epochs: {epochs}")
    
    # Model
    model = MLP(len(features), hidden_size, len(le.classes_))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Training loop
    losses = []
    accuracies = []
    
    for epoch in range(epochs):
        model.train()
        
        # Forward
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Track metrics
        losses.append(loss.item())
        
        with torch.no_grad():
            model.eval()
            test_outputs = model(X_test_t)
            _, predicted = torch.max(test_outputs, 1)
            accuracy = (predicted == y_test_t).float().mean().item()
            accuracies.append(accuracy)
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1:3d}: loss={loss.item():.4f}, acc={accuracy:.4f}")
    
    # Final evaluation
    model.eval()
    with torch.no_grad():
        outputs = model(X_test_t)
        _, predicted = torch.max(outputs, 1)
        final_acc = (predicted == y_test_t).float().mean().item()
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Final Test Accuracy: {final_acc:.4f}")
    print(f"Final Loss: {losses[-1]:.4f}")
    
    # Model summary
    print("\n" + "-" * 40)
    print("MODEL SUMMARY")
    print("-" * 40)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params}")
    for name, param in model.named_parameters():
        print(f"  {name}: {param.shape}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_DIR / "model.pt")
    torch.save({
        "scaler_mean": scaler.mean_,
        "scaler_scale": scaler.scale_,
        "classes": le.classes_,
        "input_size": len(features),
        "hidden_size": hidden_size,
        "output_size": len(le.classes_),
    }, MODEL_DIR / "config.pt")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.pt'}")
    
    return {"model": model, "accuracy": final_acc}


def main():
    parser = argparse.ArgumentParser(description="Train Neural Network")
    parser.add_argument("--hidden-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--lr", type=float, default=0.01)
    
    args = parser.parse_args()
    train_model(hidden_size=args.hidden_size, epochs=args.epochs, lr=args.lr)


if __name__ == "__main__":
    main()
