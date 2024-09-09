import sqlite3

def get_db_connection():
    try:
        conn = sqlite3.connect('C:\\Users\\PC\\Desktop\\Precision_Agriculture\\PrecisionAgriculture.db')
        conn.row_factory = sqlite3.Row
        print("Database connection established successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None