# Bag-of-Words Learning Path

Building on your TF-IDF implementation in `engine.py`.

---

## What You Already Have

Your `EmojiMatchingEngine` covers: TF-IDF vectorization, cosine similarity,
bigrams, stop-word removal, sublinear TF scaling. The LEARN comments in
`engine.py` are thorough. This document picks up where they leave off.

---

## Level 1: Build TF-IDF From Scratch

The single most valuable exercise. You use sklearn's `TfidfVectorizer` as a
black box -- now open it.

**Goal:** Implement TF-IDF + cosine similarity using only `math` and basic
Python. No sklearn, no numpy.

```python
# exercises/tfidf_from_scratch.py
"""
Build TF-IDF from scratch to understand every step.
Target: match sklearn's output for the same inputs.
"""
import math
from collections import Counter

def tokenize(text: str) -> list[str]:
    """Split on whitespace, lowercase. Extend later."""
    return text.lower().split()

def compute_tf(tokens: list[str]) -> dict[str, float]:
    """Term frequency: count / total tokens in this document."""
    counts = Counter(tokens)
    total = len(tokens)
    return {word: count / total for word, count in counts.items()}

def compute_idf(corpus_tokens: list[list[str]]) -> dict[str, float]:
    """Inverse document frequency: log(N / df) for each term."""
    n_docs = len(corpus_tokens)
    df = Counter()  # document frequency
    for doc_tokens in corpus_tokens:
        for word in set(doc_tokens):  # set() = count each word once per doc
            df[word] += 1
    return {word: math.log(n_docs / count) for word, count in df.items()}

def tfidf_vector(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float]:
    """TF-IDF = tf * idf for each term."""
    return {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}

def cosine_sim(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Cosine similarity between two sparse vectors (dicts)."""
    # Dot product: only words in both vectors contribute
    dot = sum(vec_a.get(w, 0) * vec_b.get(w, 0)
              for w in set(vec_a) | set(vec_b))
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

# --- Try it on your emoji data ---
# Load your entries, compute TF-IDF manually, compare to sklearn output.
# They won't match exactly (sklearn uses smoothed IDF, L2 normalization),
# but the ranking should be the same. Understanding WHY they differ is
# the entire point.
```

**What you'll discover:**
- sklearn's IDF uses `log((1 + N) / (1 + df)) + 1` (smoothed), not raw `log(N/df)`
- sklearn L2-normalizes each row, which is why cosine similarity works with just a dot product
- `sublinear_tf=True` replaces `tf` with `1 + log(tf)` -- implement this yourself
- Bigrams are just tokenization: `["merge", "queue"]` also produces `["merge queue"]`

**Validation:** Run both your scratch implementation and sklearn on the same
3-4 emoji descriptions. Print the vectors side by side. Reconcile differences.

---

## Level 2: Understand Your Engine's Blind Spots

Before adding techniques, understand what breaks. Run these queries against
your current engine and observe what happens:

```python
# exercises/blind_spots.py
"""
Test cases that expose TF-IDF limitations in YOUR emoji data.
Run each query and note the result. Then figure out WHY.
"""

TEST_CASES = [
    # (query, expected_emoji_name, why_it_might_fail)

    # STOP WORD REMOVAL: "on" and "it" are both stop words.
    # After removal, the query is EMPTY. Score = 0 for everything.
    ("on it", "on_it", "stop words remove entire query"),

    # VOCABULARY GAP: "k8s" isn't in any emoji description or alias.
    # TF-IDF can only match words it saw during fit(). Unknown = ignored.
    ("k8s deploy", "deploying", "abbreviation not in vocabulary"),

    # TYPO: "mreged" has no overlap with "merged" at the word level.
    # Character-level matching would catch this; word-level can't.
    ("pr got mreged", "pr_approved_merged", "typo has zero word overlap"),

    # SLANG / SEMANTIC GAP: "ship it" means deploy, but "ship" only appears
    # as "shipped" in the registry. Stemming would help (ship->ship).
    ("ship it", "deploying", "unstemmed word mismatch + stop word"),

    # FIGURATIVE LANGUAGE: "on fire" is an alias for crushed_it,
    # but also appears nowhere near "deploying". Does it match?
    ("everything is on fire", "crushed_it", "figurative vs literal meaning"),

    # PARTIAL PHRASE: "ci is red" -- "red build" is an alias for checks_failed.
    # But "red" alone appears in only one entry, so IDF should be high enough.
    ("ci is red", "checks_failed", "partial phrase match via high-IDF word"),

    # NEAR-MISS: "lets sync" should match needs_discussion ("lets sync on this").
    # Bigram "lets sync" helps here -- does it work?
    ("lets sync", "needs_discussion", "bigram should rescue this"),
]

# Run and score:
for query, expected, note in TEST_CASES:
    results = engine.search(query, top_k=3)
    top_match = results[0].entry.name if results else "NO MATCH"
    status = "PASS" if top_match == expected else "FAIL"
    print(f"[{status}] '{query}' -> {top_match} (expected: {expected}) | {note}")
```

**This exercise teaches more than any new algorithm.** You'll see exactly
where BOW breaks and why each remedy (stemming, char n-grams, synonyms) exists.

---

## Level 3: Targeted Fixes

Each fix addresses a specific blind spot from Level 2.

### 3.1 Custom Tokenizer for Dev-Speak

**Fixes:** vocabulary gaps, abbreviation handling, stop-word over-removal.

The default sklearn tokenizer splits on non-alphanumeric characters and
lowercases. This mangles dev terms: `CI/CD` becomes `["ci", "cd"]` (fine),
but `k8s` stays `k8s` (unknown). And stop-word removal kills `"on it"` entirely.

```python
# emoji_generator/tokenizer.py
"""
Custom tokenizer that understands dev abbreviations and protects
short phrases from stop-word annihilation.
"""
import re

# Expand common dev abbreviations BEFORE tokenization
EXPANSIONS = {
    "k8s": "kubernetes",
    "ci/cd": "ci cd continuous integration continuous delivery",
    "pr": "pull request",
    "mr": "merge request",
    "ooo": "out of office",
    "afk": "away from keyboard",
    "rca": "root cause analysis",
    "ff": "feature flag",
}

# Phrases that should survive stop-word removal
PROTECTED_PHRASES = {"on it", "got it"}

def dev_tokenizer(text: str) -> list[str]:
    """Tokenizer that understands dev-speak."""
    text = text.lower().strip()

    # Expand abbreviations
    for abbrev, expansion in EXPANSIONS.items():
        text = re.sub(rf'\b{re.escape(abbrev)}\b', expansion, text)

    # Protect known phrases by joining with underscore
    for phrase in PROTECTED_PHRASES:
        text = text.replace(phrase, phrase.replace(" ", "_"))

    return re.findall(r'[a-z0-9_]+', text)

# Usage:
# TfidfVectorizer(tokenizer=dev_tokenizer, stop_words="english", ...)
# Now "on it" becomes ["on_it"] which survives stop-word removal.
# And "k8s deploy" becomes ["kubernetes", "deploy"] which matches.
```

**Learning concepts:**
- Why tokenization is the most impactful preprocessing step
- Domain-specific tokenizers vs generic ones
- The tension between stop-word removal and short queries

---

### 3.2 Stemming / Lemmatization

**Fixes:** "ship" vs "shipped", "mreged" still won't match (that's 3.3).

```python
# Add to tokenizer or as a preprocessor
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def stemmed_tokenizer(text: str) -> list[str]:
    tokens = dev_tokenizer(text)
    return [stemmer.stem(t) for t in tokens]

# "shipped" -> "ship", "deploying" -> "deploy", "merged" -> "merg"
# Now query "ship it" stems to "ship" and matches "shipped" -> "ship"

# Trade-off: stemming is lossy.
# "merging" and "merged" both become "merg" -- good!
# "university" and "universe" both become "univers" -- bad!
# For dev-speak, stemming is almost always a win.
```

---

### 3.3 Character N-Grams for Typo Tolerance

**Fixes:** "mreged" -> "merged" via character-level overlap.

```python
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer

# You need TWO vectorizers -- char_wb replaces word analysis entirely,
# it does NOT supplement it. Combine them by stacking matrices.

word_vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))

X_words = word_vec.fit_transform(texts)
X_chars = char_vec.fit_transform(texts)
X_combined = hstack([X_words, X_chars])

# Now "mreged" shares char n-grams with "merged":
# "mre", "reg", "ged" overlap with "mer", "erg", "rge", "ged"
# The char-level features rescue the match even though word-level fails.

# Weight trade-off: you may want to weight word features higher:
# X_combined = hstack([X_words * 2.0, X_chars])
```

**Learning concepts:**
- Why you can't just set `analyzer='char_wb'` on a single vectorizer
- Character n-gram range: (3,5) is the sweet spot for typos
- Combining feature spaces with `scipy.sparse.hstack`
- Weighting: word features are more precise, char features add recall

---

### 3.4 Query Expansion with Synonyms

**Fixes:** semantic gaps where user's word doesn't appear in registry.

```python
# emoji_generator/synonyms.py
"""
Expand queries with domain-specific synonyms.
Keep it small and curated -- auto-generated synonyms add noise.
"""

SYNONYMS = {
    "deploy": ["ship", "release", "push", "launch"],
    "bug": ["defect", "issue", "error", "regression"],
    "fix": ["patch", "resolve", "repair"],
    "fast": ["quick", "rapid", "blazing"],
    "help": ["assist", "support", "clarification"],
}

def expand_query(query: str) -> str:
    words = query.lower().split()
    expanded = list(words)  # keep original words
    for word in words:
        if word in SYNONYMS:
            expanded.extend(SYNONYMS[word])
    return " ".join(expanded)

# Careful: expansion increases recall but can hurt precision.
# "deploy fix" expands to "deploy ship release push launch fix patch resolve repair"
# which might match too many things. Test with your blind_spots.py harness.
```

---

### 3.5 BM25 as Alternative Ranker

**Fixes:** TF-IDF's weak document-length normalization.

```python
# pip install rank-bm25
from rank_bm25 import BM25Okapi

class BM25MatchingEngine:
    def __init__(self, entries):
        self.entries = entries
        tokenized = [e.searchable_text.lower().split() for e in entries]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, top_k: int = 5):
        scores = self.bm25.get_scores(query.lower().split())
        top_indices = scores.argsort()[::-1][:top_k]
        return [(self.entries[i], scores[i]) for i in top_indices if scores[i] > 0]
```

**When BM25 actually helps vs TF-IDF:**
- Documents vary widely in length (your emoji entries are ~uniform, so marginal)
- Queries are short, documents are long (opposite of your case)
- You want saturation: a word appearing 10x shouldn't score 10x higher

For your emoji registry (~44 entries, all short), BM25 and TF-IDF will
produce near-identical rankings. But it's worth implementing to understand
the parameters `k1` (term saturation) and `b` (length normalization).

---

## Level 4: Evaluation Harness

Without measurement, everything above is guesswork.

```python
# exercises/evaluate.py
"""
Ground-truth evaluation for comparing engines.
The most important file in this learning path.
"""
from dataclasses import dataclass

@dataclass
class TestCase:
    query: str
    expected: str        # expected top-1 emoji name
    category: str        # what aspect this tests

GROUND_TRUTH = [
    # Exact matches (should always work)
    TestCase("pr merged", "pr_approved_merged", "exact"),
    TestCase("deploying", "deploying", "exact"),
    TestCase("merge conflicts", "merge_conflicts", "exact"),
    TestCase("hotfix", "hotfix", "exact"),

    # Paraphrases (same meaning, different words)
    TestCase("change landed in main", "landed", "paraphrase"),
    TestCase("ci is broken", "checks_failed", "paraphrase"),
    TestCase("not available today", "out_of_office", "paraphrase"),
    TestCase("nice work", "great_job", "paraphrase"),

    # Slang / dev-speak
    TestCase("ship it", "deploying", "slang"),
    TestCase("lgtm", "pr_approved", "slang"),
    TestCase("on it", "on_it", "stop_word_victim"),
    TestCase("wip", "work_in_progress", "abbreviation"),

    # Typos
    TestCase("mreged", "pr_approved_merged", "typo"),
    TestCase("delpoyed", "deployed", "typo"),

    # Ambiguous (multiple valid answers -- just check it's reasonable)
    TestCase("everything is on fire", "crushed_it", "figurative"),
]

def evaluate(engine, test_cases=GROUND_TRUTH):
    """Run evaluation, return metrics."""
    correct = 0
    results = []
    for tc in test_cases:
        matches = engine.search(tc.query, top_k=3)
        top_1 = matches[0].entry.name if matches else "NO_MATCH"
        passed = top_1 == tc.expected
        correct += passed
        results.append((tc, top_1, passed))

    precision_at_1 = correct / len(test_cases)

    # Print report
    for tc, got, passed in results:
        icon = "PASS" if passed else "FAIL"
        print(f"[{icon}] [{tc.category}] '{tc.query}' -> {got}"
              f"{'' if passed else f' (expected: {tc.expected})'}")

    print(f"\nPrecision@1: {precision_at_1:.0%} ({correct}/{len(test_cases)})")
    return precision_at_1

# Usage:
# baseline = evaluate(tfidf_engine)        # e.g. 65%
# with_stemming = evaluate(stemmed_engine)  # e.g. 75%
# with_char_ngrams = evaluate(combo_engine) # e.g. 80%
# Each fix should move the number up. If it doesn't, you learned something.
```

**Metrics to understand:**
- **Precision@1**: did the top result match? (most important for your tool)
- **MRR (Mean Reciprocal Rank)**: where did the correct result appear? (1/rank)
- **Recall@5**: is the correct result in the top 5?

---

## Level 5: Document Similarity

Not query matching -- find which emojis are similar to each other.

```python
# emoji_generator/similarity.py
from sklearn.metrics.pairwise import cosine_similarity

def similarity_matrix(engine):
    """All-pairs similarity between emoji entries."""
    sim = cosine_similarity(engine.tfidf_matrix)
    return sim

def find_similar(engine, emoji_name: str, top_k: int = 5):
    """Find emojis most similar to a given one."""
    idx = next(i for i, e in enumerate(engine.entries) if e.name == emoji_name)
    scores = cosine_similarity(engine.tfidf_matrix[idx], engine.tfidf_matrix).flatten()
    ranked = scores.argsort()[::-1][1:top_k+1]  # skip self
    return [(engine.entries[i].name, float(scores[i])) for i in ranked]

# Try it:
# find_similar(engine, "deploying")
# -> [("deployed", 0.72), ("shipped", 0.55), ("rollback", 0.31), ...]
# This reveals overlap in your registry. If two entries are > 0.8 similar,
# maybe they should be merged.
```

**CLI extension:** add `devmoji --similar "deployed"` to your CLI.

---

## What's Next: Beyond Bag-of-Words

Once you've exhausted BOW, here's the landscape -- high level.

```
YOU ARE HERE
    |
    v
[ Bag-of-Words ]  -- words as independent features, no semantics
    |
    | What's missing: word ORDER, MEANING, CONTEXT
    |
    v
[ Word Embeddings ]  -- Word2Vec, GloVe, FastText
    |
    | Words become dense vectors in semantic space.
    | "ship" and "deploy" are nearby. "ship" and "banana" are far.
    | Solves the synonym problem WITHOUT a manual synonym dict.
    |
    | Key idea: average word vectors to get document vectors.
    | Limitation: loses word order ("dog bites man" = "man bites dog")
    |
    v
[ Sentence Embeddings ]  -- Sentence-BERT, all-MiniLM-L6-v2
    |
    | Entire sentences become vectors. Order matters.
    | Pre-trained on massive corpora. Near-zero effort to use.
    | This is what you'd use in production for semantic search.
    |
    | pip install sentence-transformers
    | model.encode(["pr got merged"])  # -> 384-dim vector
    |
    v
[ Topic Models ]  -- LSA (SVD), LDA
    |
    | Discover latent topics: "deployment", "code review", "incidents"
    | Each document is a mixture of topics.
    | Useful for clustering and exploration, less for search.
    |
    | LSA = SVD on TF-IDF matrix (linear algebra)
    | LDA = probabilistic model (Bayesian inference)
    |
    v
[ Neural Retrieval ]  -- ColBERT, dense retrieval, cross-encoders
    |
    | State of the art for search. Expensive but accurate.
    | Bi-encoders for recall, cross-encoders for re-ranking.
    | Probably overkill for 44 emoji entries, but the concepts
    | power every modern search engine.
    |
    v
[ RAG ]  -- Retrieval-Augmented Generation
    |
    | Combine retrieval with LLMs.
    | Retrieve relevant docs, feed to LLM for answer synthesis.
    | The architecture behind ChatGPT plugins, Perplexity, etc.
```

### Suggested Exploration Order

| Phase | Topic | Time | What You Build |
|-------|-------|------|----------------|
| 1 | Word2Vec (gensim) | Weekend | Replace TF-IDF engine, compare precision@1 |
| 2 | Sentence Transformers | 2-3 hours | Drop-in engine, benchmark all 3 approaches |
| 3 | LSA/LDA | Weekend | Topic discovery on your emoji categories |
| 4 | FAISS vector search | 1 day | Scale to thousands of entries efficiently |
| 5 | RAG pattern | Project | Build a "smart" code search over your repos |

### Key Insight

For 44 short-text emoji entries, TF-IDF with good tokenization will match
or beat Word2Vec. Embeddings shine when you have thousands of documents
and diverse vocabulary. Understanding WHY is the whole point of this path.

### Reading

- Manning, Raghavan, Schutze: *Introduction to Information Retrieval* (free online)
  - Ch 1-2: Boolean + TF-IDF fundamentals
  - Ch 6: Scoring and ranking
  - Ch 16-18: Clustering, LSI, topic models
- Jurafsky & Martin: *Speech and Language Processing* (free online)
  - Ch 6: Vector semantics and embeddings

---

## Suggested File Layout

```
emoji_generator/
  engine.py               # Current TF-IDF (keep as primary)
  tokenizer.py            # Custom dev-speak tokenizer (Level 3.1)
  synonyms.py             # Query expansion (Level 3.4)
  similarity.py           # Document similarity (Level 5)
  exercises/
    tfidf_from_scratch.py  # Level 1
    blind_spots.py         # Level 2
    evaluate.py            # Level 4
```

Keep it lean. Add engines only when evaluation proves they're better.

---

**Last Updated:** 2026-02-15
