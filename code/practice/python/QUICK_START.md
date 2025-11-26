# Quick Start Guide - Daily Python Practice

## Starting Your Daily Session

1. **Open Files**:
   - `PYTHON_PRACTICE_PLAN.md` - See today's topic
   - `PRACTICE_LOG.md` - Track your progress
   - Create exercise file: `exercises/week_XX/dayX_topic.py`

2. **Session Flow** (10-15 minutes):
   - Review concept (2-3 min)
   - Hands-on coding (7-10 min)
   - Log insights (1-2 min)

3. **Update Log**:
   - Fill in date, status, and notes in `PRACTICE_LOG.md`

---

## Week 1 Day 1 Example: List Comprehensions vs Generator Expressions

### Concept Review (3 minutes)

**List Comprehension**: Creates entire list in memory
```python
squares = [x**2 for x in range(1000)]  # All 1000 values in memory
```

**Generator Expression**: Lazy evaluation, one item at a time
```python
squares = (x**2 for x in range(1000))  # Values created on demand
```

**Key Differences**:
- Memory: List = O(n), Generator = O(1)
- Speed: List faster for small data, Generator better for large
- Reusability: List reusable, Generator single-use
- Syntax: `[]` vs `()`

### Exercise (10 minutes)

**Task**: Implement both approaches and compare memory usage

```python
import sys
import tracemalloc

def list_approach(n):
    """Return list of squares"""
    return [x**2 for x in range(n)]

def generator_approach(n):
    """Return generator of squares"""
    return (x**2 for x in range(n))

# TODO: Measure memory for both with n=1_000_000
# TODO: Time how long it takes to sum all values
# TODO: Try to iterate twice - what happens with generator?
# TODO: Convert generator to list when needed

# Hint: Use tracemalloc.start() and get_traced_memory()
# Hint: Use time.perf_counter() for timing
```

**Bonus Challenge**: 
- When would you use `list()` instead of `[]`?
- Implement a pipeline: filter evens, square them, sum result

### Reflection

- What surprised you about the memory difference?
- When would you choose list over generator?
- How does this relate to `map()` and `filter()`?

---

## Week 1 Day 2 Example: Dictionary Comprehensions & defaultdict

### Concept Review

**Dict Comprehension**:
```python
word_lengths = {word: len(word) for word in words}
```

**defaultdict**:
```python
from collections import defaultdict
groups = defaultdict(list)
groups['key'].append(value)  # No KeyError if 'key' missing
```

### Exercise

**Task**: Group anagrams together

```python
from collections import defaultdict

words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']

# TODO: Group anagrams using defaultdict
# Expected: {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}

# TODO: Now do it with dict comprehension
# TODO: Compare both approaches - which is clearer?

# Hint: Use sorted(word) as key
# Hint: Consider setdefault() vs defaultdict
```

**Bonus**: Count character frequencies in a string without using Counter

---

## Tips for Success

### When Stuck:
1. ✅ Read official Python docs for the module
2. ✅ Write small test cases
3. ✅ Break problem into smaller parts
4. ✅ Check if there's a standard library solution
5. ⚠️ Avoid googling full solutions (you want to think it through!)

### Making It Stick:
- Explain the concept in your own words
- Think of real-world use case from your work
- Note performance implications (time/space complexity)
- Consider edge cases

### Difficulty Adjustments:
- **Too Easy?** Add constraints (no imports, optimize for space, etc.)
- **Too Hard?** Break it down, review docs, or discuss with AI for hints (not solutions!)
- **No Time?** Do the reading, defer coding to next day

---

## Example Exercise Structure (Template)

Create: `exercises/week_XX/dayX_topic.py`

```python
"""
Week X Day X: [Topic Name]
Date: YYYY-MM-DD
Time: 10-15 minutes

Concept: [Brief explanation]
Goal: [What you're practicing]
"""

# ============================================================
# EXERCISE
# ============================================================

def solution():
    """
    Your implementation here
    """
    pass

# ============================================================
# TESTS (Optional but recommended)
# ============================================================

def test_basic():
    assert solution() == expected
    print("✅ Basic test passed")

def test_edge_cases():
    # Test empty input, large input, etc.
    pass

# ============================================================
# PERFORMANCE ANALYSIS (For algorithm days)
# ============================================================

def analyze_performance():
    """
    Time Complexity: O(?)
    Space Complexity: O(?)
    Trade-offs: ...
    """
    pass

# ============================================================
# NOTES & INSIGHTS
# ============================================================

"""
What I learned:
- 

Gotchas:
- 

Questions:
- 

Real-world application:
- 
"""

if __name__ == "__main__":
    test_basic()
    # test_edge_cases()
    # analyze_performance()
```

---

## Resume Conversation with AI

To resume practice with AI assistance:

1. Share your current progress: "I'm on Week X Day Y"
2. Show your code if you want hints (not solutions!)
3. Ask specific questions: "How does this compare to...?" or "What's the trade-off between...?"
4. Request next exercise: "Ready for the next challenge"

**Example prompt**:
> "I'm working on Week 1 Day 3 (unpacking idioms). I wrote this code [paste code]. Can you give me hints on making it more Pythonic without giving away the answer? Also, what are the performance implications?"

---

## Resources Quick Links

- **Python Docs**: https://docs.python.org/3/
- **PEP 8 Style**: https://pep8.org/
- **Built-in Functions**: https://docs.python.org/3/library/functions.html
- **Standard Library**: https://docs.python.org/3/library/

---

**Ready to start? Begin with Week 1 Day 1!**

Update `PRACTICE_LOG.md` with today's date and dive in. 🚀

