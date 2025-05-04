from Question_Model import Question
from Quiz_data import question_data
from Quiz_Brain import QuizBrain

question_bank = []
for question in question_data:
    question_text = question["text"]
    question_answer = question["answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while True:
    while quiz.still_has_questions():
        correct = quiz.next_question()
        print(f"Current Score: {quiz.score}/{quiz.question_number}")
        print("\n")
        if not correct:
            print("Game over! You answered incorrectly.")
            print(f"Your final score was {quiz.score}/{quiz.question_number}")
            break

    if not quiz.still_has_questions() or not correct:
        play_again = input("Do you want to try again? (yes/no): ").lower()
        if play_again == "yes":
            quiz.question_number = 0
            quiz.score = 0
            quiz.last_answer_correct = True
        else:
            break

print("You've completed the quiz.")
print(f"Your final score was {quiz.score}/{quiz.question_number}")
