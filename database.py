import sqlite3

def get_connection():
    return sqlite3.connect("restaurant.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
    create table if not exists users (
        id integer primary key autoincrement,
        username text,
        password text,
        role text
    )
    """)

    # menu
    cur.execute("""
    create table if not exists menu (
        id integer primary key autoincrement,
        name text,
        price integer
    )
    """)

    # orders
    cur.execute("""
    create table if not exists orders (
        id integer primary key autoincrement,
        table_number integer,
        status text
    )
    """)

    # order_items
    cur.execute("""
    create table if not exists order_items (
        id integer primary key autoincrement,
        order_id integer,
        menu_id integer,
        quantity integer
    )
    """)

    # payments
    cur.execute("""
    create table if not exists payments (
        id integer primary key autoincrement,
        order_id integer,
        amount integer
    )
    """)

    # create default users
    cur.execute("select count(*) from users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "insert into users(username,password,role) values ('admin','123','admin')"
        )
        cur.execute(
            "insert into users(username,password,role) values ('duc','111','staff')"
        )

    conn.commit()
    conn.close()
