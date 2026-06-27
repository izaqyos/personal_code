# Arrays & Strings — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Prefix/suffix accumulation** — precompute running sums/products from left and right; answer at `i` combines `prefix[i-1]` and `suffix[i+1]`. Space-optimize by reusing the output array for one direction + a running scalar for the other.
- **Frequency counting** — fixed alphabet → `[0]*26` array; arbitrary chars/case-sensitive → dict/Counter. Increment one string, decrement the other, check all-zero.
- **Index-as-hash (in-place marking)** — when values are bounded by array length, the array itself is the hash table: flip sign at index `v-1`, or place `v` at slot `v-1` (cyclic sort). Gives O(1) space on problems that look like they need a set.
- **Kadane's algorithm** — max subarray sum: `cur = max(x, cur + x)`, `best = max(best, cur)`. Extends to max product (track min too, signs flip).
- **String building** — strings are immutable; repeated `+=` is O(n²). Collect parts in a list, `''.join(parts)` at the end.
- **Matrix tricks** — rotate 90° = transpose + reverse each row; spiral = four shrinking boundaries; set-zeroes in O(1) space = use row 0 / col 0 as marker arrays.

### Sorting fundamentals (drill these from scratch)
```
merge_sort(a):                      # O(n log n) time, O(n) space, stable
    if len(a) <= 1: return a
    L, R = merge_sort(left half), merge_sort(right half)
    merge: two pointers over L and R, take smaller, drain leftovers

quicksort partition (Lomuto):       # avg O(n log n), worst O(n²), in place
    pivot = a[hi]; i = lo
    for j in lo..hi-1: if a[j] < pivot: swap(a[i], a[j]); i += 1
    swap(a[i], a[hi]); return i
```
Know when sorting *is* the answer: dedup, anagram keys, meeting-style problems, two-pointer preconditions.

### Pitfalls
- Off-by-one at boundaries — write the loop invariant in a comment before coding.
- Mutating a list while iterating it — iterate a copy or build a new list.
- Python negative indexing silently "works" — a stray `-1` index reads the last element instead of crashing.
- `enumerate` yields `(i, val)` in that order.

## Easy
- Two Sum (LC 1)
- Best Time to Buy and Sell Stock (LC 121)
- Contains Duplicate (LC 217)
- Valid Anagram (LC 242)
- Merge Sorted Array (LC 88)
- Longest Common Prefix (LC 14)
- Plus One (LC 66)
- Remove Duplicates from Sorted Array (LC 26)
- Length of Last Word (LC 58)
- Merge Strings Alternately (LC 1768)

## Medium
- Product of Array Except Self (LC 238)
- Container With Most Water (LC 11)
- Group Anagrams (LC 49)
- Longest Consecutive Sequence (LC 128)
- Top K Frequent Elements (LC 347)
- Encode and Decode Strings (LC 271)
- String to Integer (atoi) (LC 8)
- 3Sum (LC 15)
- Maximum Subarray (LC 53)
- Maximum Product Subarray (LC 152)
- Rotate Array (LC 189)
- Rotate Image (LC 48)
- Spiral Matrix (LC 54)
- Set Matrix Zeroes (LC 73)
- String Compression (LC 443)
- Zigzag Conversion (LC 6)
- Sort Colors (LC 75)

## Hard
- Trapping Rain Water (LC 42)
- First Missing Positive (LC 41)
- Minimum Window Substring (LC 76)
- Text Justification (LC 68)
- Candy (LC 135)

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
| 2026-06-21 | Encode and Decode Strings | 271 | Medium | PASS | 0 | O(N)/O(N) | VARIANT 3 of 3 (escaping/sentinel, no length prefix; encodeDecodeStrings_v3.py). Self-derived scheme: bare '#' as TERMINATOR; escape '\'→'\\' and '#'→'\#'. Did escaping in a SINGLE pass (prefix '\' before any '\' or '#' while walking) — sidesteps the two-replace ordering trap entirely. decode invariant: a '\' is always followed by an escaped char and last char is always '#', so s[i+1] never OOB. Key simplification (review): the char after '\' is ALWAYS literal → `cur_word.append(s[i+1])` regardless of which char; no need to case-split on '#' vs '\'. Design decisions resolved correctly: terminator (not separator) keeps [] / [""] / ["",""] distinct; escape order would matter for two-pass but single-pass avoids it. Solved sharp/unfatigued, 13/13 incl. brutal cases. Earlier: v1 fixed-width header also PASS 11/11. Interview soundbite: length-prefixed decode = O(1) seek per string, never scans content; escaping decode must scan every char |
| 2026-06-13 | Encode and Decode Strings (v2: len#str) | 271 | Medium | PASS | 1 (socratic) | O(N)/O(N) | length-prefix + `#` separator variant: `L0#s0L1#s1...`, no count header (decode walks to end-of-string), no padding → handles arbitrary-length strings (passed 250-char test that v1's 3-digit cap couldn't encode). encode = one comprehension `[f"{len(s)}#{s}" for s in strs]`. decode = scan digits to `#`, read len from `s[prev:pos]`, JUMP `pos+1 : pos+1+len` for content, never scan content for `#` (content `#` rides untouched — `"4#hello"` fake-prefix trap is a non-event). Bug: `if pos == '#'` compared the int INDEX to the char → always False → returned `[]` on everything. Fix: `s[pos] == '#'`. Subtlety that works: after a hit, pos jumps to next field's first char AND prev anchors there, so trailing `pos+=1` doesn't lose the first digit. Style: cleaner idiom is `s.find('#', start)` — drops `prev` + the `pos+=1` reasoning entirely. Watch mixed 2/4-space indent. Three canonical 271 schemes: fixed-width header (v1) / len#str jump (this) / backslash-escape no-length (v3 TODO) |
| 2026-06-13 | Encode and Decode Strings | 271 | Medium | PASS | 2 (socratic) | O(N)/O(N) | fixed-width 3-digit length-prefix header: `[count][len0][len1]...[s0][s1]...`, no delimiter — unambiguous for ANY chars (the `#`/`"4#hello"` traps are non-events). encode = single list literal w/ double `*` unpack: `[f"{count:03d}", *(lengths gen), *strs]` — order in literal = order on wire. Bugs hit en route: (1) pasted the one-liner AFTER the loops → rebind discarded payload; (2) decode used `(strs_len+i+1)*3` fixed stride for payload offset — header has fixed 3-char stride but PAYLOAD does not (variable-len, packed back-to-back). Fix: running accumulator `next_str_pos += len_str`. Header read keeps `(i+1)*3` (legit fixed stride). Watch: `:03d` is MIN width not fixed — breaks silently past len 199, but constraints cap <200 so no guard needed (say it out loud in interview). `str` shadows builtin — rename. Alt: length-prefix w/ `#` delimiter + while-scan (no count header, handles arbitrary length); escaping/sentinel = the trap to avoid |
