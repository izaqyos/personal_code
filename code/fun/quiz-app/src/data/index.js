import programmingLanguages from './questions.json'
import webDevelopment from './web-development.json'
import programmingLangsQuiz from './prog_lang_quiz.json'
import nodejsTsQuiz from './nodejs-ts-quiz.json'

// All available quizzes
export const quizzes = [
  nodejsTsQuiz,
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
