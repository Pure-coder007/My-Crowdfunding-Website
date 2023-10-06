import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    

    # Users Table
    cursor.execute('CREATE DATABASE IF NOT EXISTS crowd_funding')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_admin TINYINT(1) NOT NULL DEFAULT 0,
        remaining_balance DECIMAL(10, 2) DEFAULT 0.00;
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
    
    
    # Categories table (Users inputed requests)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    fundraising_for VARCHAR(255) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    description TEXT,
    expiry_date DATE,
    minimum_amount DECIMAL(20, 2),
    user_email VARCHAR(100),
    request_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    request_id INT NOT NULL;
    
);

    """)
    
  
    # Outsiders who register to donate only
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
    CREATE TABLE donations_info(
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount_donated DECIMAL(10, 2),
    donator_name VARCHAR(255),
    required_amount DECIMAL(10, 2),
    email VARCHAR(255),
    cat_id INT NOT NULL,
);
                  
""")

    


    connection.commit()
    cursor.close()
    connection.close()
  
    
    
    
    
    if __name__ == "__main__":
        setup_database()