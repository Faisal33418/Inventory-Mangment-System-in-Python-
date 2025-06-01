import sqlite3
import os

# Ensure images directory exists
if not os.path.exists("images"):
    os.makedirs("images")

def setup_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            image_path TEXT
        )
    """)

    conn.commit()
    conn.close()

setup_database()  # Ensure the database is set up when imported
