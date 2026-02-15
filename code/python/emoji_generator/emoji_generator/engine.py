"""
Two-Stage Matching Engine for Emoji Generator.

This file is heavily annotated with # LEARN: comments so you can circle back
and study the concepts behind each decision. These aren't regular comments --
they're mini-lessons designed to teach TF-IDF, cosine similarity, bigrams,
Levenshtein distance, and the two-stage matching strategy from the ground up.

Architecture:
  Stage 1 -- Lingo Lookup: exact/fuzzy match against all known aliases.
             Catches dev shorthand like "on it", "ack", "lgtm", "ooo", "wip".
  Stage 2 -- TF-IDF Engine: cosine similarity over vectorized descriptions.
             Handles longer natural-language queries like "the pr got merged".
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from rapidfuzz import fuzz
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

# ---------------------------------------------------------------------------
# LEARN: Fuzzy match threshold for the Lingo Lookup (Stage 1).
#
# This is a Levenshtein-based similarity ratio (0-100). When a user's query
# doesn't exactly match any alias, we check if it's "close enough" to catch
# typos like "lgmt" -> "lgtm" or "deploiying" -> "deploying".
#
# 85 means the query must be at least 85% similar to an alias.
# Too low (e.g. 60) and you get false positives: "fix" matches "mix".
# Too high (e.g. 95) and you miss common typos.
# 85 is the sweet spot for short dev phrases.
# ---------------------------------------------------------------------------
FUZZY_THRESHOLD = 85


@dataclass
class MatchResult:
    """A single search result from the matching engine."""

    entry: EmojiEntry
    score: float  # similarity score, 0.0 to 1.0


class LingoLookup:
    """Stage 1: Exact and fuzzy alias matching for dev lingo.

    # LEARN: Why a separate stage for dev lingo?
    #
    # TF-IDF is great for longer natural-language queries, but it BREAKS on
    # short dev phrases like "on it", "ack", "lgtm", "ooo", "wip", "ty".
    # Why?
    #
    # Problem 1 -- Stop words: "on it" -> both words are English stop words
    #   -> TF-IDF removes them -> empty query vector -> no match at all.
    #
    # Problem 2 -- Abbreviations: "lgtm" has no IDF signal because TF-IDF
    #   works on word frequency, and "lgtm" doesn't decompose into meaningful
    #   sub-words. It's an opaque token.
    #
    # Problem 3 -- Too short for statistics: TF-IDF needs enough words to
    #   build a meaningful vector. A 1-2 word query produces a very sparse
    #   vector where random noise dominates.
    #
    # Solution: match these queries DIRECTLY against known aliases using
    # string comparison. Exact match first, then fuzzy match for typos.
    # This is the RIGHT tool for the job: short, known phrases are best
    # handled by lookup, not by statistical text similarity.
    """

    def __init__(self, entries: List[EmojiEntry]) -> None:
        """Build the alias lookup index.

        Creates a normalized dictionary mapping every alias (lowercased,
        stripped) to its parent EmojiEntry. Used for O(1) exact lookups.

        Also stores the list of all (alias, entry) pairs for fuzzy matching.

        Args:
            entries: List of EmojiEntry objects to index.
        """
        # Exact match index: normalized_alias -> EmojiEntry
        self.exact_index: Dict[str, EmojiEntry] = {}

        # All alias pairs for fuzzy matching: [(normalized_alias, entry), ...]
        self.alias_pairs: List[Tuple[str, EmojiEntry]] = []

        for entry in entries:
            # Index the description itself as an alias
            norm_desc = entry.description.lower().strip()
            self.exact_index[norm_desc] = entry
            self.alias_pairs.append((norm_desc, entry))

            # Index each explicit alias
            for alias in entry.aliases:
                norm_alias = alias.lower().strip()
                self.exact_index[norm_alias] = entry
                self.alias_pairs.append((norm_alias, entry))

    def search(self, query: str, top_k: int = 5) -> List[MatchResult]:
        """Search for emoji entries matching the query via alias lookup.

        Strategy:
        1. Exact match: if the query matches an alias verbatim, return it.
        2. Fuzzy match: if no exact match, find the closest aliases using
           Levenshtein-based similarity and return those above the threshold.

        Args:
            query: The user's search text.
            top_k: Maximum results to return.

        Returns:
            List of MatchResult with score=1.0 for exact, or the fuzzy ratio
            (normalized to 0.0-1.0) for fuzzy matches. Empty if nothing found.
        """
        normalized = query.lower().strip()

        # --- Exact match (O(1) dict lookup) ---
        if normalized in self.exact_index:
            return [MatchResult(entry=self.exact_index[normalized], score=1.0)]

        # --- Fuzzy match ---
        # LEARN: Levenshtein Distance & Fuzzy Matching
        #
        # The Levenshtein distance between two strings is the minimum number
        # of single-character edits (insertions, deletions, substitutions)
        # needed to transform one string into the other.
        #
        # Example:
        #   "lgtm" -> "lgmt"   (1 swap = 1 substitution)  distance = 1
        #   "deploy" -> "deploi" (1 substitution)          distance = 1
        #   "ack" -> "acknowledged" (8 insertions)         distance = 8
        #
        # The ALGORITHM (dynamic programming):
        #
        # Build a matrix D where D[i][j] = edit distance between the first
        # i characters of string A and the first j characters of string B.
        #
        #        ""  l  g  m  t       (string B = "lgmt")
        #   ""  [ 0  1  2  3  4 ]
        #   l   [ 1  0  1  2  3 ]
        #   g   [ 2  1  0  1  2 ]
        #   t   [ 3  2  1  1  1 ]    <- "lgt" vs "lgmt" = 1 edit
        #   m   [ 4  3  2  1  2 ]    <- "lgtm" vs "lgmt" = 2? No...
        #
        # Wait -- let's trace more carefully:
        #
        #        ""  l  g  m  t
        #   ""  [ 0  1  2  3  4 ]    base case: transforming "" into "lgmt"
        #   l   [ 1  0  1  2  3 ]    l==l: D[1][1] = D[0][0] = 0
        #   g   [ 2  1  0  1  2 ]    g==g: D[2][2] = D[1][1] = 0
        #   t   [ 3  2  1  1  1 ]    t!=m: min(D[2][2]+1, D[3][2]+1, D[2][3]+1) = 1
        #                             t==t: D[3][4] = D[2][3] = 1
        #   m   [ 4  3  2  1  2 ]    m==m: D[4][3] = D[3][2] = 1
        #                             m!=t: min(D[3][3]+1, D[4][3]+1, D[3][4]+1) = 2
        #
        # Final answer: D[4][4] = 2 (swap "t" and "m" = 2 substitutions)
        #
        # The recurrence relation:
        #   If A[i] == B[j]:
        #       D[i][j] = D[i-1][j-1]          (chars match, no edit needed)
        #   Else:
        #       D[i][j] = 1 + min(
        #           D[i-1][j],      # delete from A
        #           D[i][j-1],      # insert into A
        #           D[i-1][j-1],    # substitute in A
        #       )
        #
        # Time complexity:  O(n * m) where n, m are string lengths
        # Space complexity: O(n * m) for the matrix (can be optimized to O(min(n,m)))
        #
        # RATIO: rapidfuzz converts distance to a 0-100 similarity ratio:
        #   ratio = (1 - distance / max(len(A), len(B))) * 100
        #   "lgtm" vs "lgmt": (1 - 2/4) * 100 = 50  (actually rapidfuzz uses
        #   a more sophisticated normalized score based on optimal alignment)
        #
        # rapidfuzz.fuzz.ratio uses an optimized C implementation that's ~10x
        # faster than the pure Python difflib.SequenceMatcher. For our ~200
        # aliases, it runs in < 1ms.

        scored: List[Tuple[float, EmojiEntry]] = []
        seen_names: set = set()  # deduplicate entries with multiple matching aliases

        for alias, entry in self.alias_pairs:
            if entry.name in seen_names:
                continue

            # LEARN: fuzz.ratio computes a normalized Levenshtein similarity (0-100).
            # It's symmetric: ratio("abc", "abd") == ratio("abd", "abc").
            # We use it instead of raw Levenshtein distance because the ratio
            # accounts for string length -- a 1-char difference in a 4-char
            # string (75%) is more significant than in a 20-char string (95%).
            score = fuzz.ratio(normalized, alias)

            if score >= FUZZY_THRESHOLD:
                seen_names.add(entry.name)
                scored.append((score / 100.0, entry))  # normalize to 0.0-1.0

        # Sort by score descending, take top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [MatchResult(entry=entry, score=s) for s, entry in scored[:top_k]]

    def rebuild(self, entries: List[EmojiEntry]) -> None:
        """Rebuild the alias index with new entries."""
        self.__init__(entries)


class TfidfEngine:
    """Stage 2: TF-IDF based matching for natural language queries.

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
    """

    def __init__(self, entries: List[EmojiEntry]) -> None:
        """Build the TF-IDF index from emoji entries.

        Args:
            entries: List of EmojiEntry objects to index for searching.
        """
        self.entries = entries

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
            # Yes, this means "on it" becomes an empty vector in TF-IDF.
            # That's OK! Stage 1 (LingoLookup) handles "on it" via direct
            # alias matching BEFORE we ever reach TF-IDF. Each stage does
            # what it's best at.
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
        # For our ~45 entries with ~400 features, it doesn't matter much.
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
        """Rebuild the TF-IDF index with new entries."""
        self.__init__(entries)


class EmojiMatchingEngine:
    """Two-stage matching engine combining lingo lookup and TF-IDF.

    # LEARN: Two-Stage Strategy -- why not just one approach?
    #
    # Different types of queries need different tools:
    #
    #   Query type          | Example              | Best tool
    #   --------------------|----------------------|------------------
    #   Short dev lingo     | "on it", "lgtm"      | Exact alias match
    #   Abbreviations       | "ooo", "wip", "ack"  | Exact alias match
    #   Typos               | "lgmt", "deploiying" | Fuzzy string match
    #   Natural language    | "pr got merged"      | TF-IDF + cosine sim
    #   Long descriptions   | "the build is broken"| TF-IDF + cosine sim
    #
    # Stage 1 (LingoLookup) handles the top 3 rows. It's fast (O(1) for exact,
    # O(n) for fuzzy where n = number of aliases) and deterministic.
    #
    # Stage 2 (TfidfEngine) handles the bottom 2 rows. It's statistical and
    # excels at matching partial/paraphrased descriptions.
    #
    # The pipeline is simple:
    #   1. Try lingo lookup first.
    #   2. If it found results, return them (don't bother with TF-IDF).
    #   3. If not, fall through to TF-IDF for deeper text analysis.
    #
    # This means stop_words="english" can stay in TF-IDF without worrying
    # about "on it" breaking, because Stage 1 catches it before TF-IDF
    # ever sees it.
    """

    def __init__(self, entries: List[EmojiEntry]) -> None:
        """Build both stages of the matching engine.

        Args:
            entries: List of EmojiEntry objects to index.
        """
        self.entries = entries
        self.lingo = LingoLookup(entries)
        self.tfidf = TfidfEngine(entries)

    def search(self, query: str, top_k: int = 5) -> List[MatchResult]:
        """Search for emoji entries using the two-stage pipeline.

        Stage 1: Exact/fuzzy alias match (catches lingo, abbreviations, typos).
        Stage 2: TF-IDF cosine similarity (catches natural language).

        Args:
            query: The user's search text.
            top_k: Maximum results to return.

        Returns:
            List of MatchResult sorted by descending score.
            Empty list if no matches found in either stage.
        """
        # Stage 1: Lingo Lookup
        lingo_results = self.lingo.search(query, top_k=top_k)
        if lingo_results:
            return lingo_results

        # Stage 2: TF-IDF (only if lingo found nothing)
        return self.tfidf.search(query, top_k=top_k)

    def rebuild(self, entries: List[EmojiEntry]) -> None:
        """Rebuild both stages with new entries.

        Used by the REPL's hot-reload feature after adding a new emoji.

        Args:
            entries: The updated list of EmojiEntry objects.
        """
        self.entries = entries
        self.lingo.rebuild(entries)
        self.tfidf.rebuild(entries)
