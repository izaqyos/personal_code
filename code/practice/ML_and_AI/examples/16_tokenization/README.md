# Tokenization

Converting text into tokens for neural network processing.

## Concepts Covered

- **Character-level**: Each character is a token
- **Word-level**: Each word is a token
- **Subword (BPE)**: Byte-Pair Encoding (used by GPT, BERT)
- **Vocabulary**: Mapping tokens to integer IDs

## Tokenization Methods

| Method | Pros | Cons |
|--------|------|------|
| Character | Small vocab, handles any text | Long sequences |
| Word | Intuitive | OOV problem, large vocab |
| BPE/Subword | Balance of both | Requires training |

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **BPE**: Most common for modern LLMs
2. **Special Tokens**: [PAD], [UNK], [CLS], [SEP], [MASK]
3. **Vocabulary Size**: Trade-off between coverage and efficiency
4. **Tiktoken**: OpenAI's fast BPE implementation
