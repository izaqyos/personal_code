// Storage key prefix to avoid collisions
const STORAGE_PREFIX = 'quiz_app_'

/**
 * Safely get item from localStorage with error handling
 */
export function getStorageItem(key, defaultValue = null) {
  try {
    const prefixedKey = STORAGE_PREFIX + key
    const item = localStorage.getItem(prefixedKey)
    if (item === null) return defaultValue
    return JSON.parse(item)
  } catch (error) {
    console.warn(`Error reading from localStorage key "${key}":`, error)
    return defaultValue
  }
}

/**
 * Safely set item in localStorage with error handling
 */
export function setStorageItem(key, value) {
  try {
    const prefixedKey = STORAGE_PREFIX + key
    localStorage.setItem(prefixedKey, JSON.stringify(value))
    return true
  } catch (error) {
    console.warn(`Error writing to localStorage key "${key}":`, error)
    // Handle quota exceeded error
    if (error.name === 'QuotaExceededError') {
      console.warn('localStorage quota exceeded')
    }
    return false
  }
}

/**
 * Safely remove item from localStorage with error handling
 */
export function removeStorageItem(key) {
  try {
    const prefixedKey = STORAGE_PREFIX + key
    localStorage.removeItem(prefixedKey)
    return true
  } catch (error) {
    console.warn(`Error removing localStorage key "${key}":`, error)
    return false
  }
}

/**
 * Clear all app-specific items from localStorage
 */
export function clearAppStorage() {
  try {
    const keysToRemove = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && key.startsWith(STORAGE_PREFIX)) {
        keysToRemove.push(key)
      }
    }
    keysToRemove.forEach(key => localStorage.removeItem(key))
    return true
  } catch (error) {
    console.warn('Error clearing app storage:', error)
    return false
  }
}

// Storage keys constants
export const STORAGE_KEYS = {
  PARTICIPANTS: 'participants',
  SCORES: 'scores',
  RESPONSES: 'responses',
  RESULTS: 'results',
  SCREEN: 'screen',
  QUESTION_INDEX: 'question_index',
  ACTIVE_QUESTIONS: 'active_questions'
}
