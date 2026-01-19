from database import get_connection

def login(role):
    username = input("username: ")
    password = input("password: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "select * from users where username=? and password=? and role=?",
        (username, password, role)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        print("login success")
        return True
    else:
        print("login failed")
        return False
