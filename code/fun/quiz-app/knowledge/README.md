# Knowledge Directory

This directory contains documentation on key technologies, patterns, and concepts used in this project. Great for learning and reference!

## Contents

### React & Frontend
- [React Hooks Deep Dive](./react-hooks.md) - useState, useEffect, useCallback, useMemo, useReducer
- [React Testing Patterns](./testing-patterns.md) - Unit tests, component tests, mocking

### Architecture & Patterns
- [State Management Patterns](./state-management.md) - Reducer pattern, state machines
- [Real-Time Sync Patterns](./realtime-sync.md) - Polling, WebSockets, optimistic updates

### Backend & Deployment
- [Serverless Functions](./serverless.md) - Vercel serverless API, edge functions
- [Vercel KV (Redis)](./vercel-kv.md) - Key-value storage for game state

### Data Structures & Algorithms
- [Data Structures Used](./data-structures.md) - Arrays, Objects, Sets, Maps
- [Quiz Algorithms](./algorithms.md) - Scoring, shuffling, ranking

## Quick Reference

### Key Patterns in This Codebase

| Pattern | Location | Description |
|---------|----------|-------------|
| useReducer | `App.jsx`, `quizReducer.js` | Centralized state management |
| Custom Hooks | `hooks/` | Reusable stateful logic |
| Polling | `useGameSync.js` | Real-time state synchronization |
| Serverless API | `api/game.js` | Stateless request handling |
| Optimistic Updates | `useGameSync.js` | Local state + server sync |
