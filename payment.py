from database import get_connection

def payment():
    order_id = input("order id: ")
    amount = float(input("amount: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "insert into payments(order_id,amount) values (?,?)",
        (order_id, amount)
    )

    cur.execute(
        "update orders set status='paid' where id=?",
        (order_id,)
    )

    conn.commit()
    conn.close()
    print("payment success")
