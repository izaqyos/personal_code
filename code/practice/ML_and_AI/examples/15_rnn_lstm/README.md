# Recurrent Neural Networks (RNN) and LSTM

Neural networks for sequential data.

## Concepts Covered

- **RNN**: Process sequences with hidden state
- **Vanishing Gradients**: Problem with long sequences
- **LSTM**: Long Short-Term Memory cells
- **Gates**: Forget, Input, Output gates

## Architecture

```
RNN: h_t = tanh(W_hh * h_{t-1} + W_xh * x_t)

LSTM:
  f_t = σ(W_f · [h_{t-1}, x_t])     # Forget gate
  i_t = σ(W_i · [h_{t-1}, x_t])     # Input gate
  C̃_t = tanh(W_C · [h_{t-1}, x_t])  # Candidate
  C_t = f_t * C_{t-1} + i_t * C̃_t   # Cell state
  o_t = σ(W_o · [h_{t-1}, x_t])     # Output gate
  h_t = o_t * tanh(C_t)             # Hidden state
```

## Usage

```bash
python train.py
python train.py --hidden-size 64 --epochs 20
python inference.py
```

## Key Takeaways

1. **Hidden State**: Carries information through sequence
2. **LSTM Gates**: Control what to remember/forget
3. **Bidirectional**: Process sequence both directions
4. **Sequence Length**: Longer = harder to train vanilla RNN
