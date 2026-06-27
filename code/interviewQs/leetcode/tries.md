# Tries — Problem Bank & Study Notes

## Study Notes (offline reference)

### Structure
A trie (prefix tree) stores strings character-by-character along root→leaf paths; shared prefixes share nodes. Node = `children` (dict char→node) + `is_end` flag (a node can end a word AND continue to longer ones — that's why the flag exists; "app" vs "apple").

```
insert(word):  walk/create child per char; mark last node is_end
search(word):  walk; fail on missing child; return is_end at the last node
startsWith(p): same walk; reaching the end of p is enough (ignore is_end)
```
All ops O(L) in word length — independent of how many words are stored. Space is the cost: O(total chars × pointer overhead).

### When a trie wins
Many queries against many words *by prefix*: autocomplete, prefix counting, wildcard dictionaries, multi-word grid search. One-off prefix checks don't justify it — a sorted list + bisect or a set of prefixes may be simpler.

### Core patterns
- **Wildcard search (LC 211)** — '.' branches: try EVERY child at that position (DFS over the trie). Worst case exponential in dots; fine for the constraints.
- **Trie + grid DFS (Word Search II, LC 212)** — THE killer app. Insert all dictionary words into a trie, then one DFS over the board walking board-char and trie-node *in lockstep* — dead trie branch = prune immediately. Searching each word separately is O(words × board); the trie amortizes the shared prefixes. Optimizations: store the word at its end node (no path rebuilding), null out `is_end`/prune leaf nodes after a hit to avoid duplicates.
- **Augmented nodes** — store extra data per node: count of words through here (prefix counting), value sums (Map Sum LC 677), shortest root word (Replace Words LC 648).
- **Bitwise trie (Maximum XOR, LC 421)** — insert numbers as 32-bit paths (children[0/1]); to maximize XOR against x, greedily walk taking the OPPOSITE bit when it exists. Turns O(n²) pair scan into O(32n). Niche but memorable.

### Pitfalls
- Returning `True` from search when the walk succeeds but `is_end` is False (prefix ≠ word).
- Word Search II without pruning found words → duplicate results; collect into a set or prune.
- Building TrieNode with a 26-array when input isn't lowercase-only — dict is safer.

## Easy
- Longest Common Prefix (LC 14) — honorary; solvable without a trie, instructive with one

## Medium
- Implement Trie (Prefix Tree) (LC 208)
- Design Add and Search Words Data Structure (LC 211)
- Replace Words (LC 648)
- Map Sum Pairs (LC 677)
- Lexicographical Numbers (LC 386)
- Search Suggestions System (LC 1268)
- Maximum XOR of Two Numbers in an Array (LC 421)

## Hard
- Word Search II (LC 212)
- Stream of Characters (LC 1032)
- Palindrome Pairs (LC 336)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
