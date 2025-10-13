import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt


class SinusoidalPositionalEncoding(nn.Module):
    """
    Sinusoidal Positional Encoding as introduced in 'Attention Is All You Need'
    
    This creates position embeddings using sine and cosine functions of different frequencies:
    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    def __init__(self, d_model, max_len=5000):
        """
        Initialize positional encoding
        
        Args:
            d_model: Dimensionality of the model embeddings
            max_len: Maximum sequence length
        """
        super(SinusoidalPositionalEncoding, self).__init__()
        
        # Create a tensor of shape (max_len, d_model)
        pe = torch.zeros(max_len, d_model)
        
        # Create a tensor of shape (max_len, 1)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # Create a tensor of shape (1, d_model//2)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model)
        )
        
        # Apply sine to even indices
        pe[:, 0::2] = torch.sin(position * div_term)
        
        # Apply cosine to odd indices
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # Add batch dimension (1, max_len, d_model)
        pe = pe.unsqueeze(0)
        
        # Register buffer (not a parameter but should be saved with model)
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        """
        Add positional encoding to the input embeddings
        
        Args:
            x: Input embeddings tensor of shape (batch_size, seq_len, d_model)
            
        Returns:
            x + pe[:, :seq_len]: Input with positional encoding added
        """
        # x has shape (batch_size, seq_len, d_model)
        return x + self.pe[:, :x.size(1)]


class LearnedPositionalEncoding(nn.Module):
    """
    Learned positional embeddings as an alternative to sinusoidal encodings
    """
    def __init__(self, d_model, max_len=5000):
        """
        Initialize learned positional embeddings
        
        Args:
            d_model: Dimensionality of the model embeddings
            max_len: Maximum sequence length
        """
        super(LearnedPositionalEncoding, self).__init__()
        
        # Create a learnable parameter for positions
        self.position_embeddings = nn.Parameter(torch.zeros(1, max_len, d_model))
        
    def forward(self, x):
        """
        Add learned positional embeddings to the input
        
        Args:
            x: Input embeddings tensor of shape (batch_size, seq_len, d_model)
            
        Returns:
            x + position_embeddings[:, :seq_len]: Input with positional embeddings added
        """
        # x has shape (batch_size, seq_len, d_model)
        return x + self.position_embeddings[:, :x.size(1)]


class RotaryPositionalEmbedding(nn.Module):
    """
    Rotary Positional Embedding (RoPE) implementation
    
    Paper: "Roformer: Enhanced Transformer with Rotary Position Embedding"
    This applies position-dependent rotation to the embedding vectors.
    """
    def __init__(self, d_model, max_len=5000):
        super(RotaryPositionalEmbedding, self).__init__()
        
        self.d_model = d_model
        self.max_len = max_len
        
        # Generate frequencies for rotation
        # We only need half the dimensions because we rotate pairs of dimensions
        freq = 1.0 / (10000 ** (torch.arange(0, d_model, 2).float() / d_model))
        self.register_buffer("freq", freq)
        
        # Precompute positional angles
        t = torch.arange(max_len, dtype=torch.float)
        freqs = torch.outer(t, self.freq)  # shape (max_len, d_model/2)
        
        # Create complex numbers e^(i*theta) = cos(theta) + i*sin(theta)
        self.cos_cached = torch.cos(freqs).view(1, max_len, 1, d_model // 2)
        self.sin_cached = torch.sin(freqs).view(1, max_len, 1, d_model // 2)
        
    def forward(self, q, k):
        """
        Apply rotary positional embedding to queries and keys
        
        Args:
            q: Query tensor of shape (batch_size, seq_len, heads, d_head)
            k: Key tensor of shape (batch_size, seq_len, heads, d_head)
            
        Returns:
            q_pos: Query with rotary positional embedding
            k_pos: Key with rotary positional embedding
        """
        batch_size, seq_len, heads, d_head = q.shape
        
        # Get the positional encoding for the sequence length we need
        cos = self.cos_cached[:, :seq_len]
        sin = self.sin_cached[:, :seq_len]
        
        # Reshape q and k for rotation
        # Split the last dimension to apply rotation to each pair (x_i, x_{i+d/2})
        q_evens = q[:, :, :, 0::2]
        q_odds = q[:, :, :, 1::2]
        k_evens = k[:, :, :, 0::2]
        k_odds = k[:, :, :, 1::2]
        
        # Apply rotary embeddings
        # For dimension pairs (x_i, x_{i+d/2}), we compute:
        # (x_i*cos - x_{i+d/2}*sin, x_{i+d/2}*cos + x_i*sin)
        q_pos_evens = q_evens * cos - q_odds * sin
        q_pos_odds = q_odds * cos + q_evens * sin
        k_pos_evens = k_evens * cos - k_odds * sin
        k_pos_odds = k_odds * cos + k_evens * sin
        
        # Interleave the rotated values back together
        q_pos = torch.zeros_like(q)
        k_pos = torch.zeros_like(k)
        
        q_pos[:, :, :, 0::2] = q_pos_evens
        q_pos[:, :, :, 1::2] = q_pos_odds
        k_pos[:, :, :, 0::2] = k_pos_evens
        k_pos[:, :, :, 1::2] = k_pos_odds
        
        return q_pos, k_pos


def visualize_positional_encoding(encoding, max_len=100, dim_subset=None):
    """
    Visualize positional encodings
    
    Args:
        encoding: Positional encoding tensor of shape (1, max_len, d_model)
        max_len: Maximum sequence length to visualize
        dim_subset: Optional list of dimensions to visualize (default: 20 evenly spaced dims)
    """
    encoding = encoding[0, :max_len].detach().cpu().numpy()  # (max_len, d_model)
    d_model = encoding.shape[1]
    
    if dim_subset is None:
        # Choose 20 evenly spaced dimensions to visualize
        dim_subset = np.linspace(0, d_model-1, 20, dtype=int)
    
    plt.figure(figsize=(12, 8))
    for i, dim in enumerate(dim_subset):
        plt.plot(encoding[:, dim], label=f'Dim {dim}')
    
    plt.xlabel('Position')
    plt.ylabel('Encoding Value')
    plt.title('Positional Encoding Visualization')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.savefig('positional_encoding_visualization.png')
    plt.close()
    
    # Also create a heatmap
    plt.figure(figsize=(12, 8))
    plt.imshow(encoding, aspect='auto', cmap='viridis')
    plt.xlabel('Dimension')
    plt.ylabel('Position')
    plt.title('Positional Encoding Heatmap')
    plt.colorbar()
    plt.savefig('positional_encoding_heatmap.png')
    
    return plt.gcf()


# Tests
if __name__ == "__main__":
    # Test parameters
    batch_size = 2
    seq_len = 10
    d_model = 64
    
    # Create random input embeddings
    x = torch.randn(batch_size, seq_len, d_model)
    
    # Test Sinusoidal Positional Encoding
    print("Testing Sinusoidal Positional Encoding...")
    sin_pos_enc = SinusoidalPositionalEncoding(d_model)
    output = sin_pos_enc(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Test Learned Positional Encoding
    print("\nTesting Learned Positional Encoding...")
    learned_pos_enc = LearnedPositionalEncoding(d_model)
    output = learned_pos_enc(x)
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, d_model)
    
    # Test RoPE
    print("\nTesting Rotary Positional Encoding...")
    # Reshape input for RoPE as if they were queries and keys from multi-head attention
    heads = 8
    d_head = d_model // heads
    q = x.view(batch_size, seq_len, heads, d_head)
    k = x.view(batch_size, seq_len, heads, d_head)
    
    rope = RotaryPositionalEmbedding(d_model)
    q_pos, k_pos = rope(q, k)
    print(f"Q pos shape: {q_pos.shape}")
    print(f"K pos shape: {k_pos.shape}")
    assert q_pos.shape == (batch_size, seq_len, heads, d_head)
    assert k_pos.shape == (batch_size, seq_len, heads, d_head)
    
    # Visualize positional encodings
    print("\nVisualizing positional encodings...")
    pe = sin_pos_enc.pe
    fig = visualize_positional_encoding(pe, max_len=100)
    print("Positional encoding visualizations saved as 'positional_encoding_visualization.png' and 'positional_encoding_heatmap.png'")
    
    print("\nAll tests passed!") 