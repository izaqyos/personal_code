import Redis from 'ioredis'

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

let redis = null

function getRedis() {
  if (!process.env.REDIS_URL) {
    return null
  }
  if (!redis) {
    redis = new Redis(process.env.REDIS_URL, {
      maxRetriesPerRequest: 3,
      connectTimeout: 5000,
      lazyConnect: true
    })
  }
  return redis
}

async function getGameState() {
  const client = getRedis()
  if (!client) {
    console.error('Redis not configured - missing REDIS_URL')
    return { ...defaultState, error: 'Database not configured.' }
  }

  try {
    const data = await client.get(GAME_KEY)
    return data ? JSON.parse(data) : { ...defaultState }
  } catch (error) {
    console.error('Redis get error:', error.message)
    return { ...defaultState, error: `Database error: ${error.message}` }
  }
}

async function setGameState(state) {
  const client = getRedis()
  if (!client) return false

  try {
    await client.set(GAME_KEY, JSON.stringify(state))
    return true
  } catch (error) {
    console.error('Redis set error:', error.message)
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
