import { useEffect, useMemo } from 'react'
import {
  sortParticipantsByScore,
  getTopParticipants,
  calculateStats,
  formatResultsData
} from '../utils/quizUtils'
import { setStorageItem, STORAGE_KEYS } from '../utils/storage'
import './ResultsScreen.css'

function ResultsScreen({ participants, scores, responses, questions, onReset }) {
  const sortedParticipants = useMemo(
    () => sortParticipantsByScore(participants, scores),
    [participants, scores]
  )

  const winner = sortedParticipants[0]
  const topThree = useMemo(
    () => getTopParticipants(participants, scores, 3),
    [participants, scores]
  )

  const stats = useMemo(
    () => calculateStats(responses, questions),
    [responses, questions]
  )

  // Save results to localStorage as backup
  useEffect(() => {
    const resultsData = formatResultsData(participants, scores, responses, questions)
    setStorageItem(STORAGE_KEYS.RESULTS, resultsData)
  }, [participants, scores, responses, questions])

  const handleDownloadResults = () => {
    const resultsData = formatResultsData(participants, scores, responses, questions)
    const blob = new Blob([JSON.stringify(resultsData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${new Date().toISOString().split('T')[0]}_quiz_results.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇'
    if (rank === 2) return '🥈'
    if (rank === 3) return '🥉'
    return `#${rank}`
  }

  return (
    <div className="results-screen">
      <div className="card results-card">
        <h1>Quiz Results</h1>

        {winner && (
          <div className="winner-section">
            <div className="winner-crown">👑</div>
            <h2 className="winner-name">{winner.name}</h2>
            <p className="winner-score">{scores[winner.id] || 0} points</p>
            <p className="winner-message">Congratulations! You're the champion!</p>
          </div>
        )}

        <div className="top-three-section">
          <h3>Top 3 Players</h3>
          <div className="top-three-list">
            {topThree.map((participant, index) => (
              <div key={participant.id} className={`top-three-item rank-${index + 1}`}>
                <div className="medal">{getMedalEmoji(index + 1)}</div>
                <div className="player-info">
                  <div className="player-name">{participant.name}</div>
                  <div className="player-score">{scores[participant.id] || 0} points</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="full-leaderboard">
          <h3>Full Leaderboard</h3>
          <div className="leaderboard">
            {sortedParticipants.map((participant, index) => (
              <div key={participant.id} className="leaderboard-row">
                <span className="rank">{index + 1}</span>
                <span className="name">{participant.name}</span>
                <span className="score">{scores[participant.id] || 0} pts</span>
              </div>
            ))}
          </div>
        </div>

        <div className="stats-section">
          <h3>Quiz Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">{stats.totalQuestions}</div>
              <div className="stat-label">Questions</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{participants.length}</div>
              <div className="stat-label">Participants</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{stats.correctResponses}</div>
              <div className="stat-label">Correct Answers</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{stats.accuracy}%</div>
              <div className="stat-label">Accuracy</div>
            </div>
          </div>
        </div>

        <div className="actions">
          <button onClick={handleDownloadResults} className="secondary-button">
            Download Results (JSON)
          </button>
          <button onClick={onReset} className="primary-button">
            Play Again
          </button>
        </div>
      </div>
    </div>
  )
}

export default ResultsScreen
