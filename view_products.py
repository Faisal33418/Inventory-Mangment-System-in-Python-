import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
import os

def view_products(display_frame):
    for widget in display_frame.winfo_children():
        widget.destroy()

    # Add "Available Products" Label
    label = tk.Label(display_frame, text="Available Products", font=("Arial", 14, "bold"), pady=10)
    label.pack()

    # Create a Scrollable Canvas (Centering the Products)
    outer_frame = tk.Frame(display_frame)
    outer_frame.pack(fill="both", expand=True, padx=50, pady=10)  # Increased padding for better centering

    canvas = tk.Canvas(outer_frame)
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=1050)  # Adjusted width for center alignment

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetch products from database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        tk.Label(scrollable_frame, text="No products available.", font=("Arial", 12), fg="red").pack()

    row_num = 0
    col_num = 0
    max_columns = 4  # Max 4 items per row (Centered)

    for row in rows:
        product_id, name, quantity, price, image_path = row

        # Create a frame for each product with adjusted spacing for proper alignment
        frame = tk.Frame(scrollable_frame, padx=10, pady=10, relief="solid", borderwidth=1, height=190, width=190)
        frame.grid(row=row_num, column=col_num, padx=35, pady=20)  # Adjusted padding to keep them centered

        # Load product image
        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((130, 130))  # Slightly increased image size
            img = ImageTk.PhotoImage(img)
        else:
            img = Image.new("RGB", (130, 130), color=(200, 200, 200))
            img = ImageTk.PhotoImage(img)

        img_label = tk.Label(frame, image=img)
        img_label.image = img  # Prevent garbage collection
        img_label.pack()

        tk.Label(frame, text=f"Name: {name}", font=("Arial", 10, "bold")).pack()
        tk.Label(frame, text=f"Qty: {quantity}", font=("Arial", 10)).pack()
        tk.Label(frame, text=f"Price: ${price}", font=("Arial", 10)).pack()

        col_num += 1
        if col_num >= max_columns:
            col_num = 0
            row_num += 1
