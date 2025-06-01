import sqlite3
from tkinter import Toplevel, Text, Scrollbar, messagebox
from datetime import datetime

#  Function to Record Sales in Database
def record_sale(product_name, quantity_sold, price):
    date_today = datetime.today().strftime("%Y-%m-%d")

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    #  Create the sales table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            date TEXT
        )
    """)

    cursor.execute("INSERT INTO sales (product_name, quantity, price, date) VALUES (?, ?, ?, ?)",
                   (product_name, quantity_sold, price, date_today))
    conn.commit()
    conn.close()

#  Function to Show Sales Report
def show_sales_report():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date, product_name, quantity, price FROM sales ORDER BY date DESC")
    sales = cursor.fetchall()
    conn.close()

    if not sales:
        messagebox.showinfo("No Sales", "No sales records found.")
        return

    # Open a new window for the sales report
    report_window = Toplevel()
    report_window.title("Sales Report")
    report_window.geometry("750x500")  #  Increased width for better readability

    # Create a Scrollable Text Area with Horizontal Scrollbar
    text_area = Text(report_window, wrap="none", font=("Courier", 12))  #  Monospace font for better alignment
    y_scrollbar = Scrollbar(report_window, command=text_area.yview)
    x_scrollbar = Scrollbar(report_window, orient="horizontal", command=text_area.xview)
    text_area.config(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    text_area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    y_scrollbar.pack(side="right", fill="y")
    x_scrollbar.pack(side="bottom", fill="x")

    # Header with proper spacing
    report_text = "📅 SALES REPORT\n"
    report_text += "=" * 80 + "\n"
    report_text += f"{'DATE':<12} {'PRODUCT':<20} {'QTY':<5} {'PRICE':<10} {'TOTAL':<10}\n"
    report_text += "=" * 80 + "\n"

    current_date = None
    total_revenue = {}

    for date, product, qty, price in sales:
        if date != current_date:
            if current_date:
                report_text += "-" * 80 + "\n"
                report_text += f"➡️ TOTAL REVENUE FOR {current_date}: ${total_revenue[current_date]:.2f}\n"
                report_text += "-" * 80 + "\n\n"

            report_text += f"\n📆 DATE: {date}\n"
            report_text += "-" * 80 + "\n"
            current_date = date
            total_revenue[current_date] = 0  # Initialize total revenue for the day

        revenue = qty * price
        total_revenue[current_date] += revenue

        # Structured table format with alignment
        report_text += f"{date:<12} {product:<20} {qty:<5} ${price:<9.2f} ${revenue:<10.2f}\n"

    # Add the last day's total revenue
    if current_date:
        report_text += "-" * 80 + "\n"
        report_text += f"➡️ TOTAL REVENUE FOR {current_date}: ${total_revenue[current_date]:.2f}\n"
        report_text += "=" * 80 + "\n"

    # Insert text into the text area
    text_area.insert("1.0", report_text)
    text_area.config(state="disabled")  # Make text area read-only
