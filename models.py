# models.py
import mysql.connector
from flask_login import UserMixin, LoginManager
# from db_setup import 


login_manager = LoginManager()

 

config = {
    'user': 'kingsley',
    'password': 'language007',
    'host': 'localhost',
    'port': '3306',
    'database': 'crowd_funding'
}

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password, is_admin=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def get(cls, user_id):
        pass
    
    
# Adding a user to the database (True means creating an admin while false is creating an ordinary user
def add_user(first_name, last_name, email, password, is_admin=False):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, is_admin) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, password, is_admin))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()



def get_user_by_id(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))
    user_record = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_record:
        return User(id=user_record['id'], first_name=user_record['first_name'], last_name=user_record['last_name'], email=user_record['email'], password=user_record['password'], is_admin=user_record['is_admin'])
    return None





# Getting a user logged in
def get_user(email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
    user_record = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_record:
        return User(id=user_record['id'], first_name=user_record['first_name'], last_name=user_record['last_name'], email=user_record['email'], password=user_record['password'], is_admin=user_record['is_admin'])
    return None



# Adding a category to the database
def add_category(user_id, category_name, fundraising_for, expiry_date, amount, description):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO categories (user_id, category_name, fundraising_for, expiry_date, amount, description) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, category_name, fundraising_for, expiry_date, amount, description))
    connection.commit()
    cursor.close()
    connection.close()


        
        
        
        



# Showing the requests function for users making help requests
def get_requests():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)  # fetch as dictionaries
    
    cursor.execute("""
    SELECT categories.id, users.email as user_email, category_name, fundraising_for, expiry_date, amount, description 
    FROM categories 
    JOIN users ON categories.user_id = users.id
    """)
    
    requests = cursor.fetchall()
    cursor.close()
    connection.close()
    return requests



def is_user_admin(email):
    user = get_user(email)
    return user.is_admin if user else False


def set_request_status(request_id, status):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("UPDATE requests SET status = %s WHERE id = %s", (status, request_id))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        cursor.close()
        connection.close()
