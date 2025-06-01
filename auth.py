import os
import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, Frame
from PIL import Image, ImageTk

#  Function to Hash Passwords Securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#  Function to Create Users Table if it Doesn't Exist
def create_users_table():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#  Function to Show the Login Window
def login_signup_window(root):
    def switch_to_signup():
        login_frame.pack_forget()
        signup_frame.pack()

    def switch_to_login():
        signup_frame.pack_forget()
        login_frame.pack()

    def authenticate_user():
        username = login_username.get().strip()
        password = login_password.get().strip()
        hashed_pw = hash_password(password)

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo(" Success", "Login successful!")
            login_window.destroy()
            root.deiconify()  # Show the main inventory system
        else:
            messagebox.showerror(" Error", "Invalid username or password!")

    def register_user():
        username = signup_username.get().strip()
        password = signup_password.get().strip()

        if not username or not password:
            messagebox.showerror(" Error", "All fields are required!")
            return

        hashed_pw = hash_password(password)

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            messagebox.showinfo(" Success", "Account created successfully! Please login.")
            switch_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("❌ Error", "Username already exists!")
        finally:
            conn.close()

    #  Create the Login Window
    login_window = Toplevel()
    login_window.title("User Authentication")
    login_window.geometry("400x450")
    login_window.resizable(False, False)
    login_window.configure(bg="#f4f4f4")

    #  Load and Display Logo
    if os.path.exists("logoo.png"):
        logo_img = Image.open("logoo.png").resize((80, 80))
        logo_img = ImageTk.PhotoImage(logo_img)
        logo_label = Label(login_window, image=logo_img, bg="#f4f4f4")
        logo_label.image = logo_img
        logo_label.pack(pady=10)

    #  Title Label
    Label(login_window, text="🔐 User Authentication", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50", pady=10).pack(fill="x")

    #  Login Frame
    login_frame = Frame(login_window, bg="#f4f4f4")
    login_frame.pack()

    Label(login_frame, text="👤 Username:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)
    login_username = Entry(login_frame, font=("Arial", 12), bd=2, relief="solid", width=25)
    login_username.pack(pady=5)

    Label(login_frame, text="🔑 Password:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)
    login_password = Entry(login_frame, font=("Arial", 12), bd=2, relief="solid", width=25, show="*")
    login_password.pack(pady=5)

    #  Buttons Frame (Aligned in One Line)
    button_frame = Frame(login_window, bg="#f4f4f4")
    button_frame.pack(pady=10)

    #  Button Hover Effects
    def on_enter(e): e.widget.config(bg="#45a049")
    def on_leave(e): e.widget.config(bg="#4CAF50")

    def on_register_enter(e): e.widget.config(bg="#2980b9")
    def on_register_leave(e): e.widget.config(bg="#3498db")

    # Login Button (With Icon)
    login_btn = Button(button_frame, text="🔑 Login", command=authenticate_user,
                       font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, width=10)
    login_btn.grid(row=0, column=0, padx=5)
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    #  Register Switch Button
    switch_register_btn = Button(button_frame, text="📝 Register", command=switch_to_signup,
                                 font=("Arial", 12, "bold"), bg="#3498db", fg="white", padx=10, pady=5, width=10)
    switch_register_btn.grid(row=0, column=1, padx=5)
    switch_register_btn.bind("<Enter>", on_register_enter)
    switch_register_btn.bind("<Leave>", on_register_leave)

    #  Signup Frame (Initially Hidden)
    signup_frame = Frame(login_window, bg="#f4f4f4")

    Label(signup_frame, text="👤 New Username:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)
    signup_username = Entry(signup_frame, font=("Arial", 12), bd=2, relief="solid", width=25)
    signup_username.pack(pady=5)

    Label(signup_frame, text="🔑 New Password:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)
    signup_password = Entry(signup_frame, font=("Arial", 12), bd=2, relief="solid", width=25, show="*")
    signup_password.pack(pady=5)

    #  Register Button
    register_btn = Button(signup_frame, text="📝 Register", command=register_user,
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, width=10)
    register_btn.pack(pady=10)
    register_btn.bind("<Enter>", on_enter)
    register_btn.bind("<Leave>", on_leave)

    #  Switch Back to Login Button
    switch_login_btn = Button(signup_frame, text="🔑 Already have an account? Login", command=switch_to_login,
                              font=("Arial", 10, "bold"), fg="blue", bd=0, bg="#f4f4f4")
    switch_login_btn.pack(pady=5)

    #  Show Login Frame by Default
    login_frame.pack()
