import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TransitionSlide from '../TransitionSlide'

const mockSlide = {
  title: 'כל הכבוד!',
  body: 'פתרת את החידה!',
  challenge: 'נפחי בלון!',
}

describe('TransitionSlide', () => {
  it('renders title, body, and challenge', () => {
    render(<TransitionSlide slide={mockSlide} onDone={vi.fn()} />)
    expect(screen.getByText('כל הכבוד!')).toBeInTheDocument()
    expect(screen.getByText('פתרת את החידה!')).toBeInTheDocument()
    expect(screen.getByText('נפחי בלון!')).toBeInTheDocument()
  })

  it('calls onDone when button is clicked', async () => {
    const onDone = vi.fn()
    render(<TransitionSlide slide={mockSlide} onDone={onDone} />)
    await userEvent.click(screen.getByText('!סיימתי'))
    expect(onDone).toHaveBeenCalledOnce()
  })
})
