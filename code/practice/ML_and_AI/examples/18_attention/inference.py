#!/usr/bin/env python3
"""Attention Mechanism Reference"""


def show_reference():
    print("\n" + "=" * 60)
    print("ATTENTION MECHANISM REFERENCE")
    print("=" * 60)
    
    print("""
THE ATTENTION FORMULA
---------------------

    Attention(Q, K, V) = softmax(QK^T / √d_k) · V

Where:
    Q = Query  (what am I looking for?)
    K = Key    (what information is available?)
    V = Value  (what information to retrieve?)
    d_k = dimension of keys (for scaling)

STEP BY STEP
------------

1. COMPUTE SCORES
   scores = Q @ K^T
   Shape: (seq_len, seq_len)

2. SCALE
   scaled_scores = scores / √d_k
   Why? Prevents softmax saturation for large d_k

3. MASK (optional)
   For causal/autoregressive models:
   scores[future positions] = -inf

4. SOFTMAX
   attention_weights = softmax(scaled_scores, dim=-1)
   Each row sums to 1 (probability distribution)

5. WEIGHTED SUM
   output = attention_weights @ V
   Each output position is weighted combination of values

TYPES OF ATTENTION
------------------

Self-Attention:
    Q, K, V all come from same sequence
    Used in encoder

Cross-Attention:
    Q from one sequence, K/V from another
    Used in decoder (attending to encoder output)

Causal/Masked Attention:
    Future positions masked out
    Used in decoder for autoregressive generation

COMPLEXITY
----------

Time:  O(n² · d)  where n = sequence length
Space: O(n²)      for attention weights matrix

This is why long-context models are expensive!

VISUALIZATION
-------------

Attention weights can be visualized as heatmaps:

         Key positions
       ┌─────────────────┐
    Q  │ 0.1  0.7  0.1  0.1 │ <- Position 0 attends mostly to position 1
    u  │ 0.2  0.2  0.5  0.1 │ <- Position 1 attends mostly to position 2
    e  │ 0.1  0.1  0.3  0.5 │ <- etc.
    r  │ 0.3  0.2  0.2  0.3 │
    y  └─────────────────┘
    """)


if __name__ == "__main__":
    show_reference()
