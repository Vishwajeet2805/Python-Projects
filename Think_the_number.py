# Project Number Guessing Game
from random import randint

Easy_level_turn = 10
Hard_level_turn = 5

def check_answer(user_guess, actual_answer, turns):
    if user_guess > actual_answer:
        print("Too High.")
        return turns-1
    elif user_guess < actual_answer:
        print("Too Low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {actual_answer}")
        return turns

def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard'")

    if level == "easy":
        return Easy_level_turn

    else:
        return Hard_level_turn


def games():
    print("\nWelcome to the Number Guessing Game!\n")
    print("\nI'm thinking of a number between 1 to 100\n")

    answer = randint(1,100)


    turns = set_difficulty()
    guess = 0

    while guess != answer:
        print(f"You have {turns} attempts remaining to guess the number.")
        guess = int(input("Make a Guess:\n"))
        turns = check_answer(guess,answer, turns)

        if turns == 0:
            print(f"You've ran out of chances, Game over.\n The answer was {answer}")
            return
        elif guess != answer:
            print ("Guess again")

def game():
    while True:
        games()
        play_again = input("\nDo you want to play again? Type 'yes' or 'no': ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

game()
