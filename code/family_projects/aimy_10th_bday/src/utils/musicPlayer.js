const NOTE_FREQ = {
  C4: 261.63, D4: 293.66, E4: 329.63, F4: 349.23,
  G4: 392.00, A4: 440.00, B4: 493.88,
  C5: 523.25, D5: 587.33, E5: 659.25, F5: 698.46,
  G5: 784.00, A5: 880.00,
  C3: 130.81, E3: 164.81, F3: 174.61, G3: 196.00,
}

// Happy Birthday melody (note, duration in beats)
const MELODY = [
  ['C4', 0.75], ['C4', 0.25], ['D4', 1], ['C4', 1], ['F4', 1], ['E4', 2],
  ['C4', 0.75], ['C4', 0.25], ['D4', 1], ['C4', 1], ['G4', 1], ['F4', 2],
  ['C4', 0.75], ['C4', 0.25], ['C5', 1], ['A4', 1], ['F4', 1], ['E4', 1], ['D4', 1],
  ['B4', 0.75], ['B4', 0.25], ['A4', 1], ['F4', 1], ['G4', 1], ['F4', 2],
]

// Bass line following the harmony
const BASS = [
  ['C3', 2], ['C3', 2], ['F3', 2], ['C3', 2],
  ['C3', 2], ['C3', 2], ['G3', 2], ['F3', 2],
  ['C3', 2], ['C3', 2], ['F3', 2], ['C3', 1], ['G3', 1],
  ['G3', 2], ['F3', 2], ['C3', 2], ['F3', 2],
]

// Grand finale fanfare
const FANFARE = [
  ['C5', 0.25], ['E5', 0.25], ['G5', 0.25], ['C5', 0.5],
  ['E5', 0.25], ['G5', 0.25], ['A5', 0.5],
  ['G5', 0.25], ['E5', 0.25], ['C5', 0.5],
  ['C5', 0.25], ['D5', 0.25], ['E5', 0.25], ['F5', 0.25],
  ['G5', 0.5], ['A5', 0.5], ['G5', 0.5],
  ['C5', 1.5],
]

let audioCtx = null
let masterGain = null
let isPlaying = false
let isMuted = false
let scheduledNodes = []
let loopTimeout = null

function getContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    masterGain = audioCtx.createGain()
    masterGain.gain.value = 0.3
    masterGain.connect(audioCtx.destination)
  }
  return audioCtx
}

function playNote(freq, startTime, duration, type = 'triangle', volume = 0.5) {
  const ctx = getContext()
  const osc = ctx.createOscillator()
  const gain = ctx.createGain()

  osc.type = type
  osc.frequency.value = freq

  gain.gain.setValueAtTime(0, startTime)
  gain.gain.linearRampToValueAtTime(volume, startTime + 0.05)
  gain.gain.setValueAtTime(volume, startTime + duration - 0.1)
  gain.gain.linearRampToValueAtTime(0, startTime + duration)

  osc.connect(gain)
  gain.connect(masterGain)

  osc.start(startTime)
  osc.stop(startTime + duration)
  scheduledNodes.push(osc)
}

function playSequence(notes, startTime, bpm, type = 'triangle', volume = 0.5) {
  const beatDuration = 60 / bpm
  let time = startTime

  for (const [note, beats] of notes) {
    const freq = NOTE_FREQ[note]
    if (freq) {
      playNote(freq, time, beats * beatDuration * 0.9, type, volume)
    }
    time += beats * beatDuration
  }

  return time
}

function scheduleLoop() {
  if (!isPlaying) return

  const ctx = getContext()
  const now = ctx.currentTime + 0.1
  const bpm = 120

  const melodyEnd = playSequence(MELODY, now, bpm, 'triangle', 0.4)
  playSequence(BASS, now, bpm, 'sine', 0.25)

  // Add a soft high sparkle layer
  const sparkle = MELODY.filter((_, i) => i % 3 === 0).map(([note, dur]) => {
    const octaveUp = note.replace('4', '5').replace('3', '4')
    return [NOTE_FREQ[octaveUp] ? octaveUp : note, dur]
  })
  playSequence(sparkle, now, bpm, 'sine', 0.1)

  const loopDuration = (melodyEnd - now) * 1000
  loopTimeout = setTimeout(scheduleLoop, loopDuration - 200)
}

export function startMusic() {
  if (isPlaying) return
  const ctx = getContext()
  if (ctx.state === 'suspended') {
    ctx.resume()
  }
  isPlaying = true
  isMuted = false
  masterGain.gain.value = 0.3
  scheduleLoop()
}

export function stopMusic() {
  isPlaying = false
  if (loopTimeout) {
    clearTimeout(loopTimeout)
    loopTimeout = null
  }
  scheduledNodes.forEach(node => {
    try { node.stop() } catch (_) { /* already stopped */ }
  })
  scheduledNodes = []
}

export function toggleMute() {
  if (!masterGain) return false
  isMuted = !isMuted
  masterGain.gain.value = isMuted ? 0 : 0.3
  return !isMuted
}

export function isMusicMuted() {
  return isMuted
}

export function playGrandFinale() {
  stopMusic()
  isPlaying = true

  const ctx = getContext()
  if (ctx.state === 'suspended') {
    ctx.resume()
  }
  isMuted = false
  masterGain.gain.value = 0.4

  const now = ctx.currentTime + 0.1
  const bpm = 140

  // Play fanfare with multiple layers
  playSequence(FANFARE, now, bpm, 'triangle', 0.5)
  playSequence(FANFARE, now, bpm, 'square', 0.15)

  // After fanfare, loop the melody faster and brighter
  const fanfareDuration = FANFARE.reduce((sum, [, d]) => sum + d, 0) * (60 / bpm)

  const scheduleFinaleLoop = () => {
    if (!isPlaying) return
    const loopNow = ctx.currentTime + 0.1
    const end = playSequence(MELODY, loopNow, 140, 'triangle', 0.45)
    playSequence(BASS, loopNow, 140, 'sine', 0.3)
    // Sparkle layer
    playSequence(
      MELODY.map(([n, d]) => [n.replace('4', '5').replace('3', '4'), d]),
      loopNow, 140, 'sine', 0.15
    )
    const dur = (end - loopNow) * 1000
    loopTimeout = setTimeout(scheduleFinaleLoop, dur - 200)
  }

  setTimeout(scheduleFinaleLoop, fanfareDuration * 1000)
}

export function cleanup() {
  stopMusic()
  if (audioCtx) {
    audioCtx.close()
    audioCtx = null
    masterGain = null
  }
}
