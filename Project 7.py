# Project To-Do list

todos = []

while True:
    print("\n To-Do List Menu")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose an option (1-5):\n ")

    if choice == '1':
        task = input("Enter new task: ")
        todos.append({"task": task, "done": False})
        print("Task added!")

    elif choice == '2':
        if not todos:
            print("No tasks yet!")
        else:
            print("\n Your Tasks:")
            for i, t in enumerate(todos, 1):
                status = "✅" if t["done"] else "❌"
                print(f"{i}. {t['task']} {status}")

    elif choice == '3':
        num = int(input("Task number to mark as done: ")) - 1
        if 0 <= num < len(todos):
            todos[num]["done"] = True
            print("Marked as done!")
        else:
            print("Invalid task number.")

    elif choice == '4':
        num = int(input("Task number to delete: ")) - 1
        if 0 <= num < len(todos):
            removed = todos.pop(num)
            print(f"Deleted: {removed['task']}")
        else:
            print("Invalid task number.")

    elif choice == '5':
        print("Exiting To-Do List. Goodbye!")
        break

    else:
        print("Invalid option. Please choose 1-5.")
