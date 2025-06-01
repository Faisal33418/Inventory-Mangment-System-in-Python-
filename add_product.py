import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
from PIL import Image, ImageTk
from view_products import view_products

def add_product_popup(root, display_frame):
    popup = tk.Toplevel(root)
    popup.title("Add Product")
    popup.geometry("450x550")
    popup.resizable(False, False)
    popup.configure(bg="#f4f4f4")

    #  Title Label
    tk.Label(popup, text="Add New Product", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50", pady=10).pack(fill="x")

    form_frame = tk.Frame(popup, bg="#f4f4f4")
    form_frame.pack(pady=10)

    #  Product Name
    tk.Label(form_frame, text="Product Name:", font=("Arial", 12), bg="#f4f4f4").grid(row=0, column=0, pady=5, sticky="w")
    entry_name = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_name.grid(row=0, column=1, pady=5, padx=10)

    #  Quantity
    tk.Label(form_frame, text="Quantity:", font=("Arial", 12), bg="#f4f4f4").grid(row=1, column=0, pady=5, sticky="w")
    entry_quantity = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_quantity.grid(row=1, column=1, pady=5, padx=10)

    #  Price
    tk.Label(form_frame, text="Price:", font=("Arial", 12), bg="#f4f4f4").grid(row=2, column=0, pady=5, sticky="w")
    entry_price = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    entry_price.grid(row=2, column=1, pady=5, padx=10)

    #  Image Upload Section
    img_label = tk.Label(form_frame, text="No image selected", font=("Arial", 10), fg="red", bg="#f4f4f4")
    img_label.grid(row=3, column=1, pady=5, sticky="w")

    img_preview = tk.Label(form_frame, bg="#f4f4f4", relief="solid", width=15, height=7)
    img_preview.grid(row=4, column=1, pady=5, padx=10)

    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            popup.image_path = file_path
            img_label.config(text=os.path.basename(file_path), fg="green")

            img = Image.open(file_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            img_preview.config(image=img)
            img_preview.image = img

    #  Buttons Frame (Aligned in One Line)
    button_frame = tk.Frame(popup, bg="#f4f4f4")
    button_frame.pack(pady=10)

    #  Image Upload Button
    select_img_btn = tk.Button(button_frame, text="Select Image", command=select_image, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    select_img_btn.grid(row=0, column=0, padx=10)

    #  Save Product Function
    def add_product():
        name = entry_name.get().strip()
        quantity = entry_quantity.get().strip()
        price = entry_price.get().strip()
        image_path = getattr(popup, "image_path", None)

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price!")
            return

        if image_path:
            if not os.path.exists("images"):
                os.makedirs("images")
            new_image_path = os.path.join("images", f"{name}.png")
            img = Image.open(image_path)
            img = img.resize((100, 100))
            img.save(new_image_path)
        else:
            new_image_path = None

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price, image_path) VALUES (?, ?, ?, ?)",
                       (name, quantity, price, new_image_path))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        popup.destroy()
        view_products(display_frame)

    #  Save Button (Aligned with Image Button)
    save_btn = tk.Button(button_frame, text="Save Product", command=add_product, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    save_btn.grid(row=0, column=1, padx=10)

    button_frame.pack()
