import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import JoinScreen from '../JoinScreen'

describe('JoinScreen', () => {
  it('should render join form', () => {
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} quizTitle="Test Quiz" />)

    expect(screen.getByText(/Test Quiz/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/your name/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /join quiz/i })).toBeInTheDocument()
  })

  it('should call onJoin when form is submitted with valid name', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    const button = screen.getByRole('button', { name: /join quiz/i })

    await user.type(input, 'John Doe')
    await user.click(button)

    expect(mockOnJoin).toHaveBeenCalledWith('John Doe')
  })

  it('should not call onJoin with empty name and show error', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const button = screen.getByRole('button', { name: /join quiz/i })
    await user.click(button)

    expect(mockOnJoin).not.toHaveBeenCalled()
    expect(screen.getByRole('alert')).toHaveTextContent(/please enter your name/i)
  })

  it('should trim whitespace from name', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    const button = screen.getByRole('button', { name: /join quiz/i })

    await user.type(input, '  Jane Smith  ')
    await user.click(button)

    // Component trims the name before calling onJoin
    expect(mockOnJoin).toHaveBeenCalledWith('Jane Smith')
  })

  it('should submit on Enter key press', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    await user.type(input, 'Test User{Enter}')

    expect(mockOnJoin).toHaveBeenCalledWith('Test User')
  })

  it('should show error for name too short', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    const button = screen.getByRole('button', { name: /join quiz/i })

    await user.type(input, 'A')
    await user.click(button)

    expect(mockOnJoin).not.toHaveBeenCalled()
    expect(screen.getByRole('alert')).toHaveTextContent(/at least 2 characters/i)
  })

  it('should show error for invalid characters', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    const button = screen.getByRole('button', { name: /join quiz/i })

    await user.type(input, 'Test@User!')
    await user.click(button)

    expect(mockOnJoin).not.toHaveBeenCalled()
    expect(screen.getByRole('alert')).toHaveTextContent(/can only contain/i)
  })

  it('should clear error when user types', async () => {
    const user = userEvent.setup()
    const mockOnJoin = vi.fn()
    render(<JoinScreen onJoin={mockOnJoin} />)

    const input = screen.getByPlaceholderText(/your name/i)
    const button = screen.getByRole('button', { name: /join quiz/i })

    // Submit empty to trigger error
    await user.click(button)
    expect(screen.getByRole('alert')).toBeInTheDocument()

    // Start typing to clear error
    await user.type(input, 'A')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })
})
