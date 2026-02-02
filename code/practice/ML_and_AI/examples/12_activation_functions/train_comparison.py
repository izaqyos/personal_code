#!/usr/bin/env python3
"""Compare activation functions on XOR problem."""

import torch
import torch.nn as nn
import torch.optim as optim


def compare_activations():
    """Compare different activations on XOR problem."""
    # XOR dataset
    X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)
    
    activations = {
        "ReLU": nn.ReLU(),
        "Sigmoid": nn.Sigmoid(),
        "Tanh": nn.Tanh(),
        "LeakyReLU": nn.LeakyReLU(0.01),
        "GELU": nn.GELU(),
    }
    
    results = {}
    
    for name, activation in activations.items():
        # Simple network
        model = nn.Sequential(
            nn.Linear(2, 8),
            activation,
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )
        
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.1)
        
        # Train
        for epoch in range(200):
            optimizer.zero_grad()
            output = model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
        
        # Final accuracy
        with torch.no_grad():
            preds = (model(X) > 0.5).float()
            accuracy = (preds == y).float().mean().item()
        
        results[name] = {"loss": loss.item(), "accuracy": accuracy}
        print(f"  {name:<12}: loss={loss.item():.4f}, accuracy={accuracy:.2f}")
    
    return results


if __name__ == "__main__":
    compare_activations()
