import mysql.connector

def setup_database():
    config = {
        'user': 'kingsley',
        'password': 'language007',
        'host': 'localhost',
        'port': '3306'
    }
    
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    cursor.execute('CREATE DATABASE IF NOT EXIST user_registration')
    cursor.execute('USE user_registration')
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
        )
        """)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    if __name__ == "__main__":
        setup_database()