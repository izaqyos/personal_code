# Exercise: Cache Strategy Comparison

## Objective
Understand when to use different caching strategies.

## Problem Statement
You're building a social media application with the following features:
- User profiles (viewed frequently, updated occasionally)
- News feed (personalized, frequently changing)
- Friend count (computed value, changes on follow/unfollow)

## Tasks

### Task 1: Strategy Matching

Match each feature to the best caching strategy and explain why:

Strategies:
- Cache-Aside (Lazy Loading)
- Read-Through
- Write-Through  
- Write-Behind (Write-Back)

| Feature | Strategy | Reason |
|---------|----------|--------|
| User Profiles | | |
| News Feed | | |
| Friend Count | | |

### Task 2: Pseudocode

Write pseudocode for the Cache-Aside pattern:

```python
def get_user_profile(user_id):
    # Your code here
    pass

def update_user_profile(user_id, new_data):
    # Your code here
    pass
```

### Task 3: Cache Key Design

Design cache keys for each feature. Consider:
- Uniqueness
- Readability for debugging
- Potential for cache pollution

```
User Profile: ___
News Feed: ___
Friend Count: ___
```

### Task 4: TTL Selection

Choose appropriate TTL values and justify:

| Feature | TTL | Justification |
|---------|-----|---------------|
| User Profile | | |
| News Feed | | |
| Friend Count | | |

---

<details>
<summary>Hints</summary>

- Cache-Aside is good when: reads are frequent, cache misses are acceptable
- Write-Through is good when: data consistency is critical
- Write-Behind is good when: high write throughput needed, some lag acceptable
- Consider how often data changes vs how often it's read

</details>

<details>
<summary>Solution</summary>

### Task 1: Strategy Matching

| Feature | Strategy | Reason |
|---------|----------|--------|
| User Profiles | Cache-Aside | Read-heavy, updates infrequent, stale data briefly acceptable |
| News Feed | Cache-Aside with short TTL | Personalized, changes often, computed on demand |
| Friend Count | Write-Through | Changes infrequently, always needs accurate value |

### Task 2: Pseudocode

```python
def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    
    # Check cache first
    profile = cache.get(cache_key)
    if profile:
        return profile
    
    # Cache miss - fetch from DB
    profile = db.query("SELECT * FROM users WHERE id = ?", user_id)
    
    # Populate cache
    cache.set(cache_key, profile, ttl=3600)
    
    return profile

def update_user_profile(user_id, new_data):
    # Update database first
    db.update("users", user_id, new_data)
    
    # Invalidate cache (not update - avoids race conditions)
    cache_key = f"user:profile:{user_id}"
    cache.delete(cache_key)
```

### Task 3: Cache Key Design

```
User Profile: user:profile:{user_id}
News Feed: feed:{user_id}:page:{page_number}
Friend Count: user:friends:count:{user_id}
```

Key design principles:
- Prefix with entity type
- Include all uniqueness dimensions
- Use colons as separators (Redis convention)

### Task 4: TTL Selection

| Feature | TTL | Justification |
|---------|-----|---------------|
| User Profile | 1 hour | Updates infrequent, brief staleness OK |
| News Feed | 5 minutes | Changes frequently, freshness important |
| Friend Count | No TTL (invalidate on change) | Infrequent changes, always accurate |

</details>
