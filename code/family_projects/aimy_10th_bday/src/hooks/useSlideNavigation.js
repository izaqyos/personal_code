import { useState, useCallback } from 'react'
import { slides } from '../data/slides'

export function useSlideNavigation() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [wrongAttempts, setWrongAttempts] = useState(0)

  const currentSlide = slides[currentIndex]
  const totalSlides = slides.length

  const goToNextSlide = useCallback(() => {
    if (currentIndex < slides.length - 1) {
      setCurrentIndex(prev => prev + 1)
      setWrongAttempts(0)
    }
  }, [currentIndex])

  const recordWrongAttempt = useCallback(() => {
    setWrongAttempts(prev => prev + 1)
  }, [])

  const resetPresentation = useCallback(() => {
    setCurrentIndex(0)
    setWrongAttempts(0)
  }, [])

  return {
    currentIndex,
    currentSlide,
    totalSlides,
    wrongAttempts,
    goToNextSlide,
    recordWrongAttempt,
    resetPresentation,
  }
}
