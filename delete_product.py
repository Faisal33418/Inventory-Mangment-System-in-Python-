import tkinter as tk
from tkinter import messagebox
import sqlite3
from view_products import view_products

def delete_product_popup(root, display_frame):
    popup = tk.Toplevel(root)
    popup.title("Delete Product")
    popup.geometry("320x180")  #  Adjusted Popup Size for Better Fit
    popup.resizable(False, False)
    popup.configure(bg="#f4f4f4")

    #  Title Label
    tk.Label(popup, text="Delete Product", font=("Arial", 14, "bold"), fg="white", bg="#c0392b", pady=10).pack(fill="x")

    form_frame = tk.Frame(popup, bg="#f4f4f4")
    form_frame.pack(pady=10)

    #  Product Name Input Field (Reduced Width)
    tk.Label(form_frame, text="Product Name:", font=("Arial", 12), bg="#f4f4f4").grid(row=0, column=0, pady=5, padx=5, sticky="w")
    entry_name = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=20)  #  Reduced Width
    entry_name.grid(row=0, column=1, pady=5, padx=5)

    #  Delete Product Function with Validation
    def delete_product():
        name = entry_name.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter product name to delete!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        #  Check if the product exists before deleting
        cursor.execute("SELECT COUNT(*) FROM products WHERE name=?", (name,))
        result = cursor.fetchone()

        if result[0] == 0:  # No product found
            messagebox.showerror("Error", f"No product found with the name '{name}'!")
            conn.close()
            return

        #  Delete Product if it exists
        cursor.execute("DELETE FROM products WHERE name=?", (name,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product deleted successfully!")
        popup.destroy()
        view_products(display_frame)

    #  Buttons Frame (Button Centered)
    button_frame = tk.Frame(popup, bg="#f4f4f4")
    button_frame.pack(pady=10)

    #  Delete Button with Hover Effects (Centered)
    def on_enter(e): e.widget.config(bg="#e74c3c")
    def on_leave(e): e.widget.config(bg="#c0392b")

    delete_btn = tk.Button(popup, text="Delete Product", command=delete_product, font=("Arial", 12, "bold"), bg="#c0392b", fg="white", padx=10, pady=5)
    delete_btn.pack(pady=5)  #  Button is Centered
    delete_btn.bind("<Enter>", on_enter)
    delete_btn.bind("<Leave>", on_leave)
