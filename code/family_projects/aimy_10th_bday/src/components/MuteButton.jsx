import { useState } from 'react'
import { toggleMute } from '../utils/musicPlayer'
import './MuteButton.css'

export default function MuteButton() {
  const [muted, setMuted] = useState(false)

  const handleToggle = () => {
    const isPlaying = toggleMute()
    setMuted(!isPlaying)
  }

  return (
    <button
      className="mute-button"
      onClick={handleToggle}
      data-testid="mute-button"
      aria-label={muted ? 'unmute music' : 'mute music'}
    >
      {muted ? '🔇' : '🔊'}
    </button>
  )
}
