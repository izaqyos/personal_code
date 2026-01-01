import { useState } from 'react'
import './JoinScreen.css'

const MIN_NAME_LENGTH = 2
const MAX_NAME_LENGTH = 30

function JoinScreen({ onJoin, onHostJoin, quizTitle }) {
  const [name, setName] = useState('')
  const [error, setError] = useState('')

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
    onJoin(name.trim())
    setName('')
  }

  const handleChange = (e) => {
    setName(e.target.value)
    // Clear error when user starts typing
    if (error) setError('')
  }

  return (
    <div className="join-screen">
      <div className="card">
        <h1>{quizTitle || 'Quiz'}</h1>
        <p>Enter your name to join the quiz!</p>
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
          <button type="submit" className="primary-button">
            Join Quiz
          </button>
        </form>
        {onHostJoin && (
          <div className="host-section">
            <p className="divider">or</p>
            <button onClick={onHostJoin} className="secondary-button host-button">
              Join as Host
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default JoinScreen
