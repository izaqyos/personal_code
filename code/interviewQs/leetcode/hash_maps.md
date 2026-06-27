# Hash Maps — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Complement lookup** — one pass; for each element ask "have I seen what completes this?" then insert. Two Sum is the archetype. Decide up front what you store (value→index? complement→index?) and name the dict accordingly.
- **Prefix-sum + count map** — count subarrays with sum k: running `prefix`, map `prefix_value → occurrences`. At each step add `counts[prefix - k]` to the answer, THEN insert current prefix. Seed `counts[0] = 1` for subarrays starting at index 0. Extends to "divisible by k" (store prefix % k) and binary trees (path sum III).
- **Canonical-form key** — group things that are "the same under some transformation" by mapping each to a canonical representative: sorted string (anagrams), char-count tuple (anagrams without sort), normalized shift deltas (shifted strings), normalized slope fraction (points on a line).
- **Seen-set for cycle/state detection** — iterate a process, store visited states, stop on repeat (happy number, linked-list cycle by node id). Alternative: Floyd's fast/slow when O(1) space matters.
- **Two-way mapping** — bijection checks (isomorphic strings, word pattern) need BOTH directions enforced; one dict catches only half the violations.
- **Design** — hash map internals: array of buckets + hash function + collision policy (chaining = linked lists per bucket; open addressing = probing). Resize at load factor ~0.75. Know this story for "design HashMap" and system-design crossover.

### Python specifics
- `dict.get(k, default)`, `defaultdict(int)`, `Counter` (supports `&`, `-`, `most_common`). `defaultdict` inserts on READ access too — can bloat or surprise.
- Dict keys must be hashable → tuples yes, lists no (convert: `tuple(lst)`).
- CPython dicts preserve insertion order (3.7+) — handy, but don't conflate with sorted order.

### Pitfalls
- Prefix-sum map: inserting the current prefix BEFORE querying counts the empty subarray — order matters.
- Forgetting to seed `counts[0] = 1`.
- Using a 26-array when input is case-sensitive or non-alphabetic.

## Easy
- Ransom Note (LC 383)
- Isomorphic Strings (LC 205)
- Word Pattern (LC 290)
- Happy Number (LC 202)
- Majority Element (LC 169)
- First Unique Character in a String (LC 387)
- Intersection of Two Arrays (LC 349)

## Medium
- Subarray Sum Equals K (LC 560)
- Longest Substring Without Repeating Characters (LC 3)
- Group Shifted Strings (LC 249)
- Brick Wall (LC 554)
- Design HashMap (LC 706)
- Continuous Subarray Sum (LC 523)
- Insert Delete GetRandom O(1) (LC 380)
- Valid Sudoku (LC 36)
- Longest Consecutive Sequence (LC 128)

## Hard
- Substring with Concatenation of All Words (LC 30)
- Max Points on a Line (LC 149)
- Subarrays with K Different Integers (LC 992)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
