# Transformer Block

The complete encoder block combining all components.

## Concepts Covered

- **Multi-Head Attention**: The attention mechanism
- **Layer Normalization**: Stabilize training
- **Feed-Forward Network**: Position-wise MLP
- **Residual Connections**: Skip connections for gradient flow

## Architecture

```
Input
  │
  ├──────────────────────────┐
  ▼                          │
[Multi-Head Attention]       │
  │                          │
  └─────────────────────(+)──┘ <- Residual
                          │
                  [LayerNorm]
                          │
  ├──────────────────────────┐
  ▼                          │
[Feed-Forward Network]       │
  │                          │
  └─────────────────────(+)──┘ <- Residual
                          │
                  [LayerNorm]
                          │
                        Output
```

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Pre-LN vs Post-LN**: Modern models use Pre-LayerNorm (more stable)
2. **FFN Expansion**: Usually 4x the model dimension
3. **Stacking**: GPT-3 has 96 of these blocks
4. **Residual Importance**: Critical for training deep networks
