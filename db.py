import mysql.connector

# Connect to MySQL without selecting a database (for creating the new database)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Khan@123"
)

cursor = db.cursor()

# Step 1: Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS POLIO_DB")

# Step 2: Use the created database
cursor.execute("USE POLIO_DB")

# Step 3: Create the `register` table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS register (
        USER_NAME VARCHAR(50) PRIMARY KEY,
        mail VARCHAR(100),
        Ph_Number VARCHAR(15),
        PASSWORD VARCHAR(100)
    )
""")

# Step 4: Create the `book_vac` table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS book_vac (
        id INT PRIMARY KEY,
        Mother_name VARCHAR(20),
        Father_Name VARCHAR(20),
        Child_Name VARCHAR(20),
        Child_DOB DATE,
        Gender VARCHAR(20),
        ID_Proof VARCHAR(20),
        ID_No VARCHAR(20),
        State VARCHAR(20),
        District VARCHAR(20),
        Town VARCHAR(20),
        Center VARCHAR(20)
    )
""")

# Step 5: Create the `child` table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS child (
        id INT PRIMARY KEY AUTO_INCREMENT,
        User_Name VARCHAR(50),
        child_name VARCHAR(50),
        mother_name VARCHAR(50),
        father_name VARCHAR(50),
        date_of_birth DATE,
        blood_group VARCHAR(5),
        doses_taken INT,
        doses_left INT,
        gender VARCHAR(10),
        address VARCHAR(255)
    )
""")

# Commit the changes
db.commit()

# Close the connection
cursor.close()
db.close()

print("Database and tables created successfully!")
