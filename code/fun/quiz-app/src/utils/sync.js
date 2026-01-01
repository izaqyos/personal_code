// Cross-tab synchronization using BroadcastChannel API
const CHANNEL_NAME = 'quiz-app-sync'

let channel = null
let listeners = []

export const SYNC_EVENTS = {
  PARTICIPANT_JOINED: 'participant_joined',
  QUIZ_STARTED: 'quiz_started',
  ANSWER_SUBMITTED: 'answer_submitted',
  NEXT_QUESTION: 'next_question',
  QUIZ_RESET: 'quiz_reset',
  STATE_REQUEST: 'state_request',
  STATE_RESPONSE: 'state_response'
}

export function initSync() {
  if (channel) return channel

  try {
    channel = new BroadcastChannel(CHANNEL_NAME)
    channel.onmessage = (event) => {
      listeners.forEach(listener => listener(event.data))
    }
  } catch (e) {
    console.warn('BroadcastChannel not supported, falling back to localStorage events')
    // Fallback for browsers without BroadcastChannel
    window.addEventListener('storage', (event) => {
      if (event.key === CHANNEL_NAME && event.newValue) {
        try {
          const data = JSON.parse(event.newValue)
          listeners.forEach(listener => listener(data))
        } catch (e) {
          // ignore parse errors
        }
      }
    })
  }

  return channel
}

export function broadcast(type, payload = {}) {
  const message = { type, payload, timestamp: Date.now() }

  if (channel) {
    channel.postMessage(message)
  } else {
    // Fallback: use localStorage for cross-tab communication
    localStorage.setItem(CHANNEL_NAME, JSON.stringify(message))
    // Clear it immediately (the storage event fires on other tabs)
    setTimeout(() => localStorage.removeItem(CHANNEL_NAME), 100)
  }
}

export function subscribe(listener) {
  listeners.push(listener)
  return () => {
    listeners = listeners.filter(l => l !== listener)
  }
}

export function cleanup() {
  if (channel) {
    channel.close()
    channel = null
  }
  listeners = []
}

// Session management - track which participant this tab controls
const SESSION_KEY = 'quiz_app_session'

export function getSessionParticipantId() {
  return sessionStorage.getItem(SESSION_KEY)
}

export function setSessionParticipantId(participantId) {
  sessionStorage.setItem(SESSION_KEY, participantId)
}

export function clearSession() {
  sessionStorage.removeItem(SESSION_KEY)
}

export function isHost() {
  return sessionStorage.getItem('quiz_app_is_host') === 'true'
}

export function setIsHost(value) {
  sessionStorage.setItem('quiz_app_is_host', value ? 'true' : 'false')
}
