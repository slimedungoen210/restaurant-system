import sqlite3


def get_connection():
    return sqlite3.connect("restaurant.db")


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    create table if not exists users(
        id integer primary key autoincrement,
        username text,
        password text,
        role text
    )
    """)

    cur.execute("""
    create table if not exists menu(
        id integer primary key autoincrement,
        name text,
        price real
    )
    """)

    cur.execute("""
    create table if not exists orders(
        id integer primary key autoincrement,
        table_no text,
        total real,
        status text
    )
    """)

    cur.execute("""
    create table if not exists order_items(
        id integer primary key autoincrement,
        order_id integer,
        menu_id integer,
        name text,
        price real,
        quantity integer
    )
    """)

    cur.execute("select * from users")
    if not cur.fetchall():
        cur.execute("insert into users values(null,'duc','111','admin')")
        cur.execute("insert into users values(null,'mai','222','admin')")
        cur.execute("insert into users values(null,'ha','111','staff')")
        cur.execute("insert into users values(null,'my','222','staff')")

    conn.commit()
    conn.close()
