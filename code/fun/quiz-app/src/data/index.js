import programmingLanguages from './questions.json'
import webDevelopment from './web-development.json'
import dogsHebrew from './dogs-quiz.json'

// All available quizzes
export const quizzes = [
  dogsHebrew,
  programmingLanguages,
  webDevelopment
]

// Get quiz by ID
export function getQuizById(id) {
  return quizzes.find(quiz => quiz.id === id)
}

// Default quiz
export const defaultQuiz = dogsHebrew
