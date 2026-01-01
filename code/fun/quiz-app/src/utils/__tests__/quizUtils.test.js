import { describe, it, expect } from 'vitest'
import {
  calculatePoints,
  sortParticipantsByScore,
  getTopParticipants,
  calculateStats,
  formatResultsData
} from '../quizUtils'

describe('quizUtils', () => {
  describe('calculatePoints', () => {
    it('should return 0 for incorrect answers', () => {
      expect(calculatePoints(15, false)).toBe(0)
      expect(calculatePoints(5, false)).toBe(0)
    })

    it('should return points based on time remaining for correct answers', () => {
      expect(calculatePoints(15, true)).toBe(7) // floor(15/2) = 7
      expect(calculatePoints(10, true)).toBe(5) // floor(10/2) = 5
      expect(calculatePoints(2, true)).toBe(1) // max(1, floor(2/2)) = 1
      expect(calculatePoints(1, true)).toBe(1) // max(1, floor(1/2)) = 1
    })
  })

  describe('sortParticipantsByScore', () => {
    it('should sort participants by score descending', () => {
      const participants = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' }
      ]
      const scores = {
        '1': 10,
        '2': 20,
        '3': 5
      }

      const sorted = sortParticipantsByScore(participants, scores)
      expect(sorted[0].id).toBe('2')
      expect(sorted[1].id).toBe('1')
      expect(sorted[2].id).toBe('3')
    })

    it('should handle participants with no score', () => {
      const participants = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' }
      ]
      const scores = {
        '1': 10
      }

      const sorted = sortParticipantsByScore(participants, scores)
      expect(sorted[0].id).toBe('1')
      expect(sorted[1].id).toBe('2')
    })
  })

  describe('getTopParticipants', () => {
    it('should return top N participants', () => {
      const participants = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' },
        { id: '3', name: 'Charlie' },
        { id: '4', name: 'David' }
      ]
      const scores = {
        '1': 10,
        '2': 30,
        '3': 20,
        '4': 5
      }

      const top3 = getTopParticipants(participants, scores, 3)
      expect(top3).toHaveLength(3)
      expect(top3[0].id).toBe('2')
      expect(top3[1].id).toBe('3')
      expect(top3[2].id).toBe('1')
    })
  })

  describe('calculateStats', () => {
    it('should calculate correct statistics', () => {
      const responses = [
        { isCorrect: true },
        { isCorrect: true },
        { isCorrect: false },
        { isCorrect: true }
      ]
      const questions = [{ id: 1 }, { id: 2 }, { id: 3 }]

      const stats = calculateStats(responses, questions)
      expect(stats.totalQuestions).toBe(3)
      expect(stats.totalResponses).toBe(4)
      expect(stats.correctResponses).toBe(3)
      expect(stats.accuracy).toBe(75)
    })

    it('should handle empty responses', () => {
      const responses = []
      const questions = [{ id: 1 }]

      const stats = calculateStats(responses, questions)
      expect(stats.accuracy).toBe(0)
    })
  })

  describe('formatResultsData', () => {
    it('should format results data correctly', () => {
      const participants = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' }
      ]
      const scores = {
        '1': 20,
        '2': 10
      }
      const responses = [
        { participantId: '1', isCorrect: true }
      ]
      const questions = [
        { id: 1, question: 'Test?', correctAnswer: 'A' }
      ]

      const result = formatResultsData(participants, scores, responses, questions)
      
      expect(result.quizTitle).toBe('Programming Languages Quiz')
      expect(result.participants).toHaveLength(2)
      expect(result.participants[0].rank).toBe(1)
      expect(result.participants[0].score).toBe(20)
      expect(result.summary.winner.name).toBe('Alice')
      expect(result.summary.topThree).toHaveLength(2)
    })
  })
})

