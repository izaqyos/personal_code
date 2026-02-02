#!/usr/bin/env python3
"""
Multi-Head Attention Implementation

Demonstrates parallel attention with multiple heads.

Usage:
    python train.py
"""

from pathlib import Path
import math

import torch
import torch.nn as nn
import torch.nn.functional as F

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"


class MultiHeadAttention(nn.Module):
    """
    Multi-Head Attention mechanism.
    
    Each head operates on a different projection of the input,
    allowing the model to attend to different aspects.
    """
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads
        
        # Linear projections for Q, K, V (combined for all heads)
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # Output projection
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def split_heads(self, x: torch.Tensor) -> torch.Tensor:
        """
        Split the last dimension into (num_heads, d_head).
        
        (batch, seq_len, d_model) -> (batch, num_heads, seq_len, d_head)
        """
        batch_size, seq_len, _ = x.size()
        x = x.view(batch_size, seq_len, self.num_heads, self.d_head)
        return x.transpose(1, 2)  # (batch, num_heads, seq_len, d_head)
    
    def merge_heads(self, x: torch.Tensor) -> torch.Tensor:
        """
        Merge heads back together.
        
        (batch, num_heads, seq_len, d_head) -> (batch, seq_len, d_model)
        """
        batch_size, _, seq_len, _ = x.size()
        x = x.transpose(1, 2)  # (batch, seq_len, num_heads, d_head)
        return x.contiguous().view(batch_size, seq_len, self.d_model)
    
    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            query: (batch, seq_len, d_model)
            key: (batch, seq_len, d_model)
            value: (batch, seq_len, d_model)
            mask: Optional attention mask
        
        Returns:
            output: (batch, seq_len, d_model)
            attention_weights: (batch, num_heads, seq_len, seq_len)
        """
        batch_size = query.size(0)
        
        # 1. Project Q, K, V
        Q = self.W_q(query)  # (batch, seq_len, d_model)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # 2. Split into heads
        Q = self.split_heads(Q)  # (batch, num_heads, seq_len, d_head)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        # 3. Scaled dot-product attention (per head)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_head)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # 4. Apply attention to values
        attn_output = torch.matmul(attention_weights, V)
        
        # 5. Merge heads
        attn_output = self.merge_heads(attn_output)  # (batch, seq_len, d_model)
        
        # 6. Output projection
        output = self.W_o(attn_output)
        
        return output, attention_weights


def demo_multi_head_attention():
    """Demonstrate multi-head attention."""
    print("\n" + "=" * 60)
    print("MULTI-HEAD ATTENTION DEMO")
    print("=" * 60)
    
    # Configuration
    batch_size = 1
    seq_len = 6
    d_model = 64
    num_heads = 8
    
    print(f"\nConfiguration:")
    print(f"  d_model: {d_model}")
    print(f"  num_heads: {num_heads}")
    print(f"  d_head: {d_model // num_heads}")
    print(f"  seq_len: {seq_len}")
    
    # Create input
    torch.manual_seed(42)
    x = torch.randn(batch_size, seq_len, d_model)
    
    # Create multi-head attention
    mha = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
    
    # Count parameters
    total_params = sum(p.numel() for p in mha.parameters())
    print(f"  Total parameters: {total_params:,}")
    
    # Forward pass
    output, attention_weights = mha(x, x, x)  # Self-attention
    
    print(f"\nInput shape:  {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attention_weights.shape}")
    print(f"  (batch, num_heads, seq_len, seq_len)")
    
    # Analyze per-head attention
    print("\n" + "-" * 40)
    print("PER-HEAD ATTENTION PATTERNS")
    print("-" * 40)
    
    weights = attention_weights[0].detach().numpy()  # (num_heads, seq_len, seq_len)
    
    # Show diagonal attention (self-attention strength)
    print("\nDiagonal attention (how much each head focuses on same position):")
    for head_idx in range(num_heads):
        diag_mean = weights[head_idx].diagonal().mean()
        bar = "█" * int(diag_mean * 20)
        print(f"  Head {head_idx}: {diag_mean:.3f} {bar}")
    
    # Show which positions each head attends to most
    print("\nPeak attention per head (which position gets most attention):")
    for head_idx in range(num_heads):
        # Average over query positions
        avg_attention = weights[head_idx].mean(axis=0)
        peak_pos = avg_attention.argmax()
        print(f"  Head {head_idx}: Position {peak_pos} (avg weight: {avg_attention[peak_pos]:.3f})")
    
    # Visualize first head's attention
    print("\n" + "-" * 40)
    print("HEAD 0 ATTENTION MATRIX")
    print("-" * 40)
    
    head_0 = weights[0]
    print("\n      ", end="")
    for i in range(seq_len):
        print(f"  P{i}  ", end="")
    print()
    
    for i, row in enumerate(head_0):
        print(f"P{i}: ", end="")
        for w in row:
            if w > 0.3:
                print(" ██  ", end="")
            elif w > 0.15:
                print(" ▓▓  ", end="")
            else:
                print(" ░░  ", end="")
        print(f" max={row.max():.2f}")
    
    # Head diversity analysis
    print("\n" + "-" * 40)
    print("HEAD DIVERSITY ANALYSIS")
    print("-" * 40)
    
    # Compute pairwise similarity between heads
    print("\nHead similarity (cosine between flattened attention matrices):")
    
    from torch.nn.functional import cosine_similarity
    
    flat_weights = attention_weights[0].view(num_heads, -1)  # (num_heads, seq_len*seq_len)
    
    similarities = []
    for i in range(num_heads):
        for j in range(i + 1, num_heads):
            sim = cosine_similarity(flat_weights[i:i+1], flat_weights[j:j+1]).item()
            similarities.append((i, j, sim))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    print("Most similar heads:")
    for i, j, sim in similarities[:3]:
        print(f"  Head {i} - Head {j}: {sim:.3f}")
    
    print("\nMost different heads:")
    for i, j, sim in similarities[-3:]:
        print(f"  Head {i} - Head {j}: {sim:.3f}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(mha.state_dict(), MODEL_DIR / "mha.pt")
    torch.save({
        "d_model": d_model,
        "num_heads": num_heads,
    }, MODEL_DIR / "config.pt")
    
    print(f"\nModel saved to: {MODEL_DIR / 'mha.pt'}")


def main():
    demo_multi_head_attention()


if __name__ == "__main__":
    main()
