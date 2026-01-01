import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ResultsScreen from '../ResultsScreen'

describe('ResultsScreen', () => {
  const mockParticipants = [
    { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
    { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' },
    { id: '3', name: 'Charlie', joinedAt: '2024-01-01T00:02:00Z' }
  ]

  const mockScores = {
    '1': 30,
    '2': 20,
    '3': 10
  }

  const mockResponses = [
    { participantId: '1', isCorrect: true },
    { participantId: '2', isCorrect: true },
    { participantId: '3', isCorrect: false }
  ]

  const mockQuestions = [
    { id: 1, question: 'Test?', correctAnswer: 'A' }
  ]

  beforeEach(() => {
    // Mock URL.createObjectURL and URL.revokeObjectURL globally
    global.URL.createObjectURL = vi.fn(() => 'blob:mock-url')
    global.URL.revokeObjectURL = vi.fn()
  })

  it('should display winner', () => {
    const mockOnReset = vi.fn()

    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )

    expect(screen.getByText(/quiz results/i)).toBeInTheDocument()
    // Winner name appears in winner section with class winner-name
    const winnerSection = document.querySelector('.winner-section')
    expect(winnerSection).toBeInTheDocument()
    expect(winnerSection).toHaveTextContent(/alice/i)
    expect(winnerSection).toHaveTextContent(/30 points/i)
  })

  it('should display top 3 players', () => {
    const mockOnReset = vi.fn()

    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )

    expect(screen.getByText(/top 3 players/i)).toBeInTheDocument()
    // Names appear multiple times (winner section, top 3, leaderboard)
    const topThreeSection = document.querySelector('.top-three-section')
    expect(topThreeSection).toBeInTheDocument()
    expect(topThreeSection).toHaveTextContent(/alice/i)
    expect(topThreeSection).toHaveTextContent(/bob/i)
    expect(topThreeSection).toHaveTextContent(/charlie/i)
  })

  it('should display full leaderboard', () => {
    const mockOnReset = vi.fn()
    
    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )
    
    expect(screen.getByText(/full leaderboard/i)).toBeInTheDocument()
    const leaderboardItems = screen.getAllByText(/alice|bob|charlie/i)
    expect(leaderboardItems.length).toBeGreaterThan(0)
  })

  it('should display quiz statistics', () => {
    const mockOnReset = vi.fn()

    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )

    expect(screen.getByText(/quiz statistics/i)).toBeInTheDocument()
    // Check stats within the stats-section to avoid matching other numbers
    const statsSection = document.querySelector('.stats-section')
    expect(statsSection).toBeInTheDocument()
    // Check for Questions and Participants labels
    expect(statsSection).toHaveTextContent(/questions/i)
    expect(statsSection).toHaveTextContent(/participants/i)
  })

  it('should call onReset when play again button is clicked', async () => {
    const user = userEvent.setup()
    const mockOnReset = vi.fn()
    
    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )
    
    const playAgainButton = screen.getByRole('button', { name: /play again/i })
    await user.click(playAgainButton)
    
    expect(mockOnReset).toHaveBeenCalledTimes(1)
  })

  it('should download results when download button is clicked', async () => {
    const user = userEvent.setup()
    const mockOnReset = vi.fn()

    // Mock appendChild and removeChild to avoid jsdom issues
    const originalAppendChild = document.body.appendChild.bind(document.body)
    const originalRemoveChild = document.body.removeChild.bind(document.body)

    let capturedAnchor = null
    document.body.appendChild = vi.fn((node) => {
      if (node.tagName === 'A') {
        capturedAnchor = node
        // Spy on the click method
        vi.spyOn(node, 'click')
        return node
      }
      return originalAppendChild(node)
    })
    document.body.removeChild = vi.fn((node) => {
      if (node.tagName === 'A') {
        return node
      }
      return originalRemoveChild(node)
    })

    render(
      <ResultsScreen
        participants={mockParticipants}
        scores={mockScores}
        responses={mockResponses}
        questions={mockQuestions}
        onReset={mockOnReset}
      />
    )

    const downloadButton = screen.getByRole('button', { name: /download results/i })
    await user.click(downloadButton)

    expect(global.URL.createObjectURL).toHaveBeenCalled()
    expect(capturedAnchor).not.toBeNull()
    expect(capturedAnchor.click).toHaveBeenCalled()

    // Restore
    document.body.appendChild = originalAppendChild
    document.body.removeChild = originalRemoveChild
  })
})

