/**
 * Normalize a Hebrew string for comparison:
 * - Trim whitespace
 * - Remove niqqud (Hebrew diacritical marks)
 * - Remove maqaf (Hebrew hyphen)
 * - Collapse multiple spaces
 */
export function normalizeHebrew(str) {
  return str
    .trim()
    .replace(/[\u0591-\u05C7]/g, '')
    .replace(/\u05BE/g, '')
    .replace(/\s+/g, ' ')
}

/**
 * Check if the user's answer matches any of the accepted answers.
 */
export function validateAnswer(userInput, acceptedAnswers) {
  const normalizedInput = normalizeHebrew(userInput)
  if (!normalizedInput) return false
  return acceptedAnswers.some(
    accepted => normalizeHebrew(accepted) === normalizedInput
  )
}
