import sqlite3
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#  Function to Generate Sales Report (Graphical)
def show_sales_analytics():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    #  Get Total Sales per Product
    cursor.execute("SELECT product_name, SUM(quantity) FROM sales GROUP BY product_name ORDER BY SUM(quantity) DESC")
    sales_data = cursor.fetchall()
    conn.close()
    
    if not sales_data:
        tk.messagebox.showinfo("No Sales Data", "No sales records available to display analytics.")
        return

    #  Create Window for Analytics
    analytics_window = tk.Toplevel()
    analytics_window.title("📊 Sales Analytics")
    analytics_window.geometry("600x400")

    #  Create Figure
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    #  Data for Chart
    products = [item[0] for item in sales_data]
    sales = [item[1] for item in sales_data]

    ax.barh(products, sales, color="#4CAF50")
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Product Name")
    ax.set_title("📊 Top Selling Products")

    #  Display Chart
    canvas = FigureCanvasTkAgg(fig, analytics_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
