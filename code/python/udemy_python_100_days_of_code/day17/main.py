from data import question_data, question_data_opentdb , normalize_tdb_questions
from question_model import Question
from quiz_brain import QuizBrain

def question(quiz_brain):
    q,n = quiz_brain.get_q()
    if q == None:
        return False
    ans = input(f"Q. {n}: {q.text} (True/False): ")
    #print(f"You answered: {ans}, correct answer {q.ans}")
    if ans == q.ans:
        print("Correct Answer!")
        return True
    else:
        print("Wrong Answer!")
        return False
    

def main():
    qs = []
    question_data_tdb = normalize_tdb_questions(question_data_opentdb)
    for q in question_data_tdb:
        #print(f"Adding question {q}")
        qs.append(Question(q['text'], q['answer']))
    #for q in question_data:
    #    qs.append(Question(q['text'], q['answer']))
    qb = QuizBrain(qs)
    while qb.questions_left():
        qb.next_question()
    qb.final_msg()

def main_ver1():
    qs = []
    for q in question_data:
        #print(q)
        qs.append(Question(q['text'], q['answer']))
    qb = QuizBrain(qs)
    while question(qb):
        pass


if __name__ == "__main__":
    main()
else:
    main()
