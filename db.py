import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Change if needed
        database="SecureHer"
    )