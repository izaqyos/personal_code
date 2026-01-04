# Tokenization

> Converting text to numbers - the first step in NLP.

---

## Overview

Neural networks need numbers, not text. Tokenization converts text into a sequence of tokens (integers).

```
Text: "Hello, world!"

Character level: ['H','e','l','l','o',',',' ','w','o','r','l','d','!']
                 [72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]

Word level:      ['Hello', ',', 'world', '!']
                 [1523, 8, 892, 15]

Subword level:   ['Hello', ',', ' world', '!']
                 [9906, 11, 995, 0]
```

---

## Tokenization Methods

### Character-Level

```
Vocabulary: All characters (~100-300 tokens)

Pros:
- Tiny vocabulary
- Handles any word/typo
- No unknown tokens

Cons:
- Very long sequences
- Hard to capture meaning
- Each char = 1 token (inefficient)

"Hello" → ['H', 'e', 'l', 'l', 'o'] → [72, 101, 108, 108, 111]
```

### Word-Level

```
Vocabulary: All words (~100,000+ tokens)

Pros:
- Each word = 1 token (efficient)
- Captures word meaning

Cons:
- Huge vocabulary
- Out-of-vocabulary (OOV) problem
- Can't handle typos/new words

"Hello" → ['Hello'] → [1523]
"Helloooo" → [UNK] → [0]  # Unknown!
```

### Subword-Level (Modern Standard)

```
Split words into meaningful subunits:

"unhappiness" → ['un', 'happiness'] or ['un', 'happ', 'iness']

Pros:
- Balanced vocabulary size (30k-50k)
- Handles rare/new words
- Efficient representation

Cons:
- Slightly more complex
- Language-dependent
```

---

## Byte-Pair Encoding (BPE)

Most popular subword algorithm (used by GPT):

### Training Algorithm

```
1. Start with character vocabulary
2. Count all adjacent pairs
3. Merge most frequent pair → new token
4. Repeat until vocabulary size reached

Example:
Corpus: "low lower lowest"

Step 0: Vocab = {l, o, w, e, r, s, t, _}
        Tokens: l o w _ l o w e r _ l o w e s t _

Step 1: Most frequent pair: (l, o) → "lo"
        Vocab = {..., lo}
        Tokens: lo w _ lo w e r _ lo w e s t _

Step 2: Most frequent pair: (lo, w) → "low"
        Vocab = {..., low}
        Tokens: low _ low e r _ low e s t _

Step 3: Most frequent pair: (low, _) → "low_"
        Vocab = {..., low_}
        Tokens: low_ low e r _ low e s t _

...continue until desired vocab size
```

### Tokenizing New Text

```
def bpe_tokenize(text, merges):
    tokens = list(text)
    while True:
        # Find all pairs
        pairs = get_pairs(tokens)
        # Find pair with highest priority in merges
        best_pair = min(pairs, key=lambda p: merges.get(p, float('inf')))
        if best_pair not in merges:
            break
        # Merge
        tokens = merge(tokens, best_pair)
    return tokens
```

---

## WordPiece

Variant of BPE (used by BERT):

```
Difference: Uses likelihood instead of frequency

Merge criterion: Maximize P(corpus) = Π P(token)

"playing" → ["play", "##ing"]  # ## marks continuation

BERT vocabulary:
- 30,522 tokens
- Includes [CLS], [SEP], [MASK], [PAD], [UNK]
```

---

## SentencePiece / Unigram

Alternative algorithm (used by many models):

```
Start with large vocabulary, prune tokens that hurt likelihood least

"unbelievable" might become:
- ["▁un", "believ", "able"] or
- ["▁unbeliev", "able"]

▁ (lower one eighth block) marks word start
```

---

## Special Tokens

Most tokenizers include special tokens:

```
[PAD]   (0)    - Padding for batching
[UNK]   (1)    - Unknown token
[CLS]   (101)  - Classification token (BERT)
[SEP]   (102)  - Separator token (BERT)
[MASK]  (103)  - Masking for MLM (BERT)

GPT-style:
<|endoftext|>   - End of document
<|im_start|>    - Start of message (chat)
<|im_end|>      - End of message (chat)
```

---

## Implementation

### Using Hugging Face Tokenizers

```python
from transformers import AutoTokenizer

# Load pretrained tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Tokenize text
text = "Hello, how are you doing today?"
tokens = tokenizer.tokenize(text)
print(tokens)
# ['Hello', ',', ' how', ' are', ' you', ' doing', ' today', '?']

# Convert to IDs
token_ids = tokenizer.encode(text)
print(token_ids)
# [15496, 11, 703, 389, 345, 1804, 1909, 30]

# Decode back to text
decoded = tokenizer.decode(token_ids)
print(decoded)
# "Hello, how are you doing today?"

# Full encoding with attention mask
encoding = tokenizer(text, return_tensors="pt")
print(encoding)
# {'input_ids': tensor([[15496, ...]]),
#  'attention_mask': tensor([[1, 1, 1, ...]])}
```

### Training Custom BPE Tokenizer

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Initialize
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

# Trainer
trainer = BpeTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]
)

# Train on files
tokenizer.train(files=["corpus.txt"], trainer=trainer)

# Save
tokenizer.save("my-tokenizer.json")

# Use
output = tokenizer.encode("Hello, world!")
print(output.tokens)
print(output.ids)
```

### Tiktoken (OpenAI's Tokenizer)

```python
import tiktoken

# Load encoding for specific model
enc = tiktoken.encoding_for_model("gpt-4")

# Encode
tokens = enc.encode("Hello, how are you?")
print(tokens)  # [9906, 11, 1268, 527, 499, 30]

# Decode
text = enc.decode(tokens)
print(text)  # "Hello, how are you?"

# Count tokens (useful for API limits)
num_tokens = len(enc.encode("Your text here"))
print(f"Token count: {num_tokens}")
```

---

## Token Counts and Context Limits

```
Model context limits:
GPT-3.5:      4,096 tokens (~3,000 words)
GPT-4:        8,192 or 32,768 or 128,000 tokens
Claude:       100,000+ tokens

Rule of thumb:
- 1 token ≈ 4 characters (English)
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

Non-English often uses more tokens:
"Hello" → 1 token
"こんにちは" → 3-5 tokens
"🎉" → 1-2 tokens
```

---

## Tokenization Gotchas

```python
# Whitespace matters!
tokenizer.encode("Hello")    # [15496]
tokenizer.encode(" Hello")   # [18435]  # Different!

# Numbers are weird
tokenizer.encode("2023")     # [1238, 1954]  # Split!
tokenizer.encode("$100")     # [3, 1558]     # $ separate

# Special characters
tokenizer.encode("don't")    # ['don', "'", 't']  # Apostrophe splits

# Capitalization
tokenizer.encode("Apple")    # Different from
tokenizer.encode("apple")    # Different tokens!
```

---

## Exercises

1. **Implement**: Write BPE training from scratch
2. **Compare**: Tokenize same text with GPT-2, BERT, and T5 tokenizers
3. **Analyze**: What tokens make up your name? Any surprises?
4. **Custom**: Train a tokenizer on code vs natural language. Compare
5. **Efficiency**: Compare token counts: English vs Chinese vs code

---

## Key Takeaways

- Tokenization converts text to integers for models
- Subword tokenization (BPE, WordPiece) balances vocabulary size and coverage
- Different models use different tokenizers
- Whitespace and special characters can behave unexpectedly
- Token count determines context usage

---

## Next Steps

→ Continue to [02-embeddings.md](./02-embeddings.md)
