"""
TF-IDF Matching Engine for Emoji Generator.

This file is heavily annotated with # LEARN: comments so you can circle back
and study the concepts behind each decision. These aren't regular comments --
they're mini-lessons designed to teach TF-IDF, cosine similarity, bigrams,
and vectorization from the ground up.
"""

from dataclasses import dataclass
from typing import List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from emoji_generator.registry import EmojiEntry

# ---------------------------------------------------------------------------
# LEARN: What is a "confidence threshold"?
#
# When we compute cosine similarity between a query and an emoji description,
# the score ranges from 0.0 (completely unrelated) to 1.0 (identical text).
#
# In practice, scores for our short-text domain look like:
#   0.0  - 0.10  : garbage, no meaningful overlap
#   0.10 - 0.20  : weak match, probably wrong
#   0.20 - 0.40  : decent match, likely relevant
#   0.40 - 0.70  : strong match, high confidence
#   0.70+        : near-exact wording match
#
# We set MIN_CONFIDENCE at 0.15 as the cutoff. Below this, we tell the user
# "no match found" rather than showing misleading results.
# ---------------------------------------------------------------------------
MIN_CONFIDENCE = 0.15


@dataclass
class MatchResult:
    """A single search result from the matching engine."""

    entry: EmojiEntry
    score: float  # cosine similarity score, 0.0 to 1.0


class EmojiMatchingEngine:
    """TF-IDF based matching engine for finding emoji combos.

    How it works (the big picture):
    1. On init, we take all emoji entries' searchable text and feed them through
       a TF-IDF vectorizer. This creates a matrix where each row is an emoji
       entry and each column is a word/bigram "feature."
    2. When the user queries "pr got merged", we vectorize that query the same
       way and compute cosine similarity against every emoji entry.
    3. We return the top-K entries sorted by similarity score.
    """

    def __init__(self, entries: List[EmojiEntry]) -> None:
        """Build the TF-IDF index from emoji entries.

        Args:
            entries: List of EmojiEntry objects to index for searching.
        """
        self.entries = entries

        # LEARN: TF-IDF stands for "Term Frequency - Inverse Document Frequency."
        #
        # Term Frequency (TF): how often a word appears in ONE document
        #   (here, one emoji's description + aliases).
        #
        # Inverse Document Frequency (IDF): penalizes words that appear in
        #   MANY documents across the entire registry.
        #   e.g. "merge" appears in lots of entries -> lower IDF weight.
        #        "canary" appears rarely -> higher IDF weight.
        #
        # The product TF * IDF gives each word a score per document:
        #   - Common-everywhere words get downweighted (low IDF).
        #   - Distinctive words get boosted (high IDF).
        #
        # This is why a query "canary deploy" matches the canary entry even
        # though "deploy" appears in 10 other entries -- "canary" has high IDF
        # and dominates the match.

        self.vectorizer = TfidfVectorizer(
            # LEARN: ngram_range=(1, 2) means we extract BOTH:
            #   - Unigrams (single words): "merge", "queue", "pull", "request"
            #   - Bigrams (two-word pairs): "merge queue", "pull request"
            #
            # Why bigrams matter:
            #   Without bigrams, "merge queue" and "merge conflicts" would score
            #   similarly for the query "merge queue" because both contain "merge."
            #   With bigrams, "merge queue" as a PHRASE becomes its own feature,
            #   and entries containing that exact phrase get a boost.
            #
            # We don't go to trigrams (ngram_range=(1, 3)) because our descriptions
            # are short -- trigrams would create too many sparse features for little
            # benefit. Bigrams hit the sweet spot for 3-6 word phrases.
            ngram_range=(1, 2),

            # LEARN: stop_words="english" removes common words like
            # "the", "is", "in", "to", "a", "and", "for", etc.
            #
            # These words appear in almost every entry, so their IDF score
            # would be near zero anyway. Removing them upfront:
            #   1. Keeps the vocabulary (feature set) smaller and faster.
            #   2. Prevents the query "will get back to you" from matching
            #      everything just because of "will", "to", and "you."
            #
            # Note: stop-word removal sometimes hurts. For example, "on it"
            # loses both words! But for our dev-lingo domain, the benefit
            # outweighs the occasional miss, because aliases provide fallback.
            stop_words="english",

            # LEARN: sublinear_tf=True applies logarithmic TF scaling.
            #
            # Without it:  tf("deploy") = 5 if "deploy" appears 5 times.
            # With it:     tf("deploy") = 1 + log(5) ≈ 2.6
            #
            # Why? Diminishing returns. If an emoji description repeats "deploy"
            # 5 times, it's not 5x more about deploying than one that mentions
            # it once. Log scaling prevents keyword-stuffed entries from
            # dominating results.
            sublinear_tf=True,
        )

        # LEARN: fit_transform() does TWO things in one call:
        #
        # 1. fit(): Learns the vocabulary from all emoji descriptions.
        #    - Scans every entry's text, builds a list of all unique words/bigrams.
        #    - Computes IDF weights (how rare each word is across all entries).
        #    - Stores this as the vectorizer's "learned" state.
        #
        # 2. transform(): Converts each entry's text into a TF-IDF vector.
        #    - For each entry, counts word/bigram frequencies (TF).
        #    - Multiplies by the IDF weights computed in fit().
        #    - Returns a sparse matrix: rows = entries, columns = features.
        #
        # Why fit_transform() and not fit() + transform() separately?
        # It's an optimization -- internally, scikit-learn can do both passes
        # in a single scan of the data, which is faster than two separate scans.
        #
        # IMPORTANT: The user's query will only use transform() (not fit!),
        # because we want it mapped into the SAME feature space that was
        # learned from the emoji registry. If we re-fit on the query, we'd
        # get a completely different vocabulary and the similarity scores
        # would be meaningless.

        texts = [entry.searchable_text for entry in self.entries]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

        # LEARN: What is a "sparse matrix"?
        #
        # self.tfidf_matrix is a scipy sparse matrix, not a regular numpy array.
        # Why? Most entries only contain a few words out of the full vocabulary.
        # A dense matrix would be mostly zeros (wasteful). Sparse format only
        # stores non-zero values, saving memory and speeding up computation.
        #
        # For our ~35 entries with ~200 features, it doesn't matter much.
        # But the same code scales to thousands of entries without changes.

    def search(self, query: str, top_k: int = 5) -> List[MatchResult]:
        """Find the top-K emoji entries matching a natural language query.

        Args:
            query: Natural language text like "pr got merged" or "deploying now".
            top_k: Number of results to return (default 5).

        Returns:
            List of MatchResult objects sorted by descending similarity score.
            Returns empty list if no matches exceed MIN_CONFIDENCE.
        """
        # LEARN: transform() (not fit_transform!) maps the query into the
        # SAME feature space as the emoji registry.
        #
        # It uses the vocabulary and IDF weights learned during fit().
        # If the query contains a word not in the vocabulary (e.g., "kubernetes"
        # when no entry mentions it), that word is simply ignored -- it gets
        # zero weight because it has no corresponding feature column.
        #
        # This is a key limitation: the engine can only match words it has
        # seen in the registry. That's why good aliases are important!

        query_vector = self.vectorizer.transform([query])

        # LEARN: Cosine Similarity -- why angles, not distances?
        #
        # Each TF-IDF vector is a point in high-dimensional space (one
        # dimension per word/bigram feature). Cosine similarity measures
        # the ANGLE between two vectors, ignoring their magnitude (length).
        #
        # Why not Euclidean distance?
        #   - A long emoji description with many words would have a larger
        #     vector magnitude than a short one, even if both are about
        #     the same topic.
        #   - Euclidean distance would penalize short descriptions unfairly.
        #   - Cosine similarity is scale-invariant: it only cares about the
        #     DIRECTION the vectors point, not how long they are.
        #
        # Intuition: imagine two arrows from the origin. If they point in
        # the same direction (small angle), cosine similarity is close to 1.
        # If they're perpendicular (unrelated topics), it's 0.
        #
        # Formula: cos(θ) = (A · B) / (|A| × |B|)
        #   - A · B is the dot product (sum of element-wise products)
        #   - |A| and |B| are the vector magnitudes (lengths)

        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Build results sorted by score (descending)
        results = []
        for idx in similarities.argsort()[::-1][:top_k]:
            score = float(similarities[idx])
            if score < MIN_CONFIDENCE:
                break  # All remaining scores are even lower, stop here
            results.append(MatchResult(entry=self.entries[idx], score=score))

        return results

    def rebuild(self, entries: List[EmojiEntry]) -> None:
        """Rebuild the TF-IDF index with new entries.

        Used by the REPL's hot-reload feature after adding a new emoji.

        Args:
            entries: The updated list of EmojiEntry objects.
        """
        self.entries = entries
        texts = [entry.searchable_text for entry in self.entries]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
