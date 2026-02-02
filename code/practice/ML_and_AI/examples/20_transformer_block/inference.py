#!/usr/bin/env python3
"""Transformer Block Reference"""


def show_reference():
    print("\n" + "=" * 60)
    print("TRANSFORMER ARCHITECTURE REFERENCE")
    print("=" * 60)
    
    print("""
TRANSFORMER BLOCK (Encoder)
---------------------------

                Input (batch, seq_len, d_model)
                    │
                    ▼
    ┌───────────────────────────────────┐
    │           LayerNorm               │
    └───────────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │      Multi-Head Attention         │
    │   (Q, K, V all from same input)   │
    └───────────────────────────────────┘
                    │
                    │◄────── + (residual)
                    │
                    ▼
    ┌───────────────────────────────────┐
    │           LayerNorm               │
    └───────────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │      Feed-Forward Network         │
    │     (Linear → GELU → Linear)      │
    │     (d_model → 4*d_model → d_model)│
    └───────────────────────────────────┘
                    │
                    │◄────── + (residual)
                    │
                    ▼
                Output (batch, seq_len, d_model)


PRE-LN vs POST-LN
-----------------

Post-LN (Original, 2017):
    x → Attention → + → LayerNorm → FFN → + → LayerNorm → out
                    ↑                      ↑
                    x                      x

Pre-LN (Modern, more stable):
    x → LayerNorm → Attention → + → LayerNorm → FFN → + → out
                                ↑                      ↑
                                x                      x


MODEL SIZES
-----------

| Model       | Layers | d_model | Heads | d_ff  | Params  |
|-------------|--------|---------|-------|-------|---------|
| GPT-2 Small | 12     | 768     | 12    | 3072  | 117M    |
| GPT-2 Large | 36     | 1280    | 20    | 5120  | 774M    |
| GPT-3       | 96     | 12288   | 96    | 49152 | 175B    |
| LLaMA 7B    | 32     | 4096    | 32    | 11008 | 7B      |
| LLaMA 70B   | 80     | 8192    | 64    | 28672 | 70B     |


COMMON MODIFICATIONS
--------------------

1. RoPE (Rotary Position Embedding):
   - Encodes position in attention computation
   - Used by LLaMA, GPT-NeoX

2. SwiGLU Activation:
   - FFN: Linear → SwiGLU → Linear
   - Used by LLaMA, PaLM

3. Grouped Query Attention (GQA):
   - Share K, V heads across multiple Q heads
   - More efficient, used by LLaMA 2

4. Flash Attention:
   - Memory-efficient attention computation
   - O(n) memory instead of O(n²)


PYTORCH IMPLEMENTATION
----------------------

# Using nn.TransformerEncoderLayer
layer = nn.TransformerEncoderLayer(
    d_model=512,
    nhead=8,
    dim_feedforward=2048,
    dropout=0.1,
    activation='gelu',
    batch_first=True,
    norm_first=True,  # Pre-LN
)

# Stack layers
encoder = nn.TransformerEncoder(layer, num_layers=6)

output = encoder(x)
    """)


if __name__ == "__main__":
    show_reference()
