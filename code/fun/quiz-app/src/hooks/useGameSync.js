import { useState, useEffect, useCallback, useRef } from 'react'

const API_URL = '/api/game'
const POLL_INTERVAL = 1000 // Poll every second
const LOCAL_STORAGE_KEY = 'quiz_game_state_local'

// Check if we're in local development mode (no Vercel API available)
const isLocalDev = import.meta.env.DEV && !import.meta.env.VITE_USE_API

// Default game state
const defaultState = {
  participants: [],
  scores: {},
  responses: [],
  screen: 'join',
  currentQuestionIndex: 0,
  activeQuestions: null,
  quizStarted: false,
  lastUpdated: Date.now()
}

// Local storage helpers for development mode
function getLocalState() {
  try {
    const stored = localStorage.getItem(LOCAL_STORAGE_KEY)
    return stored ? JSON.parse(stored) : { ...defaultState }
  } catch {
    return { ...defaultState }
  }
}

function setLocalState(state) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(state))
    // Dispatch storage event for cross-tab sync in local mode
    window.dispatchEvent(new StorageEvent('storage', {
      key: LOCAL_STORAGE_KEY,
      newValue: JSON.stringify(state)
    }))
    return true
  } catch {
    return false
  }
}

// Process local actions (mirrors server-side logic)
function processLocalAction(currentState, action, payload) {
  let gameState = { ...currentState }

  switch (action) {
    case 'JOIN': {
      const participant = payload.participant
      if (!gameState.participants.find(p => p.id === participant.id)) {
        gameState.participants = [...gameState.participants, participant]
        gameState.scores = { ...gameState.scores, [participant.id]: 0 }
      }
      if (gameState.screen === 'join') {
        gameState.screen = 'waiting'
      }
      break
    }
    case 'START':
      gameState.screen = 'quiz'
      gameState.quizStarted = true
      gameState.currentQuestionIndex = 0
      gameState.activeQuestions = payload.activeQuestions || null
      break

    case 'SUBMIT_ANSWER': {
      const { participantId, answer, isCorrect, timeRemaining, questionIndex, questionId } = payload
      const alreadySubmitted = gameState.responses.some(
        r => r.participantId === participantId && r.questionIndex === questionIndex
      )
      if (!alreadySubmitted) {
        gameState.responses = [...gameState.responses, {
          participantId,
          questionIndex,
          questionId,
          answer,
          isCorrect,
          timeRemaining,
          timestamp: new Date().toISOString()
        }]
        if (isCorrect) {
          const points = Math.max(1, Math.floor(timeRemaining / 2))
          gameState.scores = {
            ...gameState.scores,
            [participantId]: (gameState.scores[participantId] || 0) + points
          }
        }
      }
      break
    }
    case 'NEXT_QUESTION': {
      const totalQuestions = payload.totalQuestions
      if (gameState.currentQuestionIndex < totalQuestions - 1) {
        gameState.currentQuestionIndex++
      } else {
        gameState.screen = 'results'
      }
      break
    }
    case 'RESET':
      gameState = { ...defaultState, lastUpdated: Date.now() }
      break

    default:
      console.warn('[useGameSync] Unknown action:', action)
  }

  gameState.lastUpdated = Date.now()
  return gameState
}

export function useGameSync() {
  const [gameState, setGameState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const lastUpdatedRef = useRef(0)

  // Log mode on mount
  useEffect(() => {
    if (isLocalDev) {
      console.log('[useGameSync] 🏠 Running in LOCAL DEV mode (using localStorage)')
      console.log('[useGameSync] Set VITE_USE_API=true to use the API endpoint')
    } else {
      console.log('[useGameSync] 🌐 Running in API mode (using /api/game)')
    }
  }, [])

  // Fetch current state
  const fetchState = useCallback(async () => {
    try {
      if (isLocalDev) {
        // Local development mode - use localStorage
        const data = getLocalState()
        if (data.lastUpdated !== lastUpdatedRef.current) {
          lastUpdatedRef.current = data.lastUpdated
          setGameState(data)
        }
        setError(null)
        setLoading(false)
        return
      }

      // Production mode - use API
      const res = await fetch(API_URL)
      if (!res.ok) throw new Error('Failed to fetch game state')
      
      // Check if response is JSON
      const contentType = res.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('API returned non-JSON response. Are you running locally? Set VITE_USE_API=false or use vercel dev.')
      }
      
      const data = await res.json()

      // Only update if state changed
      if (data.lastUpdated !== lastUpdatedRef.current) {
        lastUpdatedRef.current = data.lastUpdated
        setGameState(data)
      }
      setError(null)
    } catch (err) {
      console.error('[useGameSync] Fetch error:', err.message)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  // Send action to server (or process locally in dev mode)
  const sendAction = useCallback(async (action, payload = {}) => {
    console.log(`[useGameSync] Action: ${action}`, payload)
    
    try {
      if (isLocalDev) {
        // Local development mode - process action locally
        const currentState = getLocalState()
        const newState = processLocalAction(currentState, action, payload)
        setLocalState(newState)
        lastUpdatedRef.current = newState.lastUpdated
        setGameState(newState)
        console.log(`[useGameSync] ✅ Action processed locally:`, newState)
        return newState
      }

      // Production mode - send to API
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, payload })
      })
      if (!res.ok) throw new Error('Failed to send action')
      const data = await res.json()
      lastUpdatedRef.current = data.lastUpdated
      setGameState(data)
      console.log(`[useGameSync] ✅ Action sent to API:`, data)
      return data
    } catch (err) {
      console.error(`[useGameSync] ❌ Action failed:`, err.message)
      setError(err.message)
      throw err
    }
  }, [])

  // Initial fetch and polling
  useEffect(() => {
    fetchState()

    const interval = setInterval(fetchState, POLL_INTERVAL)
    
    // In local mode, also listen for storage events from other tabs
    const handleStorageChange = (e) => {
      if (isLocalDev && e.key === LOCAL_STORAGE_KEY) {
        console.log('[useGameSync] 🔄 Detected state change from another tab')
        fetchState()
      }
    }
    
    if (isLocalDev) {
      window.addEventListener('storage', handleStorageChange)
    }

    return () => {
      clearInterval(interval)
      if (isLocalDev) {
        window.removeEventListener('storage', handleStorageChange)
      }
    }
  }, [fetchState])

  // Action helpers
  const joinGame = useCallback((participant) => {
    return sendAction('JOIN', { participant })
  }, [sendAction])

  const startQuiz = useCallback((activeQuestions) => {
    return sendAction('START', { activeQuestions })
  }, [sendAction])

  const submitAnswer = useCallback((participantId, answer, isCorrect, timeRemaining, questionIndex, questionId) => {
    return sendAction('SUBMIT_ANSWER', {
      participantId,
      answer,
      isCorrect,
      timeRemaining,
      questionIndex,
      questionId
    })
  }, [sendAction])

  const nextQuestion = useCallback((totalQuestions) => {
    return sendAction('NEXT_QUESTION', { totalQuestions })
  }, [sendAction])

  const resetGame = useCallback(() => {
    return sendAction('RESET')
  }, [sendAction])

  return {
    gameState,
    loading,
    error,
    joinGame,
    startQuiz,
    submitAnswer,
    nextQuestion,
    resetGame,
    refetch: fetchState
  }
}
