from services.crud import author_service
from services.crud.author_service import delete_author

def show_menu():
    print("Author Management")
    print("1. Create Author")
    print("2. View All Authors")
    print("3. View Author by ID")
    print("4. Update Author")
    print("5. Delete Author")
    print("0. Exit")

def print_author(author):
    print(f"{author[0]} - {author[1]} {author[2]}")

def create_author():
    first_name = input("Author's first name: ").strip()
    last_name = input("Author's last name: ").strip()
    success = author_service.create_author(first_name, last_name)
    if success:
        print("Author created successfully.")

def view_all_authors():
    authors = author_service.read_all_authors()
    if not authors:
        print("No authors found.")
    else:
        for author in authors:
            print_author(author)


def view_author_by_id():
    try:
        id = int(input("Enter author ID: "))
        author = author_service.read_author_id(id)
        if author:
            print_author(author)
        else:
            print("Author not found.")
    except ValueError:
        print ("Invalid input. Please enter a numeric ID.")

def update_author():
    try:
        author_id = int(input("Enter author ID to be updated: "))
        print("Leave blank to keep current values.")
        new_first_name = input("New first name: ")
        new_last_name = input("New last name: ")

        success = author_service.update_author(author_id, new_first_name, new_last_name)
        if success:
            print("Author updated successfully")
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")

def delete_author():
    try:
        id = int(input("Enter author ID to delete:"))
        author_service.delete_author(id)
        print("Author deleted successfully.")
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")

def run():
    while True:
        show_menu()
        choice = input("Choice: ")
        if choice == "1":
            create_author()
        elif choice == "2":
            view_all_authors()
        elif choice == "3":
            view_author_by_id()
        elif choice == "4":
            update_author()
        elif choice == "5":
            delete_author()
        elif choice == "0":
            break
        else:
            print("Invalid command")