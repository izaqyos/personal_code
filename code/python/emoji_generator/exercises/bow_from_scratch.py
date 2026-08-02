"""
Bag of Words from scratch — numpy only.

Track item: ML Models / Phase 1 / "Bag of Words (BOW)" — vectorize sentences in numpy.

The exercise: turn a corpus of sentences into count vectors, then measure
similarity between them — using only numpy. No sklearn, no Counter magic
you don't understand.

========================================================================
THEORY — how Bag of Words actually works
========================================================================

The core move. Text is variable-length and symbolic; math wants
fixed-length and numeric. BOW is the simplest bridge: pick a fixed
vocabulary of V words, then represent ANY document as a vector of V
numbers where position j holds "how many times does vocab word j appear
in this document". That single decision buys you all of linear algebra —
distance, similarity, matrix factorization, classifiers — at the cost of
throwing away everything BUT word identity and count.

Why "bag"? A bag (multiset) is a set that remembers multiplicity but not
order. "dog bites man" and "man bites dog" produce the IDENTICAL vector.
BOW's modeling assumption, stated honestly: the meaning of a document is
approximated by which words occur and how often, independent of order,
position, or context. Obviously false in general — and yet strong enough
to power decades of spam filters, search engines, and topic models.
Knowing WHERE the assumption breaks (negation: "not good"; word order;
polysemy: "bank") tells you when to reach for n-grams or embeddings.

The vector space picture. Each vocab word is one AXIS of a V-dimensional
space; each document is one POINT (equivalently, an arrow from the
origin). Documents about similar things use overlapping words, so their
arrows point in similar directions. That geometric intuition is why
"similarity" becomes an angle:

    cos(a, b) = (a . b) / (|a| * |b|)

Why the angle and not euclidean distance? Length of a BOW vector grows
with document LENGTH (a doc concatenated with itself doubles its vector
but means the same thing). Cosine ignores magnitude and compares only
direction — it's length-invariant, which is exactly the invariance you
want for "are these about the same thing". For count vectors (all
entries >= 0) cosine lands in [0, 1]: 1 = same direction (same word
proportions), 0 = orthogonal (no shared words at all).

The dot product, read out loud: a . b = sum over every vocab word of
(count in a) x (count in b). Words absent from either doc contribute 0,
so ONLY shared words move the score — the dot product literally counts
weighted word overlap. That also means BOW vectors are mostly zeros
(each doc uses a tiny slice of the vocabulary), which is why real
systems store them sparse (Q5).

The matrix view. Stack n document vectors into an n x V "document-term
matrix" M. Rows are documents, columns are words. Suddenly whole-corpus
questions are one matrix op: M @ M.T gives all-pairs dot products,
column sums give corpus word frequencies. LSA is literally an SVD of
this matrix; your TfidfVectorizer in engine.py builds exactly this, just
sparse and reweighted.

What BOW cannot see (the ladder out): every word is its own axis, so
"cat" and "cats" — and "deploy" and "ship" — are as unrelated as "cat"
and "carburetor" (orthogonal, similarity 0). Fixes, in increasing
ambition: stemming folds inflections onto one axis; n-grams sneak local
order back in as extra axes; TF-IDF (your next exercise) reweights axes
so rare words count more than common ones; embeddings abandon
one-axis-per-word entirely and place related words NEAR each other in a
dense space. Each rung of that ladder exists to patch a specific hole
you can point at in this file's test corpus.
========================================================================

Pipeline you're building:

    corpus (list[str])
        -> tokenize each doc          (list[list[str]])
        -> build_vocab                (word -> column index)
        -> bow_vector per doc         (np.ndarray of counts, len == vocab size)
        -> bow_matrix                 (n_docs x vocab_size)
        -> cosine_sim between rows    (float in [0, 1] for count vectors)

Questions to answer WHILE implementing (write answers as comments at the
bottom — this is the "knowledge & understanding" part):

  Q1. Why must the vocabulary have a deterministic word->index order?
      What silently breaks if two runs order it differently?
  A1.    the cos sim between two rows should be the same regardless of the order.
      what breaks is different vectors r created 4 same vocab across different runs
      depending on random order

  Q2. "the cat sat" vs "cats sit there" — what similarity does BOW give,
      and what does that tell you about BOW's core limitation?
      0 similarity b/c it doesn't use embeddings (semantic meaining repr) and doesn't factor in stem, past,future plural singular etc

  Q3. What happens to a query word that's not in the vocabulary?
      What does that imply for a search engine built on BOW?
      if not in vocab sim is 0 similarity b/c it doesn't have any count
      search engine on Bow needs full vocab

  Q4. Variants: raw counts vs binary (0/1) vs frequency (count/len).
      When does each matter? (Hint: think long doc vs short doc.)
      raw count - biased towards doc length , good when magnitude is signal (like spam indicating words)
      binary - signal capped at 1, good 4 short docs
      freq - loses magnitude bias , can lose "sensitivity" low weight to key word

  Q5. Your bow_matrix is dense. Estimate its memory for vocab=100k words,
      docs=1M, float64. Why does every real system use sparse matrices?
      1M * 100K * 64bit = 10^6 * 10^5 * 8 bytes = 8*10^11 bytes = 800GB 

Stretch (after tests pass): compare your vocab + counts against
sklearn.feature_extraction.text.CountVectorizer on the same corpus.
Expect differences — its default token_pattern drops 1-char tokens.
Reconciling why is the point.
"""

import numpy as np


def tokenize(text: str) -> list[str]:
    """Lowercase, split on whitespace. Keep it dumb on purpose."""
    return text.lower().split()


def build_vocab(corpus: list[str]) -> dict[str, int]:
    """Map each unique token in the corpus to a column index.

    Order must be deterministic (see Q1). Convention for the tests:
    alphabetically sorted vocabulary -> indices 0..V-1.
    """
    vocab = set()
    for doc in corpus:
        doc_words = tokenize(doc)
        vocab.update(doc_words)
    vocab_list = sorted(vocab)
    return {word: idx for idx, word in enumerate(vocab_list) }


def bow_vector(tokens: list[str], vocab: dict[str, int]) -> np.ndarray:
    """Count vector for one document. Length == len(vocab).

    Tokens not in vocab are ignored (see Q3).
    """
    ndarr = np.zeros(len(vocab), dtype=int)
    for token in tokens:
        if token in vocab:
            ndarr[vocab[token]] += 1
    return ndarr


def bow_matrix(corpus: list[str], vocab: dict[str, int]) -> np.ndarray:
    """Stack bow_vectors for the whole corpus: shape (n_docs, len(vocab))."""
    return np.vstack([ bow_vector(tokenize(doc), vocab) for doc in corpus])


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors, in numpy.

    Handle the all-zero vector (return 0.0 — why can it occur here?).
    """
    assert a.ndim == 1 and b.ndim == 1, "cosine_sim expects 1-D vectors"
    if not a.any() or not b.any():
        return 0.0
    return float((a@b)/(np.linalg.norm(a) * np.linalg.norm(b) ))


if __name__ == "__main__":
    corpus = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "cats and dogs",
    ]

    vocab = build_vocab(corpus)

    # --- vocabulary ---
    assert len(vocab) == 10, f"expected 10 unique words, got {len(vocab)}"
    assert sorted(vocab) == list(vocab) or list(vocab.keys()) == sorted(vocab.keys()), \
        "vocab must be alphabetically ordered"
    assert vocab["and"] == 0 and vocab["the"] == 9, \
        "alphabetical convention: 'and' first, 'the' last"

    # --- single vector ---
    v0 = bow_vector(tokenize(corpus[0]), vocab)
    assert isinstance(v0, np.ndarray), "must be a numpy array"
    assert v0.shape == (10,), f"expected shape (10,), got {v0.shape}"
    assert v0[vocab["the"]] == 2, "'the' appears twice in doc 0"
    assert v0[vocab["cat"]] == 1
    assert v0[vocab["dog"]] == 0
    assert v0.sum() == 6, "doc 0 has 6 tokens total"

    # --- out-of-vocabulary tokens are ignored ---
    vq = bow_vector(tokenize("the zebra"), vocab)
    assert vq.sum() == 1, "'zebra' is OOV and must contribute nothing"

    # --- matrix ---
    M = bow_matrix(corpus, vocab)
    assert M.shape == (3, 10)
    assert np.array_equal(M[0], v0)

    # --- cosine similarity ---
    assert abs(cosine_sim(M[0], M[0]) - 1.0) < 1e-9, "self-similarity is 1"
    assert abs(cosine_sim(M[0], M[1]) - 0.75) < 1e-9, \
        "docs 0 and 1 share 'the'x2, 'sat', 'on' -> exactly 0.75 (do the math by hand!)"
    assert cosine_sim(M[0], M[2]) == 0.0, \
        "'cat' vs 'cats': zero overlap — that's Q2 staring at you"
    assert cosine_sim(M[0], np.zeros(10)) == 0.0, "zero vector must not crash"

    print("ALL TESTS PASS — 12/12")
    print("Now answer Q1-Q5 as comments below, then try the sklearn stretch.")
