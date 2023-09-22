import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    cursor.execute('CRAETE DATABASE IF NOT EXISTS user_registration')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)
    
    
    
    # Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(255) NOT NULL,
        fundraising_for VARCHAR(255),
        amount DECIMAL(20, 2) NOT NULL,
        description TEXT
    )
    """)
    
    
    # Requests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        category_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
        
    )
    """)
    
    
    
    connection.commit()
    cursor.close()
    connection.close()
    
    
    
    
    
    
    
    
    
    
    
    
    if __name__ == "__main__":
        setup_database()