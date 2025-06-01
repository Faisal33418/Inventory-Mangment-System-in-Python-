import tkinter as tk
from tkinter import messagebox
import sqlite3
from view_products import view_products

def update_product_popup(root, display_frame):
    popup = tk.Toplevel(root)
    popup.title("Update Product")
    popup.geometry("450x350")
    popup.resizable(False, False)
    popup.configure(bg="#f4f4f4")

    # ✅ Title Label
    tk.Label(popup, text="Update Product Details", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50", pady=10).pack(fill="x")

    form_frame = tk.Frame(popup, bg="#f4f4f4")
    form_frame.pack(pady=10)

    # ✅ Product Name
    tk.Label(form_frame, text="Product Name:", font=("Arial", 12), bg="#f4f4f4").grid(row=0, column=0, pady=5, sticky="w")
    entry_name = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_name.grid(row=0, column=1, pady=5, padx=10)

    # ✅ New Quantity
    tk.Label(form_frame, text="New Quantity:", font=("Arial", 12), bg="#f4f4f4").grid(row=1, column=0, pady=5, sticky="w")
    entry_quantity = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_quantity.grid(row=1, column=1, pady=5, padx=10)

    # ✅ New Price
    tk.Label(form_frame, text="New Price:", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0, pady=5, sticky="w")
    entry_price = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_price.grid(row=2, column=1, pady=5, padx=10)

    # ✅ Update Product Function with Validation
    def update_product():
        name = entry_name.get().strip()
        quantity = entry_quantity.get().strip()
        price = entry_price.get().strip()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        #  Check if the product exists
        cursor.execute("SELECT COUNT(*) FROM products WHERE name = ?", (name,))
        result = cursor.fetchone()

        if result[0] == 0:  # No product found
            messagebox.showerror("Error", f"No product found with the name '{name}'!")
            conn.close()
            return

        #  Update Product if it exists
        cursor.execute("UPDATE products SET quantity = ?, price = ? WHERE name = ?", (quantity, price, name))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product updated successfully!")
        popup.destroy()
        view_products(display_frame)

    # ✅ Buttons Frame (Aligned in One Line)
    button_frame = tk.Frame(popup, bg="#f4f4f4")
    button_frame.pack(pady=10)

    # ✅ Update Button with Hover Effects
    def on_enter(e): e.widget.config(bg="#45a049")
    def on_leave(e): e.widget.config(bg="#4CAF50")

    update_btn = tk.Button(button_frame, text="Update Product", command=update_product, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    update_btn.grid(row=0, column=0, padx=10)

    button_frame.pack()
