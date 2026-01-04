# Recurrent Neural Networks (RNNs) and LSTMs

> Neural networks for sequential data - time series, text, and more.

---

## Why Recurrent Networks?

Standard networks can't handle sequences:
- Variable length inputs
- Order matters
- Long-range dependencies

```
Sequence:  "The cat sat on the ___"
           ↓   ↓   ↓   ↓   ↓    ↓
Standard: Each word processed independently (no context!)

RNN:      h₁ → h₂ → h₃ → h₄ → h₅ → h₆
          ↑    ↑    ↑    ↑    ↑    ↑
          The  cat  sat  on  the   ?
          (context flows through hidden state)
```

---

## Vanilla RNN

### Architecture

```
        h_{t-1} ──────┐
                      ↓
        x_t ───→ [   RNN   ] ───→ h_t ───→ y_t
                  Cell

Equations:
h_t = tanh(W_hh × h_{t-1} + W_xh × x_t + b_h)
y_t = W_hy × h_t + b_y
```

### Unrolled View

```
        h₀ → [RNN] → h₁ → [RNN] → h₂ → [RNN] → h₃
              ↑           ↑           ↑
              x₁          x₂          x₃
              ↓           ↓           ↓
              y₁          y₂          y₃

Same weights shared across all timesteps!
```

---

## The Vanishing Gradient Problem

Gradients decay exponentially over long sequences:

```
∂L/∂h₁ = ∂L/∂h_T × ∂h_T/∂h_{T-1} × ... × ∂h₂/∂h₁

Each ∂h_t/∂h_{t-1} involves W_hh and tanh derivative (≤1)

If |W_hh| < 1: Gradients → 0 (vanishing)
If |W_hh| > 1: Gradients → ∞ (exploding)

Result: Can't learn long-range dependencies
"The cat, which was sitting on the mat, ___" → forgets "cat"
```

---

## LSTM (Long Short-Term Memory)

Solves vanishing gradient with **gating mechanisms**:

```
                    ┌───────────────────────────┐
                    │         LSTM Cell          │
                    │                            │
    c_{t-1} ───────→│─→ [×] ────→ [+] ─────────→│───→ c_t
                    │    ↑         ↑             │
                    │   f_t       i_t⊙c̃_t       │
                    │                            │
    h_{t-1} ───→    │   ┌─────────────────┐     │
                    │   │ Gates           │     │
    x_t ────────→   │   │ f: forget       │     │───→ h_t
                    │   │ i: input        │     │
                    │   │ o: output       │     │
                    │   │ c̃: candidate    │     │
                    │   └─────────────────┘     │
                    └───────────────────────────┘

Key insight: Cell state c flows with only linear operations
(addition) - gradients flow unchanged!
```

### LSTM Equations

```
# Gates (all sigmoid → output in [0,1])
f_t = σ(W_f × [h_{t-1}, x_t] + b_f)    # Forget gate
i_t = σ(W_i × [h_{t-1}, x_t] + b_i)    # Input gate
o_t = σ(W_o × [h_{t-1}, x_t] + b_o)    # Output gate

# Candidate cell state
c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c)

# Update cell state
c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t

# Output hidden state
h_t = o_t ⊙ tanh(c_t)

Where ⊙ is element-wise multiplication
```

### Gate Intuition

```
Forget Gate (f_t): What to remove from memory?
"The cat sat on the mat. The dog ___"
→ Forget "cat", remember "dog"

Input Gate (i_t): What new info to add?
"The dog ran quickly"
→ Add "dog" + "ran" to memory

Output Gate (o_t): What to output now?
"The dog ran to the ___"
→ Output info relevant for next word prediction
```

---

## GRU (Gated Recurrent Unit)

Simplified LSTM with only 2 gates:

```
# Reset and update gates
r_t = σ(W_r × [h_{t-1}, x_t])
z_t = σ(W_z × [h_{t-1}, x_t])

# Candidate hidden state
h̃_t = tanh(W × [r_t ⊙ h_{t-1}, x_t])

# Final hidden state
h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t

Fewer parameters than LSTM, often similar performance
```

---

## Implementation

### PyTorch LSTM

```python
import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim,
                 n_layers=2, dropout=0.5, bidirectional=False):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            dropout=dropout if n_layers > 1 else 0,
            bidirectional=bidirectional,
            batch_first=True
        )

        direction_factor = 2 if bidirectional else 1
        self.fc = nn.Linear(hidden_dim * direction_factor, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: [batch, seq_len]
        embedded = self.dropout(self.embedding(x))
        # embedded: [batch, seq_len, embedding_dim]

        outputs, (hidden, cell) = self.lstm(embedded)
        # outputs: [batch, seq_len, hidden_dim * directions]
        # hidden: [n_layers * directions, batch, hidden_dim]

        # Use final hidden state
        if self.lstm.bidirectional:
            hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        else:
            hidden = hidden[-1]

        return self.fc(self.dropout(hidden))

# Usage
model = LSTMModel(
    vocab_size=10000,
    embedding_dim=256,
    hidden_dim=512,
    output_dim=2,  # binary classification
    n_layers=2,
    bidirectional=True
)

# Input: batch of tokenized sequences
x = torch.randint(0, 10000, (32, 100))  # [batch, seq_len]
output = model(x)  # [32, 2]
```

### LSTM from Scratch

```python
import numpy as np

class LSTMCell:
    def __init__(self, input_size, hidden_size):
        # Initialize weights
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.01

        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def forward(self, x, h_prev, c_prev):
        # Concatenate input and previous hidden state
        concat = np.vstack([h_prev, x])

        # Gates
        f = self.sigmoid(self.Wf @ concat + self.bf)
        i = self.sigmoid(self.Wi @ concat + self.bi)
        o = self.sigmoid(self.Wo @ concat + self.bo)
        c_tilde = np.tanh(self.Wc @ concat + self.bc)

        # Update cell and hidden state
        c = f * c_prev + i * c_tilde
        h = o * np.tanh(c)

        # Cache for backprop
        self.cache = (x, h_prev, c_prev, f, i, o, c_tilde, c, h, concat)

        return h, c
```

---

## RNN Architectures

### Many-to-One (Classification)

```
h₁ → h₂ → h₃ → h₄ → h₅
↑    ↑    ↑    ↑    ↑
x₁   x₂   x₃   x₄   x₅
                    ↓
                   output

Use case: Sentiment analysis, document classification
```

### One-to-Many (Generation)

```
                h₁ → h₂ → h₃ → h₄
                ↑
input ─────────→
                     ↓    ↓    ↓
                    y₁   y₂   y₃

Use case: Image captioning, music generation
```

### Many-to-Many (Sequence-to-Sequence)

```
Encoder:     h₁ → h₂ → h₃ → context
             ↑    ↑    ↑
             x₁   x₂   x₃

Decoder:                    h₁' → h₂' → h₃'
                            ↑     ↑     ↑
                        context  y₁'   y₂'
                                  ↓     ↓
                                 y₁'   y₂'  y₃'

Use case: Translation, summarization
```

### Bidirectional RNN

```
Forward:  h₁→ → h₂→ → h₃→
          ↑     ↑     ↑
          x₁    x₂    x₃
          ↓     ↓     ↓
Backward: h₁← ← h₂← ← h₃←

Output: [h_t→, h_t←] concatenated

Sees both past AND future context
```

---

## Attention Mechanism (Preview)

RNNs struggle with very long sequences. Attention helps:

```
Instead of encoding entire sequence into one vector,
attend to relevant parts at each decoding step.

Query: "What should I focus on for this output?"
Keys/Values: Encoded representations of all input positions

This leads to Transformers (next module)!
```

---

## Exercises

1. **Implement**: Build vanilla RNN from scratch, show vanishing gradient
2. **Compare**: LSTM vs GRU on sequence classification task
3. **Bidirectional**: Train bidirectional LSTM, compare to unidirectional
4. **Generation**: Build character-level LSTM for text generation
5. **Attention**: Add simple attention to encoder-decoder model

---

## Key Takeaways

- RNNs process sequences by maintaining hidden state
- Vanilla RNNs suffer from vanishing gradients
- LSTMs use gates to control information flow
- Cell state provides "highway" for gradients
- GRUs are simpler alternative to LSTMs
- Bidirectional RNNs see both past and future
- Modern NLP has largely moved to Transformers

---

## Track Complete!

You've completed the Neural Networks track. Next:
→ Continue to [03-transformers-llms/01-tokenization.md](../03-transformers-llms/01-tokenization.md)
