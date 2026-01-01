/**
 * Calculate points based on time remaining
 * Faster answers get more points
 */
export function calculatePoints(timeRemaining, isCorrect) {
  if (!isCorrect) return 0
  return Math.max(1, Math.floor(timeRemaining / 2))
}

/**
 * Sort participants by score (descending)
 */
export function sortParticipantsByScore(participants, scores) {
  return [...participants].sort(
    (a, b) => (scores[b.id] || 0) - (scores[a.id] || 0)
  )
}

/**
 * Get top N participants
 */
export function getTopParticipants(participants, scores, topN = 3) {
  const sorted = sortParticipantsByScore(participants, scores)
  return sorted.slice(0, topN)
}

/**
 * Calculate quiz statistics
 */
export function calculateStats(responses, questions) {
  const totalResponses = responses.length
  const correctResponses = responses.filter(r => r.isCorrect).length
  const accuracy = totalResponses > 0 
    ? Math.round((correctResponses / totalResponses) * 100) 
    : 0

  return {
    totalQuestions: questions.length,
    totalResponses,
    correctResponses,
    accuracy
  }
}

/**
 * Format results data for JSON export
 */
export function formatResultsData(participants, scores, responses, questions) {
  const sortedParticipants = sortParticipantsByScore(participants, scores)
  const topThree = getTopParticipants(participants, scores, 3)
  const winner = sortedParticipants[0]

  return {
    quizTitle: "Programming Languages Quiz",
    completedAt: new Date().toISOString(),
    participants: participants.map(p => ({
      id: p.id,
      name: p.name,
      score: scores[p.id] || 0,
      rank: sortedParticipants.findIndex(sp => sp.id === p.id) + 1
    })),
    responses: responses,
    questions: questions.map(q => ({
      id: q.id,
      question: q.question,
      correctAnswer: q.correctAnswer
    })),
    summary: {
      totalQuestions: questions.length,
      totalParticipants: participants.length,
      winner: winner ? {
        name: winner.name,
        score: scores[winner.id] || 0
      } : null,
      topThree: topThree.map(p => ({
        name: p.name,
        score: scores[p.id] || 0
      }))
    }
  }
}

