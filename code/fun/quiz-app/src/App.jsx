import { useState, useCallback, useEffect } from 'react'
import JoinScreen from './components/JoinScreen'
import WaitingRoom from './components/WaitingRoom'
import QuizScreen from './components/QuizScreen'
import ResultsScreen from './components/ResultsScreen'
import QuizSelector from './components/QuizSelector'
import { defaultQuiz, quizzes } from './data'
import { useGameSync } from './hooks/useGameSync'
import './App.css'

// Session storage for this tab's participant
const SESSION_KEY = 'quiz_participant_id'
const HOST_KEY = 'quiz_is_host'

function getSessionParticipantId() {
  return sessionStorage.getItem(SESSION_KEY)
}

function setSessionParticipantId(id) {
  sessionStorage.setItem(SESSION_KEY, id)
}

function clearSession() {
  sessionStorage.removeItem(SESSION_KEY)
  sessionStorage.removeItem(HOST_KEY)
}

function isHost() {
  return sessionStorage.getItem(HOST_KEY) === 'true'
}

function setIsHost(value) {
  sessionStorage.setItem(HOST_KEY, value ? 'true' : 'false')
}

function App() {
  const { gameState, loading, error, joinGame, startQuiz, submitAnswer, nextQuestion, resetGame } = useGameSync()

  const [selectedQuiz, setSelectedQuiz] = useState(defaultQuiz)
  const [sessionParticipantId, setLocalSessionParticipantId] = useState(getSessionParticipantId)
  const [hostMode, setHostMode] = useState(isHost)

  // Get quiz data
  const allQuestions = selectedQuiz?.questions || []
  const questions = gameState?.activeQuestions || allQuestions
  const timerSeconds = selectedQuiz?.timerSeconds || 20

  // Derive screen from game state
  const screen = gameState?.screen || 'join'
  const participants = gameState?.participants || []
  const scores = gameState?.scores || {}
  const responses = gameState?.responses || []
  const currentQuestionIndex = gameState?.currentQuestionIndex || 0

  // Find current participant
  const currentParticipant = participants.find(p => p.id === sessionParticipantId)

  const handleSelectQuiz = useCallback((quiz) => {
    setSelectedQuiz(quiz)
  }, [])

  const handleJoin = useCallback(async (name) => {
    const participantId = Date.now().toString()
    const participant = {
      id: participantId,
      name: name.trim(),
      joinedAt: new Date().toISOString()
    }

    // Save to session
    setSessionParticipantId(participantId)
    setLocalSessionParticipantId(participantId)

    await joinGame(participant)
  }, [joinGame])

  const handleHostJoin = useCallback(async () => {
    setIsHost(true)
    setHostMode(true)

    // Create a host participant (can also play)
    const participantId = 'host_' + Date.now().toString()
    const participant = {
      id: participantId,
      name: 'Host',
      joinedAt: new Date().toISOString(),
      isHost: true
    }

    setSessionParticipantId(participantId)
    setLocalSessionParticipantId(participantId)

    await joinGame(participant)
  }, [joinGame])

  const handleStartQuiz = useCallback(async (smokeTest = false) => {
    const selectedQuestions = smokeTest
      ? [...allQuestions].sort(() => Math.random() - 0.5).slice(0, 3)
      : allQuestions

    await startQuiz(selectedQuestions)
  }, [allQuestions, startQuiz])

  const handleAnswerSubmit = useCallback(async (participantId, answer, isCorrect, timeRemaining) => {
    await submitAnswer(
      participantId,
      answer,
      isCorrect,
      timeRemaining,
      currentQuestionIndex,
      questions[currentQuestionIndex]?.id
    )
  }, [currentQuestionIndex, questions, submitAnswer])

  const handleNextQuestion = useCallback(async () => {
    await nextQuestion(questions.length)
  }, [questions.length, nextQuestion])

  const handleReset = useCallback(async () => {
    await resetGame()
    clearSession()
    setLocalSessionParticipantId(null)
    setHostMode(false)
  }, [resetGame])

  // Loading state
  if (loading) {
    return (
      <div className="app loading-screen">
        <div className="card">
          <h2>Loading...</h2>
          <p>Connecting to game server</p>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="app error-screen">
        <div className="card">
          <h2>Connection Error</h2>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="primary-button">
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      {screen === 'join' && (
        <div className="join-wrapper">
          <QuizSelector
            onSelectQuiz={handleSelectQuiz}
            selectedQuizId={selectedQuiz?.id}
          />
          <JoinScreen
            onJoin={handleJoin}
            onHostJoin={handleHostJoin}
            quizTitle={selectedQuiz?.title}
          />
        </div>
      )}

      {screen === 'waiting' && (
        <WaitingRoom
          participants={participants}
          onStart={handleStartQuiz}
          onReset={handleReset}
          quizTitle={selectedQuiz?.title}
          isHost={hostMode}
          currentParticipant={currentParticipant}
        />
      )}

      {screen === 'quiz' && questions[currentQuestionIndex] && (
        <QuizScreen
          question={questions[currentQuestionIndex]}
          questionNumber={currentQuestionIndex + 1}
          totalQuestions={questions.length}
          participants={participants}
          currentParticipant={currentParticipant}
          isHost={hostMode}
          scores={scores}
          responses={responses}
          onAnswerSubmit={handleAnswerSubmit}
          onNextQuestion={handleNextQuestion}
          timerDuration={timerSeconds}
        />
      )}

      {screen === 'results' && (
        <ResultsScreen
          participants={participants}
          scores={scores}
          responses={responses}
          questions={questions}
          onReset={handleReset}
          quizTitle={selectedQuiz?.title}
        />
      )}
    </div>
  )
}

export default App
