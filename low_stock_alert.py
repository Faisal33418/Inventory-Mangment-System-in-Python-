import sqlite3
import tkinter as tk
from tkinter import messagebox, Scrollbar

def low_stock_popup(root):
    popup = tk.Toplevel(root)
    popup.title("Low Stock Alert")
    popup.geometry("350x250")  #  Adjusted Size for Better View
    popup.resizable(False, False)
    popup.configure(bg="#f4f4f4")

    #  Title Label
    tk.Label(popup, text="⚠️ Low Stock Alert", font=("Arial", 14, "bold"), fg="white", bg="#c0392b", pady=10).pack(fill="x")

    #  Scrollable Frame for Low Stock Items
    frame = tk.Frame(popup, bg="#f4f4f4")
    frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(frame, bg="#f4f4f4", highlightthickness=0)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    #  Fetch Low Stock Products
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity FROM products WHERE quantity < 5 ORDER BY quantity ASC")
    rows = cursor.fetchall()
    conn.close()

    #  Show Products or "No Low Stock" Message
    if not rows:
        tk.Label(scrollable_frame, text=" No low stock items.", font=("Arial", 12), fg="green", bg="#f4f4f4").pack(pady=5)
    else:
        for row in rows:
            tk.Label(scrollable_frame, text=f"❌ {row[0]} - {row[1]} left!", font=("Arial", 12, "bold"), fg="red", bg="#f4f4f4").pack(pady=2, anchor="w")

    #  Pack Scrollable Components
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
