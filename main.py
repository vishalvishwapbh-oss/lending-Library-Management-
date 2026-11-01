from models import Book, Magazine, ReferenceBook
from models import StudentMember, FacultyMember, ResearchStudent, NotifiedMember
from library_service import LibraryManager
from storage import save_data, load_data


library = LibraryManager()

load_data(library)


while True:

    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Register Book")
    print("2. Register Magazine")
    print("3. Register Reference Book")
    print("4. Register Member")
    print("5. Borrow Item")
    print("6. Return Item")
    print("7. Show All Items")
    print("8. Show Available Items")
    print("9. Show Active Loans")
    print("10. Show Overdue Loans")
    print("11. Show Member Report")
    print("12. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        item_id = input("Enter Book ID: ")
        title = input("Enter Book Title: ")

        library.register_item(Book(item_id, title))

    elif choice == "2":

        item_id = input("Enter Magazine ID: ")
        title = input("Enter Magazine Title: ")

        library.register_item(Magazine(item_id, title))

    elif choice == "3":

        item_id = input("Enter Reference Book ID: ")
        title = input("Enter Reference Book Title: ")

        library.register_item(ReferenceBook(item_id, title))

    elif choice == "4":

        print("1. Student Member")
        print("2. Faculty Member")
        print("3. Research Student")
        print("4. Notified Member")

        member_choice = input("Enter member type: ")

        member_id = input("Enter Member ID: ")
        name = input("Enter Member Name: ")

        if member_choice == "1":
            member = StudentMember(member_id, name)

        elif member_choice == "2":
            member = FacultyMember(member_id, name)

        elif member_choice == "3":
            member = ResearchStudent(member_id, name)

        elif member_choice == "4":
            member = NotifiedMember(member_id, name, 3)

        else:
            print("Invalid member type.")
            continue

        library.register_member(member)

    elif choice == "5":

        member_id = input("Enter Member ID: ")
        item_id = input("Enter Item ID: ")

        library.borrow_item(member_id, item_id)

    elif choice == "6":

        member_id = input("Enter Member ID: ")
        item_id = input("Enter Item ID: ")

        library.return_item(member_id, item_id)

    elif choice == "7":

        library.show_all_items()

    elif choice == "8":

        library.show_available_items()

    elif choice == "9":

        library.show_active_loans()

    elif choice == "10":

        library.show_overdue_loans()

    elif choice == "11":

        library.show_member_report()

    elif choice == "12":

        save_data(library)
        print("Thank you for using Library Management System.")
        break

    else:

        print("Invalid choice. Try again.")