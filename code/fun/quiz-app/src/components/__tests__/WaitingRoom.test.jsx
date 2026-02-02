import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import WaitingRoom from '../WaitingRoom'

describe('WaitingRoom', () => {
  const mockPlayers = [
    { id: '1', name: 'Alice', joinedAt: '2024-01-01T00:00:00Z' },
    { id: '2', name: 'Bob', joinedAt: '2024-01-01T00:01:00Z' }
  ]

  const mockHost = { id: 'host_1', name: 'Host', joinedAt: '2024-01-01T00:00:00Z', isHost: true }
  
  // All participants including host
  const mockParticipants = [...mockPlayers, mockHost]

  // Current participant for non-host view (a player)
  const mockCurrentParticipant = mockPlayers[0]

  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should render waiting room with participants', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    // Check for lobby badge
    expect(screen.getByText('LOBBY', { selector: '.lobby-badge' })).toBeInTheDocument()
    // Check for player count
    expect(screen.getByText(/2 players in lobby/i)).toBeInTheDocument()
    // Check participant names are shown in player cards
    expect(screen.getByText('Alice', { selector: '.player-name' })).toBeInTheDocument()
    expect(screen.getByText('Bob', { selector: '.player-name' })).toBeInTheDocument()
  })

  it('should show singular form for one participant', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={[mockParticipants[0]]}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    expect(screen.getByText(/1 player in lobby/i)).toBeInTheDocument()
  })

  it('should start countdown and call onStart when countdown completes (host view)', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime })
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    const startButton = screen.getByRole('button', { name: /start quiz/i })
    await user.click(startButton)
    
    // Countdown should be visible
    expect(screen.getByText(/get ready/i)).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()
    
    // Advance through the countdown (10 seconds)
    for (let i = 0; i < 10; i++) {
      await act(async () => {
        vi.advanceTimersByTime(1000)
      })
    }
    
    // onStart should be called after countdown completes
    expect(mockOnStart).toHaveBeenCalledTimes(1)
    expect(mockOnStart).toHaveBeenCalledWith(false) // Not smoke test
  })

  it('should allow host to cancel countdown', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime })
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    const startButton = screen.getByRole('button', { name: /start quiz/i })
    await user.click(startButton)
    
    // Countdown should be visible
    expect(screen.getByText(/get ready/i)).toBeInTheDocument()
    
    // Click cancel
    const cancelButton = screen.getByRole('button', { name: /cancel/i })
    await user.click(cancelButton)
    
    // Countdown should be gone
    expect(screen.queryByText(/get ready/i)).not.toBeInTheDocument()
    
    // onStart should not have been called
    expect(mockOnStart).not.toHaveBeenCalled()
  })

  it('should disable start button when no participants', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={[]}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
      />
    )
    
    const startButton = screen.getByRole('button', { name: /start quiz/i })
    expect(startButton).toBeDisabled()
  })

  it('should show waiting message for non-host participants', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={false}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    expect(screen.getByText(/waiting for host to start the quiz/i)).toBeInTheDocument()
    // Start button should not be visible for non-host
    expect(screen.queryByRole('button', { name: /start quiz/i })).not.toBeInTheDocument()
  })

  it('should display player avatars with initials', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    // Check for avatar initials (first letter of names)
    expect(screen.getByText('A')).toBeInTheDocument() // Alice
    expect(screen.getByText('B')).toBeInTheDocument() // Bob
  })

  it('should show current participant identity', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={false}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    // Check the "You joined as" section exists
    expect(screen.getByText(/you joined as/i)).toBeInTheDocument()
    // Check the name is displayed
    expect(screen.getByText('Alice', { selector: '.identity-name' })).toBeInTheDocument()
  })

  it('should show "You" badge on current participant card', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    // Check for the "You" badge
    expect(screen.getByText('You', { selector: '.you-badge' })).toBeInTheDocument()
  })

  it('should show reset button for host', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime })
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
        currentParticipant={mockCurrentParticipant}
      />
    )
    
    const resetButton = screen.getByRole('button', { name: /reset game/i })
    await user.click(resetButton)
    
    expect(mockOnReset).toHaveBeenCalledTimes(1)
  })

  it('should show countdown overlay when countdownActive prop is true', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={mockParticipants}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={false}
        currentParticipant={mockCurrentParticipant}
        countdownActive={true}
        countdownValue={5}
      />
    )
    
    // Countdown should be visible for non-host when synced from host
    expect(screen.getByText(/get ready/i)).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
  })

  it('should show no players message when empty', () => {
    const mockOnStart = vi.fn()
    const mockOnReset = vi.fn()
    
    render(
      <WaitingRoom
        participants={[]}
        onStart={mockOnStart}
        onReset={mockOnReset}
        isHost={true}
      />
    )
    
    expect(screen.getByText(/waiting for players to join/i)).toBeInTheDocument()
  })
})
