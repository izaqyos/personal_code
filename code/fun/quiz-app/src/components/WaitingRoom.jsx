import './WaitingRoom.css'

function WaitingRoom({ participants, onStart, onReset, quizTitle, isHost, currentParticipant }) {
  const isSmokeTest = import.meta.env.VITE_SMOKE_TEST === 'true'

  return (
    <div className="waiting-room">
      <div className="card">
        <h1>{quizTitle || 'Quiz'}</h1>
        <h2>Waiting Room</h2>

        {currentParticipant && (
          <p className="your-name">You joined as: <strong>{currentParticipant.name}</strong></p>
        )}

        <p className="participant-count">
          {participants.length} {participants.length === 1 ? 'participant' : 'participants'} joined
        </p>

        <div className="participants-list">
          {participants.map((participant, index) => (
            <div
              key={participant.id}
              className={`participant-item ${participant.id === currentParticipant?.id ? 'current' : ''}`}
            >
              <span className="participant-number">{index + 1}</span>
              <span className="participant-name">
                {participant.name}
                {participant.id === currentParticipant?.id && ' (You)'}
                {participant.isHost && ' (Host)'}
              </span>
            </div>
          ))}
        </div>

        {isHost ? (
          <div className="host-controls">
            <p className="host-note">You are the host. Start the quiz when everyone has joined!</p>
            <button
              onClick={() => onStart(isSmokeTest)}
              className="primary-button start-button"
              disabled={participants.length === 0}
            >
              {isSmokeTest ? 'Start Smoke Test' : 'Start Quiz'}
            </button>
            <button
              onClick={onReset}
              className="secondary-button reset-button"
            >
              Reset Game
            </button>
          </div>
        ) : (
          <div className="participant-waiting">
            <p className="waiting-message">Waiting for host to start the quiz...</p>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default WaitingRoom
