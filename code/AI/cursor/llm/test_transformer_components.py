import unittest
import torch
import numpy as np
from transformer_components import (
    FeedForwardNetwork,
    GLU,
    LayerNorm,
    RMSNorm,
    TransformerBlock
)


class TestTransformerComponents(unittest.TestCase):
    def setUp(self):
        # Common test parameters
        self.batch_size = 4
        self.seq_len = 16
        self.d_model = 64
        self.d_ff = 256
        self.num_heads = 8
        
        # Create random input tensor
        self.x = torch.randn(self.batch_size, self.seq_len, self.d_model)
        
        # Create a mask for testing the transformer block
        self.mask = torch.tril(torch.ones(self.seq_len, self.seq_len)).unsqueeze(0)
        self.mask = self.mask.repeat(self.batch_size, 1, 1)

    def test_feed_forward_network_shape(self):
        """Test that the feed-forward network produces correct output shapes."""
        ffn = FeedForwardNetwork(self.d_model, self.d_ff)
        output = ffn(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_feed_forward_network_projection(self):
        """Test that the feed-forward network correctly projects to higher dimensions and back."""
        # Create a simplified FFN for testing
        d_model = 4
        d_ff = 8
        
        # Create deterministic weights
        ffn = FeedForwardNetwork(d_model, d_ff, dropout=0)
        
        # Set weights manually for reproducible test
        with torch.no_grad():
            ffn.linear1.weight.fill_(0.1)
            ffn.linear1.bias.fill_(0.1)
            ffn.linear2.weight.fill_(0.1)
            ffn.linear2.bias.fill_(0.1)
        
        # Create a simple input with known values
        x = torch.ones(1, 1, d_model)
        
        # Compute expected output manually
        # First projection: (1*0.1 + 0.1) * 4 = 0.8 after adding all inputs
        # ReLU keeps it at 0.8 for all neurons in hidden layer
        # Second projection: (0.8*0.1 + 0.1) * 8 = 0.74 after adding all inputs
        expected = torch.ones(1, 1, d_model) * 0.74
        
        # Get actual output
        output = ffn(x)
        
        # Check that outputs match expected values
        self.assertTrue(torch.allclose(output, expected, rtol=1e-4))
    
    def test_glu_shape(self):
        """Test that the GLU produces correct output shapes."""
        glu = GLU(self.d_model, self.d_ff)
        output = glu(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_glu_mechanisms(self):
        """Test that GLU's gating mechanism works correctly."""
        d_model = 4
        d_ff = 4
        
        # Test with sigmoid activation
        glu = GLU(d_model, d_ff, activation='sigmoid')
        
        # Set weights manually for reproducible test
        with torch.no_grad():
            # First weight for both gate and value parts
            glu.linear.weight.fill_(0.1)
            glu.linear.bias[:d_ff].fill_(0.0)  # gate bias
            glu.linear.bias[d_ff:].fill_(1.0)  # value bias
            
            # Second projection weight
            glu.linear2.weight.fill_(0.2)
            glu.linear2.bias.fill_(0.0)
        
        # Create a simple input with known values
        x = torch.ones(1, 1, d_model)
        
        # Get actual output
        output = glu(x)
        
        # Check gating works (output should be less than without gating)
        # Value computed with biases should be 1.4
        # Gate should be sigmoid(0.4) ~= 0.6
        # So gated value is about 1.4 * 0.6 = 0.84 before final projection
        
        # Final projection should be around 0.84 * 0.2 * 4 = 0.672
        self.assertTrue(output.mean().item() < 1.0)
        self.assertTrue(output.mean().item() > 0.0)
    
    def test_layer_norm_shape(self):
        """Test that layer normalization produces correct output shapes."""
        ln = LayerNorm(self.d_model)
        output = ln(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_layer_norm_statistics(self):
        """Test that layer normalization correctly normalizes the input."""
        ln = LayerNorm(self.d_model)
        output = ln(self.x)
        
        # Compute mean and standard deviation along the last dimension
        means = output.mean(dim=-1)
        stds = output.std(dim=-1)
        
        # Check that the means are close to 0 and stds are close to 1
        # Note: They may not be exactly 0 and 1 due to the learnable parameters
        self.assertTrue(torch.allclose(means, torch.zeros_like(means), atol=1e-5))
        
        # If weights are initialized to 1, the std should be close to 1
        self.assertTrue(torch.allclose(stds, torch.ones_like(stds), atol=0.1))
    
    def test_rms_norm_shape(self):
        """Test that RMS normalization produces correct output shapes."""
        rmsn = RMSNorm(self.d_model)
        output = rmsn(self.x)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_rms_norm_statistics(self):
        """Test that RMS normalization correctly normalizes the input."""
        rmsn = RMSNorm(self.d_model)
        output = rmsn(self.x)
        
        # Compute mean and RMS along the last dimension
        means = output.mean(dim=-1)
        rms = torch.sqrt(torch.mean(output**2, dim=-1))
        
        # RMS norm doesn't center the data, so means can be anything
        # But RMS should be close to 1 (if weights are initialized to 1)
        self.assertTrue(torch.allclose(rms, torch.ones_like(rms), atol=0.1))
    
    def test_transformer_block_shape(self):
        """Test that the transformer block produces correct output shapes."""
        transformer_block = TransformerBlock(self.d_model, self.num_heads, self.d_ff)
        output = transformer_block(self.x, self.mask)
        
        self.assertEqual(output.shape, (self.batch_size, self.seq_len, self.d_model))
    
    def test_transformer_block_masking(self):
        """Test that the transformer block correctly uses masks."""
        # Create a transformer block
        transformer_block = TransformerBlock(self.d_model, self.num_heads, self.d_ff)
        
        # Run with and without mask
        output_with_mask = transformer_block(self.x, self.mask)
        output_without_mask = transformer_block(self.x, None)
        
        # The outputs should be different when using a mask
        self.assertFalse(torch.allclose(output_with_mask, output_without_mask))
    
    def test_pre_vs_post_norm(self):
        """Test that pre-norm and post-norm variants behave differently."""
        pre_norm_block = TransformerBlock(self.d_model, self.num_heads, self.d_ff, pre_norm=True)
        post_norm_block = TransformerBlock(self.d_model, self.num_heads, self.d_ff, pre_norm=False)
        
        # Run both blocks with the same input
        output_pre_norm = pre_norm_block(self.x, self.mask)
        output_post_norm = post_norm_block(self.x, self.mask)
        
        # The outputs should be different for different normalization strategies
        self.assertFalse(torch.allclose(output_pre_norm, output_post_norm))
        
        # Check that post-norm outputs are more normalized (closer to mean 0, std 1)
        pre_norm_std = output_pre_norm.std()
        post_norm_std = output_post_norm.std()
        
        # Post-norm should have the final layer norm applied
        self.assertLess(torch.abs(post_norm_std - 1.0), torch.abs(pre_norm_std - 1.0))
    
    def test_gradient_flow(self):
        """Test that gradients flow correctly through the transformer block."""
        transformer_block = TransformerBlock(self.d_model, self.num_heads, self.d_ff)
        
        # Create an input that requires gradients
        x = self.x.clone().detach().requires_grad_(True)
        
        # Forward pass
        output = transformer_block(x, self.mask)
        
        # Create a mock loss that's just the sum of the output
        loss = output.sum()
        
        # Backward pass
        loss.backward()
        
        # Check that gradients were computed for the input
        self.assertIsNotNone(x.grad)
        self.assertFalse(torch.allclose(x.grad, torch.zeros_like(x.grad)))
        
        # Ensure gradients aren't too small or too large (which might indicate vanishing/exploding gradients)
        grad_mean = x.grad.abs().mean().item()
        self.assertTrue(0.0001 < grad_mean < 10.0)


if __name__ == "__main__":
    unittest.main() 