from collections import Counter
from collections.abc import Iterable

def tally_two_choice(candidates: Iterable[str], ballots: Iterable[Iterable[str]]) -> list[tuple[str, int]]:
    """
    Each voter selects up to TWO candidates.
    Rules:
      - Ignore unknown candidate names.
      - Within a single ballot, count each candidate at most once (dedupe).
      - If a ballot lists more than two valid unique candidates, count only the first two encountered.
      - Return all candidates (including zero-vote ones), sorted by votes DESC, then name ASC.
    """
    candidates_votes = list()
    flat_dedup_ballots = [ elem for sublist in ballots for elem in set(sublist[:2]) if elem in candidates ]
    ballots_count = Counter(flat_dedup_ballots)
    candidates_votes = [ (k, ballots_count[k]) for k in ballots_count ]
    return sorted(candidates_votes, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    cands = ["Alice", "Bob", "Charlie"]
    # Five voters, two choices each
    ballots = [
        ["Alice", "Bob"],
        ["Alice", "Charlie"],
        ["Bob", "Charlie"],
        ["Alice", "Bob"],
        ["Charlie", "Alice"],
    ]
    got = tally_two_choice(cands, ballots)
    expected = [("Alice", 4), ("Bob", 3), ("Charlie", 3)]
    print(got)
    assert got == expected, f"Unexpected two-choice tally: {got}"

    # Dedupe, unknown, and >2 choices handled
    ballots2 = [
        ["Alice", "Alice"],                 # duplicate -> counts once for Alice
        ["Bob", "Dora"],                    # Dora ignored
        ["Charlie", "Bob", "Alice"],       # >2 -> first two valid: Charlie, Bob
        ["Charlie", "Charlie", "Charlie"], # duplicate -> one for Charlie
        ["Alice", "Bob", "Charlie"],       # >2 -> first two valid: Alice, Bob
    ]
    got2 = tally_two_choice(cands, ballots2)
    expected2 = [("Bob", 3), ("Alice", 2), ("Charlie", 2)]
    print(got2)
    assert got2 == expected2, f"Unexpected two-choice tally #2: {got2}"
    print("QOTD #3b OK")
