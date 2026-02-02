#!/usr/bin/env python3
"""Neural Network Inference Script"""

from pathlib import Path
import numpy as np
import torch
import torch.nn as nn

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class MLP(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
    
    def forward(self, x):
        return self.layers(x)


def load_model():
    config = torch.load(MODEL_DIR / "config.pt", weights_only=False)
    
    model = MLP(config["input_size"], config["hidden_size"], config["output_size"])
    model.load_state_dict(torch.load(MODEL_DIR / "model.pt", weights_only=True))
    model.eval()
    
    return model, config


def demo_predictions():
    print("\n" + "=" * 60)
    print("NEURAL NETWORK INFERENCE DEMO")
    print("=" * 60)
    
    model, config = load_model()
    classes = config["classes"]
    scaler_mean = config["scaler_mean"]
    scaler_scale = config["scaler_scale"]
    
    print(f"\nModel: MLP with hidden_size={config['hidden_size']}")
    print(f"Classes: {list(classes)}")
    
    # Sample predictions
    samples = [
        [5.0, 3.4, 1.5, 0.2],  # Setosa-like
        [5.9, 2.8, 4.3, 1.3],  # Versicolor-like
        [6.6, 3.0, 5.6, 2.0],  # Virginica-like
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for sample in samples:
        # Scale
        x = (np.array(sample) - scaler_mean) / scaler_scale
        x_tensor = torch.FloatTensor(x).unsqueeze(0)
        
        with torch.no_grad():
            logits = model(x_tensor)
            probs = torch.softmax(logits, dim=1)
            pred = torch.argmax(probs, dim=1).item()
        
        print(f"Input: {sample}")
        print(f"  -> Predicted: {classes[pred]}")
        print(f"  -> Probabilities: {dict(zip(classes, probs[0].numpy().round(3)))}")
        print()
    
    # Show activations
    print("-" * 60)
    print("Layer Activations (for first sample):")
    print("-" * 60)
    
    x = (np.array(samples[0]) - scaler_mean) / scaler_scale
    x_tensor = torch.FloatTensor(x).unsqueeze(0)
    
    # Manual forward to see activations
    with torch.no_grad():
        h1 = model.layers[0](x_tensor)  # Linear
        a1 = model.layers[1](h1)         # ReLU
        h2 = model.layers[2](a1)         # Linear
        a2 = model.layers[3](h2)         # ReLU
        out = model.layers[4](a2)        # Linear
    
    print(f"Input:          {x.round(3)}")
    print(f"After Linear1:  {h1[0][:5].numpy().round(3)}...")
    print(f"After ReLU1:    {a1[0][:5].numpy().round(3)}...")
    print(f"After Linear2:  {h2[0][:5].numpy().round(3)}...")
    print(f"After ReLU2:    {a2[0][:5].numpy().round(3)}...")
    print(f"Output (logits):{out[0].numpy().round(3)}")


if __name__ == "__main__":
    demo_predictions()
