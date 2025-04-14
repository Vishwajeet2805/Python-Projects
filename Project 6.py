# Project Password Manager
manager = {}


while True:
    print("\n Password Manager")
    print("1. Add Password\n2. View Password\n3. Delete Password\n4. Exit")
    choice = input("Choose: ")

    if choice == '1':
        site = input("Site name: ")
        password = input("Password: ")
        manager[site] = password
        print(" Saved!")
    elif choice == '2':
        site = input("Enter site: ")
        print(f"{site} password: {manager.get(site, 'Not found')}")
    elif choice == '3':
        site = input("Site to delete: ")
        if site in manager:
            del manager[site]
            print("Deleted!")
        else:
            print("Site not found.")
    elif choice == '4':
        print("Exiting Password Manager.")
        break
    else:
        print("Invalid choice.")


