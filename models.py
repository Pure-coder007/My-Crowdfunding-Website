# models.py
import mysql.connector

config = {
    'user': 'kingsley',
    'password': 'language007',
    'host': 'localhost',
    'port': '3306',
    'database': 'user_registration'
}

# Adding a user to the database
def add_user(first_name, last_name, email, password):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()


# Getting a user logged in
def get_user(email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user



# Adding a category to the database
def add_category(category_name, fundraising_for, amount, description):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categories (category_name, fundraising_for, amount, description) VALUES (%s, %s, %s, %s)",(category_name, fundraising_for, amount, description))
                   



# Showing the requests function for users making help requests
def get_requests():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    cursor.close()
    connection.close()
    return requests
