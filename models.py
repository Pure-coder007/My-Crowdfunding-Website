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
def add_category(user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO categories (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount))
    connection.commit()
    cursor.close()
    connection.close()


        
        
        
        



def get_all_requests():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
        SELECT categories.id, users.email as user_email, category_name, fundraising_for, expiry_date, amount, description, minimum_amount
        FROM categories 
        JOIN users ON categories.user_id = users.id
        """)

        requests = cursor.fetchall()
        cursor.close()
        connection.close()
        return requests
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []
    


# Sowing a user his request
def get_user_requests(user_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
        SELECT categories.id, users.email as user_email, category_name, fundraising_for, expiry_date, amount, description, minimum_amount
        FROM categories 
        JOIN users ON categories.user_id = users.id
        WHERE categories.user_id = %s
        """, (user_id,))

        user_requests = cursor.fetchall()
        cursor.close()
        connection.close()
        return user_requests
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []





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
