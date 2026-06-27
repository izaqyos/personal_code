# Stacks & Queues — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Matching / nesting** — push opens, pop and verify on close. Generalizes to nested structures: decode-string pushes (current_string, multiplier) frames; simplify-path pushes directory names; calculator pushes (result, sign) at '('.
- **Monotonic stack** — THE pattern of this topic. Maintain a stack whose values are monotonic; each new element pops everything that violates the order, and each pop ANSWERS a question for the popped element ("first element to my right that is greater = the one popping me"). Every index pushed/popped once → O(n).
```
for i in range(n):                 # next-greater flavor: decreasing stack
    while stack and a[i] > a[stack[-1]]:
        j = stack.pop()
        answer[j] = i - j          # or a[i], per problem
    stack.append(i)
```
- **Histogram (LC 84)** — increasing stack of indices; when a shorter bar arrives, pop: popped bar's rectangle has height `h[popped]`, width from the new stack top +1 to current −1. Append a sentinel 0 bar to flush. Maximal-rectangle (LC 85) = histogram per matrix row.
- **Min stack** — store pairs `(value, min_so_far)` or a parallel min-stack; both O(1) per op.
- **Queue via two stacks** — `in_stack` for push; `out_stack` for pop/peek, refilled by draining `in_stack` only when empty. Amortized O(1).
- **Expression evaluation** — RPN: push numbers, pop two on operator (note operand ORDER for − and ÷, and Python's truncation: use `int(a/b)`, not `//`, for negative results). Infix without parens (calc II): keep a running term, commit on +/-, multiply/divide into the term immediately.
- **Stack as recursion eliminator** — iterative DFS and iterative tree traversals are "manual call stacks". If recursion depth is a risk (Python default ~1000), convert.

### Pitfalls
- Monotonic stack direction (increasing vs decreasing) flips per question — derive it from "what pops me answers what?"
- Forgetting the flush/sentinel step, leaving unanswered elements on the stack.
- Python lists are fine stacks (`append`/`pop`); for queues use `collections.deque` — `list.pop(0)` is O(n).

## Easy
- Valid Parentheses (LC 20)
- Implement Queue using Stacks (LC 232)
- Implement Stack using Queues (LC 225)
- Min Stack (LC 155)
- Next Greater Element I (LC 496)

## Medium
- Evaluate Reverse Polish Notation (LC 150)
- Daily Temperatures (LC 739)
- Decode String (LC 394)
- Asteroid Collision (LC 735)
- Car Fleet (LC 853)
- Simplify Path (LC 71)
- Basic Calculator II (LC 227)
- Next Greater Element II (LC 503)
- Online Stock Span (LC 901)
- Remove K Digits (LC 402)

## Hard
- Largest Rectangle in Histogram (LC 84)
- Maximal Rectangle (LC 85)
- Basic Calculator (LC 224)
- Longest Valid Parentheses (LC 32)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
