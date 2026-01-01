import { quizzes } from '../data'
import './QuizSelector.css'

function QuizSelector({ onSelectQuiz, selectedQuizId }) {
  return (
    <div className="quiz-selector">
      <h2>Select a Quiz</h2>
      <div className="quiz-list">
        {quizzes.map(quiz => (
          <button
            key={quiz.id}
            className={`quiz-card-btn ${selectedQuizId === quiz.id ? 'selected' : ''}`}
            onClick={() => onSelectQuiz(quiz)}
            aria-pressed={selectedQuizId === quiz.id}
          >
            <h3>{quiz.title}</h3>
            <p className="quiz-description">{quiz.description}</p>
            <div className="quiz-meta">
              <span className="quiz-questions">{quiz.questions.length} questions</span>
              <span className="quiz-timer">{quiz.timerSeconds}s per question</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuizSelector
