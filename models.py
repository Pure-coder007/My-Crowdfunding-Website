# models.py
import mysql.connector

config = {
    'user': 'kingsley',
    'password': 'language007',
    'host': 'localhost',
    'port': '3306',
    'database': 'user_registration'
}

def add_user(first_name, last_name, email, password):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password))
    
    connection.commit()
    cursor.close()
    connection.close()
