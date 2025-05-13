import pandas as pd
import os
from datetime import datetime


# Function to input food intake data
def input_food_data():
    food_name = input("Enter the food item: ")
    calories = float(input(f"Enter calories for {food_name}: "))
    carbs = float(input(f"Enter carbs (in grams) for {food_name}: "))
    proteins = float(input(f"Enter proteins (in grams) for {food_name}: "))
    fats = float(input(f"Enter fats (in grams) for {food_name}: "))

    return {
        "Food Item": food_name,
        "Calories": calories,
        "Carbs (g)": carbs,
        "Proteins (g)": proteins,
        "Fats (g)": fats,
        "Date": datetime.now().strftime("%Y-%m-%d")
    }


# Function to save data to CSV
def save_to_csv(food_data, filename='diet_tracker.csv'):
    if not os.path.isfile(filename):
        # If the file doesn't exist, write header
        df = pd.DataFrame([food_data])
        df.to_csv(filename, index=False)
    else:
        # Append new data to the CSV
        df = pd.DataFrame([food_data])
        df.to_csv(filename, mode='a', header=False, index=False)


# Function to analyze the diet data
def analyze_diet_data(filename='diet_tracker.csv'):
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(filename)

    # Display last 5 entries
    print("\nLast 5 Entries in Diet Data:")
    print(df.tail())

    # Calculate daily total calories, carbs, proteins, fats
    daily_totals = df.groupby("Date")[["Calories", "Carbs (g)", "Proteins (g)", "Fats (g)"]].sum()
    print("\nDaily Nutrition Totals:")
    print(daily_totals)

    # Calculate average daily calorie intake
    avg_calories = df["Calories"].mean()
    print(f"\nAverage daily calorie intake: {avg_calories:.2f} kcal")

    # Find the highest calorie day
    highest_calorie_day = df.groupby("Date")["Calories"].sum().idxmax()
    print(f"\nHighest calorie day: {highest_calorie_day}")

    # Find the lowest calorie day
    lowest_calorie_day = df.groupby("Date")["Calories"].sum().idxmin()
    print(f"\nLowest calorie day: {lowest_calorie_day}")


# Main function
def main():
    print("Welcome to the Health and Diet Tracker!")
    while True:
        # Input food data
        food_data = input_food_data()

        # Save food data to CSV
        save_to_csv(food_data)

        # Ask the user if they want to add another food item
        another = input("Do you want to add another food item? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    # Analyze the diet data after data entry is complete
    analyze_diet_data()


# Run the main function
if __name__ == "__main__":
    main()
