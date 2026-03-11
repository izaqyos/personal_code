import { useEffect, useCallback } from 'react'
import { useSlideNavigation } from './hooks/useSlideNavigation'
import { startMusic, playGrandFinale, cleanup } from './utils/musicPlayer'
import ProgressBar from './components/ProgressBar'
import MuteButton from './components/MuteButton'
import IntroSlide from './components/IntroSlide'
import RiddleSlide from './components/RiddleSlide'
import TransitionSlide from './components/TransitionSlide'
import VideoSlide from './components/VideoSlide'
import FinalSlide from './components/FinalSlide'
import './App.css'

export default function App() {
  const {
    currentIndex,
    currentSlide,
    totalSlides,
    wrongAttempts,
    goToNextSlide,
    recordWrongAttempt,
    resetPresentation,
  } = useSlideNavigation()

  useEffect(() => {
    return () => cleanup()
  }, [])

  useEffect(() => {
    if (currentSlide.type === 'final') {
      playGrandFinale()
    }
  }, [currentSlide.type])

  const handleStart = useCallback(() => {
    startMusic()
    goToNextSlide()
  }, [goToNextSlide])

  const handleRestart = useCallback(() => {
    resetPresentation()
    startMusic()
  }, [resetPresentation])

  const renderSlide = () => {
    switch (currentSlide.type) {
      case 'intro':
        return <IntroSlide slide={currentSlide} onStart={handleStart} />
      case 'riddle':
        return (
          <RiddleSlide
            key={currentIndex}
            slide={currentSlide}
            onSolved={goToNextSlide}
            wrongAttempts={wrongAttempts}
            onWrongAttempt={recordWrongAttempt}
          />
        )
      case 'transition':
        return <TransitionSlide slide={currentSlide} onDone={goToNextSlide} />
      case 'video':
        return <VideoSlide slide={currentSlide} onContinue={goToNextSlide} />
      case 'final':
        return <FinalSlide onRestart={handleRestart} />
      default:
        return null
    }
  }

  return (
    <div className="app">
      <ProgressBar current={currentIndex} total={totalSlides} />
      <main className="slide-container">
        <div className="slide-content" key={currentIndex}>
          {renderSlide()}
        </div>
      </main>
      <MuteButton />
    </div>
  )
}
