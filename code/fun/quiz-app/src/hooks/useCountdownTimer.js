import { useState, useEffect, useCallback, useRef } from 'react'

/**
 * Custom hook for countdown timer functionality
 *
 * @param {number} initialSeconds - Starting time in seconds
 * @param {Object} options - Configuration options
 * @param {Function} options.onComplete - Callback when timer reaches zero
 * @param {boolean} options.autoStart - Start timer automatically (default: true)
 * @returns {Object} Timer state and controls
 */
export function useCountdownTimer(initialSeconds, options = {}) {
  const { onComplete, autoStart = true } = options

  const [timeRemaining, setTimeRemaining] = useState(initialSeconds)
  const [isRunning, setIsRunning] = useState(autoStart)
  const [isComplete, setIsComplete] = useState(false)

  // Store callback in ref to avoid stale closures
  const onCompleteRef = useRef(onComplete)
  useEffect(() => {
    onCompleteRef.current = onComplete
  }, [onComplete])

  // Timer effect
  useEffect(() => {
    if (!isRunning || timeRemaining <= 0) return

    const timer = setTimeout(() => {
      setTimeRemaining(prev => prev - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [timeRemaining, isRunning])

  // Handle completion
  useEffect(() => {
    if (timeRemaining === 0 && isRunning && !isComplete) {
      setIsComplete(true)
      setIsRunning(false)
      onCompleteRef.current?.()
    }
  }, [timeRemaining, isRunning, isComplete])

  // Reset timer to initial value
  const reset = useCallback((newInitialSeconds) => {
    const seconds = newInitialSeconds ?? initialSeconds
    setTimeRemaining(seconds)
    setIsComplete(false)
    setIsRunning(autoStart)
  }, [initialSeconds, autoStart])

  // Pause timer
  const pause = useCallback(() => {
    setIsRunning(false)
  }, [])

  // Resume timer
  const resume = useCallback(() => {
    if (!isComplete) {
      setIsRunning(true)
    }
  }, [isComplete])

  // Start timer (alias for resume, but clearer intent)
  const start = useCallback(() => {
    if (!isComplete && !isRunning) {
      setIsRunning(true)
    }
  }, [isComplete, isRunning])

  // Check if timer is in warning zone (last 5 seconds)
  const isWarning = timeRemaining <= 5 && timeRemaining > 0

  return {
    timeRemaining,
    isRunning,
    isComplete,
    isWarning,
    reset,
    pause,
    resume,
    start
  }
}

export default useCountdownTimer
