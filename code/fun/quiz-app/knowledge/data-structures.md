# Data Structures Used in This Project

## Overview

This document covers the JavaScript data structures used in the quiz app and their use cases.

## Arrays

### Basic Usage
```javascript
const participants = [
  { id: '1', name: 'Alice' },
  { id: '2', name: 'Bob' }
];
```

### Common Operations

**Add item:**
```javascript
// At end
const newArr = [...participants, newParticipant];

// At beginning
const newArr = [newParticipant, ...participants];

// At specific index
const newArr = [
  ...participants.slice(0, index),
  newParticipant,
  ...participants.slice(index)
];
```

**Remove item:**
```javascript
// By value
const newArr = participants.filter(p => p.id !== '1');

// By index
const newArr = participants.filter((_, i) => i !== index);
```

**Update item:**
```javascript
const newArr = participants.map(p =>
  p.id === '1' ? { ...p, name: 'Alice Updated' } : p
);
```

**Find item:**
```javascript
const alice = participants.find(p => p.name === 'Alice');
const index = participants.findIndex(p => p.id === '1');
const exists = participants.some(p => p.id === '1');
```

### In This Project

**Participants Array:**
```javascript
// Store in order of joining
participants: [
  { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
  { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' }
]
```

**Responses Array:**
```javascript
// Each answer submission
responses: [
  { participantId: '1', questionIndex: 0, answer: 'B', isCorrect: true, timeRemaining: 8 },
  { participantId: '2', questionIndex: 0, answer: 'C', isCorrect: false, timeRemaining: 3 }
]
```

## Objects (Hash Maps)

### Basic Usage
```javascript
const scores = {
  '1': 25,
  '2': 18,
  '3': 30
};
```

### Common Operations

**Access:**
```javascript
const score = scores['1'];        // 25
const score = scores[participantId];  // Dynamic key
```

**Add/Update:**
```javascript
const newScores = {
  ...scores,
  [participantId]: newScore
};
```

**Remove key:**
```javascript
const { [removeId]: removed, ...remaining } = scores;
```

**Check existence:**
```javascript
const hasScore = participantId in scores;
const hasScore = scores.hasOwnProperty(participantId);
```

**Iterate:**
```javascript
// Keys
Object.keys(scores)  // ['1', '2', '3']

// Values
Object.values(scores)  // [25, 18, 30]

// Entries
Object.entries(scores)  // [['1', 25], ['2', 18], ['3', 30]]

// Loop
for (const [id, score] of Object.entries(scores)) {
  console.log(`${id}: ${score}`);
}
```

### In This Project

**Scores Object:**
```javascript
// O(1) lookup by participant ID
scores: {
  'participant_1': 25,
  'participant_2': 18
}

// Usage
const myScore = scores[currentParticipant.id] || 0;
```

### Time Complexity

| Operation | Array | Object |
|-----------|-------|--------|
| Access by index/key | O(1) | O(1) |
| Search by value | O(n) | O(n) |
| Insert at end | O(1) | O(1) |
| Insert at beginning | O(n) | O(1) |
| Delete | O(n) | O(1) |

**When to use which:**
- **Array**: Ordered data, need to maintain sequence
- **Object**: Key-value lookup, unique IDs

## Sets

### Basic Usage
```javascript
const submittedIds = new Set(['1', '2']);
```

### Common Operations
```javascript
// Add
submittedIds.add('3');

// Check
submittedIds.has('1');  // true

// Remove
submittedIds.delete('1');

// Size
submittedIds.size;

// Iterate
for (const id of submittedIds) { ... }
```

### In This Project

**Track Submitted Answers:**
```javascript
// Create Set of participant IDs who submitted
const submittedParticipantIds = useMemo(() => {
  return new Set(
    responses
      .filter(r => r.questionIndex === currentQuestionIndex)
      .map(r => r.participantId)
  );
}, [responses, currentQuestionIndex]);

// Usage: O(1) lookup
if (submittedParticipantIds.has(participant.id)) {
  // Already submitted
}
```

### Why Sets?
- O(1) lookup vs O(n) with Array.includes()
- Automatic uniqueness
- Clean API for checking membership

## Maps

### Basic Usage
```javascript
const scoresMap = new Map();
scoresMap.set('1', 25);
scoresMap.get('1');  // 25
```

### Map vs Object

| Feature | Object | Map |
|---------|--------|-----|
| Keys | Strings only | Any type |
| Size | Object.keys().length | map.size |
| Order | Not guaranteed | Insertion order |
| Iteration | Object.entries() | Direct iteration |
| Performance | Good | Better for frequent add/remove |

**Use Map when:**
- Keys are not strings (objects, functions)
- Need guaranteed order
- Frequent additions/deletions
- Need size property

**Use Object when:**
- Simple string keys
- JSON serialization needed
- Object literal syntax preferred

## Sorting Algorithms

### Array.sort()

```javascript
// Default: string comparison (wrong for numbers!)
[10, 2, 1].sort()  // [1, 10, 2] ❌

// Numeric sort
[10, 2, 1].sort((a, b) => a - b)  // [1, 2, 10] ✅

// Descending
[1, 2, 10].sort((a, b) => b - a)  // [10, 2, 1]

// Objects by property
participants.sort((a, b) => 
  (scores[b.id] || 0) - (scores[a.id] || 0)
);
```

### In This Project

**Leaderboard Sorting:**
```javascript
function sortParticipantsByScore(participants, scores) {
  return [...participants].sort((a, b) => {
    const scoreA = scores[a.id] || 0;
    const scoreB = scores[b.id] || 0;
    return scoreB - scoreA;  // Descending (highest first)
  });
}
```

**Complexity:** O(n log n) average

## JSON Serialization

### Converting Data

```javascript
// Object/Array → JSON string
const json = JSON.stringify(gameState);

// JSON string → Object/Array  
const state = JSON.parse(json);
```

### Limitations

Cannot serialize:
- Functions
- `undefined`
- `Symbol`
- Circular references
- `Map`, `Set` (become `{}` or `[]`)

### In This Project

**localStorage persistence:**
```javascript
// Save
localStorage.setItem('quiz_state', JSON.stringify(gameState));

// Load
const saved = localStorage.getItem('quiz_state');
const gameState = saved ? JSON.parse(saved) : defaultState;
```

**API communication:**
```javascript
// Send
await fetch('/api/game', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ action, payload })
});

// Receive
const data = await response.json();
```

## Summary Table

| Structure | Use Case | Lookup | Insert | Delete |
|-----------|----------|--------|--------|--------|
| Array | Ordered list | O(n) | O(1)* | O(n) |
| Object | Key-value (string keys) | O(1) | O(1) | O(1) |
| Set | Unique values, membership | O(1) | O(1) | O(1) |
| Map | Key-value (any keys) | O(1) | O(1) | O(1) |

*O(1) at end, O(n) at beginning/middle
