import { useState, useEffect, useCallback } from 'react'
import { getStorageItem, setStorageItem, removeStorageItem } from '../utils/storage'

/**
 * Custom hook for syncing state with localStorage
 * Provides automatic persistence and error handling
 *
 * @param {string} key - Storage key (will be prefixed automatically)
 * @param {*} initialValue - Default value if nothing in storage
 * @returns {[value, setValue, removeValue]} - State value, setter, and remover
 */
export function useLocalStorage(key, initialValue) {
  // Initialize state from localStorage or use initial value
  const [storedValue, setStoredValue] = useState(() => {
    const item = getStorageItem(key, null)
    return item !== null ? item : initialValue
  })

  // Update localStorage when state changes
  useEffect(() => {
    setStorageItem(key, storedValue)
  }, [key, storedValue])

  // Memoized setter to prevent unnecessary re-renders
  const setValue = useCallback((value) => {
    setStoredValue(prevValue => {
      // Allow functional updates like useState
      const valueToStore = value instanceof Function ? value(prevValue) : value
      return valueToStore
    })
  }, [])

  // Remove value from storage and reset to initial
  const removeValue = useCallback(() => {
    removeStorageItem(key)
    setStoredValue(initialValue)
  }, [key, initialValue])

  return [storedValue, setValue, removeValue]
}

export default useLocalStorage
