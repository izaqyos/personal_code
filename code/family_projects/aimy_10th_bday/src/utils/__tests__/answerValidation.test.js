import { describe, it, expect } from 'vitest'
import { normalizeHebrew, validateAnswer } from '../answerValidation'

describe('normalizeHebrew', () => {
  it('trims whitespace', () => {
    expect(normalizeHebrew('  בלון  ')).toBe('בלון')
  })

  it('removes niqqud', () => {
    expect(normalizeHebrew('בָּלוֹן')).toBe('בלון')
  })

  it('removes maqaf', () => {
    expect(normalizeHebrew('יום־הולדת')).toBe('יוםהולדת')
  })

  it('collapses multiple spaces', () => {
    expect(normalizeHebrew('יום   הולדת')).toBe('יום הולדת')
  })

  it('handles empty string', () => {
    expect(normalizeHebrew('')).toBe('')
  })
})

describe('validateAnswer', () => {
  it('returns true for exact match', () => {
    expect(validateAnswer('בלון', ['בלון'])).toBe(true)
  })

  it('returns true with extra whitespace', () => {
    expect(validateAnswer('  בלון  ', ['בלון'])).toBe(true)
  })

  it('returns true with niqqud in input', () => {
    expect(validateAnswer('בָּלוֹן', ['בלון'])).toBe(true)
  })

  it('returns true for any accepted answer', () => {
    expect(validateAnswer('בלונים', ['בלון', 'בלונים'])).toBe(true)
  })

  it('returns false for wrong answer', () => {
    expect(validateAnswer('כדור', ['בלון'])).toBe(false)
  })

  it('returns false for empty input', () => {
    expect(validateAnswer('', ['בלון'])).toBe(false)
  })

  it('returns false for whitespace-only input', () => {
    expect(validateAnswer('   ', ['בלון'])).toBe(false)
  })
})
