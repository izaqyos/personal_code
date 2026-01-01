import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import QuizScreen from '../QuizScreen'

const TEST_TIMER_DURATION = 15

describe('QuizScreen', () => {
  const mockQuestion = {
    id: 1,
    question: 'What is 2+2?',
    emoji: '🧮',
    options: [
      { id: 'A', text: '3' },
      { id: 'B', text: '4' },
      { id: 'C', text: '5' },
      { id: 'D', text: '6' }
    ],
    correctAnswer: 'B',
    hint: 'Basic math!'
  }

  const mockParticipants = [
    { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
    { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' }
  ]

  const mockScores = {
    '1': 10,
    '2': 5
  }

  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.clearAllTimers()
  })

  it('should render question and options', () => {
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()

    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )

    expect(screen.getByText(/question 1 of 10/i)).toBeInTheDocument()
    expect(screen.getByText(/what is 2\+2\?/i)).toBeInTheDocument()
    // Options appear multiple times (once per participant), so use getAllByText
    expect(screen.getAllByText('3').length).toBeGreaterThan(0)
    expect(screen.getAllByText('4').length).toBeGreaterThan(0)
  })

  it('should display timer countdown', async () => {
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()

    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )

    // Timer is within .timer-value element
    const timerElement = document.querySelector('.timer-value')
    expect(timerElement).toHaveTextContent(`${TEST_TIMER_DURATION}s`)

    await act(async () => {
      vi.advanceTimersByTime(1000)
    })
    expect(timerElement).toHaveTextContent(`${TEST_TIMER_DURATION - 1}s`)
  })

  it('should allow selecting answers', async () => {
    const user = userEvent.setup({ delay: null })
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()
    
    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )
    
    const optionB = screen.getAllByText('4')[0].closest('button')
    await user.click(optionB)
    
    expect(optionB).toHaveClass('selected')
  })

  it('should submit answer when submit button is clicked', async () => {
    const user = userEvent.setup({ delay: null })
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()
    
    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )
    
    const optionB = screen.getAllByText('4')[0].closest('button')
    await user.click(optionB)
    
    const submitButton = screen.getAllByRole('button', { name: /submit answer/i })[0]
    await user.click(submitButton)
    
    expect(mockOnAnswerSubmit).toHaveBeenCalledWith(
      '1',
      'B',
      true,
      expect.any(Number)
    )
  })

  it('should disable submit button when no answer selected', () => {
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()
    
    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )
    
    const submitButtons = screen.getAllByRole('button', { name: /submit answer/i })
    submitButtons.forEach(button => {
      expect(button).toBeDisabled()
    })
  })

  it('should show leaderboard with scores', () => {
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()

    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )

    expect(screen.getByText(/current scores/i)).toBeInTheDocument()
    // Names appear multiple times (in participant sections and leaderboard)
    expect(screen.getAllByText(/alice/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/bob/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/10 pts/i).length).toBeGreaterThan(0)
  })

  it('should show results when time expires', async () => {
    const mockOnAnswerSubmit = vi.fn()
    const mockOnNextQuestion = vi.fn()

    render(
      <QuizScreen
        question={mockQuestion}
        questionNumber={1}
        totalQuestions={10}
        participants={mockParticipants}
        scores={mockScores}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
      />
    )

    // Advance time in steps to allow state updates
    for (let i = 0; i < TEST_TIMER_DURATION; i++) {
      await act(async () => {
        vi.advanceTimersByTime(1000)
      })
    }

    expect(screen.getByText(/correct answer: b/i)).toBeInTheDocument()
    expect(mockOnAnswerSubmit).toHaveBeenCalled()
  })
})

