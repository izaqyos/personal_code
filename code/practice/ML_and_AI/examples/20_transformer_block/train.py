#!/usr/bin/env python3
"""
Complete Transformer Encoder Block

Combines Multi-Head Attention, FFN, LayerNorm, and Residual connections.

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
    """Multi-Head Attention mechanism."""
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        batch_size, seq_len, _ = x.size()
        
        # Project
        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.d_head).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.d_head).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.d_head).transpose(1, 2)
        
        # Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_head)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        attn_output = torch.matmul(attn_weights, V)
        
        # Merge heads
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        
        return self.W_o(attn_output)


class FeedForward(nn.Module):
    """Position-wise Feed-Forward Network."""
    
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
        return self.linear2(self.dropout(F.gelu(self.linear1(x))))


class TransformerBlock(nn.Module):
    """
    Complete Transformer Encoder Block.
    
    Uses Pre-LayerNorm architecture (more stable than Post-LN).
    """
    
    def __init__(
        self,
        d_model: int,
        num_heads: int,
        d_ff: int | None = None,
        dropout: float = 0.1,
    ):
        super().__init__()
        
        if d_ff is None:
            d_ff = 4 * d_model  # Standard expansion factor
        
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        # Pre-LN architecture
        # 1. Self-attention with residual
        normed = self.norm1(x)
        attn_output = self.attention(normed, mask)
        x = x + self.dropout(attn_output)  # Residual connection
        
        # 2. Feed-forward with residual
        normed = self.norm2(x)
        ffn_output = self.ffn(normed)
        x = x + self.dropout(ffn_output)  # Residual connection
        
        return x


class TransformerEncoder(nn.Module):
    """Stack of Transformer Blocks."""
    
    def __init__(
        self,
        num_layers: int,
        d_model: int,
        num_heads: int,
        d_ff: int | None = None,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)  # Final layer norm
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding."""
    
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        
        # Create positional encoding matrix
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, d_model)
        return x + self.pe[:, :x.size(1)]


def demo_transformer_block():
    """Demonstrate the complete Transformer block."""
    print("\n" + "=" * 60)
    print("TRANSFORMER BLOCK DEMO")
    print("=" * 60)
    
    # Configuration
    batch_size = 2
    seq_len = 10
    d_model = 64
    num_heads = 4
    num_layers = 2
    d_ff = 256
    
    print(f"\nConfiguration:")
    print(f"  d_model: {d_model}")
    print(f"  num_heads: {num_heads}")
    print(f"  d_head: {d_model // num_heads}")
    print(f"  d_ff: {d_ff} (4x expansion)")
    print(f"  num_layers: {num_layers}")
    
    # Create encoder
    encoder = TransformerEncoder(
        num_layers=num_layers,
        d_model=d_model,
        num_heads=num_heads,
        d_ff=d_ff,
    )
    
    pos_encoding = PositionalEncoding(d_model)
    
    # Count parameters
    total_params = sum(p.numel() for p in encoder.parameters())
    print(f"\nEncoder parameters: {total_params:,}")
    
    # Breakdown per block
    print("\nPer-block parameter breakdown:")
    block = encoder.layers[0]
    
    attn_params = sum(p.numel() for p in block.attention.parameters())
    ffn_params = sum(p.numel() for p in block.ffn.parameters())
    norm_params = sum(p.numel() for p in block.norm1.parameters()) + sum(p.numel() for p in block.norm2.parameters())
    
    print(f"  Attention: {attn_params:,}")
    print(f"  FFN: {ffn_params:,}")
    print(f"  LayerNorm: {norm_params:,}")
    print(f"  Total: {attn_params + ffn_params + norm_params:,}")
    
    # Forward pass
    print("\n" + "-" * 40)
    print("FORWARD PASS")
    print("-" * 40)
    
    torch.manual_seed(42)
    x = torch.randn(batch_size, seq_len, d_model)
    
    print(f"\nInput shape: {x.shape}")
    
    # Add positional encoding
    x_pos = pos_encoding(x)
    print(f"After positional encoding: {x_pos.shape}")
    
    # Forward through encoder
    output = encoder(x_pos)
    print(f"Encoder output: {output.shape}")
    
    # Trace through single block
    print("\n" + "-" * 40)
    print("SINGLE BLOCK TRACE")
    print("-" * 40)
    
    block = encoder.layers[0]
    
    # Layer 1: Attention
    print("\n1. Layer Norm 1")
    normed = block.norm1(x_pos)
    print(f"   Mean: {normed.mean().item():.4f}, Std: {normed.std().item():.4f}")
    
    print("\n2. Multi-Head Attention")
    attn_output = block.attention(normed)
    print(f"   Output shape: {attn_output.shape}")
    
    print("\n3. Residual Connection 1")
    residual1 = x_pos + attn_output
    print(f"   x + attention(norm(x))")
    
    print("\n4. Layer Norm 2")
    normed2 = block.norm2(residual1)
    print(f"   Mean: {normed2.mean().item():.4f}, Std: {normed2.std().item():.4f}")
    
    print("\n5. Feed-Forward Network")
    ffn_output = block.ffn(normed2)
    print(f"   d_model ({d_model}) -> d_ff ({d_ff}) -> d_model ({d_model})")
    
    print("\n6. Residual Connection 2")
    residual2 = residual1 + ffn_output
    print(f"   Final output shape: {residual2.shape}")
    
    # Show scaling across layers
    print("\n" + "-" * 40)
    print("ACTIVATION STATISTICS PER LAYER")
    print("-" * 40)
    
    x_trace = x_pos.clone()
    print(f"\nInput: mean={x_trace.mean().item():.4f}, std={x_trace.std().item():.4f}")
    
    for i, layer in enumerate(encoder.layers):
        x_trace = layer(x_trace)
        print(f"Layer {i+1}: mean={x_trace.mean().item():.4f}, std={x_trace.std().item():.4f}")
    
    x_trace = encoder.norm(x_trace)
    print(f"Final: mean={x_trace.mean().item():.4f}, std={x_trace.std().item():.4f}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(encoder.state_dict(), MODEL_DIR / "encoder.pt")
    torch.save({
        "d_model": d_model,
        "num_heads": num_heads,
        "num_layers": num_layers,
        "d_ff": d_ff,
    }, MODEL_DIR / "config.pt")
    
    print(f"\nEncoder saved to: {MODEL_DIR / 'encoder.pt'}")


def main():
    demo_transformer_block()


if __name__ == "__main__":
    main()
