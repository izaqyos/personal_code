# leetcode_coach — Agent Context

This file is read by the leetcode coach agent on every invocation (when file tools are available).
It supplements SKILL.md with paths, schema, and the topic-to-filename mapping.

---

## Canonical File Paths

| File | Absolute Path | Agent Access |
|------|--------------|--------------|
| tracks.yaml | `/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml` | Read only |
| schedule.yaml | `/Users/yosii/work/git/personal_KB/learning/config/schedule.yaml` | Read only |
| Solution & topic files | `/Users/yosii/work/git/personal_code/code/interviewQs/leetcode/` | Read + Write |
| LeetCode export (reference) | `/Users/yosii/work/git/personal_code/code/interviewQs/full_leetcode_export/` | Read only |
| This file | `/Users/yosii/work/git/personal_code/agents/leetcode_coach/AGENT_CONTEXT.md` | Read only |

---

## Topic Name to Filename Mapping

Topic names from `tracks.yaml` → filename slug rule: lowercase, replace ` & ` and ` / ` with `_`, replace spaces with `_`, strip consecutive underscores.

| tracks.yaml name | Filename |
|-----------------|----------|
| Arrays & Strings | `arrays_and_strings.md` |
| Hash Maps | `hash_maps.md` |
| Two Pointers | `two_pointers.md` |
| Sliding Window | `sliding_window.md` |
| Binary Search | `binary_search.md` |
| Linked Lists | `linked_lists.md` |
| Stacks & Queues | `stacks_and_queues.md` |
| Trees & BST | `trees_and_bst.md` |
| Graphs & BFS/DFS | `graphs_and_bfs_dfs.md` |
| Dynamic Programming | `dynamic_programming.md` |
| Greedy | `greedy.md` |
| Backtracking | `backtracking.md` |
| Heap / Priority Queue | `heap_priority_queue.md` |
| Tries | `tries.md` |
| Union Find | `union_find.md` |
| Intervals | `intervals.md` |

---

## Problem Bank File Format

Each topic file in the leetcode directory follows this format:

```markdown
# {Topic Name} — Problem Bank

## Easy
- Problem Name (LC {number})

## Medium
- Problem Name (LC {number})

## Hard
- Problem Name (LC {number})

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
```

---

## Solve Log Schema

| Field | Values | Description |
|-------|--------|-------------|
| Date | ISO 8601 (YYYY-MM-DD) | Date problem was attempted |
| Problem | string | Problem name |
| LC# | integer | LeetCode problem number |
| Difficulty | Easy / Medium / Hard | Problem difficulty |
| Result | PASS / PASS-SUBOPTIMAL / SKIP | Outcome |
| Hints | count (types) | e.g., "2 (socratic, layered)" |
| Time-Space | O(x)/O(y) | User's solution complexity |
| Notes | string | Brief takeaway |

**Result values:**
- `PASS` — correct solution with optimal complexity
- `PASS-SUBOPTIMAL` — correct but not optimal time/space complexity
- `SKIP` — user moved on without solving

---

## Solution File Convention

- Location: `/Users/yosii/work/git/personal_code/code/interviewQs/leetcode/`
- Naming: `camelCase.py` (e.g., `containerWithMostWater.py`)
- If file already exists: offer `_v2.py` suffix or reuse existing
- Format: docstring + function signature with type hints + test cases in `__main__` block using `assert`

---

## Agent-Editable Files

| File | Access | Operations |
|------|--------|------------|
| `leetcode/*.md` (topic files) | Read + Write | Create on bootstrap, append solve log entries |
| `leetcode/*.py` (solution files) | Write | Create scaffold only, never modify existing |
| `tracks.yaml` | Read only | Topic list and status |
| `schedule.yaml` | Read only | Current week/track check |

## Never Touch

- `tracks.yaml` — owned by `yosi_learn_helper`, never write
- `schedule.yaml` — owned by `yosi_learn_helper`, never write
- `MASTER_LEARNING_ROADMAP.md`
- Existing solution `.py` files — user's code, never modify
- `full_leetcode_export/` — reference data, never write
