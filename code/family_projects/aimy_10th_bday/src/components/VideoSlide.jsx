import './VideoSlide.css'

export default function VideoSlide({ slide, onContinue }) {
  return (
    <div className="video-slide">
      <h2 className="video-title">{slide.title}</h2>
      <div className="video-container">
        <video
          controls
          autoPlay
          className="video-player"
          data-testid="video-player"
        >
          <source src={slide.src} type="video/mp4" />
        </video>
      </div>
      <button className="video-button" onClick={onContinue}>
        !המשך
      </button>
    </div>
  )
}
