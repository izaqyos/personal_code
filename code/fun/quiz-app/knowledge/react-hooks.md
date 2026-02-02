# React Hooks Deep Dive

## Overview

React Hooks are functions that let you "hook into" React state and lifecycle features from function components.

## Hooks Used in This Project

### 1. useState

**Purpose**: Add local state to function components

```jsx
const [count, setCount] = useState(0);
const [user, setUser] = useState({ name: '', id: null });
```

**Key Points:**
- Returns `[currentValue, setterFunction]`
- Setter replaces the entire value (not merging like class `this.setState`)
- For objects, spread to merge: `setUser(prev => ({ ...prev, name: 'Alice' }))`
- Initial value only used on first render

**In This Project:**
- `selectedAnswer` - Track user's answer selection
- `timeRemaining` - Countdown timer value
- `error` - Form validation errors

### 2. useEffect

**Purpose**: Run side effects (data fetching, subscriptions, DOM manipulation)

```jsx
// Run on every render
useEffect(() => {
  document.title = `Count: ${count}`;
});

// Run only when count changes
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);

// Run only on mount
useEffect(() => {
  fetchData();
}, []);

// Cleanup on unmount
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe();  // cleanup
}, []);
```

**Dependency Array Rules:**
- `[]` - Run once on mount
- `[dep1, dep2]` - Run when deps change
- No array - Run on every render (usually a mistake)

**In This Project:**
- Polling for game state updates
- Timer countdown intervals
- Session storage persistence

### 3. useCallback

**Purpose**: Memoize functions to prevent unnecessary re-renders

```jsx
// Without useCallback - new function every render
const handleClick = () => { doSomething(count); };

// With useCallback - same function reference if deps don't change
const handleClick = useCallback(() => {
  doSomething(count);
}, [count]);
```

**When to Use:**
- Passing callbacks to optimized child components (React.memo)
- Dependencies in useEffect that are functions
- Event handlers in render-heavy components

**In This Project:**
- `handleJoin`, `handleStartQuiz`, `handleSubmit` - Prevent re-creating handlers

### 4. useMemo

**Purpose**: Memoize computed values to avoid expensive recalculations

```jsx
// Without useMemo - sorts on every render
const sortedItems = items.sort((a, b) => a.score - b.score);

// With useMemo - only sorts when items change
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.score - b.score);
}, [items]);
```

**When to Use:**
- Expensive calculations (sorting, filtering large arrays)
- Object/array references for dependency arrays
- Derived state that shouldn't trigger effects

**In This Project:**
- `sortedParticipants` - Leaderboard sorting
- `submittedParticipantIds` - Set creation from responses array

### 5. useReducer

**Purpose**: Complex state logic with predictable state transitions

```jsx
const initialState = { count: 0, step: 1 };

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + state.step };
    case 'SET_STEP':
      return { ...state, step: action.payload };
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);
  
  return (
    <button onClick={() => dispatch({ type: 'INCREMENT' })}>
      {state.count}
    </button>
  );
}
```

**When to Use:**
- Multiple related state values
- Complex state transitions
- State that depends on previous state
- Sharing update logic between components

**In This Project:**
- Game state management (participants, scores, responses)
- Screen transitions (join → waiting → quiz → results)

### 6. useRef

**Purpose**: Persist mutable values without triggering re-renders

```jsx
// Store a value that survives re-renders
const renderCount = useRef(0);
renderCount.current++; // Doesn't trigger re-render

// Reference DOM elements
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();

// Store previous values
const prevValue = useRef(value);
useEffect(() => {
  prevValue.current = value;
}, [value]);
```

**In This Project:**
- `lastUpdatedRef` - Track last synced timestamp
- `submittingRef` - Prevent duplicate submissions

## Hook Rules

1. **Only call at top level** - Never in loops, conditions, or nested functions
2. **Only call in React functions** - Components or custom hooks
3. **Name custom hooks with `use` prefix** - `useGameSync`, `useLocalStorage`

## Common Patterns

### Fetching Data
```jsx
function useData(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    
    async function fetchData() {
      try {
        const res = await fetch(url);
        const json = await res.json();
        if (!cancelled) {
          setData(json);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      }
    }

    fetchData();
    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}
```

### Debouncing Input
```jsx
function useDebouncedValue(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### Previous Value
```jsx
function usePrevious(value) {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}
```

## Performance Tips

1. **Avoid creating objects in render**
   ```jsx
   // Bad - new object every render
   <Component style={{ color: 'red' }} />
   
   // Good - stable reference
   const style = useMemo(() => ({ color: 'red' }), []);
   <Component style={style} />
   ```

2. **Memoize expensive children**
   ```jsx
   const MemoChild = React.memo(ExpensiveChild);
   ```

3. **Split context to prevent unnecessary renders**
   ```jsx
   // Separate frequently-changing data
   <UserContext.Provider value={user}>
     <ThemeContext.Provider value={theme}>
       ...
     </ThemeContext.Provider>
   </UserContext.Provider>
   ```

## Resources

- [React Docs - Hooks](https://react.dev/reference/react)
- [useHooks.com](https://usehooks.com/) - Hook recipes
- [React Hooks FAQ](https://react.dev/learn/hooks-faq)
