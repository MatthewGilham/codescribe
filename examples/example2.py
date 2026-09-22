from operator import index
class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def still_has_questions(self):
        if self.question_number < len(self.question_list):
            return True
        else:
            print(f"You've completed the quiz your final score was {self.score}/{self.question_number}!")
            return False

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)



    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print(f"You got it right! Your current score is: {self.score}/{self.question_number}")
        else:
            print(f"You got it wrong :( Your current score is: {self.score}/{self.question_number}")
        print(f"The correct answer was {correct_answer}")
        print("\n")