"""
TF-IDF from scratch — dicts + math only, no numpy, no sklearn.

Track item: ML Models / Phase 1 / "TF-IDF" — implement from scratch, compare with sklearn.

DON'T PEEK: BOW_LEARNING_PATH.md Level 1 contains a fully worked TF-IDF
solution. It exists to describe the destination, not to be copy-pasted here.
Implement the functions below yourself first; use that doc only to check
your work after tests pass.

========================================================================
THEORY — what TF-IDF adds on top of BOW
========================================================================

You already built BOW (bow_from_scratch.py): count vectors, one axis per
vocab word, cosine similarity for "same direction = same topic." BOW's
failure mode you found in Q2/Q4 there: every word counts equally, so
"the" (appears everywhere) pulls exactly as much weight as "lgtm"
(appears in one entry). TF-IDF's whole point is fixing THAT ONE problem —
nothing else. It still can't see order, negation, synonyms, or stems;
that ladder is unchanged from BOW's docstring.

The fix has two halves multiplied together:

  TF (term frequency) — how important is this word to THIS document?
  IDF (inverse document frequency) — how rare is this word ACROSS the
  whole corpus, i.e. how much does seeing it actually tell you?

  weight(word, doc) = TF(word, doc) * IDF(word, corpus)

TF variants (same length-bias question as BOW Q4, applied to the weight
inside one document instead of the raw count):
  - raw:        count(word, doc)                    — biased by doc length
  - normalized: count(word, doc) / len(doc)          — a frequency, length-invariant
  - sublinear:  1 + log(count(word, doc))  if count > 0 else 0
                — diminishing returns: 10 occurrences isn't 10x the signal
                  of 1 (this is `sublinear_tf=True` in engine.py)

IDF variants — this is the part BOW didn't have at all:
  - raw:      log(N / df(word))               where N = num docs, df = doc frequency
  - smoothed: log((1 + N) / (1 + df(word))) + 1     — what sklearn actually uses

Why does sklearn bother smoothing? Two failure modes of the raw formula:
  1. A word in EVERY document has df == N, so log(N/df) == log(1) == 0.
     Zero IDF means that word vanishes from every TF-IDF vector no matter
     how much TF says about it. Reasonable in the limit, but harsh in a
     small corpus where "reasonably common" and "in literally every doc"
     are one unlucky example apart.
  2. A brand-new word at QUERY time (never seen when IDF was computed)
     has no entry in the idf dict at all — not df=0 (that would be
     division by zero), just *absent*. tfidf_vector has to decide what
     that word is worth. Compare this to BOW's Q3 (OOV token contributes
     nothing to the count vector): same root cause, different mechanism.

Once you have per-word weights, TF-IDF vectors are just sparse dicts
(word -> weight), and cosine similarity from BOW comes back almost
unchanged — ALMOST. That "almost" is Q4 below; don't skip it.

Pipeline you're building:

    corpus (list[str])
        -> tokenize each doc              (list[list[str]])
        -> compute_tf per doc             (word -> tf weight, one dict per doc)
        -> compute_idf over whole corpus  (word -> idf weight, one dict, shared)
        -> tfidf_vector per doc           (word -> tf*idf weight)
        -> cosine_sim between docs        (float, same shape as BOW's version)

Questions to answer WHILE implementing (write answers as comments at the
bottom, same convention as bow_from_scratch.py):

  Q1. Sklearn's smoothed IDF never produces log(1) == 0, and never
      divides by zero for an unseen df. Walk through the smoothed formula
      with df == N (word in every doc) and explain in one sentence why
      the result is small-but-nonzero instead of exactly zero.
  A1.

  Q2. sublinear TF (1 + log(count)) vs raw count: is this solving the
      SAME length-bias problem as normalized TF (count/len), a
      DIFFERENT problem, or both? (Hint: think about a single document
      where one word appears 50 times vs 2 times — does normalized TF
      fix that? Does sublinear?)
  A2.

  Q3. A query contains a word that never appeared anywhere in the corpus
      compute_idf was built from. What should tfidf_vector do with it,
      and how is that decision similar to / different from BOW's
      out-of-vocabulary handling (BOW Q3)?
  A3.

  Q4. BOW's cosine_sim checked `if not a.any(): return 0.0` — an exact
      equality check, safe because counts are integers and an
      empty/OOV-only vector is EXACTLY all zeros. Your TF-IDF vectors are
      floats. Why might checking `magnitude == 0.0` exactly be the wrong
      guard here, and what should you use instead? (This is the
      epsilon-guard beat — think about what floating point arithmetic
      can produce that is "basically zero" but not "== 0.0".)
  A4.

  Q5. sklearn's TfidfVectorizer L2-normalizes every row (divides each
      vector by its own magnitude) as the LAST step of fit_transform.
      If you did that here, what would change about cosine_sim's job?
      (You don't have to implement row normalization — just say what it
      would buy you.)
  A5.

Stretch (after tests pass): run your tfidf_vector output and sklearn's
TfidfVectorizer side by side on the same corpus. They will NOT match
exactly even with smooth=True — figure out why (L2 normalization is one
reason; there's a second one about how ties in log-space get handled).
Then try the emoji entries from engine.py and compare rankings, not raw
numbers.
"""

import math
from collections import Counter


def tokenize(text: str) -> list[str]:
    """Lowercase, split on whitespace. Same dumb tokenizer as BOW."""
    return text.lower().split()


def compute_tf(tokens: list[str], variant: str = "normalized") -> dict[str, float]:
    """Term frequency for one document.

    variant:
      "raw"        -> plain count
      "normalized" -> count / total tokens in this doc
      "sublinear"  -> 1 + log(count) for count > 0, else absent

    Words not present in `tokens` should not appear in the returned dict
    (this stays a sparse representation, like BOW's zero-skipping).
    """
    raise NotImplementedError


def compute_idf(corpus_tokens: list[list[str]], smooth: bool = True) -> dict[str, float]:
    """Inverse document frequency over the whole corpus.

    smooth=True  -> log((1 + N) / (1 + df)) + 1   (sklearn's formula)
    smooth=False -> log(N / df)                   (textbook formula, can be 0)

    Every word that appears in ANY document must get an idf entry —
    this dict is the frozen vocabulary + weights that later queries get
    transformed against (see Q3).
    """
    raise NotImplementedError


def tfidf_vector(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float]:
    """Combine one document's TF dict with the corpus IDF dict.

    A word in `tf` but missing from `idf` (see Q3) should not crash this —
    decide what it contributes and be able to justify it.
    """
    raise NotImplementedError


def cosine_sim(vec_a: dict[str, float], vec_b: dict[str, float], eps: float = 1e-12) -> float:
    """Cosine similarity between two sparse TF-IDF vectors (dicts).

    Dot product: sum over words in EITHER vector of vec_a.get(w,0)*vec_b.get(w,0)
    (words absent from one side contribute 0 — same idea as BOW's dot product).

    Guard the denominator with `eps`, not an exact `== 0.0` check (Q4).
    """
    raise NotImplementedError


if __name__ == "__main__":
    corpus = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "cats and dogs",
    ]
    corpus_tokens = [tokenize(doc) for doc in corpus]

    # --- TF: raw vs normalized vs sublinear, checked against hand counts ---
    tf0_raw = compute_tf(corpus_tokens[0], variant="raw")
    assert tf0_raw["the"] == 2 and tf0_raw["cat"] == 1, \
        f"raw TF is just counts, got {tf0_raw}"

    tf0_norm = compute_tf(corpus_tokens[0], variant="normalized")
    assert abs(tf0_norm["the"] - 2 / 6) < 1e-9, \
        f"'the' appears 2x in a 6-token doc -> 2/6, got {tf0_norm['the']}"
    assert abs(tf0_norm["cat"] - 1 / 6) < 1e-9

    tf0_sub = compute_tf(corpus_tokens[0], variant="sublinear")
    assert abs(tf0_sub["the"] - (1 + math.log(2))) < 1e-9, \
        "sublinear('the', count=2) must be 1 + log(2)"
    assert abs(tf0_sub["cat"] - (1 + math.log(1))) < 1e-9, \
        "sublinear(count=1) must be 1 + log(1) == 1.0"

    # --- IDF: raw vs smoothed, oracle computed independently right here ---
    idf_raw = compute_idf(corpus_tokens, smooth=False)
    idf_smooth = compute_idf(corpus_tokens, smooth=True)

    df = Counter()
    for doc_tokens in corpus_tokens:
        for w in set(doc_tokens):
            df[w] += 1
    n_docs = len(corpus_tokens)

    for word, doc_freq in df.items():
        expected_raw = math.log(n_docs / doc_freq)
        expected_smooth = math.log((1 + n_docs) / (1 + doc_freq)) + 1
        assert abs(idf_raw[word] - expected_raw) < 1e-9, \
            f"raw idf mismatch for {word!r}: {idf_raw[word]} vs {expected_raw}"
        assert abs(idf_smooth[word] - expected_smooth) < 1e-9, \
            f"smoothed idf mismatch for {word!r}: {idf_smooth[word]} vs {expected_smooth}"

    # 'the', 'sat', 'on' appear in 2 of 3 docs -> lower idf than words unique to one doc
    assert idf_smooth["cat"] > idf_smooth["the"], \
        "a word unique to one doc must score higher idf than one shared across docs"

    # --- tfidf_vector: combine tf and idf ---
    doc0_tf = compute_tf(corpus_tokens[0], variant="normalized")
    doc0_vec = tfidf_vector(doc0_tf, idf_smooth)
    assert abs(doc0_vec["cat"] - doc0_tf["cat"] * idf_smooth["cat"]) < 1e-9

    # word present in tf but absent from a DIFFERENT idf table (simulates query-time OOV, Q3)
    tiny_idf = {"the": idf_smooth["the"]}  # deliberately missing "cat"
    oov_vec = tfidf_vector(doc0_tf, tiny_idf)
    assert "cat" not in oov_vec or oov_vec["cat"] == 0.0, \
        "a word with no idf entry must not silently get an arbitrary nonzero weight"

    # --- cosine_sim: build full corpus vectors, check ranking (not hand-computed floats) ---
    tfs = [compute_tf(toks, variant="normalized") for toks in corpus_tokens]
    vecs = [tfidf_vector(tf, idf_smooth) for tf in tfs]

    assert abs(cosine_sim(vecs[0], vecs[0]) - 1.0) < 1e-9, "self-similarity is 1"

    sim_01 = cosine_sim(vecs[0], vecs[1])  # share "the", "sat", "on"
    sim_02 = cosine_sim(vecs[0], vecs[2])  # share nothing ("cat" != "cats")
    assert sim_02 == 0.0, "'cat' vs 'cats' still share zero tokens at word level"
    assert sim_01 > sim_02, "shared words must score higher than zero shared words"
    assert 0.0 < sim_01 < 1.0, f"expected a partial match in (0, 1), got {sim_01}"

    # --- epsilon guard: an all-empty vector must not crash or divide by zero ---
    assert cosine_sim(vecs[0], {}) == 0.0, "empty vector (e.g. all-OOV query) must not crash"
    assert cosine_sim({}, {}) == 0.0

    print("ALL TESTS PASS")
    print("Now answer Q1-Q5 as comments above, then try the sklearn stretch.")
