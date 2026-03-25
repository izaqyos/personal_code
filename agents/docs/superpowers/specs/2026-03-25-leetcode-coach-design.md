# leetcode_coach Agent — Design Spec

**Date:** 2026-03-25
**Status:** Draft
**Location:** `agents/leetcode_coach/`

---

## Overview

A coaching agent that guides Yosi through LeetCode practice sessions. It manages the full session lifecycle — problem selection, scaffolding, hints, and post-solve review — while never solving problems for the user.

**Core principle:** The agent never gives solutions. It guides, hints, and reviews. If the user asks for a solution directly, the agent refuses and offers a hint instead.

**Invocation:**
- Claude Code: `/leetcode` (via Skill tool, name `leetcode`)
- Cursor: `@leetcode_coach` (attaches `SKILL.md` as context)

---

## Goals

- Guide problem-solving practice without doing the work for the user
- Suggest problems at appropriate difficulty for the current topic
- Provide context-dependent hints that teach rather than reveal
- Deliver thorough post-solve reviews (correctness, style, complexity, alternatives)
- Track solve history to spot weak patterns over time
- Improve Python fluency through style feedback during reviews

## Non-Goals

- No web scraping or LeetCode API integration — problems are curated in local files
- Does not replace `yosi_learn_helper` for schedule/progress management
- No spaced repetition or flashcard system
- No timed contest simulation

---

## Session Lifecycle

### 1. Pick

Agent reads `tracks.yaml` to find the current in-progress LeetCode topic, then reads the topic's problem bank file. It checks the solve log for already-solved problems and suggests 2-3 unsolved problems at different difficulty levels. The user picks one.

### 2. Scaffold

Agent creates a solution file in `interviewQs/leetcode/` with:
- Problem description as a docstring (including constraints and examples)
- Function signature with type hints
- Test cases in a `__main__` block

Naming convention: `camelCase.py` matching existing files (e.g., `twoSum.py`, `productOfArrayExceptSelf.py`).

### 3. Solve (Hints)

User works on the problem. When stuck, the agent provides hints using a context-dependent mix of strategies:

**Hint Strategies:**

- **Socratic** — asks a guiding question ("What happens if you traverse from both ends?"). Best when the user is close but hasn't considered an angle.
- **Pattern-based** — names the pattern ("This is a sliding window problem"). Best when the user hasn't identified the approach yet.
- **Layered** — escalating sequence: nudge → bigger hint → pseudocode. Best when the user is genuinely stuck and needs progressive help.

**Hint Rules:**
- Never give code. Pseudocode is the maximum escalation.
- Never reveal the full approach unprompted — wait for the user to ask for more.
- If the user asks for the answer directly, refuse and offer the next hint level instead.
- Track hints given per problem (type and count) for the solve log.

### 4. Review

Triggered after the user's tests pass. Four parts, always in this order:

1. **Correctness** — confirm all test cases pass, flag edge cases not covered (empty input, negatives, duplicates, overflow).
2. **Python style** — point out un-Pythonic patterns as they come up naturally (e.g., `while` loop where `for range` is cleaner, manual index tracking vs `enumerate`). Keep it light.
3. **Complexity analysis** — state time and space Big-O. Compare to optimal if the user's solution isn't optimal.
4. **Alternative approaches** — briefly describe 1-2 other ways to solve it. Additionally, call out when relevant:
   - **Novel data structures** (segment tree, trie, disjoint set)
   - **Lesser-known algorithms** (Kadane's, Floyd's cycle detection, Boyer-Moore voting)
   - **Advanced math** (modular arithmetic, combinatorics, number theory)
   - **Probabilistic / large-scale approaches** (Bloom filter, HyperLogLog, Count-Min Sketch, consistent hashing) — when the problem has a "what if this was at massive scale?" angle, mention the probabilistic approach and its trade-offs (false positive rate, memory savings, etc.)

   Don't give code — name it, explain why it applies in one line, and note the trade-off. The goal is broadening exposure.

**If tests fail:** don't review. Instead, hint at what's wrong using the hint engine.

After review, the agent appends a solve log entry and asks if the user wants another problem or to end the session.

---

## Problem Bank & Solve Log

One markdown file per topic in `interviewQs/leetcode/`, e.g., `arrays_and_strings.md`.

### Problem Bank Format

```markdown
# Arrays & Strings — Problem Bank

## Easy
- Two Sum (LC 1)
- Best Time to Buy and Sell Stock (LC 121)

## Medium
- Product of Array Except Self (LC 238)
- Container With Most Water (LC 11)

## Hard
- Trapping Rain Water (LC 42)
```

### Solve Log Format

Appended to the same file:

```markdown
## Solve Log

| Date | Problem | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|------------|--------|-------|------------|-------|
| 2026-03-25 | Product of Array Except Self | Medium | PASS | 1 (layered) | O(n)/O(n) | prefix/suffix pattern, could optimize to O(1) space |
```

**Fields:**
- **Result:** `PASS` / `PASS-SUBOPTIMAL` (correct but not optimal complexity)
- **Hints:** count and type used (e.g., "2 (socratic, layered)")
- **Time-Space:** the user's solution complexity
- **Notes:** brief takeaway — weak spots, patterns learned

The agent reads the log to spot patterns over time (e.g., "You've needed hints on sliding window 3 times — want to do an extra problem on that?").

---

## File Structure

```
agents/leetcode_coach/
├── SKILL.md              # Behavior: session lifecycle, hint engine, review protocol
├── AGENT_CONTEXT.md      # Problem bank paths, solve log schema, topic list
└── README.md             # Invocation docs

interviewQs/leetcode/
├── arrays_and_strings.md          # Problem bank + solve log
├── hash_maps.md                   # Problem bank + solve log
├── two_pointers.md                # ...one per topic from tracks.yaml
├── sliding_window.md
├── binary_search.md
├── linked_lists.md
├── stacks_and_queues.md
├── trees_and_bst.md
├── graphs_and_bfs_dfs.md
├── dynamic_programming.md
├── greedy.md
├── backtracking.md
├── heap_priority_queue.md
├── tries.md
├── union_find.md
├── intervals.md
├── productOfArrayExceptSelf.py    # Solution files (created by agent per session)
├── twoSum.py                      # Existing solutions
└── BestTimeToBuySellStocks.py     # Existing solutions
```

---

## Integration with yosi_learn_helper

- `leetcode_coach` owns the session (pick → scaffold → hints → review)
- `yosi_learn_helper` owns the schedule and track-level progress in `tracks.yaml`
- They don't call each other. The user updates progress manually via `/learn` (e.g., "mark Arrays & Strings done") after completing a topic's problems.
- The solve log in `interviewQs/leetcode/` is the source of truth for problem-level detail; `tracks.yaml` tracks topic-level status.
- `leetcode_coach` reads `tracks.yaml` to know which topics exist and their status (to suggest the current topic) but never writes to it.

---

## Agent-Editable Files

| File | Access |
|------|--------|
| `interviewQs/leetcode/*.md` (topic files) | Read + Write (append solve log entries) |
| `interviewQs/leetcode/*.py` (solution files) | Write (create scaffold only) |
| `tracks.yaml` | Read only |

## Never Touch

- `tracks.yaml` (owned by `yosi_learn_helper`)
- `MASTER_LEARNING_ROADMAP.md`
- Existing solution files (user's code, never modify)
- `full_leetcode_export/` (reference data, read-only)

---

## Success Criteria

- `/leetcode` starts a session with problem suggestions for the current topic
- Agent never gives code solutions, only hints
- Hints use the right strategy for the context (Socratic/pattern/layered)
- Post-solve review covers all four areas (correctness, style, complexity, alternatives)
- Solve log is appended correctly after each problem
- Agent spots weak patterns from solve log data
- Python style tips are delivered naturally, not as lectures
- Works from both Claude Code (`/leetcode`) and Cursor (`@leetcode_coach`)
