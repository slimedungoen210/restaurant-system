from database import get_connection

def report():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select sum(amount) from payments")
    total = cur.fetchone()[0]

    print("total revenue:", total if total else 0)

    conn.close()
