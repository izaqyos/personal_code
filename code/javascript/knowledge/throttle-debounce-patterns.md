# Throttle & Debounce Patterns in JavaScript

## Overview

**Throttle** and **Debounce** are rate-limiting techniques used to control how often a function executes, especially for high-frequency events like scrolling, resizing, typing, or mouse movement.

Both prevent performance issues by reducing function calls, but they work differently.

---

## The Problem They Solve

```javascript
// Without rate limiting - BAD
window.addEventListener('scroll', () => {
  console.log('Scrolling...'); // Fires hundreds of times per second!
  makeExpensiveAPICall();       // RIP your API limits and performance
});

// This fires 100+ times when you scroll for 1 second
// Each triggering expensive DOM queries, API calls, or computations
```

---

## Debounce

### Concept

**Debounce delays execution until the user stops the action for a specified time.**

Think: "Wait until they're done, then act once."

```
User types: h-e-l-l-o
Without debounce:  h -> API call
                   e -> API call
                   l -> API call
                   l -> API call
                   o -> API call (5 API calls!)

With debounce (300ms):
                   h -> wait 300ms... (cancelled by 'e')
                   e -> wait 300ms... (cancelled by 'l')
                   l -> wait 300ms... (cancelled by 'l')
                   l -> wait 300ms... (cancelled by 'o')
                   o -> wait 300ms... ✓ Execute! (1 API call)
```

### Implementation

```javascript
function debounce(func, delay) {
  let timeoutId;

  return function(...args) {
    // Clear previous timer
    clearTimeout(timeoutId);

    // Start new timer
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}
```

### Use Cases

1. **Search Input / Autocomplete**
   ```javascript
   const searchInput = document.getElementById('search');

   const debouncedSearch = debounce((query) => {
     fetch(`/api/search?q=${query}`)
       .then(res => res.json())
       .then(showResults);
   }, 300);

   searchInput.addEventListener('input', (e) => {
     debouncedSearch(e.target.value);
   });
   ```

2. **Form Validation**
   ```javascript
   const validateEmail = debounce((email) => {
     const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
     showValidationMessage(isValid);
   }, 500);

   emailInput.addEventListener('input', (e) => {
     validateEmail(e.target.value);
   });
   ```

3. **Window Resize**
   ```javascript
   const handleResize = debounce(() => {
     updateLayout();
     recalculatePositions();
   }, 250);

   window.addEventListener('resize', handleResize);
   ```

4. **Auto-save Draft**
   ```javascript
   const saveDraft = debounce((content) => {
     localStorage.setItem('draft', content);
     console.log('Draft saved!');
   }, 1000);

   editor.addEventListener('input', (e) => {
     saveDraft(e.target.value);
   });
   ```

---

## Throttle

### Concept

**Throttle executes at most once per specified time interval, regardless of how many times triggered.**

Think: "Execute now, then ignore calls for X milliseconds."

```
User scrolls continuously:
Without throttle:   Event Event Event Event Event Event Event...
                    ↓     ↓     ↓     ↓     ↓     ↓     ↓
                    All execute (100+ times!)

With throttle (100ms):
                    Event Event Event Event Event Event Event...
                    ↓           ↓           ↓           ↓
                    Execute     Execute     Execute     Execute (4 times)
                    |--100ms----|--100ms----|--100ms----|
```

### Implementation

#### Basic Throttle (Leading Edge)
```javascript
function throttle(func, delay) {
  let lastCall = 0;

  return function(...args) {
    const now = Date.now();

    if (now - lastCall >= delay) {
      lastCall = now;
      func.apply(this, args);
    }
  };
}
```

#### Advanced Throttle (Trailing Edge Support)
```javascript
function throttle(func, delay) {
  let timeoutId;
  let lastRan;

  return function(...args) {
    if (!lastRan) {
      // First call - execute immediately
      func.apply(this, args);
      lastRan = Date.now();
    } else {
      // Clear existing timeout
      clearTimeout(timeoutId);

      // Set new timeout for trailing call
      timeoutId = setTimeout(() => {
        if ((Date.now() - lastRan) >= delay) {
          func.apply(this, args);
          lastRan = Date.now();
        }
      }, delay - (Date.now() - lastRan));
    }
  };
}
```

### Use Cases

1. **Infinite Scroll**
   ```javascript
   const loadMore = throttle(() => {
     const scrollPosition = window.scrollY + window.innerHeight;
     const documentHeight = document.documentElement.scrollHeight;

     if (scrollPosition >= documentHeight - 200) {
       fetchNextPage();
     }
   }, 200);

   window.addEventListener('scroll', loadMore);
   ```

2. **Button Click Spam Prevention**
   ```javascript
   const submitButton = document.getElementById('submit');

   const throttledSubmit = throttle(() => {
     submitForm();
   }, 2000);

   submitButton.addEventListener('click', throttledSubmit);
   ```

3. **Mouse Movement Tracking**
   ```javascript
   const trackMouse = throttle((e) => {
     sendAnalytics('mouse_position', {
       x: e.clientX,
       y: e.clientY
     });
   }, 500);

   document.addEventListener('mousemove', trackMouse);
   ```

4. **Game Loop / Animation**
   ```javascript
   const updateGameState = throttle(() => {
     calculatePhysics();
     updatePositions();
     detectCollisions();
   }, 16); // ~60fps

   requestAnimationFrame(function gameLoop() {
     updateGameState();
     requestAnimationFrame(gameLoop);
   });
   ```

5. **API Rate Limiting**
   ```javascript
   const apiCall = throttle((data) => {
     fetch('/api/track', {
       method: 'POST',
       body: JSON.stringify(data)
     });
   }, 1000); // Max 1 call per second
   ```

---

## Debounce vs Throttle - When to Use Which?

| Scenario | Use | Why |
|----------|-----|-----|
| Search autocomplete | **Debounce** | Wait until user stops typing |
| Form validation | **Debounce** | Validate after user finishes input |
| Auto-save | **Debounce** | Save after user stops editing |
| Window resize | **Debounce** | Recalculate after resize ends |
| Infinite scroll | **Throttle** | Check scroll position periodically |
| Button spam prevention | **Throttle** | Allow max 1 click per interval |
| Mouse position tracking | **Throttle** | Track at regular intervals |
| Scroll progress indicator | **Throttle** | Update indicator smoothly |
| Rate-limited API | **Throttle** | Respect API limits |

### Quick Decision Guide

**Use Debounce when:**
- You only care about the **final state** after user stops
- Examples: search, validation, auto-save

**Use Throttle when:**
- You want **regular updates** during continuous action
- Examples: scroll tracking, analytics, rate limiting

---

## React Implementations

### Custom Debounce Hook

```javascript
import { useEffect, useState } from 'react';

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    if (debouncedSearchTerm) {
      // API call happens only after user stops typing for 500ms
      searchAPI(debouncedSearchTerm);
    }
  }, [debouncedSearchTerm]);

  return (
    <input
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

### Custom Throttle Hook

```javascript
import { useRef, useCallback } from 'react';

function useThrottle(callback, delay) {
  const lastRan = useRef(Date.now());

  return useCallback((...args) => {
    if (Date.now() - lastRan.current >= delay) {
      callback(...args);
      lastRan.current = Date.now();
    }
  }, [callback, delay]);
}

// Usage
function ScrollTracker() {
  const handleScroll = useThrottle(() => {
    console.log('Scroll position:', window.scrollY);
    // Update analytics, progress bar, etc.
  }, 200);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return <div>Scroll me!</div>;
}
```

### Debounced Callback Hook

```javascript
import { useRef, useCallback } from 'react';

function useDebouncedCallback(callback, delay) {
  const timeoutRef = useRef(null);

  return useCallback((...args) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, delay);
  }, [callback, delay]);
}

// Usage
function FormComponent() {
  const saveToAPI = useDebouncedCallback((formData) => {
    fetch('/api/save', {
      method: 'POST',
      body: JSON.stringify(formData)
    });
  }, 1000);

  const handleChange = (field, value) => {
    const formData = { ...currentForm, [field]: value };
    saveToAPI(formData);
  };

  return <input onChange={(e) => handleChange('name', e.target.value)} />;
}
```

---

## Common Pitfalls

### 1. Creating New Debounced Function on Every Render

```javascript
// ❌ BAD - Creates new debounced function every render
function Component() {
  const handleSearch = (query) => { /* ... */ };

  return <input onChange={debounce(handleSearch, 300)} />;
}

// ✅ GOOD - Stable reference across renders
function Component() {
  const handleSearch = useCallback(
    debounce((query) => { /* ... */ }, 300),
    []
  );

  return <input onChange={handleSearch} />;
}
```

### 2. Not Cleaning Up Timers

```javascript
// ❌ BAD - Memory leak
useEffect(() => {
  const handler = debounce(() => { /* ... */ }, 300);
  window.addEventListener('scroll', handler);
  // Missing cleanup!
}, []);

// ✅ GOOD - Cleanup on unmount
useEffect(() => {
  const handler = debounce(() => { /* ... */ }, 300);
  window.addEventListener('scroll', handler);

  return () => {
    window.removeEventListener('scroll', handler);
  };
}, []);
```

### 3. Wrong Context (`this` binding)

```javascript
// ❌ BAD - Loses context
class Component {
  handleClick() {
    console.log(this); // undefined!
  }

  render() {
    return <button onClick={debounce(this.handleClick, 300)} />;
  }
}

// ✅ GOOD - Preserves context
class Component {
  handleClick = () => {
    console.log(this); // Component instance
  }

  render() {
    return <button onClick={debounce(this.handleClick, 300)} />;
  }
}
```

---

## Performance Comparison

```javascript
// Test scenario: User types "hello" quickly (5 keystrokes in 500ms)

// No rate limiting
// Executions: 5 (one per keystroke)
// API calls: 5
// Total time: immediate

// Debounce (300ms)
// Executions: 1 (after 300ms of silence)
// API calls: 1
// Total time: 800ms (500ms typing + 300ms wait)

// Throttle (300ms)
// Executions: 2 (at 0ms and 300ms)
// API calls: 2
// Total time: immediate + 300ms
```

---

## Advanced: Immediate Execution Option

Sometimes you want the function to execute **immediately** on the first call, then debounce/throttle subsequent calls.

### Debounce with Immediate

```javascript
function debounce(func, delay, immediate = false) {
  let timeoutId;

  return function(...args) {
    const callNow = immediate && !timeoutId;

    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      timeoutId = null;
      if (!immediate) {
        func.apply(this, args);
      }
    }, delay);

    if (callNow) {
      func.apply(this, args);
    }
  };
}

// Usage: Execute immediately, then ignore calls for 1 second
const handleClick = debounce(() => {
  console.log('Clicked!');
}, 1000, true);
```

---

## Testing

```javascript
// Using Jest fake timers
describe('debounce', () => {
  jest.useFakeTimers();

  it('delays function execution', () => {
    const func = jest.fn();
    const debounced = debounce(func, 300);

    debounced();
    expect(func).not.toHaveBeenCalled();

    jest.advanceTimersByTime(299);
    expect(func).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1);
    expect(func).toHaveBeenCalledTimes(1);
  });

  it('resets timer on subsequent calls', () => {
    const func = jest.fn();
    const debounced = debounce(func, 300);

    debounced();
    jest.advanceTimersByTime(100);
    debounced(); // Resets timer
    jest.advanceTimersByTime(299);
    expect(func).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1);
    expect(func).toHaveBeenCalledTimes(1);
  });
});
```

---

## Libraries

While it's good to understand the implementation, production apps often use battle-tested libraries:

### Lodash
```javascript
import { debounce, throttle } from 'lodash';

const debouncedSearch = debounce(searchAPI, 300);
const throttledScroll = throttle(trackScroll, 200);
```

### use-debounce (React)
```javascript
import { useDebounce } from 'use-debounce';

function Component() {
  const [value, setValue] = useState('');
  const [debouncedValue] = useDebounce(value, 1000);

  useEffect(() => {
    // API call with debounced value
  }, [debouncedValue]);
}
```

---

## Summary Cheat Sheet

| Feature | Debounce | Throttle |
|---------|----------|----------|
| **When executes** | After quiet period | At regular intervals |
| **Best for** | Final state matters | Regular updates matter |
| **Example** | Search input | Scroll tracking |
| **Frequency** | Once after delay | Multiple at intervals |
| **Cancel previous** | Yes | No |
| **Immediate option** | Available | Not typical |

**Remember:**
- **Debounce** = "Wait for calm, then act"
- **Throttle** = "Act every X seconds, ignore extra calls"

**Memory Tricks:**

- **De-BOUNCE** = Ball bouncing settles down → wait for stillness
- **THROTTLE** = Car throttle → steady controlled speed

**Implementation Mnemonics:**

- **Debounce** = "**C**lear, **S**et" (clearTimeout, setTimeout) - like clearing your desk before starting fresh
- **Throttle** = "**N**ow vs **L**ast" (Date.now() - lastCall) - like checking your watch since last break

Choose based on whether you need the **final result** (debounce) or **periodic updates** (throttle).
