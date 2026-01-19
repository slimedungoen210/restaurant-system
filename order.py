from database import get_connection

def create_order():
    table_number = input("table number: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "insert into orders(table_number,status) values (?,?)",
        (table_number, "pending")
    )
    order_id = cur.lastrowid

    while True:
        food = input("food id (done to finish): ")
        if food == "done":
            break

        qty = int(input("quantity: "))
        cur.execute(
            "insert into order_items(order_id,menu_id,quantity) values (?,?,?)",
            (order_id, food, qty)
        )

    conn.commit()
    conn.close()
    print("order created")

def view_orders():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from orders")
    rows = cur.fetchall()

    print("\n--- orders ---")
    for r in rows:
        print(r)

    conn.close()

def search_order():
    order_id = input("order id: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select * from orders where id=?", (order_id,))
    print(cur.fetchone())

    conn.close()

def update_order():
    order_id = input("order id: ")
    status = input("new status: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "update orders set status=? where id=?",
        (status, order_id)
    )

    conn.commit()
    conn.close()
    print("updated")

def delete_order():
    order_id = input("order id: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("delete from order_items where order_id=?", (order_id,))
    cur.execute("delete from orders where id=?", (order_id,))

    conn.commit()
    conn.close()
    print("deleted")
