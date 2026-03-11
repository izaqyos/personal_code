import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ProgressBar from '../ProgressBar'

describe('ProgressBar', () => {
  it('renders correct number of dots', () => {
    render(<ProgressBar current={0} total={10} />)
    const dots = screen.getAllByTestId(/progress-dot-/)
    expect(dots).toHaveLength(10)
  })

  it('marks completed dots', () => {
    render(<ProgressBar current={3} total={10} />)
    expect(screen.getByTestId('progress-dot-0')).toHaveClass('completed')
    expect(screen.getByTestId('progress-dot-1')).toHaveClass('completed')
    expect(screen.getByTestId('progress-dot-2')).toHaveClass('completed')
    expect(screen.getByTestId('progress-dot-3')).toHaveClass('active')
    expect(screen.getByTestId('progress-dot-4')).not.toHaveClass('completed')
  })

  it('marks current dot as active', () => {
    render(<ProgressBar current={5} total={10} />)
    expect(screen.getByTestId('progress-dot-5')).toHaveClass('active')
  })
})
