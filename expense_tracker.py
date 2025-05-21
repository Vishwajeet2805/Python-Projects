import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ANSI escape codes for colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("="*40)
    print("     💸 Welcome to Expense Tracker 💸     ")
    print("="*40)
    print(f"{Colors.ENDC}")

def get_date():
    while True:
        date_input = input(f"{Colors.OKCYAN}Enter date (DD-MM-YYYY) or press Enter for today:{Colors.ENDC} ").strip()
        if date_input == "":
            return datetime.now().strftime("%d-%m-%Y")
        try:
            datetime.strptime(date_input, "%d-%m-%Y")
            return date_input
        except ValueError:
            print(f"{Colors.FAIL}Invalid date format! Please try again.{Colors.ENDC}")

def get_amount():
    while True:
        amount_str = input(f"{Colors.OKCYAN}Enter amount spent (₹): {Colors.ENDC}").strip()
        try:
            amount = float(amount_str)
            if amount < 0:
                print(f"{Colors.FAIL}Amount cannot be negative. Try again.{Colors.ENDC}")
                continue
            return amount
        except ValueError:
            print(f"{Colors.FAIL}Invalid input! Please enter a valid number.{Colors.ENDC}")

def get_yes_no(prompt):
    while True:
        ans = input(f"{Colors.OKGREEN}{prompt} (yes/no): {Colors.ENDC}").strip().lower()
        if ans in ("yes", "no"):
            return ans
        print(f"{Colors.WARNING}Please type 'yes' or 'no'.{Colors.ENDC}")

def main():
    file_name = "expenses.csv"
    columns = ["Date", "Item", "Amount"]

    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=columns)

    print_header()

    date_input = get_date()
    new_entries = []

    while True:
        item = input(f"{Colors.OKBLUE}Enter the item you purchased:{Colors.ENDC} ").strip()
        if not item:
            print(f"{Colors.WARNING}Item name can't be empty. Try again.{Colors.ENDC}")
            continue

        amount = get_amount()

        new_entries.append({"Date": date_input, "Item": item, "Amount": amount})
        cont = get_yes_no("Do you want to add another item?")
        if cont == "no":
            break

    # Create DataFrame for new session entries
    new_df = pd.DataFrame(new_entries)

    # Calculate and show session total
    session_total = new_df["Amount"].sum()
    print(f"\n{Colors.BOLD} Total expenses this session: ₹{session_total:.2f}{Colors.ENDC}")

    # Append and save - future-proof fix
    if not new_df.empty:
        new_df = new_df.dropna(axis=1, how='all')  # Drop all-NA columns
        for col in columns:
            if col not in new_df.columns:
                new_df[col] = ""

        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(file_name, index=False)

    # Calculate and show overall total
    overall_total = df["Amount"].sum()
    print(f"{Colors.BOLD} Overall total expenses: ₹{overall_total:.2f}{Colors.ENDC}")

    if get_yes_no("Do you want to see a graph of your expenses?") == "yes":
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors='coerce')
        df = df.dropna(subset=["Date"])  # Drop rows where date conversion failed
        daily_total = df.groupby("Date")["Amount"].sum()

        plt.figure(figsize=(10, 5))
        plt.plot(daily_total.index, daily_total.values, marker='o', linestyle='-', color='#1f77b4')
        plt.title("Daily Expenses Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount Spent (₹)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
