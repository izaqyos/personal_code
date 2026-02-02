# Exercise: Cache Invalidation Strategies

## Objective
Design robust cache invalidation for complex scenarios.

## Problem Statement
You're building an e-commerce product catalog with:
- Product details (name, description, images)
- Pricing (changes during sales/promotions)
- Inventory count (changes frequently with purchases)
- Category pages (aggregate of products)

The system handles 100K requests/second with 95% cache hit rate target.

## Tasks

### Task 1: Invalidation Strategy Design

For each data type, design an invalidation strategy:

| Data Type | Invalidation Method | Trigger |
|-----------|---------------------|---------|
| Product details | | |
| Pricing | | |
| Inventory | | |
| Category pages | | |

### Task 2: Handling Updates

A product update changes name, price, and category. Design the invalidation flow:

```python
def update_product(product_id, updates):
    # What caches need to be invalidated?
    # In what order?
    # How do you handle partial failures?
    pass
```

List all cache keys that need invalidation:
```
1. ___
2. ___
3. ___
...
```

### Task 3: Cache Stampede Prevention

When a popular product's cache expires, 1000 requests hit simultaneously.

Design a solution to prevent:
1. All 1000 requests hitting the database
2. Database overload
3. Inconsistent cache population

Implement one of these approaches in pseudocode:
- Locking
- Request coalescing
- Probabilistic early expiration

### Task 4: Version-Based Invalidation

Design a versioning scheme where:
- Product cache includes a version number
- Updates increment the version
- Old versions are automatically ignored

```python
def get_product_with_version(product_id):
    # Your implementation
    pass

def update_product_with_version(product_id, updates):
    # Your implementation
    pass
```

### Task 5: Trade-off Analysis

For each approach, list pros and cons:

1. **TTL-only invalidation**
   - Pros: ___
   - Cons: ___

2. **Event-based invalidation**
   - Pros: ___
   - Cons: ___

3. **Hybrid (TTL + Events)**
   - Pros: ___
   - Cons: ___

---

<details>
<summary>Hints</summary>

- Event-based gives immediate consistency but requires infrastructure
- TTL is simpler but has staleness window
- Stampede prevention is critical for popular items
- Version keys allow atomic updates without race conditions

</details>

<details>
<summary>Solution</summary>

### Task 1: Invalidation Strategy

| Data Type | Invalidation Method | Trigger |
|-----------|---------------------|---------|
| Product details | Event + 1hr TTL | Product update event |
| Pricing | Event + 5min TTL | Price change event, sale start/end |
| Inventory | Write-through (no cache) or 30s TTL | Every purchase |
| Category pages | Event + 15min TTL | Product added/removed from category |

### Task 2: Handling Updates

```python
def update_product(product_id, updates):
    # 1. Update database (source of truth)
    old_product = db.get_product(product_id)
    db.update_product(product_id, updates)
    
    # 2. Invalidate in order of importance
    cache_keys_to_invalidate = [
        f"product:{product_id}",
        f"product:{product_id}:price",
    ]
    
    # 3. Handle category changes
    if 'category_id' in updates:
        cache_keys_to_invalidate.extend([
            f"category:{old_product.category_id}:products",
            f"category:{updates['category_id']}:products",
        ])
    
    # 4. Batch invalidate with fallback
    for key in cache_keys_to_invalidate:
        try:
            cache.delete(key)
        except CacheError:
            # Log and continue - TTL will eventually fix it
            log.warning(f"Failed to invalidate {key}")
    
    # 5. Publish event for other consumers
    event_bus.publish("product_updated", product_id)
```

### Task 3: Cache Stampede Prevention

Using locking approach:

```python
def get_product_with_lock(product_id):
    cache_key = f"product:{product_id}"
    lock_key = f"lock:{cache_key}"
    
    # Try cache first
    product = cache.get(cache_key)
    if product:
        return product
    
    # Try to acquire lock
    if cache.set(lock_key, "1", nx=True, ex=10):  # NX=only if not exists
        try:
            # We have the lock - fetch and cache
            product = db.get_product(product_id)
            cache.set(cache_key, product, ex=3600)
            return product
        finally:
            cache.delete(lock_key)
    else:
        # Another request has the lock - wait and retry
        for _ in range(50):  # 5 seconds max
            time.sleep(0.1)
            product = cache.get(cache_key)
            if product:
                return product
        
        # Fallback to database
        return db.get_product(product_id)
```

### Task 4: Version-Based Invalidation

```python
def get_product_with_version(product_id):
    # Get current version from fast store
    version = cache.get(f"product:{product_id}:version") or 0
    
    cache_key = f"product:{product_id}:v{version}"
    product = cache.get(cache_key)
    
    if product:
        return product
    
    # Fetch from DB
    product = db.get_product(product_id)
    cache.set(cache_key, product, ex=3600)
    return product

def update_product_with_version(product_id, updates):
    # Update DB
    db.update_product(product_id, updates)
    
    # Increment version (atomic)
    new_version = cache.incr(f"product:{product_id}:version")
    
    # Old cached version will expire naturally via TTL
    # New requests will use new version key
```

### Task 5: Trade-off Analysis

1. **TTL-only**
   - Pros: Simple, no infrastructure needed, self-healing
   - Cons: Stale data window, unpredictable freshness

2. **Event-based**
   - Pros: Immediate consistency, precise control
   - Cons: Complex infrastructure, event delivery guarantees needed

3. **Hybrid**
   - Pros: Fast updates + self-healing, best of both
   - Cons: Dual complexity, need to maintain both systems

</details>
