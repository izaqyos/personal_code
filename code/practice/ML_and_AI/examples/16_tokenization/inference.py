#!/usr/bin/env python3
"""Tokenization Reference"""


def show_reference():
    print("\n" + "=" * 60)
    print("TOKENIZATION REFERENCE")
    print("=" * 60)
    
    print("""
SPECIAL TOKENS
--------------
<PAD>  - Padding (makes sequences same length)
<UNK>  - Unknown token (OOV words)
<BOS>  - Beginning of sequence
<EOS>  - End of sequence
<CLS>  - Classification token (BERT)
<SEP>  - Separator token (BERT)
<MASK> - Masked token (for MLM training)

COMMON TOKENIZERS
-----------------
| Model   | Tokenizer | Vocab Size |
|---------|-----------|------------|
| GPT-2   | BPE       | 50,257     |
| GPT-3/4 | BPE       | 100,277    |
| BERT    | WordPiece | 30,522     |
| T5      | SentencePiece | 32,000 |
| LLaMA   | SentencePiece | 32,000 |

TIKTOKEN ENCODINGS
------------------
- cl100k_base: GPT-4, GPT-3.5-turbo
- p50k_base: Codex, text-davinci-002/003
- r50k_base: GPT-3 (davinci)
- o200k_base: GPT-4o

USAGE EXAMPLE
-------------
```python
import tiktoken

# Get encoding
enc = tiktoken.get_encoding("cl100k_base")

# Encode
tokens = enc.encode("Hello, world!")  # [9906, 11, 1917, 0]

# Decode
text = enc.decode([9906, 11, 1917, 0])  # "Hello, world!"

# Count tokens
num_tokens = len(enc.encode("Some text"))
```
    """)


if __name__ == "__main__":
    show_reference()
