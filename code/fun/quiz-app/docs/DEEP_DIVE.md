# Quiz App - Deep Dive for Developers

This guide explains the codebase for developers who may be new to React or want to understand how everything works together.

## Table of Contents
1. [React Basics](#react-basics)
2. [Project Entry Point](#project-entry-point)
3. [Component Walkthrough](#component-walkthrough)
4. [State Management](#state-management)
5. [Custom Hooks](#custom-hooks)
6. [Utility Functions](#utility-functions)
7. [Testing](#testing)

---

## React Basics

### What is a Component?

A React component is a function that returns JSX (HTML-like syntax). Components are reusable building blocks.

```jsx
// Simple component
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>
}

// Usage
<Greeting name="Alice" />  // Renders: <h1>Hello, Alice!</h1>
```

### Key React Concepts Used in This App

| Concept | What it Does | Example in App |
|---------|--------------|----------------|
| `useState` | Stores component state | Timer countdown, selected answers |
| `useEffect` | Runs side effects | Save to localStorage, timer interval |
| `useReducer` | Complex state management | Quiz state (participants, scores) |
| `useCallback` | Memoizes functions | Event handlers in App.jsx |
| `useMemo` | Memoizes values | Sorted leaderboard |
| `useRef` | Persists value without re-render | Prevent duplicate submissions |

---

## Project Entry Point

### `src/main.jsx` - Where It All Starts

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

This file:
1. Imports the main `App` component
2. Finds the `<div id="root">` in `index.html`
3. Renders the React app inside it

### `src/App.jsx` - The Main Component

App.jsx is the "brain" of the application. It:
- Manages all quiz state using `useReducer`
- Decides which screen to show based on `state.screen`
- Passes data and callbacks to child components

```jsx
function App() {
  // 1. Initialize state with reducer
  const [state, dispatch] = useReducer(quizReducer, initialState)

  // 2. Load saved data from localStorage on mount
  useEffect(() => {
    const saved = getStorageItem('participants', [])
    if (saved.length > 0) {
      dispatch({ type: 'LOAD_SAVED_STATE', payload: { participants: saved } })
    }
  }, [])

  // 3. Render appropriate screen based on state
  return (
    <div className="app">
      {state.screen === 'join' && <JoinScreen onJoin={handleJoin} />}
      {state.screen === 'waiting' && <WaitingRoom ... />}
      {state.screen === 'quiz' && <QuizScreen ... />}
      {state.screen === 'results' && <ResultsScreen ... />}
    </div>
  )
}
```

---

## Component Walkthrough

### 1. JoinScreen (`src/components/JoinScreen.jsx`)

**Purpose:** Let users enter their name and join the quiz.

**Key Features:**
- Form with controlled input (React manages the input value)
- Validation (min 2 characters, allowed characters)
- Error display with accessibility (role="alert")

```jsx
function JoinScreen({ onJoin, quizTitle }) {
  // Local state for form
  const [name, setName] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()  // Don't reload page

    // Validate
    const validationError = validateName(name)
    if (validationError) {
      setError(validationError)
      return
    }

    // Success - call parent's handler
    onJoin(name.trim())
    setName('')  // Clear input
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => {
          setName(e.target.value)
          if (error) setError('')  // Clear error on typing
        }}
      />
      {error && <div role="alert">{error}</div>}
      <button type="submit">Join Quiz</button>
    </form>
  )
}
```

**Data Flow:**
```
User types → onChange → setName() → input updates
User clicks Join → handleSubmit → validate → onJoin(name) → App updates state
```

### 2. QuizScreen (`src/components/QuizScreen.jsx`)

**Purpose:** Display questions, handle answers, show timer.

**This is the most complex component. Key parts:**

```jsx
function QuizScreen({ question, participants, scores, onAnswerSubmit, ... }) {
  // Multiple pieces of state
  const [timeRemaining, setTimeRemaining] = useState(timerDuration)
  const [selectedAnswers, setSelectedAnswers] = useState({})  // { participantId: answerId }
  const [submittedAnswers, setSubmittedAnswers] = useState(new Set())
  const [showResults, setShowResults] = useState(false)

  // Ref to prevent double-submissions (doesn't cause re-render)
  const submittingRef = useRef(new Set())

  // Timer effect - runs every second
  useEffect(() => {
    if (timeRemaining > 0 && !showResults) {
      const timer = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
      return () => clearTimeout(timer)  // Cleanup on unmount
    } else if (timeRemaining === 0) {
      handleTimeUp()  // Auto-submit when time runs out
    }
  }, [timeRemaining, showResults])

  // Reset state when question changes
  useEffect(() => {
    setTimeRemaining(timerDuration)
    setSelectedAnswers({})
    setSubmittedAnswers(new Set())
    setShowResults(false)
  }, [question.id])  // Dependency: runs when question.id changes

  // ... render logic
}
```

**Understanding `useEffect` Dependencies:**
```jsx
useEffect(() => {
  // This code runs...
}, [dependency1, dependency2])  // ...when these values change
```
- `[]` = run once on mount
- `[question.id]` = run when question changes
- No array = run on every render (avoid this!)

### 3. ResultsScreen (`src/components/ResultsScreen.jsx`)

**Purpose:** Show final scores and allow downloading results.

**Key Feature - Download as JSON:**
```jsx
const handleDownload = () => {
  // 1. Format the data
  const resultsData = formatResultsData(participants, scores, responses, questions)

  // 2. Convert to JSON string
  const json = JSON.stringify(resultsData, null, 2)

  // 3. Create downloadable blob
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)

  // 4. Trigger download via hidden link
  const link = document.createElement('a')
  link.href = url
  link.download = `quiz-results-${new Date().toISOString().split('T')[0]}.json`
  link.click()

  // 5. Cleanup
  URL.revokeObjectURL(url)
}
```

---

## State Management

### The Reducer Pattern

Instead of many `useState` calls, we use one `useReducer` for complex, related state.

**`src/reducers/quizReducer.js`:**

```jsx
// Define action types as constants (prevents typos)
export const QUIZ_ACTIONS = {
  SELECT_QUIZ: 'SELECT_QUIZ',
  ADD_PARTICIPANT: 'ADD_PARTICIPANT',
  START_QUIZ: 'START_QUIZ',
  SUBMIT_ANSWER: 'SUBMIT_ANSWER',
  NEXT_QUESTION: 'NEXT_QUESTION',
  RESET_QUIZ: 'RESET_QUIZ',
}

// Initial state shape
export const initialQuizState = {
  screen: 'join',
  selectedQuiz: null,
  participants: [],
  currentQuestionIndex: 0,
  scores: {},
  responses: [],
}

// Reducer function - takes current state + action, returns new state
export function quizReducer(state, action) {
  switch (action.type) {
    case QUIZ_ACTIONS.ADD_PARTICIPANT:
      return {
        ...state,  // Copy existing state
        participants: [
          ...state.participants,  // Copy existing participants
          {
            id: crypto.randomUUID(),
            name: action.payload.name,
            joinedAt: new Date().toISOString()
          }
        ],
        screen: 'waiting'  // Navigate to waiting room
      }

    case QUIZ_ACTIONS.SUBMIT_ANSWER: {
      const { participantId, isCorrect, timeRemaining } = action.payload
      const points = isCorrect ? 10 + timeRemaining : 0

      return {
        ...state,
        scores: {
          ...state.scores,
          [participantId]: (state.scores[participantId] || 0) + points
        },
        responses: [...state.responses, action.payload]
      }
    }

    // ... other cases

    default:
      return state  // Unknown action, return unchanged state
  }
}
```

**How to Use:**
```jsx
// In App.jsx
const [state, dispatch] = useReducer(quizReducer, initialQuizState)

// Dispatch an action
dispatch({
  type: QUIZ_ACTIONS.ADD_PARTICIPANT,
  payload: { name: 'Alice' }
})
```

**Why Reducer?**
1. All state changes in one place (easier to debug)
2. Actions describe *what happened* (ADD_PARTICIPANT, not "set participants to...")
3. Easy to add logging/middleware
4. State changes are predictable and testable

---

## Custom Hooks

Hooks let you extract and reuse stateful logic.

### `useLocalStorage` (`src/hooks/useLocalStorage.js`)

**What it does:** Like `useState`, but persists to localStorage.

```jsx
export function useLocalStorage(key, initialValue) {
  // Initialize state from localStorage or use default
  const [storedValue, setStoredValue] = useState(() => {
    const item = window.localStorage.getItem(key)
    return item ? JSON.parse(item) : initialValue
  })

  // Wrapper that saves to localStorage
  const setValue = (value) => {
    setStoredValue(value)
    window.localStorage.setItem(key, JSON.stringify(value))
  }

  return [storedValue, setValue]
}

// Usage
const [participants, setParticipants] = useLocalStorage('quiz_participants', [])
```

### `useCountdownTimer` (`src/hooks/useCountdownTimer.js`)

**What it does:** Countdown timer with pause/resume/reset.

```jsx
export function useCountdownTimer(initialTime, onComplete) {
  const [timeRemaining, setTimeRemaining] = useState(initialTime)
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    if (!isRunning || timeRemaining <= 0) return

    const interval = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          onComplete?.()  // Call callback when done
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(interval)  // Cleanup
  }, [isRunning, timeRemaining, onComplete])

  return {
    timeRemaining,
    isRunning,
    start: () => setIsRunning(true),
    pause: () => setIsRunning(false),
    reset: (newTime) => {
      setTimeRemaining(newTime ?? initialTime)
      setIsRunning(false)
    }
  }
}
```

---

## Utility Functions

### `src/utils/quizUtils.js`

Pure functions (no side effects) for business logic:

```jsx
// Calculate points based on correctness and time remaining
export function calculatePoints(timeRemaining, isCorrect) {
  if (!isCorrect) return 0
  const BASE_POINTS = 10
  const TIME_BONUS = 1
  return BASE_POINTS + (TIME_BONUS * timeRemaining)
}

// Sort participants by score (highest first)
export function sortParticipantsByScore(participants, scores) {
  return [...participants].sort((a, b) => {
    return (scores[b.id] || 0) - (scores[a.id] || 0)
  })
}

// Format results for export
export function formatResultsData(participants, scores, responses, questions) {
  return {
    timestamp: new Date().toISOString(),
    participants: participants.map(p => ({
      name: p.name,
      finalScore: scores[p.id] || 0,
      // ... more data
    })),
    // ...
  }
}
```

### `src/utils/storage.js`

Safe localStorage operations with error handling:

```jsx
const STORAGE_PREFIX = 'quiz_app_'  // Namespace to avoid collisions

export function getStorageItem(key, defaultValue = null) {
  try {
    const item = localStorage.getItem(STORAGE_PREFIX + key)
    return item ? JSON.parse(item) : defaultValue
  } catch (error) {
    console.warn(`Error reading ${key} from localStorage:`, error)
    return defaultValue
  }
}

export function setStorageItem(key, value) {
  try {
    localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value))
    return true
  } catch (error) {
    // Handle quota exceeded, private browsing, etc.
    console.warn(`Error saving ${key} to localStorage:`, error)
    return false
  }
}
```

---

## Testing

### Test Types

| Type | Tool | Location | Purpose |
|------|------|----------|---------|
| Unit | Vitest | `src/utils/__tests__/` | Test utility functions |
| Component | React Testing Library | `src/components/__tests__/` | Test UI components |
| E2E | Playwright | `tests/e2e/` | Test full user flows |

### Unit Test Example

```jsx
// src/utils/__tests__/quizUtils.test.js
import { describe, it, expect } from 'vitest'
import { calculatePoints } from '../quizUtils'

describe('calculatePoints', () => {
  it('returns 0 for incorrect answers', () => {
    expect(calculatePoints(15, false)).toBe(0)
    expect(calculatePoints(0, false)).toBe(0)
  })

  it('returns base + time bonus for correct answers', () => {
    // 10 base + 8 time bonus = 18
    expect(calculatePoints(8, true)).toBe(18)
  })
})
```

### Component Test Example

```jsx
// src/components/__tests__/JoinScreen.test.jsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import JoinScreen from '../JoinScreen'

describe('JoinScreen', () => {
  it('calls onJoin when form submitted with valid name', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()  // Mock function

    render(<JoinScreen onJoin={mockOnJoin} />)

    // Find input and type
    const input = screen.getByPlaceholderText(/your name/i)
    await user.type(input, 'Alice')

    // Click submit
    await user.click(screen.getByRole('button', { name: /join/i }))

    // Verify callback was called with the name
    expect(mockOnJoin).toHaveBeenCalledWith('Alice')
  })

  it('shows error for empty name', async () => {
    const user = userEvent.setup()
    render(<JoinScreen onJoin={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /join/i }))

    // Error should be visible
    expect(screen.getByRole('alert')).toHaveTextContent(/enter your name/i)
  })
})
```

### E2E Test Example

```jsx
// tests/e2e/quiz-flow.spec.js
import { test, expect } from '@playwright/test'

test('complete quiz flow with 6 participants', async ({ page }) => {
  await page.goto('/')

  // Add participants
  const participants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']

  await page.getByPlaceholder(/your name/i).fill(participants[0])
  await page.getByRole('button', { name: /join/i }).click()

  // Should be in waiting room
  await expect(page.getByText(/waiting room/i)).toBeVisible()

  // Add more participants...
  for (let i = 1; i < participants.length; i++) {
    await page.getByRole('button', { name: /add another/i }).click()
    await page.getByPlaceholder(/your name/i).fill(participants[i])
    await page.getByRole('button', { name: /join/i }).click()
  }

  // Start quiz
  await page.getByRole('button', { name: /start quiz/i }).click()

  // Verify quiz screen
  await expect(page.getByText(/question 1 of/i)).toBeVisible()
})
```

### Running Tests

```bash
# Unit & Component tests
npm test              # Watch mode
npm test -- --run     # Single run

# E2E tests
npm run test:e2e      # All browsers
npm run test:e2e -- --project=chromium  # Chromium only

# All tests
npm run test:all
```

---

## Quick Reference

### File → Responsibility

| File | What it does |
|------|--------------|
| `App.jsx` | Screen routing, global state, event handlers |
| `JoinScreen.jsx` | Name input, validation, quiz selection |
| `WaitingRoom.jsx` | Participant list, add more, start button |
| `QuizScreen.jsx` | Questions, timer, answer submission |
| `ResultsScreen.jsx` | Scores, rankings, download |
| `quizReducer.js` | All state changes in one place |
| `storage.js` | Safe localStorage operations |
| `quizUtils.js` | Score calculation, data formatting |

### Common Patterns

**Props down, events up:**
```jsx
// Parent passes data down
<ChildComponent data={data} onAction={handleAction} />

// Child calls handler to notify parent
<button onClick={() => onAction(value)}>Do Thing</button>
```

**Conditional rendering:**
```jsx
{condition && <Component />}           // Show if true
{condition ? <A /> : <B />}            // Show A or B
{items.map(item => <Item key={item.id} />)}  // Render list
```

**State update patterns:**
```jsx
// Simple update
setState(newValue)

// Update based on previous
setState(prev => prev + 1)

// Update object (spread to copy)
setState(prev => ({ ...prev, newKey: value }))

// Update array
setState(prev => [...prev, newItem])
```
