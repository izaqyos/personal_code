import unittest
import torch
import numpy as np
from attention import ScaledDotProductAttention, MultiHeadAttention, SelfAttention


class TestAttention(unittest.TestCase):
    def setUp(self):
        # Common test parameters
        self.batch_size = 4
        self.seq_len = 10
        self.d_model = 64
        self.num_heads = 8
        
        # Create random input tensors
        self.x = torch.randn(self.batch_size, self.seq_len, self.d_model)
        
        # Create a causal mask (for autoregressive models)
        self.causal_mask = torch.tril(torch.ones(self.seq_len, self.seq_len)).unsqueeze(0)
        self.causal_mask = self.causal_mask.repeat(self.batch_size, 1, 1)
        
        # Create a padding mask (for variable length sequences)
        self.padding_mask = torch.ones(self.batch_size, self.seq_len)
        # Set some positions as padding (0)
        for i in range(self.batch_size):
            pad_length = np.random.randint(1, 4)
            self.padding_mask[i, -pad_length:] = 0
        self.padding_mask = self.padding_mask.unsqueeze(1).repeat(1, self.seq_len, 1)

    def test_scaled_dot_product_attention_shapes(self):
        """Test that Scaled Dot-Product Attention produces correct output shapes."""
        attention = ScaledDotProductAttention()
        output, attn_weights = attention(self.x, self.x, self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
        self.assertEqual(attn_weights.shape, (self.batch_size, self.seq_len, self.seq_len))
    
    def test_scaled_dot_product_attention_causal_mask(self):
        """Test that masked positions have zero attention with causal mask."""
        attention = ScaledDotProductAttention()
        output, attn_weights = attention(self.x, self.x, self.x, self.causal_mask)
        
        # Check that masked positions (upper triangle) have zero attention
        for i in range(self.seq_len):
            for j in range(i+1, self.seq_len):
                # Attention weights should be close to zero for all batches
                self.assertTrue(torch.all(attn_weights[:, i, j] < 1e-6))
    
    def test_multi_head_attention_shapes(self):
        """Test that Multi-Head Attention produces correct output shapes."""
        mha = MultiHeadAttention(self.d_model, self.num_heads)
        output, attn_weights = mha(self.x, self.x, self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
        self.assertEqual(attn_weights.shape, (self.batch_size, self.seq_len, self.seq_len))
    
    def test_self_attention_shapes(self):
        """Test that Self-Attention produces correct output shapes."""
        self_attn = SelfAttention(self.d_model, self.num_heads)
        output, attn_weights = self_attn(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
        self.assertEqual(attn_weights.shape, (self.batch_size, self.seq_len, self.seq_len))
    
    def test_padding_mask(self):
        """Test that padded positions don't receive attention."""
        attention = ScaledDotProductAttention()
        output, attn_weights = attention(self.x, self.x, self.x, self.padding_mask)
        
        # Check that masked positions have zero attention
        for i in range(self.batch_size):
            for j in range(self.seq_len):
                # Get positions where padding_mask is 0
                masked_positions = (self.padding_mask[i, j] == 0).nonzero(as_tuple=True)[0]
                if len(masked_positions) > 0:
                    # Attention weights should be close to zero for masked positions
                    self.assertTrue(torch.all(attn_weights[i, j, masked_positions] < 1e-6))
    
    def test_attention_equivalence(self):
        """Test attention equation: Attention(Q,K,V) = softmax(QK^T/sqrt(d_k))V."""
        # Create random Q, K, V
        d_k = 32
        q = torch.randn(2, 3, d_k)
        k = torch.randn(2, 4, d_k)
        v = torch.randn(2, 4, d_k)
        
        # Manual attention calculation
        scores = torch.matmul(q, k.transpose(-2, -1)) / np.sqrt(d_k)
        attn_weights = torch.nn.functional.softmax(scores, dim=-1)
        expected_output = torch.matmul(attn_weights, v)
        
        # Using our implementation
        attention = ScaledDotProductAttention()
        output, _ = attention(q, k, v)
        
        # Check if outputs are close
        self.assertTrue(torch.allclose(output, expected_output, rtol=1e-5))
    
    def test_multi_head_vs_single_head(self):
        """
        Test that multi-head attention with 1 head is equivalent to 
        scaled dot-product attention with the correct projections.
        """
        # Create input tensors
        d_model = 32
        batch_size = 2
        seq_len = 5
        x = torch.randn(batch_size, seq_len, d_model)
        
        # Create multi-head attention with 1 head
        mha = MultiHeadAttention(d_model, num_heads=1)
        
        # Create single-head attention
        sdpa = ScaledDotProductAttention()
        
        # Forward pass through multi-head attention
        mha_out, _ = mha(x, x, x)
        
        # To match multi-head, we need to apply the linear projections manually
        q = mha.W_q(x)
        k = mha.W_k(x)
        v = mha.W_v(x)
        sdpa_out, _ = sdpa(q, k, v)
        sdpa_out = mha.W_o(sdpa_out)
        
        # Check that outputs are similar
        # Not exactly equal due to different computation paths
        # but should be close with small relative error
        self.assertTrue(torch.allclose(mha_out, sdpa_out, rtol=1e-4))


if __name__ == "__main__":
    unittest.main() 