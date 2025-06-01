import tkinter as tk
from tkinter import messagebox
import sqlite3
from view_products import view_products
from sales_tracking import record_sale  #  Ensure this function exists in sales_tracking.py

def sell_product_popup(root, display_frame):
    popup = tk.Toplevel(root)
    popup.title("Sell Product")
    popup.geometry("300x250")
    popup.resizable(False, False)

    tk.Label(popup, text="Product Name:", font=("Arial", 12)).pack(pady=5)
    entry_name = tk.Entry(popup, font=("Arial", 12), width=25)
    entry_name.pack(pady=5)

    tk.Label(popup, text="Quantity to Sell:", font=("Arial", 12)).pack(pady=5)
    entry_quantity = tk.Entry(popup, font=("Arial", 12), width=25)
    entry_quantity.pack(pady=5)

    def sell_product():
        name = entry_name.get().strip()
        quantity_sold = entry_quantity.get().strip()

        if not name or not quantity_sold:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity_sold = int(quantity_sold)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity! Please enter a number.")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT quantity, price FROM products WHERE name=?", (name,))
        result = cursor.fetchone()

        if result:
            current_quantity, price_per_unit = result
            if current_quantity >= quantity_sold:
                new_quantity = current_quantity - quantity_sold
                cursor.execute("UPDATE products SET quantity = ? WHERE name=?", (new_quantity, name))
                conn.commit()

                # ✅ Record the sale correctly
                record_sale(name, quantity_sold, price_per_unit)

                messagebox.showinfo("Success", f"{quantity_sold} {name}(s) sold successfully!")  # ✅ Improved Message
                popup.destroy()
                view_products(display_frame)
            else:
                messagebox.showerror("Error", f"Not enough stock! Available: {current_quantity}")
        else:
            messagebox.showerror("Error", "Product not found!")

        conn.close()

    sell_button = tk.Button(popup, text="Sell Product", command=sell_product, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    sell_button.pack(pady=10)
