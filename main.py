from database import init_db
from user import login
from menu import view_menu, add_menu, delete_menu
from order import create_order, view_orders, search_order, update_order, delete_order
from payment import payment
from report import report

def customer_menu():
    while True:
        print("\n--- customer ---")
        print("1. view menu")
        print("2. create order")
        print("0. back")

        c = input("choose: ")
        if c == "1":
            view_menu()
        elif c == "2":
            create_order()
        elif c == "0":
            break

def staff_menu():
    if not login("staff"):
        return

    while True:
        print("\n--- staff ---")
        print("1. view orders")
        print("2. search order")
        print("3. update order")
        print("4. delete order")
        print("5. payment")
        print("0. logout")

        c = input("choose: ")
        if c == "1":
            view_orders()
        elif c == "2":
            search_order()
        elif c == "3":
            update_order()
        elif c == "4":
            delete_order()
        elif c == "5":
            payment()
        elif c == "0":
            break

def admin_menu():
    if not login("admin"):
        return

    while True:
        print("\n--- admin ---")
        print("1. view menu")
        print("2. add menu")
        print("3. delete menu")
        print("4. view orders")
        print("5. update order")
        print("6. report")
        print("0. logout")

        c = input("choose: ")
        if c == "1":
            view_menu()
        elif c == "2":
            add_menu()
        elif c == "3":
            delete_menu()
        elif c == "4":
            view_orders()
        elif c == "5":
            update_order()
        elif c == "6":
            report()
        elif c == "0":
            break

def main():
    init_db()

    while True:
        print("\n===== restaurant system =====")
        print("1. customer")
        print("2. staff")
        print("3. admin")
        print("0. exit")

        c = input("choose role: ")
        if c == "1":
            customer_menu()
        elif c == "2":  
            staff_menu()
        elif c == "3":
            admin_menu()
        elif c == "0":
            break

main()
