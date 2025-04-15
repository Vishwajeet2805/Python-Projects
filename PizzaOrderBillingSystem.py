# Project 1 Pizza Deliveries
print("Welcome to Pizza Deliveries")
# Creating variable for the user to select His/Her choice
size = input("What size of Pizza you want ? S, M or L")
pepperoni = input("Do you want peperoni on your Pizza? Y or N")
cheese = input("Do you want extra cheese? Y or N")

bill = 0

if size == "S":
    bill += 15
elif size == "M":
    bill += 20
elif size == "L":
    bill += 25
else:
    print("Your choice is not available")
if pepperoni == "Y":
    if size == "S":
        bill += 2
    elif size == "M":
        bill += 4
    elif size == "L":
        bill += 6
if cheese == "Y":
    bill += 1

print(f"Your total bill is ${bill}")
