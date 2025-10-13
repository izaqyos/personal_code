class QuizBrain:
    def __init__(self, questions) -> None:
        self.question_number = 0
        self.score = 0
        self.questions = questions

    def next_q(self):
        for q in self.questions:
            self.question_number +=1
            self.question_number %= len(self.questions)
            yield q
    
    def get_q(self):
        self.question_number+=1
        if self.question_number >= len(self.questions):
            return None, None
        return self.questions[(self.question_number-1)%len(self.questions)], self.question_number

    def next_question(self):
        q = self.questions[self.question_number]
        self.question_number +=1
        ans = input(f"Question {self.question_number}: {q.text} (True/False) ")
        self.check_ans(ans, q.ans)

    def check_ans(self, answer, correct_answer):
        if answer.lower() == correct_answer.lower():
            print("Nice!! - you got it right :)")
            self.score+=1
        else:
            print("Oops, that's wrong :(")
        print(f"The correct answer is {correct_answer}")
        print(f"Your current score is {self.score}/{self.question_number}")
        print("")

    def questions_left(self):
        return self.question_number<len(self.questions)

    def final_msg(self):
        print("Nice. You have complete the quiz!")
        print(f"Your score is {self.score}/{self.question_number}")
