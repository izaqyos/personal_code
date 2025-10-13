import unittest
import torch
import numpy as np
from positional_encoding import (
    SinusoidalPositionalEncoding,
    LearnedPositionalEncoding,
    RotaryPositionalEmbedding
)


class TestPositionalEncoding(unittest.TestCase):
    def setUp(self):
        # Common test parameters
        self.batch_size = 4
        self.seq_len = 16
        self.d_model = 64
        self.heads = 8
        self.d_head = self.d_model // self.heads
        
        # Create random input embeddings
        self.x = torch.randn(self.batch_size, self.seq_len, self.d_model)
        
        # Create q and k for RoPE
        self.q = self.x.view(self.batch_size, self.seq_len, self.heads, self.d_head)
        self.k = self.x.view(self.batch_size, self.seq_len, self.heads, self.d_head)

    def test_sinusoidal_pe_shape(self):
        """Test that sinusoidal positional encoding produces correct output shapes."""
        sin_pe = SinusoidalPositionalEncoding(self.d_model)
        output = sin_pe(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_sinusoidal_pe_values(self):
        """Test that sinusoidal positional encoding has expected properties."""
        sin_pe = SinusoidalPositionalEncoding(self.d_model)
        
        # The encoding should be the same for all positions across batches
        pe = sin_pe.pe[0, :100]  # (100, d_model)
        
        # Verify that the values are between -1 and 1
        self.assertTrue(torch.all(pe >= -1) and torch.all(pe <= 1))
        
        # Test that the wavelengths increase exponentially with dimension
        # For each position, even dimensions should be sin, odd should be cos
        for pos in range(1, 10):
            # Adjacent positions should have similar values in high-frequency dimensions
            # and different values in low-frequency dimensions
            high_freq_dims = pe[pos, :10] - pe[pos-1, :10]
            low_freq_dims = pe[pos, -10:] - pe[pos-1, -10:]
            
            # High frequency dimensions should change more between positions
            self.assertTrue(torch.norm(high_freq_dims) > torch.norm(low_freq_dims))
    
    def test_learned_pe_shape(self):
        """Test that learned positional encoding produces correct output shapes."""
        learned_pe = LearnedPositionalEncoding(self.d_model)
        output = learned_pe(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_learned_pe_parameters(self):
        """Test that learned positional encoding parameters are updated during training."""
        learned_pe = LearnedPositionalEncoding(self.d_model)
        
        # Save initial parameters
        init_params = learned_pe.position_embeddings.data.clone()
        
        # Simulate a training step
        output = learned_pe(self.x)
        loss = output.sum()
        loss.backward()
        
        # Check that gradients were computed
        self.assertTrue(learned_pe.position_embeddings.grad is not None)
        self.assertFalse(torch.allclose(learned_pe.position_embeddings.grad, torch.zeros_like(learned_pe.position_embeddings.grad)))
        
        # Apply a fake optimization step
        with torch.no_grad():
            learned_pe.position_embeddings.data -= 0.1 * learned_pe.position_embeddings.grad
        
        # Parameters should have changed
        self.assertFalse(torch.allclose(init_params, learned_pe.position_embeddings.data))
    
    def test_rope_shape(self):
        """Test that rotary positional embedding produces correct output shapes."""
        rope = RotaryPositionalEmbedding(self.d_model)
        q_pos, k_pos = rope(self.q, self.k)
        
        self.assertEqual(q_pos.shape, (self.batch_size, self.seq_len, self.heads, self.d_head))
        self.assertEqual(k_pos.shape, (self.batch_size, self.seq_len, self.heads, self.d_head))
    
    def test_rope_relative_position_property(self):
        """Test that rotary positional embedding preserves relative position information."""
        rope = RotaryPositionalEmbedding(self.d_model)
        
        # Create a simple test case with controlled values
        d_model = 4
        seq_len = 3
        batch_size = 1
        heads = 1
        d_head = d_model
        
        # Simple embedding with a single feature that varies by position
        # q: [[[1,0,0,0]], [[2,0,0,0]], [[3,0,0,0]]]
        q = torch.zeros(batch_size, seq_len, heads, d_head)
        q[0, 0, 0, 0] = 1
        q[0, 1, 0, 0] = 2
        q[0, 2, 0, 0] = 3
        
        # k: [[[1,0,0,0]], [[1,0,0,0]], [[1,0,0,0]]]
        k = torch.zeros(batch_size, seq_len, heads, d_head)
        k[0, :, 0, 0] = 1
        
        small_rope = RotaryPositionalEmbedding(d_model)
        q_pos, k_pos = small_rope(q, k)
        
        # The rotated vectors should maintain their relative positions
        # We can verify by computing dot products between q[i] and k[j]
        # The dot product should only depend on the relative position (i-j)
        
        # Extract vectors 
        q0 = q_pos[0, 0, 0]  # Position 0
        q1 = q_pos[0, 1, 0]  # Position 1
        q2 = q_pos[0, 2, 0]  # Position 2
        
        k0 = k_pos[0, 0, 0]  # Position 0
        k1 = k_pos[0, 1, 0]  # Position 1
        k2 = k_pos[0, 2, 0]  # Position 2
        
        # Compute dot products for different relative positions
        dot_00 = torch.dot(q0, k0)  # Relative position 0
        dot_11 = torch.dot(q1, k1)  # Also relative position 0
        dot_22 = torch.dot(q2, k2)  # Also relative position 0
        
        dot_01 = torch.dot(q0, k1)  # Relative position -1
        dot_12 = torch.dot(q1, k2)  # Also relative position -1
        
        dot_10 = torch.dot(q1, k0)  # Relative position 1
        dot_21 = torch.dot(q2, k1)  # Also relative position 1
        
        # Dot products for the same relative positions should be similar
        self.assertTrue(torch.isclose(dot_00, dot_11, rtol=1e-4))
        self.assertTrue(torch.isclose(dot_11, dot_22, rtol=1e-4))
        
        self.assertTrue(torch.isclose(dot_01, dot_12, rtol=1e-4))
        self.assertTrue(torch.isclose(dot_10, dot_21, rtol=1e-4))


if __name__ == "__main__":
    unittest.main() 