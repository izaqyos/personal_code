# State Management Patterns

## The Reducer Pattern

### What is a Reducer?

A reducer is a pure function that takes the current state and an action, and returns a new state.

```javascript
(state, action) => newState
```

### Why Use Reducers?

1. **Predictable** - Same input always produces same output
2. **Testable** - Pure functions are easy to test
3. **Debuggable** - Log every action and state change
4. **Maintainable** - All state logic in one place

### Basic Structure

```javascript
// Initial state
const initialState = {
  participants: [],
  scores: {},
  screen: 'join'
};

// Reducer function
function gameReducer(state, action) {
  switch (action.type) {
    case 'ADD_PARTICIPANT':
      return {
        ...state,
        participants: [...state.participants, action.payload]
      };
    
    case 'UPDATE_SCORE':
      return {
        ...state,
        scores: {
          ...state.scores,
          [action.payload.id]: action.payload.score
        }
      };
    
    case 'CHANGE_SCREEN':
      return {
        ...state,
        screen: action.payload
      };
    
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

// Usage in React
function Game() {
  const [state, dispatch] = useReducer(gameReducer, initialState);
  
  const addPlayer = (name) => {
    dispatch({
      type: 'ADD_PARTICIPANT',
      payload: { id: Date.now(), name }
    });
  };
}
```

## State Machine Pattern

### Concept

A state machine has:
- **States** - The possible modes (e.g., join, waiting, quiz, results)
- **Events** - Actions that trigger transitions
- **Transitions** - Rules for moving between states

### Visual Representation

```
┌─────────┐  JOIN    ┌──────────┐  START   ┌──────────┐
│  join   │ ───────► │  waiting │ ───────► │   quiz   │
└─────────┘          └──────────┘          └────┬─────┘
                                                 │
                                                 │ COMPLETE
                                                 ▼
┌─────────┐  RESET   ┌──────────┐  RESET   ┌──────────┐
│  join   │ ◄─────── │  waiting │ ◄─────── │  results │
└─────────┘          └──────────┘          └──────────┘
```

### Implementation

```javascript
// Define valid transitions
const transitions = {
  join: {
    JOIN: 'waiting'
  },
  waiting: {
    START: 'quiz',
    RESET: 'join'
  },
  quiz: {
    COMPLETE: 'results',
    RESET: 'join'
  },
  results: {
    RESET: 'join'
  }
};

// Transition function
function transition(currentState, action) {
  const nextState = transitions[currentState]?.[action];
  if (!nextState) {
    console.warn(`Invalid transition: ${currentState} + ${action}`);
    return currentState;
  }
  return nextState;
}
```

### Benefits

1. **No invalid states** - Only defined transitions allowed
2. **Self-documenting** - Visual flow is clear
3. **Prevents bugs** - Can't skip steps or go backwards unexpectedly

## Immutability Patterns

### Why Immutable?

- React detects changes by reference comparison
- Mutable changes: `oldState === newState` → No re-render!
- Immutable changes: `oldState !== newState` → Re-renders!

### Object Updates

```javascript
// ❌ Mutating (bad)
state.user.name = 'Alice';

// ✅ Immutable (good)
const newState = {
  ...state,
  user: {
    ...state.user,
    name: 'Alice'
  }
};
```

### Array Updates

```javascript
// Add item
const newItems = [...items, newItem];

// Remove item
const newItems = items.filter(item => item.id !== removeId);

// Update item
const newItems = items.map(item =>
  item.id === updateId
    ? { ...item, name: 'Updated' }
    : item
);

// Insert at index
const newItems = [
  ...items.slice(0, index),
  newItem,
  ...items.slice(index)
];
```

### Object with Dynamic Keys

```javascript
// Add/update key
const newScores = {
  ...scores,
  [participantId]: newScore
};

// Remove key
const { [removeKey]: removed, ...remaining } = scores;
```

## Action Best Practices

### Action Structure

```javascript
// Standard action
{
  type: 'ACTION_NAME',     // Required: string constant
  payload: { ... }         // Optional: action data
}

// Examples
{ type: 'ADD_PARTICIPANT', payload: { id: '1', name: 'Alice' } }
{ type: 'SUBMIT_ANSWER', payload: { participantId: '1', answer: 'B' } }
{ type: 'RESET' }  // No payload needed
```

### Action Creators

```javascript
// Action creator functions (optional but clean)
const addParticipant = (name) => ({
  type: 'ADD_PARTICIPANT',
  payload: { id: Date.now().toString(), name, joinedAt: new Date() }
});

const submitAnswer = (participantId, answer, isCorrect) => ({
  type: 'SUBMIT_ANSWER',
  payload: { participantId, answer, isCorrect }
});

// Usage
dispatch(addParticipant('Alice'));
dispatch(submitAnswer('1', 'B', true));
```

## Derived State

**Rule**: Don't store what you can compute.

```javascript
// ❌ Bad: Storing derived state
const state = {
  participants: [...],
  scores: {...},
  leaderboard: [...]  // Derived from participants + scores
};

// ✅ Good: Compute when needed
const state = {
  participants: [...],
  scores: {...}
};

// Compute in component
const leaderboard = useMemo(() => {
  return participants
    .map(p => ({ ...p, score: scores[p.id] || 0 }))
    .sort((a, b) => b.score - a.score);
}, [participants, scores]);
```

### When to Compute

- **useMemo** - Cache expensive computations
- **Selector functions** - Reusable derived state logic

```javascript
// Selector function
function selectLeaderboard(state) {
  return state.participants
    .map(p => ({ ...p, score: state.scores[p.id] || 0 }))
    .sort((a, b) => b.score - a.score);
}

// Usage
const leaderboard = useMemo(
  () => selectLeaderboard(state),
  [state.participants, state.scores]
);
```

## Local vs Global State

### Local State (useState)
- Form inputs
- UI toggles (modal open, dropdown open)
- Temporary data (hover states)

### Global State (useReducer, Context)
- User authentication
- Game state (shared across screens)
- Theme/preferences

### Server State (fetch, SWR, React Query)
- API data
- Remote synchronization

## State Colocation

Keep state as close to where it's used as possible.

```
                    App
                     │
         ┌───────────┼───────────┐
         │           │           │
       Header     Content      Footer
         │           │
       Auth       └── GameState (useReducer)
     (global)          │
                ┌──────┼──────┐
                │      │      │
             Screen  Screen  Screen
                │
           LocalState (useState)
             - selectedAnswer
             - isAnimating
```

## Resources

- [useReducer React Docs](https://react.dev/reference/react/useReducer)
- [State Machines in React](https://xstate.js.org/docs/)
- [Immer for Immutability](https://immerjs.github.io/immer/)
