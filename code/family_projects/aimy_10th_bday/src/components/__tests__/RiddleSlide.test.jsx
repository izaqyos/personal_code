import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RiddleSlide from '../RiddleSlide'

const mockSlide = {
  number: 1,
  label: 'רמז',
  text: 'מה אני?',
  answer: 'בלון',
  acceptedAnswers: ['בלון', 'בלונים'],
  hint: 'תחשבי על משהו שמנפחים',
}

describe('RiddleSlide', () => {
  it('renders riddle text and input', () => {
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={vi.fn()}
        wrongAttempts={0}
        onWrongAttempt={vi.fn()}
      />
    )
    expect(screen.getByText('מה אני?')).toBeInTheDocument()
    expect(screen.getByTestId('answer-input')).toBeInTheDocument()
  })

  it('calls onSolved when correct answer is submitted', async () => {
    vi.useFakeTimers()
    const onSolved = vi.fn()
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={onSolved}
        wrongAttempts={0}
        onWrongAttempt={vi.fn()}
      />
    )

    const input = screen.getByTestId('answer-input')
    await userEvent.setup({ advanceTimers: vi.advanceTimersByTime }).type(input, 'בלון')
    await userEvent.setup({ advanceTimers: vi.advanceTimersByTime }).click(screen.getByTestId('submit-button'))

    expect(screen.getByTestId('message')).toHaveTextContent('נכון')
    vi.advanceTimersByTime(1200)
    expect(onSolved).toHaveBeenCalled()
    vi.useRealTimers()
  })

  it('calls onWrongAttempt when wrong answer is submitted', async () => {
    const onWrongAttempt = vi.fn()
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={vi.fn()}
        wrongAttempts={0}
        onWrongAttempt={onWrongAttempt}
      />
    )

    const input = screen.getByTestId('answer-input')
    await userEvent.type(input, 'כדור')
    await userEvent.click(screen.getByTestId('submit-button'))

    expect(onWrongAttempt).toHaveBeenCalled()
    expect(screen.getByTestId('message')).toHaveTextContent('לא נכון')
  })

  it('shows hint after 2 wrong attempts', () => {
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={vi.fn()}
        wrongAttempts={2}
        onWrongAttempt={vi.fn()}
      />
    )
    expect(screen.getByTestId('hint')).toBeInTheDocument()
  })

  it('does not show hint before 2 wrong attempts', () => {
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={vi.fn()}
        wrongAttempts={1}
        onWrongAttempt={vi.fn()}
      />
    )
    expect(screen.queryByTestId('hint')).not.toBeInTheDocument()
  })

  it('disables submit button when input is empty', () => {
    render(
      <RiddleSlide
        slide={mockSlide}
        onSolved={vi.fn()}
        wrongAttempts={0}
        onWrongAttempt={vi.fn()}
      />
    )
    expect(screen.getByTestId('submit-button')).toBeDisabled()
  })
})
