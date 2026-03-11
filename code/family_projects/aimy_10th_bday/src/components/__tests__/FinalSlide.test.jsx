import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Mock canvas-confetti
vi.mock('canvas-confetti', () => ({
  default: vi.fn(),
}))

import FinalSlide from '../FinalSlide'

describe('FinalSlide', () => {
  it('renders congratulations message', () => {
    render(<FinalSlide onRestart={vi.fn()} />)
    expect(screen.getByText('!כל הכבוד')).toBeInTheDocument()
    expect(screen.getByText('!פתרת את כל החידות')).toBeInTheDocument()
  })

  it('calls onRestart when play again button is clicked', async () => {
    const onRestart = vi.fn()
    render(<FinalSlide onRestart={onRestart} />)
    await userEvent.click(screen.getByText('!שחקי שוב'))
    expect(onRestart).toHaveBeenCalledOnce()
  })
})
