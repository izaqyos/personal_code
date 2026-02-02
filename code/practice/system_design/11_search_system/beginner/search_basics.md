# Exercise: Search System Basics

## Objective
Understand search engine fundamentals.

## Tasks

### Task 1: Inverted Index
Explain inverted index with example:
```
Documents:
  Doc1: "the quick brown fox"
  Doc2: "the lazy dog"
  Doc3: "quick brown dog"

Inverted Index:
  // TODO: Build the index
```

### Task 2: Tokenization
Design tokenization for: "Hello, World! It's 2024."
- Tokens: ___
- Lowercase: ___
- Remove punctuation: ___
- Stemming: ___

### Task 3: TF-IDF
Calculate TF-IDF for "quick" in Doc1:
- TF (term frequency): ___
- IDF (inverse document frequency): ___
- TF-IDF: ___

---

<details>
<summary>Solution</summary>

**Inverted Index:**
```
the → [Doc1, Doc2]
quick → [Doc1, Doc3]
brown → [Doc1, Doc3]
fox → [Doc1]
lazy → [Doc2]
dog → [Doc2, Doc3]
```

**TF-IDF:** TF=1/4, IDF=log(3/2)=0.176, TF-IDF=0.044.

</details>
