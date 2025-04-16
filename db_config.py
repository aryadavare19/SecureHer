import mysql.connector

# Connect to MySQL database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",      # Replace with your MySQL username
        password="root",  # Replace with your MySQL password
        database="secure_her"
    )
    return connection
