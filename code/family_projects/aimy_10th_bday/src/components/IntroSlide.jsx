import './IntroSlide.css'

export default function IntroSlide({ slide, onStart }) {
  return (
    <div className="intro-slide">
      <h1 className="intro-title">{slide.title}</h1>
      <p className="intro-body">{slide.body}</p>
      <div className="intro-emojis">🎉 🎁 🎂</div>
      <button className="intro-button" onClick={onStart}>
        !יאללה
      </button>
    </div>
  )
}
