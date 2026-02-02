import { useState } from 'react'
import './JoinScreen.css'

const MIN_NAME_LENGTH = 2
const MAX_NAME_LENGTH = 30

function JoinScreen({ onJoin, onHostJoin, onReset, quizTitle }) {
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [mode, setMode] = useState(null) // null = choice screen, 'host' or 'player'

  const validateName = (value) => {
    const trimmed = value.trim()
    if (trimmed.length === 0) {
      return 'Please enter your name'
    }
    if (trimmed.length < MIN_NAME_LENGTH) {
      return `Name must be at least ${MIN_NAME_LENGTH} characters`
    }
    if (trimmed.length > MAX_NAME_LENGTH) {
      return `Name must be less than ${MAX_NAME_LENGTH} characters`
    }
    // Check for valid characters (letters including Hebrew, numbers, spaces, hyphens, apostrophes)
    if (!/^[\p{L}\p{N}\s\-']+$/u.test(trimmed)) {
      return 'Name can only contain letters, numbers, spaces, hyphens, and apostrophes'
    }
    return ''
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const validationError = validateName(name)
    if (validationError) {
      setError(validationError)
      return
    }
    setError('')
    if (mode === 'host') {
      onHostJoin(name.trim())
    } else {
      onJoin(name.trim())
    }
    setName('')
  }

  const handleChange = (e) => {
    setName(e.target.value)
    // Clear error when user starts typing
    if (error) setError('')
  }

  // Mode selection screen
  if (mode === null) {
    return (
      <div className="join-screen">
        <div className="card mode-selection">
          <h1>{quizTitle || 'Quiz'}</h1>
          <p className="subtitle">How would you like to join?</p>
          
          <div className="mode-buttons">
            <button 
              onClick={() => setMode('host')} 
              className="mode-button host-mode"
            >
              <span className="mode-icon">👑</span>
              <span className="mode-title">I'm the Host</span>
              <span className="mode-desc">Create & control the quiz</span>
            </button>
            
            <button 
              onClick={() => setMode('player')} 
              className="mode-button player-mode"
            >
              <span className="mode-icon">🎮</span>
              <span className="mode-title">I'm a Player</span>
              <span className="mode-desc">Join an existing quiz</span>
            </button>
          </div>

          {onReset && (
            <div className="reset-section">
              <button onClick={onReset} className="text-button reset-button" title="Clear any stale game state">
                🔄 Reset Game (if stuck)
              </button>
            </div>
          )}
        </div>
      </div>
    )
  }

  // Name entry screen (for both host and player)
  return (
    <div className="join-screen">
      <div className="card">
        <button onClick={() => setMode(null)} className="back-button">
          ← Back
        </button>
        <h1>{quizTitle || 'Quiz'}</h1>
        <div className={`role-badge ${mode === 'host' ? 'host-badge' : 'player-badge'}`}>
          {mode === 'host' ? '👑 Joining as Host' : '🎮 Joining as Player'}
        </div>
        <p>Enter your name to continue</p>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Your name"
            value={name}
            onChange={handleChange}
            autoFocus
            maxLength={MAX_NAME_LENGTH}
            minLength={MIN_NAME_LENGTH}
            aria-label="Enter your name"
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={error ? 'name-error' : undefined}
          />
          {error && (
            <div id="name-error" className="error-message" role="alert">
              {error}
            </div>
          )}
          <button type="submit" className={`primary-button ${mode === 'host' ? 'host-btn' : ''}`}>
            {mode === 'host' ? '👑 Start as Host' : '🎮 Join Quiz'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default JoinScreen
