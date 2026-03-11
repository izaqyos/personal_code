import { useState, useRef, useEffect } from 'react'
import { validateAnswer } from '../utils/answerValidation'
import './RiddleSlide.css'

export default function RiddleSlide({ slide, onSolved, wrongAttempts, onWrongAttempt }) {
  const [input, setInput] = useState('')
  const [shake, setShake] = useState(false)
  const [solved, setSolved] = useState(false)
  const [message, setMessage] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (solved) return

    if (validateAnswer(input, slide.acceptedAnswers)) {
      setSolved(true)
      setMessage('!נכון! כל הכבוד')
      setTimeout(() => onSolved(), 1200)
    } else {
      setShake(true)
      onWrongAttempt()
      setMessage('לא נכון, נסי שוב!')
      setTimeout(() => setShake(false), 500)
    }
  }

  const showHint = wrongAttempts >= 2 && !solved

  return (
    <div className="riddle-slide">
      <div className="riddle-label">{slide.label}</div>
      <h2 className="riddle-number">חידה {slide.number}</h2>
      <p className="riddle-text">{slide.text}</p>

      {showHint && slide.hint && (
        <p className="riddle-hint" data-testid="hint">
          💡 רמז: {slide.hint}
        </p>
      )}

      <form onSubmit={handleSubmit} className="riddle-form">
        <input
          ref={inputRef}
          type="text"
          dir="rtl"
          className={`riddle-input ${shake ? 'shake' : ''} ${solved ? 'solved' : ''}`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="...הקלידי את התשובה"
          disabled={solved}
          data-testid="answer-input"
        />
        <button
          type="submit"
          className={`riddle-submit ${solved ? 'solved' : ''}`}
          disabled={solved || !input.trim()}
          data-testid="submit-button"
        >
          {solved ? '✓' : '!בדקי'}
        </button>
      </form>

      {message && (
        <p className={`riddle-message ${solved ? 'success' : 'error'}`} data-testid="message">
          {message}
        </p>
      )}
    </div>
  )
}
