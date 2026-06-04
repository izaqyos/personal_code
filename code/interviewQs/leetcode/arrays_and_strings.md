# Arrays & Strings — Problem Bank

## Easy
- Two Sum (LC 1)
- Best Time to Buy and Sell Stock (LC 121)
- Contains Duplicate (LC 217)
- Valid Anagram (LC 242)
- Merge Sorted Array (LC 88)

## Medium
- Product of Array Except Self (LC 238)
- Container With Most Water (LC 11)
- Group Anagrams (LC 49)
- Longest Consecutive Sequence (LC 128)
- Top K Frequent Elements (LC 347)
- Encode and Decode Strings (LC 271)
- String to Integer (atoi) (LC 8)
- 3Sum (LC 15)

## Hard
- Trapping Rain Water (LC 42)
- First Missing Positive (LC 41)
- Minimum Window Substring (LC 76)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
| 2026-03-26 | Product of Array Except Self | 238 | Medium | PASS | 1 (layered) | O(n)/O(1) | prefix/suffix pattern; O(n) space first, then optimized to O(1) by reusing output array for suffix + running prefix variable |
| 2026-03-29 | Group Anagrams | 49 | Medium | PASS | 0 | O(n·k)/O(n·k) | prime product sieve approach (creative), then added sorted-key O(n·k log k) and char-count tuple O(n·k) alternatives |
| 2026-03-30 | Valid Anagram | 242 | Easy | PASS | 0 | O(n)/O(1) | char-count single array with increment/decrement; early exit on length mismatch |
| 2026-03-31 | Contains Duplicate | 217 | Easy | PASS | 0 | O(n)/O(n) | set with early return; also know sort+scan O(n log n)/O(1) and brute force O(n²)/O(1) |
| 2026-04-06 | Longest Consecutive Sequence | 128 | Medium | PASS | 1 | O(n)/O(n) | set + only start counting from sequence heads (n-1 not in set); 1 hint: nudge away from DP toward set approach |
| 2026-04-09 | Container With Most Water | 11 | Medium | PASS | 1 | O(n)/O(1) | two pointers from edges; always move shorter side — moving taller can never improve min(h[l],h[r]) |
| 2026-04-13 | Top K Frequent Elements | 347 | Medium | PASS | 0 | O(n)/O(n) | Counter + bucket sort (index=frequency); also know heap approach O(n log k)/O(k) — better when n is huge and k is small |
| 2026-04-14 | Best Time to Buy and Sell Stock | 121 | Easy | PASS | 0 | O(n)/O(1) | greedy: track min price so far, compute profit at each step |
| 2026-04-19 | Merge Sorted Array | 88 | Easy | PASS | 1 | O(m+n)/O(1) | back-merge: 3 pointers from the end — fill nums1 right-to-left to avoid overwriting unread data (prior solves used forward merge with O(m) copy) |
| 2026-05-05 | First Missing Positive | 41 | Hard | PASS | 4 (layered) | O(n)/O(1) | sign-marking on index v-1: pass 1 replaces invalids (≤0 or >n) with sentinel n+1; pass 2 uses abs() to recover magnitude (earlier iterations may have already flipped the slot's sign), with bounds guard before index access; pass 3 returns first positive slot's index+1, fallback n+1. Pitfalls: enumerate order (i,num), Python negative indexing if val=0 sneaks through, short-circuit guard ordering |
| 2026-05-07 | Trapping Rain Water | 42 | Hard | PASS | 3 (layered) | O(n)/O(1) | two pointers from ends, advance the lower side. Update rule on chosen side: if h>side_max → update side_max, else water += side_max - h. Correctness chain: l_max ≤ h[r] (because l_max only grows during left-processing, where h[l] ≤ h[r]) and h[r] ≤ true_rightMax[l] (h[r] is a bar to the right of l) ⇒ min(l_max, true_rightMax[l]) = l_max, safe to commit without scanning the unseen middle. Edges handled implicitly: max_*=0 init means first visit always hits update branch |
| 2026-05-18 | Minimum Window Substring | 76 | Hard | PASS | 4 (layered) | O(|s|+|t|)/O(|s|+|t|) | sliding window + freq maps + scalar satisfaction counter. Two dicts: need (immutable Counter(t)) and have (current window). Single int `formed` = count of distinct chars in need that have hit their required count exactly. Expand r every outer iter; while formed == len(need), record best (shorter, not longer), then shrink l. Key threshold semantics: bump formed only at the exact transitions — have[c] == need[c] after incr → formed+=1; have[c] < need[c] after decr → formed-=1 (NOT >= / <=, would over/undercount). Case-sensitive so use dict not 26-array. Return s[best_l : best_l+best_len], "" if best_len never set |
| 2026-05-27 | Two Sum | 1 | Easy | PASS | 0 | O(n)/O(n) | one-pass hash. Store value→index in `seen`; for each n check if (target-n) in seen — if yes return [seen[target-n], i], else store n→i. Symmetric alternative (scheme B): store (target-value)→index, check if n in map. Both work; pick name to match storage |
| 2026-06-03 | 3Sum | 15 | Medium | PASS | 3 (layered, socratic) | O(n²)/O(1) | sort first (the <0→l+=1 / >0→r-=1 branch logic is only valid on sorted input). Per-anchor reset l=anc+1, r=n-1, then an inner `while l<r` two-pointer scan holds the three branches — the scan IS the loop (first attempt put the branches at for-level → ran once per anchor). Anchor-dedup `continue` must sit at for-level; placing it inside `while l<r` spins forever (l/r unchanged). After a hit: mandatory l+=1/r-=1 BEFORE the bounded dedup-skip whiles (used l<n / r>0 guards; canonical is l<r). n==3 special-case block + vestigial line-61 init are dead weight — general algo covers them. Alt: hash-set inner 2Sum O(n²)/O(n); generalizes to kSum recursion (LC 18) |
