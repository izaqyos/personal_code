# Exercise: URL Shortener Basic Design

## Objective
Design the basic components of a URL shortening service.

## Requirements
- Shorten long URLs to short codes
- Redirect short URLs to original URLs
- Handle 1M URLs per month

## Tasks

### Task 1: Short Code Generation

Calculate the short code requirements:

1. If we want to support 1 billion URLs, what's the minimum short code length using:
   - Only lowercase letters (26 chars)?
   - Lowercase + uppercase (52 chars)?
   - Alphanumeric (62 chars)?

   Show your calculations:
   ```
   26^n >= 1,000,000,000
   n = ___
   
   52^n >= 1,000,000,000
   n = ___
   
   62^n >= 1,000,000,000
   n = ___
   ```

2. Why might you choose a longer code than the minimum?

### Task 2: Short Code Generation Methods

Compare three approaches:

**Approach A: Random Generation**
```python
def generate_random():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(7))
```

**Approach B: Hash-based**
```python
def generate_hash(url):
    hash_bytes = hashlib.md5(url.encode()).digest()
    encoded = base64.urlsafe_b64encode(hash_bytes).decode()
    return encoded[:7]
```

**Approach C: Counter-based**
```python
counter = 1000000
def generate_counter():
    global counter
    counter += 1
    return base62_encode(counter)
```

Fill in the comparison:

| Aspect | Random | Hash | Counter |
|--------|--------|------|---------|
| Collisions possible? | | | |
| Same URL → same code? | | | |
| Predictable? | | | |
| Distributed-friendly? | | | |

### Task 3: Database Schema

Design the database schema:

```sql
CREATE TABLE urls (
    -- TODO: Define columns
);

-- TODO: Add necessary indexes
```

Consider:
- Primary key choice
- What to store
- Query patterns

### Task 4: API Design

Design the REST API:

**Create short URL:**
```
Method: ___
Endpoint: ___
Request body:
{
    // TODO
}
Response:
{
    // TODO
}
```

**Redirect:**
```
Method: ___
Endpoint: ___
Response: ___
```

### Task 5: Redirect Implementation

Implement the redirect logic:

```python
def redirect(short_code):
    # TODO: Implement
    # 1. Look up short_code
    # 2. Handle not found
    # 3. Return redirect
    pass
```

Should you use 301 (Permanent) or 302 (Temporary) redirect? Why?

---

<details>
<summary>Hints</summary>

- log(1,000,000,000) / log(62) ≈ 5.95, so 6 characters is minimum
- Hash-based gives same code for same URL
- Counter-based needs central coordination
- 301 is cached by browser, 302 is not

</details>

<details>
<summary>Solution</summary>

### Task 1: Short Code Length

```
26^n >= 1,000,000,000
26^6 = 308,915,776 (not enough)
26^7 = 8,031,810,176 (enough)
n = 7

52^n >= 1,000,000,000
52^5 = 380,204,032 (not enough)
52^6 = 19,770,609,664 (enough)
n = 6

62^n >= 1,000,000,000
62^5 = 916,132,832 (not enough)
62^6 = 56,800,235,584 (enough)
n = 6
```

**Why longer:** Buffer for growth, avoid near-collisions, look more professional.

### Task 2: Comparison

| Aspect | Random | Hash | Counter |
|--------|--------|------|---------|
| Collisions possible? | Yes | Yes | No |
| Same URL → same code? | No | Yes | No |
| Predictable? | No | No | Yes |
| Distributed-friendly? | Yes | Yes | No (needs coordination) |

### Task 3: Database Schema

```sql
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    click_count BIGINT DEFAULT 0
);

CREATE INDEX idx_short_code ON urls(short_code);
CREATE INDEX idx_expires_at ON urls(expires_at) WHERE expires_at IS NOT NULL;
```

### Task 4: API Design

**Create:**
```
Method: POST
Endpoint: /api/shorten
Request body:
{
    "url": "https://example.com/very/long/path",
    "custom_alias": "my-link",  // optional
    "expires_at": "2024-12-31"  // optional
}
Response:
{
    "short_url": "https://short.ly/abc123",
    "short_code": "abc123",
    "expires_at": "2024-12-31"
}
```

**Redirect:**
```
Method: GET
Endpoint: /{short_code}
Response: 302 Redirect with Location header
```

### Task 5: Redirect Implementation

```python
from flask import Flask, redirect, abort

app = Flask(__name__)

@app.route('/<short_code>')
def redirect_url(short_code):
    # 1. Look up short code
    url_record = db.query(
        "SELECT original_url FROM urls WHERE short_code = ?",
        short_code
    )
    
    # 2. Handle not found
    if not url_record:
        abort(404)
    
    # 3. Async: Update click count
    queue.publish("click", {"short_code": short_code})
    
    # 4. Redirect
    return redirect(url_record.original_url, code=302)
```

**301 vs 302:**
- 302 (Temporary): Recommended - allows analytics, can change destination
- 301 (Permanent): Browser caches, faster, but no analytics

</details>
