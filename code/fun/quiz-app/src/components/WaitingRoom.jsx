import { useState, useEffect, useCallback } from 'react'
import './WaitingRoom.css'

const COUNTDOWN_SECONDS = 10

function WaitingRoom({ participants, onStart, onReset, quizTitle, isHost, currentParticipant, countdownActive, countdownValue }) {
  const isSmokeTest = import.meta.env.VITE_SMOKE_TEST === 'true'
  const [localCountdown, setLocalCountdown] = useState(null)
  const [isStarting, setIsStarting] = useState(false)

  // Filter out host from players
  const players = participants.filter(p => !p.isHost)

  // Use external countdown if provided (for multiplayer sync), otherwise local
  const countdown = countdownActive ? countdownValue : localCountdown
  const showCountdown = countdownActive || localCountdown !== null

  const handleStartClick = useCallback(() => {
    if (isStarting) return
    setIsStarting(true)
    setLocalCountdown(COUNTDOWN_SECONDS)
  }, [isStarting])

  // Local countdown timer
  useEffect(() => {
    if (localCountdown === null) return

    if (localCountdown <= 0) {
      // Countdown complete - start the quiz
      onStart(isSmokeTest)
      return
    }

    const timer = setTimeout(() => {
      setLocalCountdown(prev => prev - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [localCountdown, onStart, isSmokeTest])

  // Cancel countdown
  const handleCancelCountdown = useCallback(() => {
    setLocalCountdown(null)
    setIsStarting(false)
  }, [])

  return (
    <div className="waiting-room">
      {/* Countdown Overlay */}
      {showCountdown && (
        <div className="countdown-overlay">
          <div className="countdown-content">
            <div className="countdown-title">Get Ready!</div>
            <div className={`countdown-number ${countdown <= 3 ? 'countdown-pulse' : ''}`}>
              {countdown}
            </div>
            <div className="countdown-subtitle">Quiz starting soon...</div>
            {isHost && localCountdown !== null && (
              <button onClick={handleCancelCountdown} className="cancel-countdown-btn">
                Cancel
              </button>
            )}
          </div>
        </div>
      )}

      <div className="card lobby-card">
        <div className="lobby-header">
          <h1 className="quiz-title">{quizTitle || 'Quiz'}</h1>
          <div className="lobby-badge">LOBBY</div>
        </div>

        {currentParticipant && (
          <div className="your-identity">
            <span className="identity-label">You joined as</span>
            <span className="identity-name">{currentParticipant.name}</span>
            {currentParticipant.isHost && <span className="host-badge">HOST</span>}
          </div>
        )}

        <div className="participant-section">
          <div className="participant-header">
            <span className="participant-icon">👥</span>
            <span className="participant-count-text">
              {players.length} {players.length === 1 ? 'Player' : 'Players'} in Lobby
            </span>
          </div>

          <div className="participants-grid">
            {players.map((participant, index) => (
              <div
                key={participant.id}
                className={`player-card ${participant.id === currentParticipant?.id ? 'is-you' : ''}`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="player-avatar">
                  {participant.name.charAt(0).toUpperCase()}
                </div>
                <div className="player-info">
                  <span className="player-name">{participant.name}</span>
                  <div className="player-badges">
                    {participant.id === currentParticipant?.id && <span className="badge you-badge">You</span>}
                  </div>
                </div>
                <div className="player-status">
                  <span className="status-dot"></span>
                  Ready
                </div>
              </div>
            ))}
          </div>

          {players.length === 0 && (
            <div className="no-players">
              <span className="no-players-icon">⏳</span>
              <span>Waiting for players to join...</span>
            </div>
          )}
        </div>

        {isHost ? (
          <div className="host-controls">
            <div className="host-info">
              <span className="host-info-icon">👑</span>
              <span>You're the host! Start when everyone's ready.</span>
            </div>
            <button
              onClick={handleStartClick}
              className="primary-button start-button"
              disabled={players.length === 0 || isStarting}
            >
              <span className="button-icon">🚀</span>
              {isSmokeTest ? 'Start Smoke Test' : 'Start Quiz'}
            </button>
            <button
              onClick={onReset}
              className="secondary-button reset-button"
              disabled={isStarting}
            >
              Reset Game
            </button>
          </div>
        ) : (
          <div className="participant-waiting">
            <div className="waiting-animation">
              <div className="pulse-ring"></div>
              <div className="pulse-ring delay-1"></div>
              <div className="pulse-ring delay-2"></div>
              <span className="waiting-icon">⏳</span>
            </div>
            <p className="waiting-message">Waiting for host to start the quiz...</p>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <button
              onClick={onReset}
              className="text-button leave-button"
              title="Leave the game and return to join screen"
            >
              ← Leave Game
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default WaitingRoom
