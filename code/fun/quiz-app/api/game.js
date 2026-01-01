import { kv } from '@vercel/kv'

const GAME_KEY = 'quiz_game_state'

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

async function getGameState() {
  try {
    const state = await kv.get(GAME_KEY)
    return state || { ...defaultState }
  } catch (error) {
    console.error('KV get error:', error)
    return { ...defaultState }
  }
}

async function setGameState(state) {
  try {
    await kv.set(GAME_KEY, state)
    return true
  } catch (error) {
    console.error('KV set error:', error)
    return false
  }
}

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  if (req.method === 'GET') {
    const gameState = await getGameState()
    return res.status(200).json(gameState)
  }

  if (req.method === 'POST') {
    const { action, payload } = req.body
    let gameState = await getGameState()

    switch (action) {
      case 'JOIN':
        const participant = payload.participant
        if (!gameState.participants.find(p => p.id === participant.id)) {
          gameState.participants.push(participant)
          gameState.scores[participant.id] = 0
        }
        if (gameState.screen === 'join') {
          gameState.screen = 'waiting'
        }
        break

      case 'START':
        gameState.screen = 'quiz'
        gameState.quizStarted = true
        gameState.currentQuestionIndex = 0
        gameState.activeQuestions = payload.activeQuestions || null
        break

      case 'SUBMIT_ANSWER':
        const { participantId, answer, isCorrect, timeRemaining, questionIndex, questionId } = payload

        // Check if already submitted
        const alreadySubmitted = gameState.responses.some(
          r => r.participantId === participantId && r.questionIndex === questionIndex
        )

        if (!alreadySubmitted) {
          gameState.responses.push({
            participantId,
            questionIndex,
            questionId,
            answer,
            isCorrect,
            timeRemaining,
            timestamp: new Date().toISOString()
          })

          if (isCorrect) {
            const points = Math.max(1, Math.floor(timeRemaining / 2))
            gameState.scores[participantId] = (gameState.scores[participantId] || 0) + points
          }
        }
        break

      case 'NEXT_QUESTION':
        const totalQuestions = payload.totalQuestions
        if (gameState.currentQuestionIndex < totalQuestions - 1) {
          gameState.currentQuestionIndex++
        } else {
          gameState.screen = 'results'
        }
        break

      case 'RESET':
        gameState = {
          ...defaultState,
          lastUpdated: Date.now()
        }
        break

      default:
        return res.status(400).json({ error: 'Unknown action' })
    }

    gameState.lastUpdated = Date.now()
    await setGameState(gameState)
    return res.status(200).json(gameState)
  }

  return res.status(405).json({ error: 'Method not allowed' })
}
