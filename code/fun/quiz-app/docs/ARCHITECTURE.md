# Quiz App - Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser (Client)                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    React Application                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │    │
│  │  │   App.jsx   │  │  Reducer    │  │   localStorage  │  │    │
│  │  │  (Router)   │◄─┤  (State)    │◄─┤   (Persist)     │  │    │
│  │  └──────┬──────┘  └─────────────┘  └─────────────────┘  │    │
│  │         │                                                │    │
│  │         ▼                                                │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │                   Screens                        │    │    │
│  │  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌─────────┐  │    │    │
│  │  │  │ Join   │ │Waiting │ │  Quiz  │ │ Results │  │    │    │
│  │  │  │ Screen │ │  Room  │ │ Screen │ │ Screen  │  │    │    │
│  │  │  └────────┘ └────────┘ └────────┘ └─────────┘  │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │         │                                                │    │
│  │         ▼                                                │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │              Shared Components                   │    │    │
│  │  │  QuizSelector │ Timer │ Leaderboard │ etc.      │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Data Layer                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │    │
│  │  │ Quiz JSON    │  │   Hooks      │  │   Utils      │   │    │
│  │  │ (questions)  │  │ (state mgmt) │  │ (helpers)    │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Application Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│  Join   │───►│ Waiting  │───►│   Quiz   │───►│ Results │
│ Screen  │    │   Room   │    │  Screen  │    │ Screen  │
└─────────┘    └──────────┘    └──────────┘    └─────────┘
     │              │               │               │
     ▼              ▼               ▼               ▼
  Select       Add more        Answer          View scores
   quiz       participants    questions        & download
  + Join                      + Timer
```

## State Management

The app uses React's `useReducer` for centralized state management:

```
┌────────────────────────────────────────────────────────────┐
│                     Quiz State (useReducer)                 │
├────────────────────────────────────────────────────────────┤
│  screen: 'join' | 'waiting' | 'quiz' | 'results'           │
│  selectedQuiz: { id, title, questions[], timerSeconds }    │
│  participants: [{ id, name, joinedAt }]                    │
│  currentQuestionIndex: number                              │
│  scores: { participantId: points }                         │
│  responses: [{ participantId, questionId, answer, ... }]   │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                        Actions                              │
├────────────────────────────────────────────────────────────┤
│  SELECT_QUIZ      → Change active quiz                     │
│  ADD_PARTICIPANT  → Add player to game                     │
│  START_QUIZ       → Begin quiz (waiting → quiz)            │
│  SUBMIT_ANSWER    → Record answer + update score           │
│  NEXT_QUESTION    → Advance to next question or results    │
│  RESET_QUIZ       → Clear all state, start fresh           │
│  LOAD_SAVED_STATE → Restore from localStorage              │
└────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
quiz-app/
├── src/
│   ├── App.jsx              # Root component, screen router
│   ├── App.css              # Global styles
│   ├── main.jsx             # React entry point
│   │
│   ├── components/          # UI Components
│   │   ├── JoinScreen.jsx       # Name input + quiz selection
│   │   ├── WaitingRoom.jsx      # Participant list + start button
│   │   ├── QuizScreen.jsx       # Questions + answers + timer
│   │   ├── ResultsScreen.jsx    # Final scores + download
│   │   ├── QuizSelector.jsx     # Quiz picker cards
│   │   └── __tests__/           # Component tests
│   │
│   ├── data/                # Quiz data (JSON)
│   │   ├── index.js             # Exports all quizzes
│   │   ├── questions.json       # Programming quiz
│   │   └── web-development.json # Web dev quiz
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useLocalStorage.js   # Persist state to localStorage
│   │   └── useCountdownTimer.js # Timer with pause/resume
│   │
│   ├── reducers/            # State management
│   │   └── quizReducer.js       # Actions + reducer logic
│   │
│   └── utils/               # Helper functions
│       ├── storage.js           # Safe localStorage operations
│       ├── quizUtils.js         # Score calculation, sorting
│       └── __tests__/           # Unit tests
│
├── tests/
│   └── e2e/
│       └── quiz-flow.spec.js    # Playwright E2E tests
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md          # This file
│   └── DEEP_DIVE.md             # Code walkthrough
│
└── config files...
    ├── package.json
    ├── vite.config.js
    ├── vitest.config.js
    └── playwright.config.js
```

## Key Design Decisions

### 1. Single-Page App (SPA)
- No backend server required
- All state managed in browser
- Data persisted to localStorage

### 2. Screen-Based Navigation
- Simple state machine: join → waiting → quiz → results
- No URL routing needed (single flow)

### 3. Reducer Pattern
- Centralized state in `App.jsx`
- Predictable state transitions via actions
- Easy to debug and test

### 4. JSON-Based Quiz Data
- Easy to add/modify quizzes
- No code changes needed for new questions
- Configurable timer per quiz

### 5. Component Composition
- Each screen is self-contained
- Shared logic extracted to hooks/utils
- Props flow down, events flow up

## Data Flow Example: Submitting an Answer

```
┌──────────────┐
│ QuizScreen   │  User clicks answer option
└──────┬───────┘
       │ handleAnswerSelect(participantId, answerId)
       ▼
┌──────────────┐
│ Local State  │  selectedAnswers[participantId] = answerId
└──────┬───────┘
       │ User clicks "Submit Answer"
       ▼
┌──────────────┐
│ handleSubmit │  Calculate if correct, get time remaining
└──────┬───────┘
       │ onAnswerSubmit(participantId, answer, isCorrect, timeLeft)
       ▼
┌──────────────┐
│   App.jsx    │  dispatch(SUBMIT_ANSWER, payload)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Reducer     │  Update scores, add response to history
└──────┬───────┘
       │ New state returned
       ▼
┌──────────────┐
│ localStorage │  Auto-save via useEffect
└──────────────┘
```

## Scoring System

```
Points = isCorrect ? (BASE_POINTS + TIME_BONUS * timeRemaining) : 0

Where:
  BASE_POINTS = 10
  TIME_BONUS  = 1 (per second remaining)

Example:
  Correct with 8 seconds left = 10 + (1 * 8) = 18 points
  Incorrect = 0 points
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| UI Framework | React 18 | Component-based UI |
| Build Tool | Vite | Fast dev server & bundling |
| Styling | CSS3 | No external UI libraries |
| State | useReducer | Centralized state management |
| Persistence | localStorage | Browser data storage |
| Unit Tests | Vitest | Fast, Vite-native testing |
| Component Tests | React Testing Library | User-centric testing |
| E2E Tests | Playwright | Cross-browser testing |
