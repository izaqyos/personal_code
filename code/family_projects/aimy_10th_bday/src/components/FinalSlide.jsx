import { useEffect } from 'react'
import confetti from 'canvas-confetti'
import './FinalSlide.css'

export default function FinalSlide({ onRestart }) {
  useEffect(() => {
    const duration = 4000
    const end = Date.now() + duration

    const frame = () => {
      confetti({
        particleCount: 3,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
      })
      confetti({
        particleCount: 3,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
      })

      if (Date.now() < end) {
        requestAnimationFrame(frame)
      }
    }
    frame()
  }, [])

  return (
    <div className="final-slide">
      <div className="final-scene">
        <div className="rainbow" />
        <div className="unicorn unicorn-left">🦄</div>
        <div className="unicorn unicorn-right">🦄</div>
        <div className="fairy fairy-1">🧚</div>
        <div className="fairy fairy-2">🧚‍♀️</div>
        <div className="fairy fairy-3">🧚</div>
        <div className="fairy fairy-4">🧚‍♀️</div>
        <div className="magic-dust">✨✨✨</div>
      </div>
      <h1 className="final-title">!כל הכבוד</h1>
      <h2 className="final-subtitle">!פתרת את כל החידות</h2>
      <p className="final-message">
        את מדהימה! יום הולדת שמח!
        <br />
        !תהני מהעוגה
      </p>
      <div className="final-emojis">🎂🎁🎈🎶</div>
      <button className="final-button" onClick={onRestart}>
        !שחקי שוב
      </button>
    </div>
  )
}
