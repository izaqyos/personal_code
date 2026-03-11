import './TransitionSlide.css'

export default function TransitionSlide({ slide, onDone }) {
  return (
    <div className="transition-slide">
      <h2 className="transition-title">{slide.title}</h2>
      <p className="transition-body">{slide.body}</p>
      <div className="transition-challenge">
        <span className="challenge-icon">🏆</span>
        <p className="challenge-text">{slide.challenge}</p>
      </div>
      <button className="transition-button" onClick={onDone}>
        !סיימתי
      </button>
    </div>
  )
}
