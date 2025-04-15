# Project Treasure Island
print("🏝️ Welcome to Treasure Island!")
print("Your mission is to find the hidden treasure.\n")

choice1 = input("You're at a fork on the beach. Where do you want to go? (left/right): ").lower()

if choice1 == "left":
    choice2 = input("You come to a river. Do you want to swim across or wait for a boat? (swim/wait): ").lower()

    if choice2 == "wait":
        choice3 = input(
            "A boat takes you across. You find three doors: one red, one blue, and one yellow. Which do you choose? ("
            "red/blue/yellow): ").lower()

        if choice3 == "yellow":
            print("🎉 You found the treasure! You win!")
        elif choice3 == "red":
            print("🔥 It's a room full of fire. Game Over.")
        elif choice3 == "blue":
            print("🐻 You enter a room of beasts. Game Over.")
        else:
            print("🚪 That door doesn't exist. Game Over.")
    else:
        print("🦈 You were eaten by a crocodile. Game Over.")
else:
    print("💀 You fell into a trap. Game Over.")


