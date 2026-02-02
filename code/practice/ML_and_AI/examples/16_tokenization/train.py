#!/usr/bin/env python3
"""
Tokenization Demo

Demonstrates character, word, and BPE tokenization.

Usage:
    python train.py
"""

from pathlib import Path
from collections import Counter
import json

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


class CharTokenizer:
    """Character-level tokenizer."""
    
    def __init__(self):
        self.char_to_id = {}
        self.id_to_char = {}
    
    def fit(self, texts: list[str]) -> None:
        chars = set()
        for text in texts:
            chars.update(text)
        
        self.char_to_id = {"<PAD>": 0, "<UNK>": 1}
        for char in sorted(chars):
            self.char_to_id[char] = len(self.char_to_id)
        
        self.id_to_char = {v: k for k, v in self.char_to_id.items()}
    
    def encode(self, text: str) -> list[int]:
        return [self.char_to_id.get(c, 1) for c in text]
    
    def decode(self, ids: list[int]) -> str:
        return "".join(self.id_to_char.get(i, "<UNK>") for i in ids)
    
    @property
    def vocab_size(self) -> int:
        return len(self.char_to_id)


class WordTokenizer:
    """Word-level tokenizer."""
    
    def __init__(self, min_freq: int = 1):
        self.word_to_id = {}
        self.id_to_word = {}
        self.min_freq = min_freq
    
    def fit(self, texts: list[str]) -> None:
        word_counts = Counter()
        for text in texts:
            word_counts.update(text.lower().split())
        
        self.word_to_id = {"<PAD>": 0, "<UNK>": 1}
        for word, count in word_counts.items():
            if count >= self.min_freq:
                self.word_to_id[word] = len(self.word_to_id)
        
        self.id_to_word = {v: k for k, v in self.word_to_id.items()}
    
    def encode(self, text: str) -> list[int]:
        return [self.word_to_id.get(w, 1) for w in text.lower().split()]
    
    def decode(self, ids: list[int]) -> str:
        return " ".join(self.id_to_word.get(i, "<UNK>") for i in ids)
    
    @property
    def vocab_size(self) -> int:
        return len(self.word_to_id)


class SimpleBPE:
    """Simplified Byte-Pair Encoding tokenizer."""
    
    def __init__(self, vocab_size: int = 256):
        self.vocab_size = vocab_size
        self.merges = []  # List of (pair, new_token) merges
        self.vocab = {}
    
    def fit(self, texts: list[str]) -> None:
        # Start with character-level vocab
        self.vocab = {"<PAD>": 0, "<UNK>": 1}
        
        # Add all individual characters
        all_chars = set()
        for text in texts:
            all_chars.update(text)
        
        for char in sorted(all_chars):
            self.vocab[char] = len(self.vocab)
        
        # Tokenize all texts as characters
        tokenized = []
        for text in texts:
            tokens = list(text)
            tokenized.append(tokens)
        
        # BPE merging loop
        while len(self.vocab) < self.vocab_size:
            # Count pairs
            pair_counts = Counter()
            for tokens in tokenized:
                for i in range(len(tokens) - 1):
                    pair = (tokens[i], tokens[i + 1])
                    pair_counts[pair] += 1
            
            if not pair_counts:
                break
            
            # Most frequent pair
            best_pair = pair_counts.most_common(1)[0][0]
            new_token = best_pair[0] + best_pair[1]
            
            self.merges.append((best_pair, new_token))
            self.vocab[new_token] = len(self.vocab)
            
            # Apply merge to all tokenized texts
            for i, tokens in enumerate(tokenized):
                new_tokens = []
                j = 0
                while j < len(tokens):
                    if j < len(tokens) - 1 and (tokens[j], tokens[j + 1]) == best_pair:
                        new_tokens.append(new_token)
                        j += 2
                    else:
                        new_tokens.append(tokens[j])
                        j += 1
                tokenized[i] = new_tokens
        
        self.id_to_token = {v: k for k, v in self.vocab.items()}
    
    def encode(self, text: str) -> list[int]:
        tokens = list(text)
        
        # Apply merges in order
        for pair, new_token in self.merges:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                    new_tokens.append(new_token)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        
        return [self.vocab.get(t, 1) for t in tokens]
    
    def decode(self, ids: list[int]) -> str:
        return "".join(self.id_to_token.get(i, "<UNK>") for i in ids)


def demo_tokenization():
    """Demonstrate all tokenization methods."""
    print("\n" + "=" * 60)
    print("TOKENIZATION DEMO")
    print("=" * 60)
    
    # Sample texts
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is fascinating and powerful.",
        "Natural language processing uses tokenization.",
        "Transformers have revolutionized NLP.",
    ]
    
    test_text = "Machine learning is great!"
    
    print(f"\nTraining on {len(texts)} texts")
    print(f"Test text: '{test_text}'")
    
    # Character tokenizer
    print("\n" + "-" * 40)
    print("1. CHARACTER TOKENIZER")
    print("-" * 40)
    
    char_tok = CharTokenizer()
    char_tok.fit(texts)
    
    encoded = char_tok.encode(test_text)
    decoded = char_tok.decode(encoded)
    
    print(f"Vocab size: {char_tok.vocab_size}")
    print(f"Encoded: {encoded[:20]}... (len={len(encoded)})")
    print(f"Decoded: '{decoded}'")
    
    # Word tokenizer
    print("\n" + "-" * 40)
    print("2. WORD TOKENIZER")
    print("-" * 40)
    
    word_tok = WordTokenizer()
    word_tok.fit(texts)
    
    encoded = word_tok.encode(test_text)
    decoded = word_tok.decode(encoded)
    
    print(f"Vocab size: {word_tok.vocab_size}")
    print(f"Encoded: {encoded} (len={len(encoded)})")
    print(f"Decoded: '{decoded}'")
    
    # BPE tokenizer
    print("\n" + "-" * 40)
    print("3. BPE TOKENIZER (Subword)")
    print("-" * 40)
    
    bpe_tok = SimpleBPE(vocab_size=100)
    bpe_tok.fit(texts)
    
    encoded = bpe_tok.encode(test_text)
    decoded = bpe_tok.decode(encoded)
    
    print(f"Vocab size: {len(bpe_tok.vocab)}")
    print(f"Merges learned: {len(bpe_tok.merges)}")
    print(f"Encoded: {encoded[:15]}... (len={len(encoded)})")
    print(f"Decoded: '{decoded}'")
    
    # Show some BPE merges
    print("\nFirst 10 BPE merges:")
    for pair, new_token in bpe_tok.merges[:10]:
        print(f"  '{pair[0]}' + '{pair[1]}' -> '{new_token}'")
    
    # Try tiktoken if available
    print("\n" + "-" * 40)
    print("4. TIKTOKEN (OpenAI's BPE)")
    print("-" * 40)
    
    try:
        import tiktoken
        
        enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        encoded = enc.encode(test_text)
        decoded = enc.decode(encoded)
        
        print(f"Encoding: cl100k_base (GPT-4)")
        print(f"Vocab size: ~100,000")
        print(f"Encoded: {encoded} (len={len(encoded)})")
        print(f"Decoded: '{decoded}'")
        
        # Show tokens
        print("\nTokens:")
        for token_id in encoded:
            token = enc.decode([token_id])
            print(f"  {token_id:6d} -> '{token}'")
            
    except ImportError:
        print("tiktoken not installed. Install with: pip install tiktoken")
    
    # Save tokenizers
    MODEL_DIR.mkdir(exist_ok=True)
    
    with open(MODEL_DIR / "char_vocab.json", "w") as f:
        json.dump(char_tok.char_to_id, f)
    
    with open(MODEL_DIR / "word_vocab.json", "w") as f:
        json.dump(word_tok.word_to_id, f)
    
    print(f"\nTokenizers saved to: {MODEL_DIR}")
    
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"""
| Tokenizer   | Vocab Size | Sequence Length | Use Case          |
|-------------|------------|-----------------|-------------------|
| Character   | {char_tok.vocab_size:<10} | {len(char_tok.encode(test_text)):<15} | Simple, any text  |
| Word        | {word_tok.vocab_size:<10} | {len(word_tok.encode(test_text)):<15} | Traditional NLP   |
| BPE         | {len(bpe_tok.vocab):<10} | {len(bpe_tok.encode(test_text)):<15} | Modern LLMs       |
    """)


def main():
    demo_tokenization()


if __name__ == "__main__":
    main()
