import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


class FeedForwardNetwork(nn.Module):
    """
    Position-wise Feed-Forward Network as described in 'Attention Is All You Need'
    
    This is a simple network consisting of two linear transformations with a ReLU activation in between:
    FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
    
    The inner-layer dimension is typically larger than the input/output dimension.
    """
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        """
        Initialize the FFN
        
        Args:
            d_model: Model dimension (input and output)
            d_ff: Hidden dimension of the feed-forward network
            dropout: Dropout rate
        """
        super(FeedForwardNetwork, self).__init__()
        
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the feed-forward network
        
        Args:
            x: Input tensor of shape (batch_size, seq_len, d_model)
            
        Returns:
            Output tensor of shape (batch_size, seq_len, d_model)
        """
        # First linear layer with ReLU activation
        x = F.relu(self.linear1(x))
        
        # Apply dropout
        x = self.dropout(x)
        
        # Second linear layer
        x = self.linear2(x)
        
        return x


class GLU(nn.Module):
    """
    Gated Linear Unit (GLU) activation
    
    This is an alternative activation used in some modern transformer designs
    like GLM and PaLM, providing a gating mechanism.
    
    GLU(x, W, V, b, c) = (xW + b) ⊗ σ(xV + c)
    
    where ⊗ is element-wise multiplication and σ is a sigmoid function.
    """
    def __init__(self, d_model: int, d_ff: int, activation: str = 'silu'):
        """
        Initialize the GLU
        
        Args:
            d_model: Model dimension (input and output)
            d_ff: Hidden dimension
            activation: Activation function to use ('sigmoid', 'silu', or 'gelu')
        """
        super(GLU, self).__init__()
        
        self.linear = nn.Linear(d_model, d_ff * 2)  # Double size for gate and value
        self.linear2 = nn.Linear(d_ff, d_model)
        
        if activation == 'sigmoid':
            self.act_fn = torch.sigmoid
        elif activation == 'silu':
            self.act_fn = F.silu
        elif activation == 'gelu':
            self.act_fn = F.gelu
        else:
            raise ValueError(f"Activation {activation} not supported")
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the GLU
        
        Args:
            x: Input tensor of shape (batch_size, seq_len, d_model)
            
        Returns:
            Output tensor of shape (batch_size, seq_len, d_model)
        """
        # Project to twice the size
        x = self.linear(x)
        
        # Split into gate and value parts
        d_ff = x.size(-1) // 2
        gate, value = x[..., :d_ff], x[..., d_ff:]
        
        # Apply gating
        x = self.act_fn(gate) * value
        
        # Project back to original size
        x = self.linear2(x)
        
        return x


class LayerNorm(nn.Module):
    """
    Layer Normalization as described in 'Layer Normalization'
    
    Normalizes input tensor along the last dimension.
    """
    def __init__(self, d_model: int, eps: float = 1e-5):
        """
        Initialize Layer Normalization
        
        Args:
            d_model: Feature dimension to normalize over
            eps: Small constant for numerical stability
        """
        super(LayerNorm, self).__init__()
        
        # Learnable parameters
        self.weight = nn.Parameter(torch.ones(d_model))
        self.bias = nn.Parameter(torch.zeros(d_model))
        self.eps = eps
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for Layer Normalization
        
        Args:
            x: Input tensor of shape (..., d_model)
            
        Returns:
            Normalized tensor of shape (..., d_model)
        """
        # Compute mean and variance along the last dimension
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, unbiased=False, keepdim=True)
        
        # Normalize
        x_norm = (x - mean) / torch.sqrt(var + self.eps)
        
        # Scale and shift
        x_norm = self.weight * x_norm + self.bias
        
        return x_norm


class RMSNorm(nn.Module):
    """
    Root Mean Square Layer Normalization
    
    A simplified version of Layer Normalization that only 
    normalizes by the root mean square, without centering.
    
    Used in some recent models like LLaMA.
    """
    def __init__(self, d_model: int, eps: float = 1e-5):
        """
        Initialize RMS Normalization
        
        Args:
            d_model: Feature dimension to normalize over
            eps: Small constant for numerical stability
        """
        super(RMSNorm, self).__init__()
        
        # Learnable parameter
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for RMS Normalization
        
        Args:
            x: Input tensor of shape (..., d_model)
            
        Returns:
            Normalized tensor of shape (..., d_model)
        """
        # Compute root mean square along the last dimension
        rms = torch.sqrt(torch.mean(x**2, dim=-1, keepdim=True) + self.eps)
        
        # Normalize
        x_norm = x / rms
        
        # Scale
        x_norm = self.weight * x_norm
        
        return x_norm


class TransformerBlock(nn.Module):
    """
    Complete Transformer Block combining attention, feed-forward network,
    and layer normalization with residual connections.
    """
    def __init__(
        self, 
        d_model: int, 
        num_heads: int, 
        d_ff: int, 
        dropout: float = 0.1,
        use_glu: bool = False,
        use_rms_norm: bool = False,
        pre_norm: bool = True
    ):
        """
        Initialize a Transformer Block
        
        Args:
            d_model: Model dimension (embedding size)
            num_heads: Number of attention heads
            d_ff: Hidden dimension of the feed-forward network
            dropout: Dropout rate
            use_glu: Whether to use GLU instead of standard FFN
            use_rms_norm: Whether to use RMS normalization instead of layer norm
            pre_norm: Whether to apply normalization before attention and FFN (Pre-LN)
                      or after (Post-LN)
        """
        super(TransformerBlock, self).__init__()
        
        # Multi-head attention
        from attention import MultiHeadAttention
        self.mha = MultiHeadAttention(d_model, num_heads)
        
        # Feed-forward network
        if use_glu:
            self.ffn = GLU(d_model, d_ff)
        else:
            self.ffn = FeedForwardNetwork(d_model, d_ff, dropout)
        
        # Layer normalization
        if use_rms_norm:
            self.norm1 = RMSNorm(d_model)
            self.norm2 = RMSNorm(d_model)
        else:
            self.norm1 = LayerNorm(d_model)
            self.norm2 = LayerNorm(d_model)
        
        # Dropout for regularization
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        
        # Architecture choice
        self.pre_norm = pre_norm
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass for a Transformer Block
        
        Args:
            x: Input tensor of shape (batch_size, seq_len, d_model)
            mask: Optional mask tensor for attention
            
        Returns:
            Output tensor of shape (batch_size, seq_len, d_model)
        """
        # Pre-LN architecture (more stable for training)
        if self.pre_norm:
            # Layer normalization before attention
            norm_x = self.norm1(x)
            
            # Multi-head attention with residual connection
            attn_output, _ = self.mha(norm_x, norm_x, norm_x, mask)
            x = x + self.dropout1(attn_output)
            
            # Layer normalization before FFN
            norm_x = self.norm2(x)
            
            # Feed-forward network with residual connection
            ffn_output = self.ffn(norm_x)
            x = x + self.dropout2(ffn_output)
        
        # Post-LN architecture (original Transformer paper)
        else:
            # Multi-head attention with residual connection
            attn_output, _ = self.mha(x, x, x, mask)
            x = self.norm1(x + self.dropout1(attn_output))
            
            # Feed-forward network with residual connection
            ffn_output = self.ffn(x)
            x = self.norm2(x + self.dropout2(ffn_output))
        
        return x


# Tests
if __name__ == "__main__":
    # Test parameters
    batch_size = 2
    seq_len = 10
    d_model = 64
    d_ff = 256
    num_heads = 8
    
    # Create random input tensor
    x = torch.randn(batch_size, seq_len, d_model)
    
    # Test FeedForwardNetwork
    print("Testing Feed-Forward Network...")
    ffn = FeedForwardNetwork(d_model, d_ff)
    output = ffn(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Test GLU
    print("\nTesting Gated Linear Unit...")
    glu = GLU(d_model, d_ff)
    output = glu(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Test LayerNorm
    print("\nTesting Layer Normalization...")
    ln = LayerNorm(d_model)
    output = ln(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Test RMSNorm
    print("\nTesting RMS Normalization...")
    rmsn = RMSNorm(d_model)
    output = rmsn(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Check normalization properties
    ln_mean = output.mean(dim=-1)
    ln_std = output.std(dim=-1)
    print(f"RMSNorm output mean range: [{ln_mean.min().item():.4f}, {ln_mean.max().item():.4f}]")
    print(f"RMSNorm output std range: [{ln_std.min().item():.4f}, {ln_std.max().item():.4f}]")
    
    # Create a mask for testing the transformer block
    mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0)
    mask = mask.repeat(batch_size, 1, 1)
    
    # Test TransformerBlock
    print("\nTesting Transformer Block...")
    transformer_block = TransformerBlock(d_model, num_heads, d_ff)
    output = transformer_block(x, mask)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Compare different transformer configurations
    print("\nComparing different Transformer configurations...")
    # Default Pre-LN
    block1 = TransformerBlock(d_model, num_heads, d_ff, pre_norm=True, use_glu=False, use_rms_norm=False)
    # Post-LN 
    block2 = TransformerBlock(d_model, num_heads, d_ff, pre_norm=False, use_glu=False, use_rms_norm=False)
    # Pre-LN with GLU
    block3 = TransformerBlock(d_model, num_heads, d_ff, pre_norm=True, use_glu=True, use_rms_norm=False)
    # Pre-LN with RMSNorm
    block4 = TransformerBlock(d_model, num_heads, d_ff, pre_norm=True, use_glu=False, use_rms_norm=True)
    
    # Process the same input through each
    output1 = block1(x, mask)
    output2 = block2(x, mask)
    output3 = block3(x, mask)
    output4 = block4(x, mask)
    
    # Print output statistics to show they behave differently
    print(f"Pre-LN output mean: {output1.mean().item():.4f}, std: {output1.std().item():.4f}")
    print(f"Post-LN output mean: {output2.mean().item():.4f}, std: {output2.std().item():.4f}")
    print(f"Pre-LN+GLU output mean: {output3.mean().item():.4f}, std: {output3.std().item():.4f}")
    print(f"Pre-LN+RMSNorm output mean: {output4.mean().item():.4f}, std: {output4.std().item():.4f}")
    
    print("\nAll tests passed!") 