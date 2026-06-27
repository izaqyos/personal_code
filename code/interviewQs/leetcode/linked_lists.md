# Linked Lists — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Dummy head** — allocate `dummy = Node(0, head)` whenever the head itself might change (delete, merge, partition). Return `dummy.next`. Kills an entire class of edge-case ifs.
- **Iterative reverse** — three pointers: `prev, curr, nxt`. Loop: save `nxt = curr.next`, point `curr.next = prev`, advance `prev = curr`, `curr = nxt`. Return `prev`. Drill until automatic — it's a building block (reorder, k-group, palindrome check).
- **Fast/slow (Floyd's)** — `slow` 1 step, `fast` 2 steps. Middle: when fast hits the end, slow is at the middle. Cycle: they meet iff a cycle exists. Cycle START: after meeting, reset one pointer to head, advance both 1 step — they meet at the cycle entry (provable with the distance equation `head→entry = meeting→entry mod cycle length`).
- **Gap pointers (nth from end)** — advance `lead` n steps, then move `lead` and `trail` together; when `lead` hits the end, `trail` is n from the end. One pass.
- **Merge two sorted lists** — dummy + tail pointer, splice the smaller node, drain the leftover. Foundation for merge-k (pairwise or heap) and sort-list (merge sort on lists).
- **Composite problems decompose** — Reorder List = find middle + reverse second half + interleave. Palindrome List = middle + reverse + compare. Learn the lego blocks, not the monoliths.
- **LRU Cache** — hash map (key → node) + doubly-linked list (recency order). Get/put both O(1): unlink node, re-insert at head; evict from tail. In Python, `OrderedDict.move_to_end` is the shortcut — know both.

### Pitfalls
- Losing the rest of the list: save `next` BEFORE rewiring.
- Null-checks in fast/slow: condition is `while fast and fast.next` (even/odd lengths).
- Off-by-one in k-group: count k nodes exist before reversing the group.
- Copy-with-random-pointer: interleaved-clone trick (`A→A'→B→B'`) gives O(1) space vs the obvious old→new map.

## Easy
- Reverse Linked List (LC 206)
- Merge Two Sorted Lists (LC 21)
- Linked List Cycle (LC 141)
- Middle of the Linked List (LC 876)
- Palindrome Linked List (LC 234)
- Remove Duplicates from Sorted List (LC 83)
- Intersection of Two Linked Lists (LC 160)

## Medium
- Add Two Numbers (LC 2)
- Remove Nth Node From End of List (LC 19)
- Reorder List (LC 143)
- Copy List with Random Pointer (LC 138)
- LRU Cache (LC 146)
- Linked List Cycle II (LC 142)
- Sort List (LC 148)
- Partition List (LC 86)
- Reverse Linked List II (LC 92)
- Rotate List (LC 61)
- Swap Nodes in Pairs (LC 24)

## Hard
- Merge k Sorted Lists (LC 23)
- Reverse Nodes in k-Group (LC 25)
- LFU Cache (LC 460)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
