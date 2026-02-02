#!/usr/bin/env python3
"""
Scaled Dot-Product Attention from Scratch

Demonstrates the core attention mechanism.

Usage:
    python train.py
"""

from pathlib import Path
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


def scaled_dot_product_attention(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    mask: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Compute scaled dot-product attention.
    
    Args:
        query: (batch, seq_len, d_k)
        key: (batch, seq_len, d_k)
        value: (batch, seq_len, d_v)
        mask: Optional mask (batch, seq_len, seq_len)
    
    Returns:
        output: (batch, seq_len, d_v)
        attention_weights: (batch, seq_len, seq_len)
    """
    d_k = query.size(-1)
    
    # Step 1: Compute attention scores (QK^T)
    scores = torch.matmul(query, key.transpose(-2, -1))  # (batch, seq_len, seq_len)
    
    # Step 2: Scale by sqrt(d_k)
    scores = scores / math.sqrt(d_k)
    
    # Step 3: Apply mask (optional, for causal attention)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    # Step 4: Softmax to get attention weights
    attention_weights = F.softmax(scores, dim=-1)
    
    # Step 5: Weighted sum of values
    output = torch.matmul(attention_weights, value)  # (batch, seq_len, d_v)
    
    return output, attention_weights


class SelfAttention(nn.Module):
    """Self-attention layer with learnable projections."""
    
    def __init__(self, embed_dim: int):
        super().__init__()
        self.embed_dim = embed_dim
        
        # Linear projections for Q, K, V
        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)
        
        # Output projection
        self.W_o = nn.Linear(embed_dim, embed_dim)
    
    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Input tensor (batch, seq_len, embed_dim)
            mask: Optional attention mask
        
        Returns:
            output: (batch, seq_len, embed_dim)
            attention_weights: (batch, seq_len, seq_len)
        """
        # Project to Q, K, V
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)
        
        # Apply attention
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)
        
        # Output projection
        output = self.W_o(attn_output)
        
        return output, attn_weights


def demo_attention():
    """Demonstrate attention mechanism."""
    print("\n" + "=" * 60)
    print("SCALED DOT-PRODUCT ATTENTION DEMO")
    print("=" * 60)
    
    # Create sample data
    batch_size = 1
    seq_len = 4
    d_model = 8
    
    # Random input (simulating embeddings)
    torch.manual_seed(42)
    x = torch.randn(batch_size, seq_len, d_model)
    
    print(f"\nInput shape: {x.shape}")
    print(f"  batch_size: {batch_size}")
    print(f"  seq_len: {seq_len}")
    print(f"  d_model: {d_model}")
    
    # Step-by-step attention computation
    print("\n" + "-" * 40)
    print("STEP-BY-STEP COMPUTATION")
    print("-" * 40)
    
    # Use input as Q, K, V (self-attention without projection)
    Q = x
    K = x
    V = x
    
    print(f"\n1. Q, K, V shapes: {Q.shape}")
    
    # QK^T
    scores = torch.matmul(Q, K.transpose(-2, -1))
    print(f"\n2. Raw scores (QK^T) shape: {scores.shape}")
    print(f"   Raw scores:\n{scores[0].numpy().round(2)}")
    
    # Scale
    d_k = K.size(-1)
    scaled_scores = scores / math.sqrt(d_k)
    print(f"\n3. Scaled scores (÷ √{d_k}):\n{scaled_scores[0].numpy().round(2)}")
    
    # Softmax
    attention_weights = F.softmax(scaled_scores, dim=-1)
    print(f"\n4. Attention weights (softmax):\n{attention_weights[0].numpy().round(3)}")
    print(f"   Row sums: {attention_weights[0].sum(dim=-1).numpy().round(3)}")
    
    # Weighted sum
    output = torch.matmul(attention_weights, V)
    print(f"\n5. Output (weights @ V) shape: {output.shape}")
    
    # Using our function
    print("\n" + "-" * 40)
    print("SELF-ATTENTION WITH PROJECTIONS")
    print("-" * 40)
    
    self_attn = SelfAttention(embed_dim=d_model)
    output, weights = self_attn(x)
    
    print(f"\nOutput shape: {output.shape}")
    print(f"Attention weights shape: {weights.shape}")
    
    # Visualize attention
    print("\nAttention Pattern:")
    print("(each row shows what that position attends to)")
    print()
    
    weights_np = weights[0].detach().numpy()
    positions = ["Pos0", "Pos1", "Pos2", "Pos3"]
    
    print("     ", end="")
    for p in positions:
        print(f"{p:>6}", end="")
    print()
    
    for i, row in enumerate(weights_np):
        print(f"{positions[i]}: ", end="")
        for w in row:
            # Visualize weight intensity
            if w > 0.4:
                char = "██"
            elif w > 0.25:
                char = "▓▓"
            elif w > 0.15:
                char = "▒▒"
            else:
                char = "░░"
            print(f" {char} ", end="")
        print()
    
    # Causal (masked) attention
    print("\n" + "-" * 40)
    print("CAUSAL (MASKED) ATTENTION")
    print("-" * 40)
    
    # Create causal mask (lower triangular)
    causal_mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0)
    print(f"\nCausal mask:\n{causal_mask[0].numpy().astype(int)}")
    
    output_masked, weights_masked = scaled_dot_product_attention(Q, K, V, causal_mask)
    
    print(f"\nMasked attention weights:\n{weights_masked[0].detach().numpy().round(3)}")
    print("(each position can only attend to itself and previous positions)")
    
    # Save demo
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(self_attn.state_dict(), MODEL_DIR / "attention.pt")
    
    print(f"\nAttention layer saved to: {MODEL_DIR / 'attention.pt'}")


def main():
    demo_attention()


if __name__ == "__main__":
    main()
