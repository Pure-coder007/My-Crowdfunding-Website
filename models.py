# models.py
from flask import redirect, flash, url_for
import mysql.connector
from flask_login import UserMixin, LoginManager
# from db_setup import 
from datetime import datetime

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
def add_category(user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    try:
        # Validate and parse the expiry_date
        if not expiry_date:
            # Handle the case where expiry_date is empty or None
            raise ValueError('Expiry date is required')
        
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        
        insert_query = """
        INSERT INTO categories (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
        # Assuming you have access to the user's email or can obtain it
        # user_email = get_user_email_by_id(user_id)
        
        values = (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount)
        cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
        connection.close()

    except ValueError as e:
        # Handle invalid date format or missing date
        flash(str(e), 'error')
        return redirect(url_for('category'))

    except Exception as e:
        # Handle other database or general errors
        flash('An error occurred while adding the category: ' + str(e), 'error')
        return redirect(url_for('category'))

    
        
    
    

def add_request(user_email, category_name, fundraising_for, expiry_date, amount, description):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # SQL INSERT statement
        insert_query = """
        INSERT INTO pend_requests (user_email, category_name, fundraising_for, expiry_date, amount, description)
        VALUES ( %s, %s, %s, %s, %s, %s)
        """

        # Values to insert into the table
        values = (user_email, category_name, fundraising_for, expiry_date, amount, description)

        cursor.execute(insert_query, values)
        connection.commit()
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("MySQL Error:", err)



# Getting all categories
def get_all_requests():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT id, user_email, category_name, fundraising_for, expiry_date, amount, description, approved FROM pend_requests')

        requests = cursor.fetchall()
        cursor.close()
        connection.close()
        return requests
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []


# Sowing a user his request
def get_user_requests(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        # Retrieve requests for the current user based on their user ID
        select_query = """
        SELECT category_name, fundraising_for,  amount, description FROM categories WHERE user_id = %s
        """
        print(user_id, 'userid')
        cursor.execute(select_query, (user_id,))
        user_requests = cursor.fetchall()
        print(user_requests, 'userrequest')
        return user_requests

    except Exception as e:
        print(f"Error fetching user requests: {str(e)}")
        return []

    finally:
        cursor.close()
        connection.close()





def is_user_admin(email):
    user = get_user(email)
    return user.is_admin if user else False



 
# def set_request_status(request_id, status):
#     connection = None
#     cursor = None

#     try:
#         connection = mysql.connector.connect(**config)
#         cursor = connection.cursor()
#         update_query = "UPDATE approved_requests SET status = %s WHERE id = %s"
#         cursor.execute(update_query, (status, request_id))
#         connection.commit()
#         # print(f"Query executed: {update_query}")
#         return True
#     except mysql.connector.Error as err:
#         print("Error:", err)
#         return False
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
def set_request_status(request_id, status, user_email, category_name, fundraising_for, expiry_date, amount):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO approved_requests (id, status, user_email, category_name, fundraising_for, expiry_date, amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (request_id, status, user_email, category_name, fundraising_for, expiry_date, amount))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False









  




# Showing the donator all donations
def get_all_donations():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donations")
        all_donations = cursor.fetchall()
        return all_donations
    except mysql.connector.Error as err:
        print("Error fetching all donations:", err)
        return []







def add_donator(name, email, first_time_donating, gender):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO donators (name, email, first_time_donating, gender) VALUES (%s, %s, %s, %s)", (name, email, first_time_donating, gender))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()
