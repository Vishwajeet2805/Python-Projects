# Project: To-Do List

def todo_list():
    print("To-Do List Manager\n")

    filename = "todo_list.txt"
    todos = []

    file_found = False
    all_files = open("todo_list.txt", "a+")
    all_files.seek(0)
    lines = all_files.readlines()
    if lines:
        file_found = True

    if file_found:
        for line in lines:
            parts = line.strip().split("||")
            if len(parts) == 2:
                task, done = parts
                todos.append({"task": task, "done": done == "True"})
    all_files.close()

    while True:
        print("\n==== MENU ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        print("==============")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            task = input("Enter new task: ").strip()
            if task:
                todos.append({"task": task, "done": False})
                print(" Task added!")
            else:
                print(" Task cannot be empty.")

        elif choice == '2':
            print("\nYour Tasks:")
            if not todos:
                print("No tasks yet!")
            else:
                for i, t in enumerate(todos, 1):
                    status = "✅" if t["done"] else "❌"
                    print(f"{i}. {t['task']} {status}")

        elif choice == '3':
            if not todos:
                print(" No tasks to mark.")
            else:
                num = int(input("Enter task number to mark as done: ")) - 1
                if 0 <= num < len(todos):
                    todos[num]["done"] = True
                    print(" Task marked as done!")
                else:
                    print(" Invalid task number.")

        elif choice == '4':
            if not todos:
                print(" No tasks to delete.")
            else:
                num = int(input("Enter task number to delete: ")) - 1
                if 0 <= num < len(todos):
                    removed = todos.pop(num)
                    print(f" Deleted: {removed['task']}")
                else:
                    print(" Invalid task number.")

        elif choice == '5':
            break

        else:
            print("❌ Invalid option. Please choose 1–5.")

    # Save tasks to file
    with open(filename, "w") as file:
        for todo in todos:
            file.write(f"{todo['task']}||{todo['done']}\n")

    print(f"\n To-Do list saved as '{filename}'!")
    print(" Goodbye!")


todo_list()
