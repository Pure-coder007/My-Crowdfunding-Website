import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    cursor.execute('CREATE DATABASE IF NOT EXISTS crowd_funding')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_admin TINYINT(1) NOT NULL DEFAULT 0
    )
    """)
    
    
    
    # Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_email VARCHAR(100),  
        category_name VARCHAR(255) NOT NULL,
        fundraising_for VARCHAR(255) NOT NULL,  
        expiry_date DATE,  
        amount DECIMAL(20, 2) NOT NULL,
        description TEXT,
        user_id INT
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
    
    
    # Viewing users requests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_requests(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description TEXT,
    amount INT,
    status ENUM('pending', 'approved', 'disapproved') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id)
)

""")


    
    
    connection.commit()
    cursor.close()
    connection.close()
    
    
    
    
    
    
    
    
    
    
    
    
    if __name__ == "__main__":
        setup_database()