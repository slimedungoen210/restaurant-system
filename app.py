import tkinter as tk
from tkinter import messagebox, simpledialog
from database import get_connection, init_db

status = ["pending", "preparing", "served", "paid"]


class restaurantapp:
    def __init__(self, root):
        self.root = root
        self.root.title("restaurant order management")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.current_role = None
        init_db()
        self.main_menu()

    # ================= common =================
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ================= main menu =================
    def main_menu(self):
        self.current_role = None
        self.clear()

        tk.Label(self.root, text="restaurant system", font=("arial", 18, "bold")).pack(pady=30)
        tk.Button(self.root, text="customer", command=self.customer_menu).pack(fill="x", padx=100, pady=6)
        tk.Button(self.root, text="staff", command=lambda: self.login_screen("staff")).pack(fill="x", padx=100, pady=6)
        tk.Button(self.root, text="admin", command=lambda: self.login_screen("admin")).pack(fill="x", padx=100, pady=6)
        tk.Button(self.root, text="exit", command=self.root.destroy).pack(fill="x", padx=100, pady=20)

    # ================= login =================
    def login_screen(self, role):
        self.clear()
        tk.Label(self.root, text=f"{role} login", font=("arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="username").pack()
        user = tk.Entry(self.root)
        user.pack()

        tk.Label(self.root, text="password").pack()
        pw = tk.Entry(self.root, show="*")
        pw.pack()

        def do_login():
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "select * from users where username=? and password=? and role=?",
                (user.get(), pw.get(), role)
            )
            if cur.fetchone():
                self.current_role = role
                self.admin_menu() if role == "admin" else self.staff_menu()
            else:
                messagebox.showerror("error", "login failed")
            conn.close()

        tk.Button(self.root, text="login", command=do_login).pack(pady=10)
        tk.Button(self.root, text="back", command=self.main_menu).pack()

    # ================= customer =================
    def customer_menu(self):
        self.clear()
        tk.Label(self.root, text="customer menu", font=("arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="view menu", command=self.view_menu).pack(fill="x", padx=100, pady=6)
        tk.Button(self.root, text="create order", command=self.create_order).pack(fill="x", padx=100, pady=6)
        tk.Button(self.root, text="back", command=self.main_menu).pack(fill="x", padx=100, pady=15)

    def view_menu(self):
        self.clear()
        tk.Label(self.root, text="menu list", font=("arial", 16, "bold")).pack(pady=10)
        lb = tk.Listbox(self.root, width=50, height=18)
        lb.pack()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select * from menu")
        for m in cur.fetchall():
            lb.insert("end", f"id:{m[0]} | {m[1]} - {int(m[2])}$")
        conn.close()

        tk.Button(
            self.root,
            text="back",
            command=self.customer_menu if self.current_role is None else
            (self.admin_menu if self.current_role == "admin" else self.staff_menu)
        ).pack(pady=10)

    def create_order(self):
        table = simpledialog.askstring("order", "table number:")
        if not table:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select * from menu")
        menu = cur.fetchall()

        if not menu:
            messagebox.showerror("error", "menu empty")
            conn.close()
            return

        items = []
        total = 0
        msg = "menu:\n"
        for m in menu:
            msg += f"{m[0]}. {m[1]} - {m[2]}$\n"

        while True:
            fid = simpledialog.askinteger("order", msg + "\nfood id (cancel to finish)")
            if not fid:
                break

            food = next((m for m in menu if m[0] == fid), None)
            if not food:
                messagebox.showerror("error", "invalid food id")
                continue

            qty = simpledialog.askinteger("order", "quantity:")
            if not qty or qty <= 0:
                continue

            items.append((food[0], food[1], food[2], qty))
            total += food[2] * qty

        if total == 0:
            conn.close()
            return

        cur.execute("insert into orders values(null,?,?,?)", (table, total, "pending"))
        order_id = cur.lastrowid

        for it in items:
            cur.execute(
                "insert into order_items values(null,?,?,?,?,?)",
                (order_id, it[0], it[1], it[2], it[3])
            )

        conn.commit()
        conn.close()
        messagebox.showinfo("success", f"order created\n total: {total}$")

    # ================= orders =================
    def view_orders(self):
        self.clear()
        tk.Label(self.root, text="order list", font=("arial", 16, "bold")).pack(pady=10)
        self.lb = tk.Listbox(self.root, width=65, height=22)
        self.lb.pack()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select * from orders")

        for o in cur.fetchall():
            self.lb.insert("end", f"order {o[0]} | table {o[1]} | {o[3]} | total {o[2]}$")
            cur.execute("select name, price, quantity from order_items where order_id=?", (o[0],))
            for it in cur.fetchall():
                self.lb.insert("end", f"   - {it[0]} x{it[2]} = {it[1]*it[2]}$")
            self.lb.insert("end", "-" * 60)

        conn.close()
        tk.Button(self.root, text="back", command=self.go_back).pack(pady=10)

    # ================= staff =================
    def staff_menu(self):
        self.clear()
        tk.Label(self.root, text="staff menu", font=("arial", 16, "bold")).pack(pady=15)
        tk.Button(self.root, text="view orders", command=self.view_orders).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="search order", command=self.search_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="update order", command=self.update_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="delete order", command=self.delete_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="payment", command=self.payment).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="logout", command=self.main_menu).pack(fill="x", padx=100, pady=15)

    def search_order(self):
        self.view_orders()
        key = simpledialog.askstring("search", "table number or status:")
        if not key:
            self.staff_menu()
            return

        self.lb.delete(0, "end")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "select * from orders where table_no like ? or status like ?",
            (f"%{key}%", f"%{key}%")
        )
        for o in cur.fetchall():
            self.lb.insert("end", f"order {o[0]} | table {o[1]} | {o[3]} | total {o[2]}$")
        conn.close()

    def update_order(self):
        self.view_orders()
        oid = simpledialog.askinteger("update", "order id:")
        if oid is None:
            return

        st = simpledialog.askinteger("status", "0.pending 1.preparing 2.served 3.paid")
        if st not in range(4):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("update orders set status=? where id=?", (status[st], oid))
        conn.commit()
        conn.close()
        self.staff_menu()

    def delete_order(self):
        self.view_orders()
        oid = simpledialog.askinteger("delete", "order id:")
        if not oid:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("delete from order_items where order_id=?", (oid,))
        cur.execute("delete from orders where id=?", (oid,))
        conn.commit()
        conn.close()
        self.staff_menu()

    def payment(self):
        self.view_orders()
        oid = simpledialog.askinteger("payment", "order id:")
        if not oid:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("update orders set status='paid' where id=?", (oid,))
        conn.commit()
        conn.close()
        self.staff_menu()

    # ================= admin =================
    def admin_menu(self):
        self.clear()
        tk.Label(self.root, text="admin menu", font=("arial", 16, "bold")).pack(pady=15)
        tk.Button(self.root, text="view orders", command=self.view_orders).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="update order", command=self.update_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="edit order", command=self.edit_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="delete order", command=self.delete_order).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="view menu", command=self.view_menu).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="add menu", command=self.add_menu).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="report", command=self.report).pack(fill="x", padx=100, pady=4)
        tk.Button(self.root, text="logout", command=self.main_menu).pack(fill="x", padx=100, pady=15)

    def edit_order(self):
        self.view_orders()
        oid = simpledialog.askinteger("edit order", "order id:")
        if not oid:
            return

        new_table = simpledialog.askstring("edit", "new table number:")
        st = simpledialog.askinteger("status", "0.pending\n1.preparing\n2.served\n3.paid")

        if not new_table or st not in range(4):
            messagebox.showerror("error", "invalid input")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "update orders set table_no=?, status=? where id=?",
            (new_table, status[st], oid)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("success", "order edited")
        self.admin_menu()

    def add_menu(self):
        name = simpledialog.askstring("add", "food name:")
        price = simpledialog.askfloat("add", "price:")
        if name and price is not None:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("insert into menu values(null,?,?)", (name, price))
            conn.commit()
            conn.close()
            self.view_menu()

    def go_back(self):
        if self.current_role == "staff":
            self.staff_menu()
        elif self.current_role == "admin":
            self.admin_menu()
        else:
            self.main_menu()

    def report(self):
        self.clear()
        tk.Label(self.root, text="revenue report", font=("arial", 16, "bold")).pack(pady=10)
        lb = tk.Listbox(self.root, width=50, height=18)
        lb.pack()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select * from orders where status='paid'")
        total = 0
        for o in cur.fetchall():
            lb.insert("end", f"order {o[0]} | {o[2]}$")
            total += o[2]
        conn.close()

        tk.Label(self.root, text=f"total revenue: {total}$", font=("arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="back", command=self.admin_menu).pack(pady=10)
