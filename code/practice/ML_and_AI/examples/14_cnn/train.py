#!/usr/bin/env python3
"""
CNN Training on MNIST

Demonstrates Conv2d, MaxPool2d, and classification.

Usage:
    python train.py
    python train.py --epochs 5
"""

import argparse
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class SimpleCNN(nn.Module):
    """Simple CNN for digit classification."""
    
    def __init__(self, num_classes: int = 10):
        super().__init__()
        
        # Convolutional layers
        self.conv_layers = nn.Sequential(
            # Conv1: 1 channel -> 16 channels, 3x3 kernel
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 28x28 -> 14x14
            
            # Conv2: 16 -> 32 channels
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 14x14 -> 7x7
        )
        
        # Fully connected layers
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x


def generate_fake_mnist(n_samples: int = 1000):
    """Generate fake MNIST-like data for demo."""
    # Random images (28x28)
    X = torch.randn(n_samples, 1, 28, 28)
    # Random labels (0-9)
    y = torch.randint(0, 10, (n_samples,))
    
    # Add some structure: draw simple patterns for each digit
    for i in range(n_samples):
        label = y[i].item()
        # Draw horizontal/vertical lines based on label
        X[i, 0, label * 2:label * 2 + 3, :] += 2.0
        X[i, 0, :, label * 2:label * 2 + 3] += 1.0
    
    return X, y


def train_model(epochs: int = 10, lr: float = 0.001, batch_size: int = 32) -> dict:
    """Train CNN model."""
    print("\n" + "=" * 60)
    print("Training CNN (Convolutional Neural Network)")
    print("=" * 60)
    
    # Generate data (replace with real MNIST if available)
    print("\nGenerating synthetic MNIST-like data...")
    X_train, y_train = generate_fake_mnist(5000)
    X_test, y_test = generate_fake_mnist(1000)
    
    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=batch_size,
        shuffle=True,
    )
    test_loader = DataLoader(
        TensorDataset(X_test, y_test),
        batch_size=batch_size,
    )
    
    print(f"\nTrain: {len(X_train)} samples")
    print(f"Test:  {len(X_test)} samples")
    print(f"Input shape: {X_train.shape} (batch, channels, height, width)")
    
    # Model
    model = SimpleCNN(num_classes=10)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Print model architecture
    print("\n" + "-" * 40)
    print("MODEL ARCHITECTURE")
    print("-" * 40)
    print(model)
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"\nTotal parameters: {total_params:,}")
    
    # Training loop
    print("\n" + "-" * 40)
    print("TRAINING")
    print("-" * 40)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Evaluate
        model.eval()
        correct = 0
        with torch.no_grad():
            for batch_X, batch_y in test_loader:
                outputs = model(batch_X)
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == batch_y).sum().item()
        
        accuracy = correct / len(X_test)
        avg_loss = total_loss / len(train_loader)
        
        print(f"Epoch {epoch+1:2d}: loss={avg_loss:.4f}, acc={accuracy:.4f}")
    
    # Final evaluation
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Final Test Accuracy: {accuracy:.4f}")
    
    # Show feature map shapes
    print("\n" + "-" * 40)
    print("FEATURE MAP SHAPES (for single image)")
    print("-" * 40)
    
    model.eval()
    with torch.no_grad():
        x = X_test[0:1]  # Single image
        print(f"Input:       {x.shape}")
        
        x = model.conv_layers[0](x)  # Conv1
        print(f"After Conv1: {x.shape}")
        x = model.conv_layers[1](x)  # ReLU
        x = model.conv_layers[2](x)  # Pool
        print(f"After Pool1: {x.shape}")
        x = model.conv_layers[3](x)  # Conv2
        print(f"After Conv2: {x.shape}")
        x = model.conv_layers[4](x)  # ReLU
        x = model.conv_layers[5](x)  # Pool
        print(f"After Pool2: {x.shape}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_DIR / "model.pt")
    print(f"\nModel saved to: {MODEL_DIR / 'model.pt'}")
    
    return {"model": model, "accuracy": accuracy}


def main():
    parser = argparse.ArgumentParser(description="Train CNN")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.001)
    
    args = parser.parse_args()
    train_model(epochs=args.epochs, lr=args.lr)


if __name__ == "__main__":
    main()
