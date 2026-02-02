#!/usr/bin/env python3
"""CNN Inference and Visualization"""

from pathlib import Path
import torch
import torch.nn as nn

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class SimpleCNN(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x


def demo_cnn():
    print("\n" + "=" * 60)
    print("CNN INFERENCE DEMO")
    print("=" * 60)
    
    # Load model
    model = SimpleCNN()
    if (MODEL_DIR / "model.pt").exists():
        model.load_state_dict(torch.load(MODEL_DIR / "model.pt", weights_only=True))
        print("Loaded trained model")
    else:
        print("Using untrained model (run train.py first)")
    
    model.eval()
    
    # Show convolution math
    print("\n" + "-" * 60)
    print("CONVOLUTION OPERATION EXAMPLE")
    print("-" * 60)
    
    print("""
    Input (5x5):              Kernel (3x3):
    ┌─────────────────┐       ┌─────────┐
    │ 1  0  1  0  1   │       │ 1  0  1 │
    │ 0  1  0  1  0   │   *   │ 0  1  0 │ = Output value
    │ 1  0  1  0  1   │       │ 1  0  1 │
    │ 0  1  0  1  0   │       └─────────┘
    │ 1  0  1  0  1   │
    └─────────────────┘
    
    Output = Σ(Input ⊙ Kernel) = element-wise multiply and sum
    """)
    
    # Create sample input
    x = torch.randn(1, 1, 28, 28)
    print(f"Sample input shape: {x.shape}")
    print(f"  Batch size: 1")
    print(f"  Channels: 1 (grayscale)")
    print(f"  Height: 28")
    print(f"  Width: 28")
    
    # Forward pass with intermediate outputs
    print("\n" + "-" * 60)
    print("LAYER-BY-LAYER FORWARD PASS")
    print("-" * 60)
    
    with torch.no_grad():
        # Conv1
        conv1 = model.conv_layers[0]
        out = conv1(x)
        print(f"\nConv2d(1, 16, k=3, p=1): {x.shape} -> {out.shape}")
        print(f"  Kernel weights shape: {conv1.weight.shape}")
        print(f"  # parameters: {conv1.weight.numel() + conv1.bias.numel()}")
        
        # ReLU
        out = torch.relu(out)
        print(f"ReLU: (same shape)")
        
        # MaxPool
        out = nn.MaxPool2d(2)(out)
        print(f"MaxPool2d(2): -> {out.shape}")
        
        # Conv2
        conv2 = model.conv_layers[3]
        out = conv2(out)
        print(f"\nConv2d(16, 32, k=3, p=1): -> {out.shape}")
        
        out = torch.relu(out)
        out = nn.MaxPool2d(2)(out)
        print(f"ReLU + MaxPool2d(2): -> {out.shape}")
        
        # Flatten
        flat = out.flatten(1)
        print(f"\nFlatten: -> {flat.shape}")
        
        # FC
        final = model(x)
        print(f"FC layers: -> {final.shape}")
        
        # Prediction
        probs = torch.softmax(final, dim=1)
        pred = torch.argmax(probs, dim=1)
        print(f"\nPredicted class: {pred.item()}")
        print(f"Probabilities: {probs[0].numpy().round(3)}")


if __name__ == "__main__":
    demo_cnn()
