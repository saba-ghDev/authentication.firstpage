import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="root",      # your MySQL password
        database="auth_demo"  # your database name
    )
    return conn
