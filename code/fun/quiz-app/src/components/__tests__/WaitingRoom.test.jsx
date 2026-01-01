import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import WaitingRoom from '../WaitingRoom'

describe('WaitingRoom', () => {
  const mockParticipants = [
    { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
    { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' }
  ]

  it('should render waiting room with participants', () => {
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    expect(screen.getByText(/waiting room/i)).toBeInTheDocument()
    expect(screen.getByText(/2 participants joined/i)).toBeInTheDocument()
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getByText('Bob')).toBeInTheDocument()
  })

  it('should show singular form for one participant', () => {
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={[mockParticipants[0]]}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    expect(screen.getByText(/1 participant joined/i)).toBeInTheDocument()
  })

  it('should call onStart when start button is clicked', async () => {
    const user = userEvent.setup()
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    const startButton = screen.getByRole('button', { name: /start quiz/i })
    await user.click(startButton)
    
    expect(mockOnStart).toHaveBeenCalledTimes(1)
  })

  it('should disable start button when no participants', () => {
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={[]}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    const startButton = screen.getByRole('button', { name: /start quiz/i })
    expect(startButton).toBeDisabled()
  })

  it('should show join form when add participant button is clicked', async () => {
    const user = userEvent.setup()
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    const addButton = screen.getByRole('button', { name: /add another participant/i })
    await user.click(addButton)
    
    expect(screen.getByPlaceholderText(/your name/i)).toBeInTheDocument()
  })

  it('should display participant numbers correctly', () => {
    const mockOnStart = vi.fn()
    const mockOnJoin = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onJoin={mockOnJoin}
      />
    )
    
    const numbers = screen.getAllByText(/^[12]$/)
    expect(numbers.length).toBeGreaterThan(0)
  })
})

