# Dictionary Patterns: dict vs defaultdict vs .get()

**Created**: 2025-12-14  
**Related Practice**: Week 1, Day 2 (Dictionary Comprehensions & defaultdict)

---

## Overview

Python offers multiple patterns for handling dictionary operations, especially when dealing with missing keys. This deep dive compares three approaches and when to use each.

---

## The Three Patterns

### Pattern 1: Regular dict with if-else

```python
groups = {}
for word in words:
    key = word[0]
    if key not in groups:
        groups[key] = []
    groups[key].append(word)
```

### Pattern 2: Regular dict with .get() / .setdefault()

```python
# .get() for reading with default
value = my_dict.get(key, default_value)

# .setdefault() for read-or-create
groups = {}
for word in words:
    groups.setdefault(word[0], []).append(word)
```

### Pattern 3: defaultdict

```python
from collections import defaultdict

groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)
```

---

## When to Use Each Pattern

### ✅ Use Pattern 1 (if-else) when:

| Use Case | Example |
|----------|---------|
| Custom initialization per key | `groups[key] = {'count': 0, 'created_at': datetime.now()}` |
| Track "first seen" only | `if val not in seen: seen[val] = index` |
| Complex conditional logic | Different init based on key type |
| Explicit control flow needed | Debugging, logging on first access |

```python
# Example: Custom per-key initialization
inventory = {}
for item in items:
    category = item['category']
    if category not in inventory:
        inventory[category] = {
            'items': [],
            'count': 0,
            'last_updated': datetime.now()
        }
    inventory[category]['items'].append(item)
    inventory[category]['count'] += 1
```

---

### ✅ Use Pattern 2 (.get/.setdefault) when:

| Use Case | Example |
|----------|---------|
| One-liner without import | `count = d.get(key, 0) + 1` |
| Read-only default | `timeout = config.get('timeout', 30)` |
| JSON/API responses | Can't use defaultdict on parsed JSON |
| Chained access | `response.get('user', {}).get('name', 'Anon')` |
| Don't want to modify dict | `.get()` doesn't add missing keys |

```python
# Example: Safe nested access for API response
response = json.loads(api_result)
user_name = response.get('data', {}).get('user', {}).get('name', 'Unknown')
user_email = response.get('data', {}).get('user', {}).get('email')  # None if missing
```

---

### ✅ Use Pattern 3 (defaultdict) when:

| Use Case | Example |
|----------|---------|
| Building/accumulating data | Grouping, counting, aggregating |
| Repeated access pattern | Same operation on many keys |
| Clean, readable code | No boilerplate for initialization |
| Factory pattern | `defaultdict(lambda: {'count': 0})` |

```python
# Example: Word frequency counter
from collections import defaultdict

word_freq = defaultdict(int)
for word in document.split():
    word_freq[word] += 1  # No KeyError, auto-initializes to 0

# Example: Grouping by attribute
by_department = defaultdict(list)
for employee in employees:
    by_department[employee.dept].append(employee)
```

---

## defaultdict Gotchas

### 1. Accidental Key Creation

```python
dd = defaultdict(list)

# This CREATES the key 'typo' even though we're just checking!
if dd['typo']:
    print("exists")

# Now dd = {'typo': []}  ← Unintended!

# Fix: Use 'in' to check without creating
if 'typo' in dd:
    print("exists")
```

### 2. Not JSON Serializable

```python
import json
dd = defaultdict(list)
dd['a'].append(1)

json.dumps(dd)  # ❌ TypeError: Object of type defaultdict is not JSON serializable

# Fix: Convert to regular dict
json.dumps(dict(dd))  # ✅ Works
```

### 3. Confusing When Iterating

```python
dd = defaultdict(int)
dd['a'] = 1

# This creates 'b' and 'c' with value 0!
for key in ['a', 'b', 'c']:
    print(dd[key])  # 1, 0, 0

# dd is now {'a': 1, 'b': 0, 'c': 0}
```

---

## Quick Reference

| Scenario | Best Pattern |
|----------|--------------|
| Building groups/lists | `defaultdict(list)` |
| Counting occurrences | `defaultdict(int)` or `Counter` |
| Reading with fallback | `.get(key, default)` |
| JSON/API data | `.get()` chains |
| Complex per-key init | `if-else` |
| Nested defaults | `defaultdict(lambda: defaultdict(list))` |
| One-time lookup | `.get()` |
| Repeated accumulation | `defaultdict` |

---

## Performance Notes

- `defaultdict` has slight overhead for the factory function call
- For simple lookups, `.get()` is marginally faster
- For accumulation (many writes), `defaultdict` is cleaner and comparable in speed
- `Counter` (subclass of dict) is optimized for counting

---

## See Also

- Week 1, Day 2: `exercises/week_01_pythonic_idioms/day2_dict_defaultdict.py`
- Week 3, Day 1: `exercises/week_03_advanced_data_structures/day1_counter.py`
- Week 3, Day 3: `exercises/week_03_advanced_data_structures/day3_defaultdict.py`

---

**Key Insight**: Choose based on the *operation pattern*, not just preference. `defaultdict` for building, `.get()` for reading, `if-else` for complex init.

