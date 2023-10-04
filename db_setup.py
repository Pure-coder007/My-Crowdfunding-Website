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
    

    # Registering donators
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donators (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            first_time_donating BOOLEAN,
            gender VARCHAR(10),
            admin BOOLEAN
        );
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
        minimum_amount DECIMAL(20, 2) DEFAULT NULL,
        description TEXT,
        user_id INT
    );
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
    CREATE TABLE IF NOT EXISTS approved_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    fundraising_for VARCHAR(255) NOT NULL,
    expiry_date DATE NOT NULL,
    amount INT NOT NULL,
    description TEXT,
    status VARCHAR(255) NOT NULL,  -- Add a status column
    INDEX (user_email),
    FOREIGN KEY (user_email) REFERENCES users(email)
);



""")
    connection.commit()
    cursor.close()
    connection.close()
    
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fund(
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    amount INT,
    amount_donated INT,
    user_id INT
    )
""")    
    connection.commit()
    cursor.close()
    connection.close()
    
    
    
    cursor.execute("""
    CREATE TABLE donators(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_time_donating BOOLEAN NOT NULL,
    gender VARCHAR(10) NOT NULL,
   
    );

""")
    
    cursor.execute("""
    CREATE TABLE donation_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_email VARCHAR(255) NOT NULL,
    amount_donated DECIMAL(10, 2) NOT NULL,
    receiver_email VARCHAR(255) NOT NULL,
)
    """)

    
    
    
    
    
    if __name__ == "__main__":
        setup_database()