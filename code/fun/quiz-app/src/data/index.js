import programmingLanguages from './questions.json'
import webDevelopment from './web-development.json'
import programmingLangsQuiz from './prog_lang_quiz.json'

// All available quizzes
export const quizzes = [
  programmingLangsQuiz,
  programmingLanguages,
  webDevelopment
]

// Get quiz by ID
export function getQuizById(id) {
  return quizzes.find(quiz => quiz.id === id)
}

// Default quiz
export const defaultQuiz = programmingLangsQuiz
