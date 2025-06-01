import sqlite3
import tkinter as tk
from view_products import view_products
from PIL import Image, ImageTk
import os

def search_product_popup(display_frame, search_query):
    for widget in display_frame.winfo_children():
        widget.destroy()

    if not search_query or search_query == "Search Product...":
        view_products(display_frame)
        return

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_query + '%',))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        tk.Label(display_frame, text="No products found.", fg="red", font=("Arial", 14)).pack()

    row_num = 0
    col_num = 0

    for row in rows:
        product_id, name, quantity, price, image_path = row

        frame = tk.Frame(display_frame, padx=10, pady=10, relief="solid", borderwidth=1)
        frame.grid(row=row_num, column=col_num, padx=10, pady=10)

        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
        else:
            img = Image.new("RGB", (100, 100), color=(200, 200, 200))
            img = ImageTk.PhotoImage(img)

        img_label = tk.Label(frame, image=img)
        img_label.image = img
        img_label.pack()

        tk.Label(frame, text=f"Name: {name}").pack()
        tk.Label(frame, text=f"Qty: {quantity}").pack()
        tk.Label(frame, text=f"Price: ${price}").pack()

        col_num += 1
        if col_num > 3:
            col_num = 0
            row_num += 1
