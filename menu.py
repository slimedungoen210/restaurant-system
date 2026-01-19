from database import get_connection

def view_menu():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from menu")
    rows = cur.fetchall()

    print("\n--- menu ---")
    for r in rows:
        print(r[0], r[1], r[2])

    conn.close()

def add_menu():
    name = input("food name: ")
    price = float(input("price: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("insert into menu(name,price) values (?,?)", (name, price))
    conn.commit()
    conn.close()

    print("added")

def delete_menu():
    food_id = input("food id: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("delete from menu where id=?", (food_id,))
    conn.commit()
    conn.close()

    print("deleted")
