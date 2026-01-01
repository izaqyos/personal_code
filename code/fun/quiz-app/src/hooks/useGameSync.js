import { useState, useEffect, useCallback, useRef } from 'react'

const API_URL = '/api/game'
const POLL_INTERVAL = 1000 // Poll every second

export function useGameSync() {
  const [gameState, setGameState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const lastUpdatedRef = useRef(0)

  // Fetch current state
  const fetchState = useCallback(async () => {
    try {
      const res = await fetch(API_URL)
      if (!res.ok) throw new Error('Failed to fetch game state')
      const data = await res.json()

      // Only update if state changed
      if (data.lastUpdated !== lastUpdatedRef.current) {
        lastUpdatedRef.current = data.lastUpdated
        setGameState(data)
      }
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  // Send action to server
  const sendAction = useCallback(async (action, payload = {}) => {
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, payload })
      })
      if (!res.ok) throw new Error('Failed to send action')
      const data = await res.json()
      lastUpdatedRef.current = data.lastUpdated
      setGameState(data)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [])

  // Initial fetch and polling
  useEffect(() => {
    fetchState()

    const interval = setInterval(fetchState, POLL_INTERVAL)
    return () => clearInterval(interval)
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
