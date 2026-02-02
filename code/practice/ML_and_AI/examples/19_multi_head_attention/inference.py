#!/usr/bin/env python3
"""Multi-Head Attention Reference"""


def show_reference():
    print("\n" + "=" * 60)
    print("MULTI-HEAD ATTENTION REFERENCE")
    print("=" * 60)
    
    print("""
THE FORMULA
-----------

MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W^O

where head_i = Attention(Q @ W_i^Q, K @ W_i^K, V @ W_i^V)


DIMENSION BREAKDOWN
-------------------

Given d_model = 512, num_heads = 8:

    d_head = d_model / num_heads = 64

Input:  (batch, seq_len, 512)
        ↓
Split:  (batch, 8, seq_len, 64)  <- 8 parallel heads
        ↓
Each head does attention independently:
        Attention((seq, 64), (seq, 64), (seq, 64))
        ↓
Merge:  (batch, seq_len, 512)  <- Concatenate all heads
        ↓
Output: W^O projection (512 → 512)


WHY MULTIPLE HEADS?
-------------------

Different heads learn to focus on different things:

    Head 1: Syntactic relationships (subject-verb)
    Head 2: Semantic similarity
    Head 3: Positional patterns
    Head 4: Coreference (pronouns → nouns)
    ...

This is like having 8 experts looking at the same data
from different angles.


PARAMETER COUNT
---------------

For d_model=512, num_heads=8:

    W_q: 512 × 512 = 262,144
    W_k: 512 × 512 = 262,144
    W_v: 512 × 512 = 262,144
    W_o: 512 × 512 = 262,144
    ----------------------------
    Total: ~1M parameters per MHA layer


COMMON CONFIGURATIONS
---------------------

| Model      | d_model | num_heads | d_head |
|------------|---------|-----------|--------|
| BERT-base  | 768     | 12        | 64     |
| BERT-large | 1024    | 16        | 64     |
| GPT-2      | 768     | 12        | 64     |
| GPT-3      | 12288   | 96        | 128    |
| GPT-4      | ~?      | ~120?     | ~128?  |


PYTORCH IMPLEMENTATION
----------------------

# Using nn.MultiheadAttention
mha = nn.MultiheadAttention(
    embed_dim=512,
    num_heads=8,
    dropout=0.1,
    batch_first=True,  # Important!
)

output, attn_weights = mha(query, key, value)
    """)


if __name__ == "__main__":
    show_reference()
