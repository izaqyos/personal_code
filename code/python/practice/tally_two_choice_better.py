from collections import Counter
from collections.abc import Iterable

def tally_two_choice(candidates: Iterable[str], ballots: Iterable[Iterable[str]]) -> list[tuple[str, int]]:
    """
    Each voter selects up to TWO candidates.
    - Ignore unknown candidate names.
    - Within a single ballot, count each candidate at most once (dedupe).
    - If a ballot lists more than two valid unique candidates, count only the first two encountered.
    - Return all candidates (including zero-vote ones), sorted by votes DESC, then name ASC.
    """
    cand_list = list(candidates)
    cand_set = set(cand_list)
    counts = Counter()

    for ballot in ballots:
        seen = set()
        picked = []
        for choice in ballot:
            if choice in cand_set and choice not in seen:
                picked.append(choice)
                seen.add(choice)
                if len(picked) == 2:
                    break
        counts.update(picked)

    # Ensure zero-vote candidates are included
    for c in cand_list:
        counts.setdefault(c, 0)

    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


# --- Added tests ---
def _run_tests():
    # Base happy path
    cands = ["Alice", "Bob", "Charlie"]
    ballots = [
        ["Alice", "Bob"],
        ["Bob"],
        ["Alice", "Alice", "Charlie"],
        ["Dora", "Alice", "Bob"],             # unknown first -> should count Alice and Bob
        ["Charlie", "Charlie", "Charlie"],     # duplicate within ballot -> counts once
    ]
    res = tally_two_choice(cands, ballots)
    # Verify zero-vote presence (if any) and ordering invariants
    assert ("Alice", 3) in res
    assert ("Bob", 3) in res
    assert ("Charlie", 2) in res
    assert res == sorted(res, key=lambda kv: (-kv[1], kv[0]))

    # Unknown first then two valids → count the first two valid uniques
    assert tally_two_choice(["Alice","Bob","Charlie"], [["Dora","Alice","Bob"]]) == [
        ("Alice", 1), ("Bob", 1), ("Charlie", 0)
    ]

    # Duplicate before second unique → still counts the second unique
    assert tally_two_choice(["Alice","Bob","Charlie"], [["Alice","Alice","Bob"]])[:2] == [
        ("Alice", 1), ("Bob", 1)
    ]

    # Zero-vote candidate included
    res2 = tally_two_choice(["Alice","Bob","Charlie"], [["Alice","Bob"]])
    assert ("Charlie", 0) in res2

    # Tie-break by name ascending
    assert tally_two_choice(["Amy","Bob"], [["Amy"], ["Bob"]]) == [("Amy", 1), ("Bob", 1)]

if __name__ == "__main__":
    _run_tests()
    print("All tests passed.")

