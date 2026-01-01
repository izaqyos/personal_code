import { useState, useEffect, useRef, useCallback, useMemo } from 'react'
import { sortParticipantsByScore } from '../utils/quizUtils'
import './QuizScreen.css'

const DEFAULT_TIMER = 20

function QuizScreen({
  question,
  questionNumber,
  totalQuestions,
  participants,
  currentParticipant,
  isHost,
  scores,
  responses,
  onAnswerSubmit,
  onNextQuestion,
  timerDuration = DEFAULT_TIMER
}) {
  const [timeRemaining, setTimeRemaining] = useState(timerDuration)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [hasSubmitted, setHasSubmitted] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const submittingRef = useRef(false)

  // Check who has submitted for this question (from server responses)
  const submittedParticipantIds = useMemo(() => {
    return new Set(
      responses
        .filter(r => r.questionIndex === questionNumber - 1)
        .map(r => r.participantId)
    )
  }, [responses, questionNumber])

  // Check if current participant already submitted
  const currentParticipantSubmitted = currentParticipant
    ? submittedParticipantIds.has(currentParticipant.id)
    : false

  // Memoize sorted participants for leaderboard
  const sortedParticipants = useMemo(
    () => sortParticipantsByScore(participants, scores),
    [participants, scores]
  )

  // Reset state on new question
  useEffect(() => {
    setTimeRemaining(timerDuration)
    setSelectedAnswer(null)
    setHasSubmitted(false)
    setShowResults(false)
    submittingRef.current = false
  }, [question.id, timerDuration])

  // Sync hasSubmitted with server state
  useEffect(() => {
    if (currentParticipantSubmitted && !hasSubmitted) {
      setHasSubmitted(true)
    }
  }, [currentParticipantSubmitted, hasSubmitted])

  // Timer countdown
  useEffect(() => {
    if (timeRemaining > 0 && !showResults) {
      const timer = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
      return () => clearTimeout(timer)
    } else if (timeRemaining === 0 && !showResults) {
      handleTimeUp()
    }
  }, [timeRemaining, showResults])

  // Show results when all participants submitted
  useEffect(() => {
    if (submittedParticipantIds.size === participants.length && participants.length > 0) {
      setShowResults(true)
    }
  }, [submittedParticipantIds.size, participants.length])

  const handleTimeUp = () => {
    setShowResults(true)
    // Auto-submit if participant hasn't answered
    if (currentParticipant && !hasSubmitted && !currentParticipantSubmitted) {
      onAnswerSubmit(currentParticipant.id, null, false, 0)
      setHasSubmitted(true)
    }
  }

  const handleAnswerSelect = (answerId) => {
    if (hasSubmitted || showResults) return
    setSelectedAnswer(answerId)
  }

  const handleSubmit = useCallback(() => {
    if (submittingRef.current || hasSubmitted || showResults || !currentParticipant) return

    submittingRef.current = true
    const isCorrect = selectedAnswer === question.correctAnswer

    setHasSubmitted(true)
    onAnswerSubmit(currentParticipant.id, selectedAnswer, isCorrect, timeRemaining)
  }, [hasSubmitted, showResults, currentParticipant, selectedAnswer, question.correctAnswer, timeRemaining, onAnswerSubmit])

  const getAnswerClass = (answerId) => {
    if (!showResults) {
      return selectedAnswer === answerId ? 'selected' : ''
    }
    if (answerId === question.correctAnswer) {
      return 'correct'
    }
    if (selectedAnswer === answerId && answerId !== question.correctAnswer) {
      return 'incorrect'
    }
    return ''
  }

  const getAnswerIcon = (answerId) => {
    if (!showResults) return null
    if (answerId === question.correctAnswer) {
      return <span className="answer-icon correct-icon" aria-hidden="true">✓</span>
    }
    if (selectedAnswer === answerId && answerId !== question.correctAnswer) {
      return <span className="answer-icon incorrect-icon" aria-hidden="true">✗</span>
    }
    return null
  }

  // Participant view - only their own answers
  const renderParticipantView = () => (
    <div className="participant-answer-section">
      <div className="participant-header">
        <span className="participant-name">{currentParticipant?.name}</span>
        <span className="participant-score">Score: {scores[currentParticipant?.id] || 0}</span>
      </div>

      <div className="answer-options" role="group" aria-label="Answer options">
        {question.options.map(option => (
          <button
            key={option.id}
            className={`answer-option ${getAnswerClass(option.id)}`}
            onClick={() => handleAnswerSelect(option.id)}
            disabled={hasSubmitted || showResults}
          >
            <span className="option-label">{option.id}</span>
            <span className="option-text">{option.text}</span>
            {getAnswerIcon(option.id)}
          </button>
        ))}
      </div>

      {!hasSubmitted && !showResults && (
        <button
          onClick={handleSubmit}
          disabled={!selectedAnswer}
          className="submit-button"
        >
          Submit Answer
        </button>
      )}

      {hasSubmitted && !showResults && (
        <div className="submitted-indicator">
          ✓ Answer Submitted - Waiting for others...
        </div>
      )}
    </div>
  )

  // Host view - see all participants' status
  const renderHostView = () => (
    <div className="host-view">
      <div className="participants-status">
        <h3>Participants Status ({submittedParticipantIds.size}/{participants.length})</h3>
        <div className="status-list">
          {participants.map(p => (
            <div key={p.id} className="status-item">
              <span className="status-name">{p.name}</span>
              <span className={`status-badge ${submittedParticipantIds.has(p.id) ? 'submitted' : 'waiting'}`}>
                {submittedParticipantIds.has(p.id) ? '✓ Submitted' : 'Waiting...'}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="answer-preview">
        <h3>Answer Options</h3>
        <div className="answer-options readonly">
          {question.options.map(option => (
            <div
              key={option.id}
              className={`answer-option ${showResults && option.id === question.correctAnswer ? 'correct' : ''}`}
            >
              <span className="option-label">{option.id}</span>
              <span className="option-text">{option.text}</span>
              {showResults && option.id === question.correctAnswer && (
                <span className="answer-icon correct-icon">✓</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  // Waiting view - for participants who haven't joined
  const renderWaitingView = () => (
    <div className="waiting-view">
      <p>Waiting for game sync...</p>
      <p className="hint">If you just joined, please wait for the next question.</p>
    </div>
  )

  return (
    <div className="quiz-screen">
      <div className="quiz-header">
        <div className="question-info">
          <span className="question-number">Question {questionNumber} of {totalQuestions}</span>
          <div className="timer" role="timer" aria-live="polite">
            <span className={`timer-value ${timeRemaining <= 5 ? 'warning' : ''}`}>
              {timeRemaining}s
            </span>
          </div>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
      </div>

      <div className="card quiz-card">
        <h2 className="question-text">
          <span className="question-emoji">{question.emoji}</span>
          {question.question}
        </h2>

        <div className="participants-answers">
          {isHost ? renderHostView() : currentParticipant ? renderParticipantView() : renderWaitingView()}
        </div>

        {showResults && (
          <div className="results-section">
            <div className="correct-answer">
              <strong>Correct Answer: {question.correctAnswer}</strong>
              <p className="hint">{question.hint}</p>
            </div>
            {isHost && (
              <button onClick={onNextQuestion} className="primary-button next-button">
                {questionNumber === totalQuestions ? 'View Results' : 'Next Question →'}
              </button>
            )}
            {!isHost && (
              <p className="waiting-for-host">Waiting for host to continue...</p>
            )}
          </div>
        )}
      </div>

      <div className="leaderboard-mini">
        <h3>Current Scores</h3>
        <div className="leaderboard-list">
          {sortedParticipants.map((participant, index) => (
            <div
              key={participant.id}
              className={`leaderboard-item ${participant.id === currentParticipant?.id ? 'current-player' : ''}`}
            >
              <span className="rank">#{index + 1}</span>
              <span className="name">{participant.name}</span>
              <span className="score">{scores[participant.id] || 0} pts</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default QuizScreen
