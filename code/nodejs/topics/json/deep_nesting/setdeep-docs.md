# `setDeep` — Iterative DFS Deep Property Setter

Find and update a property by name **anywhere** in a deeply nested JS object, regardless of path. Cycle-safe, stack-based, zero dependencies.

---

## The Problem

You have a deeply nested object and know the **property name** but not the **path**. `lodash.set` requires a known path (`a.b.c[0].d`). No major lib offers "find by key name at any depth" out of the box.

## Why Iterative DFS

| Approach | Pros | Cons |
|---|---|---|
| Recursive DFS | Simple, readable | Call stack overflow on deep trees (~10-15k frames) |
| **Iterative DFS** | **Heap-based stack, no overflow, cycle-safe** | Slightly more code |
| BFS | Hits shallow matches first | Queue overhead, `shift()` is O(n) without a real queue |

Iterative DFS gives us full control over traversal without risking the call stack.

---

## Implementation

```js
function setDeep(obj, key, value, firstOnly = false) {
  const stack = [obj];
  const seen = new WeakSet();

  while (stack.length) {
    const node = stack.pop();
    if (seen.has(node)) continue;
    seen.add(node);

    for (const k in node) {
      if (k === key) {
        node[k] = value;
        if (firstOnly) return obj;
      }
      const child = node[k];
      if (child && typeof child === 'object') {
        stack.push(child);
      }
    }
  }

  return obj;
}
```

### Parameters

| Param | Type | Description |
|---|---|---|
| `obj` | `object` | Root object to traverse |
| `key` | `string` | Property name to find |
| `value` | `any` | New value to set |
| `firstOnly` | `boolean` | `false` = update all matches, `true` = stop after first |

### Returns

The mutated `obj` (same reference).

---

## How It Works

1. Push root object onto the stack.
2. Pop a node. If already `seen`, skip (cycle protection).
3. Mark node as `seen` via `WeakSet`.
4. Iterate own + inherited enumerable keys (`for...in`).
5. If key matches, update the value. If `firstOnly`, return early.
6. If child is a non-null object, push onto stack for further traversal.
7. Repeat until stack is empty.

---

## Key Design Decisions

### `WeakSet` for cycle detection

- `WeakSet` only holds objects — exactly what we need since primitives can't cause cycles.
- Weak references mean no memory leaks; entries are GC'd when the object is.
- O(1) lookup vs. array-based `includes()` which is O(n).

### `for...in` vs `Object.keys()`

- `for...in` covers both own and inherited enumerable properties **and** array indices.
- Use `Object.keys()` or add `hasOwnProperty` check if u want own-properties only.

### Mutation vs. Immutable

This mutates the original object. If u need immutability (React state, Redux), wrap with `structuredClone` first:

```js
const updated = setDeep(structuredClone(obj), 'target', newValue);
```

Or use **Immer** for more ergonomic immutable updates.

### DFS Traversal Order

Stack-based DFS processes children in **reverse insertion order** (last key pushed = first explored). This means `firstOnly` doesn't guarantee hitting the *shallowest* match first. If u need shallowest-first, use BFS:

```js
// BFS variant — swap stack.pop() for queue.shift()
// or use a proper queue to avoid O(n) shift cost
const queue = [obj];
// ...
const node = queue.shift(); // instead of stack.pop()
```

---

## Tests

```js
// 1. Basic nested update
const o1 = { a: { b: { target: 1 } } };
setDeep(o1, 'target', 99);
console.assert(o1.a.b.target === 99);

// 2. Multiple occurrences — updates all
const o2 = { x: { val: 1 }, y: { z: { val: 2 } } };
setDeep(o2, 'val', 42);
console.assert(o2.x.val === 42 && o2.y.z.val === 42);

// 3. firstOnly — updates only one
const o3 = { x: { val: 1 }, y: { z: { val: 2 } } };
setDeep(o3, 'val', 42, true);
const vals = [o3.x.val, o3.y.z.val];
console.assert(vals.filter(v => v === 42).length === 1);

// 4. Circular reference — no infinite loop
const o4 = { a: { target: 1 } };
o4.a.self = o4;
o4.loop = o4.a;
const start = Date.now();
setDeep(o4, 'target', 77);
console.assert(o4.a.target === 77 && Date.now() - start < 100);

// 5. Array elements traversed
const o5 = { items: [{ id: 1 }, { id: 2 }, { nested: { id: 3 } }] };
setDeep(o5, 'id', 0);
console.assert(o5.items[0].id === 0 && o5.items[1].id === 0 && o5.items[2].nested.id === 0);

// 6. Key not found — no mutation
const o6 = { a: 1, b: { c: 2 } };
const before = JSON.stringify(o6);
setDeep(o6, 'zzz', 999);
console.assert(JSON.stringify(o6) === before);

// 7. Top-level key update
const o7 = { target: 'old', nested: { x: 1 } };
setDeep(o7, 'target', 'new');
console.assert(o7.target === 'new');

// 8. Null/undefined values — no crash
const o8 = { a: null, b: undefined, c: { d: null, target: 1 } };
setDeep(o8, 'target', 50);
console.assert(o8.c.target === 50);

// 9. Deeply nested (10 levels)
let o9 = { level: 0 };
let cur = o9;
for (let i = 1; i <= 10; i++) {
  cur.child = { level: i };
  cur = cur.child;
}
cur.target = 'deep';
setDeep(o9, 'target', 'found');
console.assert(cur.target === 'found');

// 10. Mixed types — skips primitives & functions
const o10 = { a: 42, b: 'str', c: true, d: () => {}, e: { target: 1 }, f: Symbol('s') };
setDeep(o10, 'target', 99);
console.assert(o10.e.target === 99);
```

### Test Coverage Summary

| # | Case | Validates |
|---|---|---|
| 1 | Basic nested | Core traversal works |
| 2 | Multiple occurrences | All matches updated |
| 3 | `firstOnly` | Early exit after 1 match |
| 4 | Circular refs | `WeakSet` prevents infinite loop |
| 5 | Arrays | Array children are traversed |
| 6 | Key not found | No unintended side effects |
| 7 | Top-level key | Doesn't skip root-level properties |
| 8 | null/undefined | Graceful handling, no TypeError |
| 9 | 10 levels deep | Works at arbitrary depth |
| 10 | Mixed types | Primitives, functions, symbols safely skipped |

---

## Performance Considerations

- **Time complexity**: O(n) where n = total number of keys across all nested objects. Every key is visited at most once.
- **Space complexity**: O(d) for the stack + O(m) for the `WeakSet`, where d = max depth and m = number of unique object nodes.
- Fine for config objects, settings, API responses. Not ideal for massive datasets (100k+ nodes) — at that point consider indexed/flat structures.

---

## Edge Cases to Be Aware Of

1. **Prototype chain**: `for...in` enumerates inherited properties. Add `Object.hasOwn(node, k)` check if that's a concern.
2. **Symbols as keys**: `for...in` does not enumerate Symbol keys. Use `Object.getOwnPropertySymbols()` if needed.
3. **Getters/setters**: Accessing `node[k]` triggers getters. If a getter throws, it'll propagate. Wrap in try/catch if the object has unpredictable getters.
4. **Frozen/sealed objects**: `Object.freeze()` will cause the assignment to silently fail (or throw in strict mode). Check with `Object.isFrozen()` if needed.
5. **`Map`/`Set`/`TypedArray`**: These are objects but don't use string keys the same way. This function won't traverse their internal entries. Handle separately if needed.

---

## Alternatives Considered

| Tool | When to Use |
|---|---|
| `lodash.set` | Path is **known** (`a.b.c[0].d`) |
| `Immer` | Need **immutable** updates (React/Redux) |
| `jsonpath` / `jsonpath-plus` | Need full **query syntax** (`$..key`, filters) — overkill for simple key matching |
| This (`setDeep`) | Path **unknown**, only key name known, need cycle safety |
