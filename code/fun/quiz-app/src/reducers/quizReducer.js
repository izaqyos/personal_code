// Action types
export const QUIZ_ACTIONS = {
  SELECT_QUIZ: 'SELECT_QUIZ',
  ADD_PARTICIPANT: 'ADD_PARTICIPANT',
  START_QUIZ: 'START_QUIZ',
  SUBMIT_ANSWER: 'SUBMIT_ANSWER',
  NEXT_QUESTION: 'NEXT_QUESTION',
  RESET_QUIZ: 'RESET_QUIZ',
  LOAD_SAVED_STATE: 'LOAD_SAVED_STATE',
  GO_TO_WAITING: 'GO_TO_WAITING',
  // Sync actions from other tabs
  SYNC_PARTICIPANT: 'SYNC_PARTICIPANT',
  SYNC_START: 'SYNC_START',
  SYNC_ANSWER: 'SYNC_ANSWER',
  SYNC_NEXT_QUESTION: 'SYNC_NEXT_QUESTION'
}

// Initial state
export const initialQuizState = {
  screen: 'join', // join, waiting, quiz, results
  selectedQuiz: null, // Currently selected quiz data
  participants: [],
  currentQuestionIndex: 0,
  scores: {},
  responses: [],
  quizStarted: false,
  activeQuestions: null // Questions for current quiz session (null = use all)
}

/**
 * Quiz reducer for managing all quiz-related state
 */
export function quizReducer(state, action) {
  switch (action.type) {
    case QUIZ_ACTIONS.SELECT_QUIZ: {
      return {
        ...state,
        selectedQuiz: action.payload.quiz
      }
    }

    case QUIZ_ACTIONS.ADD_PARTICIPANT: {
      const { participant } = action.payload
      return {
        ...state,
        participants: [...state.participants, participant],
        scores: { ...state.scores, [participant.id]: 0 },
        screen: 'waiting'
      }
    }

    case QUIZ_ACTIONS.SYNC_PARTICIPANT: {
      // From another tab - add participant if not exists
      const { participant } = action.payload
      if (state.participants.find(p => p.id === participant.id)) {
        return state // Already exists
      }
      return {
        ...state,
        participants: [...state.participants, participant],
        scores: { ...state.scores, [participant.id]: 0 }
      }
    }

    case QUIZ_ACTIONS.GO_TO_WAITING: {
      return {
        ...state,
        screen: 'waiting'
      }
    }

    case QUIZ_ACTIONS.START_QUIZ: {
      const { activeQuestions } = action.payload
      return {
        ...state,
        quizStarted: true,
        screen: 'quiz',
        currentQuestionIndex: 0,
        activeQuestions: activeQuestions || null
      }
    }

    case QUIZ_ACTIONS.SYNC_START: {
      // From another tab - quiz started
      const { activeQuestions } = action.payload
      return {
        ...state,
        quizStarted: true,
        screen: 'quiz',
        currentQuestionIndex: 0,
        activeQuestions: activeQuestions || state.activeQuestions
      }
    }

    case QUIZ_ACTIONS.SUBMIT_ANSWER: {
      const { participantId, answer, isCorrect, timeRemaining, questionIndex, questionId } = action.payload

      // Check if already submitted
      const alreadySubmitted = state.responses.some(
        r => r.participantId === participantId && r.questionIndex === questionIndex
      )
      if (alreadySubmitted) return state

      const response = {
        participantId,
        questionIndex,
        questionId,
        answer,
        isCorrect,
        timeRemaining,
        timestamp: new Date().toISOString()
      }

      let newScores = state.scores
      if (isCorrect) {
        const points = Math.max(1, Math.floor(timeRemaining / 2))
        newScores = {
          ...state.scores,
          [participantId]: (state.scores[participantId] || 0) + points
        }
      }

      return {
        ...state,
        responses: [...state.responses, response],
        scores: newScores
      }
    }

    case QUIZ_ACTIONS.SYNC_ANSWER: {
      // From another tab - same logic as SUBMIT_ANSWER
      const { participantId, answer, isCorrect, timeRemaining, questionIndex, questionId } = action.payload

      const alreadySubmitted = state.responses.some(
        r => r.participantId === participantId && r.questionIndex === questionIndex
      )
      if (alreadySubmitted) return state

      const response = {
        participantId,
        questionIndex,
        questionId,
        answer,
        isCorrect,
        timeRemaining,
        timestamp: new Date().toISOString()
      }

      let newScores = state.scores
      if (isCorrect) {
        const points = Math.max(1, Math.floor(timeRemaining / 2))
        newScores = {
          ...state.scores,
          [participantId]: (state.scores[participantId] || 0) + points
        }
      }

      return {
        ...state,
        responses: [...state.responses, response],
        scores: newScores
      }
    }

    case QUIZ_ACTIONS.NEXT_QUESTION: {
      const { totalQuestions } = action.payload
      if (state.currentQuestionIndex < totalQuestions - 1) {
        return {
          ...state,
          currentQuestionIndex: state.currentQuestionIndex + 1
        }
      }
      // Quiz finished
      return {
        ...state,
        screen: 'results'
      }
    }

    case QUIZ_ACTIONS.SYNC_NEXT_QUESTION: {
      const { totalQuestions } = action.payload
      if (state.currentQuestionIndex < totalQuestions - 1) {
        return {
          ...state,
          currentQuestionIndex: state.currentQuestionIndex + 1
        }
      }
      return {
        ...state,
        screen: 'results'
      }
    }

    case QUIZ_ACTIONS.RESET_QUIZ: {
      return {
        ...initialQuizState
      }
    }

    case QUIZ_ACTIONS.LOAD_SAVED_STATE: {
      const { participants, scores, responses, screen, currentQuestionIndex, activeQuestions } = action.payload
      return {
        ...state,
        participants: participants || [],
        scores: scores || {},
        responses: responses || [],
        screen: screen || state.screen,
        currentQuestionIndex: currentQuestionIndex || 0,
        activeQuestions: activeQuestions || null
      }
    }

    default:
      return state
  }
}
