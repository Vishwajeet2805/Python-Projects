# Project Higher ot Lower Game

from Highlow_game_data import data
import random

def format_data(account):
    account_name = account["name"]
    account_descr = account["description"]
    account_country = account["country"]
    return f"{account_name}, a {account_descr}, from {account_country}"

def check_answer(user_guess, a_followers, b_followers):
    if a_followers > b_followers:
        return user_guess == "a"
    else:
        return user_guess == "b"

score = 0
game_should_continue = True
account_b = random.choice(data)

while game_should_continue:
    account_a = account_b
    account_b = random.choice(data)


    while account_a == account_b:
        account_b = random.choice(data)

    print(f"\nCompare A: {format_data(account_a)} \n")

    print(f"\nCompare B: {format_data(account_b)} \n")

    guess = input("Who has more followers? Type 'A' or 'B': ").lower()
    print("\n" * 20)

    a_follower_count = account_a["follower_count"]
    b_follower_count = account_b["follower_count"]
    is_correct = check_answer(guess, a_follower_count, b_follower_count)

    if is_correct:
        score += 1
        print(f"You're right! Current score: {score}")

    else:
        print(f"Sorry, that's wrong. Final score: {score}")
        game_should_continue = False
