import sqlite3
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime

#  Function to Generate Invoice PDF
def generate_invoice(product_name, quantity, price):
    total_price = quantity * price
    invoice_number = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"Invoice_{invoice_number}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    #  Invoice Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Sales Invoice", ln=True, align="C")  #  No emoji, will work correctly

    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Invoice Number:", 0, 0)
    pdf.cell(100, 10, invoice_number, 0, 1)
    pdf.cell(100, 10, "Date:", 0, 0)
    pdf.cell(100, 10, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 1)
    pdf.ln(10)

    #  Invoice Table
    pdf.cell(100, 10, "Product Name", 1, 0, "C")
    pdf.cell(40, 10, "Quantity", 1, 0, "C")
    pdf.cell(50, 10, "Total Price", 1, 1, "C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 10, product_name, 1, 0, "C")
    pdf.cell(40, 10, str(quantity), 1, 0, "C")
    pdf.cell(50, 10, f"${total_price:.2f}", 1, 1, "C")

    #  Save PDF
    pdf.output(filename)
    
    messagebox.showinfo(" Invoice Created", f"Invoice saved as {filename}")

# Function to Validate Input & Generate Invoice
def create_invoice(entry_product, entry_quantity, entry_price):
    product_name = entry_product.get().strip()
    quantity = entry_quantity.get().strip()
    price = entry_price.get().strip()

    #  Validation Checks
    if not product_name:
        messagebox.showerror("❌ Error", "Product Name cannot be empty!")
        return
    if not quantity.isdigit():
        messagebox.showerror("❌ Error", "Quantity must be a whole number!")
        return
    if not price.replace(".", "", 1).isdigit():
        messagebox.showerror("❌ Error", "Price must be a valid number!")
        return

    #  Convert to Correct Types
    quantity = int(quantity)
    price = float(price)

    #  Check if the Product Exists in the Database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
    product = cursor.fetchone()
    conn.close()

    if not product:
        messagebox.showerror("❌ Error", f"Product '{product_name}' not found in inventory!")
        return

    generate_invoice(product_name, quantity, price)

#  Popup Window to Generate Invoice Manually
def invoice_popup():
    popup = tk.Toplevel()
    popup.title("🧾 Generate Invoice")
    popup.geometry("350x300")

    tk.Label(popup, text="Enter Sale Details:", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(popup, text="Product Name").pack()
    entry_product = tk.Entry(popup, font=("Arial", 12), width=25)
    entry_product.pack(pady=5)

    tk.Label(popup, text="Quantity").pack()
    entry_quantity = tk.Entry(popup, font=("Arial", 12), width=25)
    entry_quantity.pack(pady=5)

    tk.Label(popup, text="Price per Unit").pack()
    entry_price = tk.Entry(popup, font=("Arial", 12), width=25)
    entry_price.pack(pady=5)

    tk.Button(
        popup, 
        text="🧾 Generate Invoice", 
        command=lambda: create_invoice(entry_product, entry_quantity, entry_price), 
        font=("Arial", 12, "bold"), 
        bg="#4CAF50", fg="white", padx=10, pady=5
    ).pack(pady=10)
