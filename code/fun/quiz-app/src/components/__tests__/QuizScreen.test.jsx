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

  // Current participant is Alice (first participant)
  const mockCurrentParticipant = mockParticipants[0]

  const mockScores = {
    '1': 10,
    '2': 5
  }

  // Empty responses array - no one has submitted yet
  const mockResponses = []

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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
      />
    )

    expect(screen.getByText(/question 1 of 10/i)).toBeInTheDocument()
    expect(screen.getByText(/what is 2\+2\?/i)).toBeInTheDocument()
    // Options appear in participant view
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
      />
    )
    
    const optionB = screen.getAllByText('4')[0].closest('button')
    await user.click(optionB)
    
    const submitButton = screen.getByRole('button', { name: /submit answer/i })
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
      />
    )
    
    const submitButton = screen.getByRole('button', { name: /submit answer/i })
    expect(submitButton).toBeDisabled()
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
      />
    )

    expect(screen.getByText(/current scores/i)).toBeInTheDocument()
    // Names appear in participant header and leaderboard
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
        currentParticipant={mockCurrentParticipant}
        isHost={false}
        scores={mockScores}
        responses={mockResponses}
        onAnswerSubmit={mockOnAnswerSubmit}
        onNextQuestion={mockOnNextQuestion}
        timerDuration={TEST_TIMER_DURATION}
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

  // ===== Multiplayer interaction tests =====

  describe('Player 2 (Bob) independent interaction', () => {
    const mockCurrentParticipantBob = mockParticipants[1] // Bob

    it('should render interactive answer options for Player 2', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipantBob}
          isHost={false}
          scores={mockScores}
          responses={mockResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Bob appears in participant header and leaderboard
      expect(screen.getAllByText('Bob').length).toBeGreaterThan(0)
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).not.toBeDisabled()
      })
      expect(screen.getByRole('button', { name: /submit answer/i })).toBeInTheDocument()
    })

    it('should allow Player 2 to select and submit an answer', async () => {
      const user = userEvent.setup({ delay: null })
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipantBob}
          isHost={false}
          scores={mockScores}
          responses={mockResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      const optionC = screen.getAllByText('5')[0].closest('button')
      await user.click(optionC)
      expect(optionC).toHaveClass('selected')

      const submitButton = screen.getByRole('button', { name: /submit answer/i })
      expect(submitButton).not.toBeDisabled()
      await user.click(submitButton)

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith(
        '2',    // Bob's ID
        'C',    // selected option
        false,  // incorrect answer
        expect.any(Number)
      )
    })

    it('should keep Player 2 interactive even when Player 1 has already submitted', async () => {
      const user = userEvent.setup({ delay: null })
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      // Player 1 (Alice) already submitted
      const responsesWithAlice = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipantBob}
          isHost={false}
          scores={mockScores}
          responses={responsesWithAlice}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Bob's answer buttons should NOT be disabled
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).not.toBeDisabled()
      })

      // Bob can still select and submit
      const optionA = screen.getAllByText('3')[0].closest('button')
      await user.click(optionA)
      expect(optionA).toHaveClass('selected')

      const submitButton = screen.getByRole('button', { name: /submit answer/i })
      expect(submitButton).not.toBeDisabled()
      await user.click(submitButton)

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith(
        '2', 'A', false, expect.any(Number)
      )
    })
  })

  describe('previously submitted participant', () => {
    it('should disable options when current participant already submitted', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      const responsesWithAlice = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipant} // Alice
          isHost={false}
          scores={mockScores}
          responses={responsesWithAlice}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Alice's answer buttons should be disabled since she already submitted
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).toBeDisabled()
      })

      // Submit button should not be shown
      expect(screen.queryByRole('button', { name: /submit answer/i })).not.toBeInTheDocument()

      // Should show submitted indicator
      expect(screen.getByText(/answer submitted/i)).toBeInTheDocument()
    })

    it('should not disable options for a different participant who has not submitted', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      // Only Alice submitted
      const responsesWithAlice = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockParticipants[1]} // Bob
          isHost={false}
          scores={mockScores}
          responses={responsesWithAlice}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Bob's answer buttons should NOT be disabled
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).not.toBeDisabled()
      })

      // Submit button should be present (disabled until selection)
      expect(screen.getByRole('button', { name: /submit answer/i })).toBeInTheDocument()
    })
  })

  describe('host view', () => {
    const mockHostParticipant = {
      id: 'host_1',
      name: 'Host',
      joinedAt: '2024-01-01T00:00:00Z',
      isHost: true
    }

    it('should show read-only view for host with no submit button', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={[...mockParticipants, mockHostParticipant]}
          currentParticipant={mockHostParticipant}
          isHost={true}
          scores={mockScores}
          responses={mockResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Host should see controller badge
      expect(screen.getByText(/game controller/i)).toBeInTheDocument()

      // No submit button for host
      expect(screen.queryByRole('button', { name: /submit answer/i })).not.toBeInTheDocument()

      // Answer options should be read-only (divs, not buttons)
      const readonlySection = document.querySelector('.answer-options.readonly')
      expect(readonlySection).toBeInTheDocument()
    })

    it('should show player submission status for host', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      const responsesWithAlice = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={[...mockParticipants, mockHostParticipant]}
          currentParticipant={mockHostParticipant}
          isHost={true}
          scores={mockScores}
          responses={responsesWithAlice}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Host sees player status
      expect(screen.getByText(/players status/i)).toBeInTheDocument()
      expect(screen.getByText(/submitted/i)).toBeInTheDocument()
      expect(screen.getByText(/waiting/i)).toBeInTheDocument()
    })

    it('should show next question button for host after results', async () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      // All players submitted
      const allResponses = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        },
        {
          participantId: '2',
          questionIndex: 0,
          questionId: 1,
          answer: 'C',
          isCorrect: false,
          timeRemaining: 8,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockHostParticipant}
          isHost={true}
          scores={mockScores}
          responses={allResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Tick to trigger the useEffect that shows results when all submitted
      await act(async () => {
        vi.advanceTimersByTime(0)
      })

      expect(screen.getByText(/correct answer: b/i)).toBeInTheDocument()

      // Host should see next question button
      const nextButton = screen.getByRole('button', { name: /next question/i })
      expect(nextButton).toBeInTheDocument()
    })

    it('should NOT show next question button for non-host player after results', async () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      const allResponses = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 10,
          timestamp: new Date().toISOString()
        },
        {
          participantId: '2',
          questionIndex: 0,
          questionId: 1,
          answer: 'C',
          isCorrect: false,
          timeRemaining: 8,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipant} // Alice, not host
          isHost={false}
          scores={mockScores}
          responses={allResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Tick to trigger the useEffect that shows results when all submitted
      await act(async () => {
        vi.advanceTimersByTime(0)
      })

      expect(screen.getByText(/correct answer: b/i)).toBeInTheDocument()

      // Non-host should NOT see next question button
      expect(screen.queryByRole('button', { name: /next question/i })).not.toBeInTheDocument()

      // Should see waiting message instead
      expect(screen.getByText(/waiting for host/i)).toBeInTheDocument()
    })
  })

  describe('double-submit prevention', () => {
    it('should not call onAnswerSubmit twice on rapid clicks', async () => {
      const user = userEvent.setup({ delay: null })
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipant}
          isHost={false}
          scores={mockScores}
          responses={mockResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      const optionB = screen.getAllByText('4')[0].closest('button')
      await user.click(optionB)

      const submitButton = screen.getByRole('button', { name: /submit answer/i })
      // Rapid double-click
      await user.click(submitButton)
      await user.click(submitButton)

      expect(mockOnAnswerSubmit).toHaveBeenCalledTimes(1)
    })

    it('should not allow answer selection after submission', async () => {
      const user = userEvent.setup({ delay: null })
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={mockParticipants}
          currentParticipant={mockCurrentParticipant}
          isHost={false}
          scores={mockScores}
          responses={mockResponses}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Select and submit option B
      const optionB = screen.getAllByText('4')[0].closest('button')
      await user.click(optionB)

      const submitButton = screen.getByRole('button', { name: /submit answer/i })
      await user.click(submitButton)

      // After submission, answer buttons should be disabled
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).toBeDisabled()
      })
    })
  })

  describe('three-player scenario', () => {
    const threeParticipants = [
      { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
      { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' },
      { id: '3', name: 'Charlie', joinedAt: '2024-01-01T00:02:00Z' }
    ]

    const threeScores = { '1': 10, '2': 5, '3': 0 }

    it('should keep Player 3 interactive when Players 1 and 2 have submitted', async () => {
      const user = userEvent.setup({ delay: null })
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      const twoSubmitted = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 12,
          timestamp: new Date().toISOString()
        },
        {
          participantId: '2',
          questionIndex: 0,
          questionId: 1,
          answer: 'A',
          isCorrect: false,
          timeRemaining: 8,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={threeParticipants}
          currentParticipant={threeParticipants[2]} // Charlie
          isHost={false}
          scores={threeScores}
          responses={twoSubmitted}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Charlie appears in participant header and leaderboard
      expect(screen.getAllByText('Charlie').length).toBeGreaterThan(0)

      // Charlie's answer buttons should NOT be disabled
      const answerButtons = screen.getAllByRole('button').filter(
        btn => btn.classList.contains('answer-option')
      )
      answerButtons.forEach(btn => {
        expect(btn).not.toBeDisabled()
      })

      // Charlie can select and submit
      const optionD = screen.getAllByText('6')[0].closest('button')
      await user.click(optionD)
      expect(optionD).toHaveClass('selected')

      const submitButton = screen.getByRole('button', { name: /submit answer/i })
      await user.click(submitButton)

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith(
        '3', 'D', false, expect.any(Number)
      )
    })

    it('should show results only after all three players submit', () => {
      const mockOnAnswerSubmit = vi.fn()
      const mockOnNextQuestion = vi.fn()

      // Only 2 of 3 submitted
      const twoSubmitted = [
        {
          participantId: '1',
          questionIndex: 0,
          questionId: 1,
          answer: 'B',
          isCorrect: true,
          timeRemaining: 12,
          timestamp: new Date().toISOString()
        },
        {
          participantId: '2',
          questionIndex: 0,
          questionId: 1,
          answer: 'A',
          isCorrect: false,
          timeRemaining: 8,
          timestamp: new Date().toISOString()
        }
      ]

      render(
        <QuizScreen
          question={mockQuestion}
          questionNumber={1}
          totalQuestions={10}
          participants={threeParticipants}
          currentParticipant={threeParticipants[2]}
          isHost={false}
          scores={threeScores}
          responses={twoSubmitted}
          onAnswerSubmit={mockOnAnswerSubmit}
          onNextQuestion={mockOnNextQuestion}
          timerDuration={TEST_TIMER_DURATION}
        />
      )

      // Results should NOT show yet (only 2/3 submitted)
      expect(screen.queryByText(/correct answer/i)).not.toBeInTheDocument()
    })
  })
})

