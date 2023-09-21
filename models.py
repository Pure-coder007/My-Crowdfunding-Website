# models.py
import mysql.connector

config = {
    'user': 'kingsley',
    'password': 'language007',
    'host': 'localhost',
    'port': '3306',
    'database': 'user_registration'
}

def add_user(first_name, last_name, email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)", (first_name, last_name, email))
    
    connection.commit()
    cursor.close()
    connection.close()
