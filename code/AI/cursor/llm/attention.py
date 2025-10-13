import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

class ScaledDotProductAttention(nn.Module):
    """
    Scaled Dot-Product Attention as described in 'Attention Is All You Need'
    
    This is the core attention mechanism that computes:
    Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
    """
    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()
    
    def forward(self, Q, K, V, mask=None):
        """
        Forward pass for scaled dot-product attention
        
        Args:
            Q: Query tensor of shape (batch_size, seq_len_q, d_k)
            K: Key tensor of shape (batch_size, seq_len_k, d_k)
            V: Value tensor of shape (batch_size, seq_len_k, d_v)
            mask: Optional mask tensor of shape (batch_size, seq_len_q, seq_len_k)
        
        Returns:
            output: Attention output of shape (batch_size, seq_len_q, d_v)
            attn_weights: Attention weights for visualization
        """
        # Get dimensions
        d_k = K.size(-1)
        
        # Compute scaled dot product: QK^T / sqrt(d_k)
        # Output shape: (batch_size, seq_len_q, seq_len_k)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(d_k)
        
        # Apply mask if provided (for padding or causal attention)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Apply softmax to get attention weights
        # Output shape: (batch_size, seq_len_q, seq_len_k)
        attn_weights = F.softmax(scores, dim=-1)
        
        # Multiply with values
        # Output shape: (batch_size, seq_len_q, d_v)
        output = torch.matmul(attn_weights, V)
        
        return output, attn_weights


class MultiHeadAttention(nn.Module):
    """
    Multi-Head Attention as described in 'Attention Is All You Need'
    
    MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_o
    where head_i = Attention(Q * W_q_i, K * W_k_i, V * W_v_i)
    """
    def __init__(self, d_model, num_heads):
        """
        Initialize Multi-Head Attention
        
        Args:
            d_model: Model dimension (embedding size)
            num_heads: Number of attention heads
        """
        super(MultiHeadAttention, self).__init__()
        
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # Dimension of each head
        
        # Linear projections for Q, K, V, and output
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.attention = ScaledDotProductAttention()
        
    def split_heads(self, x):
        """
        Split the last dimension into (num_heads, d_k)
        
        Args:
            x: Tensor of shape (batch_size, seq_len, d_model)
            
        Returns:
            Tensor of shape (batch_size, num_heads, seq_len, d_k)
        """
        batch_size, seq_len, _ = x.size()
        return x.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
    
    def combine_heads(self, x):
        """
        Combine the multiple heads back into original shape
        
        Args:
            x: Tensor of shape (batch_size, num_heads, seq_len, d_k)
            
        Returns:
            Tensor of shape (batch_size, seq_len, d_model)
        """
        batch_size, _, seq_len, _ = x.size()
        return x.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
    
    def forward(self, Q, K, V, mask=None):
        """
        Forward pass for Multi-Head Attention
        
        Args:
            Q: Query tensor of shape (batch_size, seq_len_q, d_model)
            K: Key tensor of shape (batch_size, seq_len_k, d_model)
            V: Value tensor of shape (batch_size, seq_len_v, d_model)
            mask: Optional mask tensor
            
        Returns:
            output: Output tensor after multi-head attention
            attn_weights: Attention weights from the last head
        """
        batch_size = Q.size(0)
        
        # Apply linear projections
        Q = self.W_q(Q)  # (batch_size, seq_len_q, d_model)
        K = self.W_k(K)  # (batch_size, seq_len_k, d_model)
        V = self.W_v(V)  # (batch_size, seq_len_v, d_model)
        
        # Split into multiple heads
        Q = self.split_heads(Q)  # (batch_size, num_heads, seq_len_q, d_k)
        K = self.split_heads(K)  # (batch_size, num_heads, seq_len_k, d_k)
        V = self.split_heads(V)  # (batch_size, num_heads, seq_len_v, d_k)
        
        # If mask exists, expand it to match the number of heads
        if mask is not None:
            mask = mask.unsqueeze(1).repeat(1, self.num_heads, 1, 1)
        
        # Apply scaled dot-product attention to each head
        outputs = []
        attn_weights_list = []
        
        # This can be optimized by processing all heads in parallel
        # But for clarity, we process each head separately
        for h in range(self.num_heads):
            output, attn_weights = self.attention(
                Q[:, h], K[:, h], V[:, h], 
                mask[:, h] if mask is not None else None
            )
            outputs.append(output)
            attn_weights_list.append(attn_weights)
        
        # Alternative parallel implementation:
        # output, attn_weights = self.attention(Q, K, V, mask)
        # return self.W_o(self.combine_heads(output)), attn_weights
        
        # Stack the heads' outputs
        output = torch.stack([o for o in outputs], dim=1)  # (batch_size, num_heads, seq_len_q, d_k)
        
        # Combine the heads
        combined_output = self.combine_heads(output)  # (batch_size, seq_len_q, d_model)
        
        # Final linear projection
        final_output = self.W_o(combined_output)  # (batch_size, seq_len_q, d_model)
        
        # Return the output and the attention weights from the last head
        return final_output, attn_weights_list[-1]


class SelfAttention(nn.Module):
    """
    Self-Attention module where Q, K, V all come from the same source
    """
    def __init__(self, d_model, num_heads):
        super(SelfAttention, self).__init__()
        self.mha = MultiHeadAttention(d_model, num_heads)
    
    def forward(self, x, mask=None):
        """
        Apply self-attention where Q = K = V = x
        
        Args:
            x: Input tensor of shape (batch_size, seq_len, d_model)
            mask: Optional mask tensor
            
        Returns:
            output: Self-attention output
            attn_weights: Attention weights
        """
        return self.mha(x, x, x, mask)


# Create a function to visualize attention weights
def visualize_attention(attention_weights, tokens=None):
    """
    Visualize attention weights as a heatmap
    
    Args:
        attention_weights: Attention weight matrix of shape (seq_len_q, seq_len_k)
        tokens: Optional list of token strings for axis labels
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    cax = ax.matshow(attention_weights.detach().cpu().numpy(), cmap='viridis')
    fig.colorbar(cax)
    
    if tokens is not None:
        ax.set_xticks(range(len(tokens)))
        ax.set_yticks(range(len(tokens)))
        ax.set_xticklabels(tokens, rotation=90)
        ax.set_yticklabels(tokens)
    
    ax.set_xlabel('Key tokens')
    ax.set_ylabel('Query tokens')
    plt.tight_layout()
    
    return fig


# Unit tests
if __name__ == "__main__":
    # Test parameters
    batch_size = 2
    seq_len = 5
    d_model = 64
    num_heads = 8
    
    # Create sample data
    x = torch.randn(batch_size, seq_len, d_model)
    
    # Test Scaled Dot-Product Attention
    print("Testing Scaled Dot-Product Attention...")
    attention = ScaledDotProductAttention()
    output, attn_weights = attention(x, x, x)
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attn_weights.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    assert attn_weights.shape == (batch_size, seq_len, seq_len)
    
    # Test Multi-Head Attention
    print("\nTesting Multi-Head Attention...")
    mha = MultiHeadAttention(d_model, num_heads)
    output, attn_weights = mha(x, x, x)
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attn_weights.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    assert attn_weights.shape == (batch_size, seq_len, seq_len)
    
    # Test Self-Attention
    print("\nTesting Self-Attention...")
    self_attn = SelfAttention(d_model, num_heads)
    output, attn_weights = self_attn(x)
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attn_weights.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    assert attn_weights.shape == (batch_size, seq_len, seq_len)
    
    print("\nAll tests passed!")
    
    # Example of masked attention (causal mask for decoder)
    print("\nTesting with causal mask...")
    mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).repeat(batch_size, 1, 1)
    output, attn_weights = attention(x, x, x, mask)
    print(f"Output shape with mask: {output.shape}")
    
    # Visualize example attention weights
    print("\nVisualizing attention weights...")
    sample_tokens = ["The", "quick", "brown", "fox", "jumps"]
    sample_attn = attn_weights[0]  # Take attention weights from the first batch
    fig = visualize_attention(sample_attn, sample_tokens)
    # Save the visualization
    plt.savefig('attention_visualization.png')
    print("Attention visualization saved as 'attention_visualization.png'") 