import tkinter as tk
from PIL import Image, ImageTk
import os
from auth import login_signup_window, create_users_table  # ✅ Import authentication module
from add_product import add_product_popup
from view_products import view_products
from update_product import update_product_popup
from sell_product import sell_product_popup
from delete_product import delete_product_popup
from search_product import search_product_popup
from low_stock_alert import low_stock_popup
from sales_tracking import show_sales_report
from sales_analytics import show_sales_analytics  #  Integrated Sales Analytics
from generate_invoice import invoice_popup  #  Integrated Invoice Generation

#  Create Users Table at Startup
create_users_table()

#  Create Main Window (Hidden Until Login is Successful)
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1100x750")  #  Adjusted Size for Better UI Fit
root.configure(bg="#f4f4f4")
root.withdraw()  # Hide main window until login is successful

#  Show Login/Signup Window First
login_signup_window(root)

#  Logout Function (Closes Main & Reopens Login)
def logout():
    root.withdraw()  # Hide main window
    login_signup_window(root)  # Reopen login screen

#  Load and Display Logo & Title
title_frame = tk.Frame(root, bg="#2c3e50")
title_frame.pack(fill="x", pady=10)

title_inner_frame = tk.Frame(title_frame, bg="#2c3e50")
title_inner_frame.pack(pady=10)

if os.path.exists("logoo.png"):
    logo_img = Image.open("logoo.png").resize((60, 60))
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(title_inner_frame, image=logo_img, bg="#2c3e50")
    logo_label.image = logo_img
    logo_label.pack(side="left", padx=10)

#  Title Label
title_label = tk.Label(title_inner_frame, text="PECHS CAFE MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
title_label.pack(side="left", padx=10)

#  Button Hover Effect
def on_enter(e):
    e.widget.config(bg="#45a049")

def on_leave(e):
    e.widget.config(bg="#4CAF50")

#  Buttons in a 4x4 Grid + Logout on the Extreme Right in the First Row
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

buttons = [
    ("➕ Add", lambda: add_product_popup(root, display_frame)),
    ("🔄 Update", lambda: update_product_popup(root, display_frame)),
    ("💰 Sell", lambda: sell_product_popup(root, display_frame)),
    ("❌ Delete", lambda: delete_product_popup(root, display_frame)),
    ("⚠️ Stock Alert", lambda: low_stock_popup(root)),
    ("📊 Sales", show_sales_report),
    ("📈 Analytics", show_sales_analytics),  #  Integrated Sales Analytics
    ("🧾 Invoice", invoice_popup)  #  Fixed Invoice Button Alignment
]

#  Arrange Buttons in a 4x4 Grid (2 Rows of 4 Buttons Each)
for i, (text, command) in enumerate(buttons):
    row = i // 4  #  Break into rows after 4 buttons
    col = i % 4
    btn = tk.Button(
        button_frame, text=text, command=command, width=14, font=("Arial", 11, "bold"), 
        bg="#4CAF50", fg="white", bd=0, relief="raised", padx=5, pady=5
    )
    btn.grid(row=row, column=col, padx=10, pady=5)  #  Grid Layout for Better Alignment
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

#  Logout Button (Placed on the Extreme Right, Aligned with the First Row of Buttons)
logout_button = tk.Button(
    button_frame, text="🚪 Logout", command=logout, width=14, font=("Arial", 11, "bold"), 
    bg="red", fg="white", bd=0, relief="raised", padx=5, pady=5
)
logout_button.grid(row=0, column=4, padx=10, pady=5, sticky="e")  #  Aligned in First Row, Extreme Right

#  Search Bar with "Show All" Fix
search_frame = tk.Frame(root, bg="#f4f4f4")
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=35, fg="grey", font=("Arial", 12), bd=2, relief="solid")
search_entry.insert(0, "🔍 Search Product")  #  Added a Search Icon

def on_entry_click(event):
    if search_entry.get() == "🔍 Search Product":
        search_entry.delete(0, "end")
        search_entry.config(fg="black")

def on_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, "🔍 Search Product")
        search_entry.config(fg="grey")

search_entry.bind("<FocusIn>", on_entry_click)
search_entry.bind("<FocusOut>", on_focus_out)
search_entry.pack(side="left", padx=10, ipady=5)

#  Search Button
search_button = tk.Button(search_frame, text="🔍 Search", command=lambda: search_product_popup(display_frame, search_entry.get()), width=12, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", bd=0, relief="raised", padx=5, pady=5)
search_button.pack(side="left", padx=10)
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

# Fix "Show All" Button - Displays All Products Again (Green Color Fixed)
def reset_view():
    search_entry.delete(0, "end")  # Clear Search Bar
    search_entry.insert(0, "🔍 Search Product")
    view_products(display_frame)  # Reload All Products

show_all_button = tk.Button(search_frame, text="📋 Show All", command=reset_view, width=12, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", bd=0, relief="raised", padx=5, pady=5)  # ✅ Color Fixed to Green
show_all_button.pack(side="left", padx=10)
show_all_button.bind("<Enter>", on_enter)
show_all_button.bind("<Leave>", on_leave)

#  Frame to Display Products
display_frame = tk.Frame(root, bg="#f4f4f4")
display_frame.pack(fill="both", expand=True)

view_products(display_frame)

root.mainloop()
