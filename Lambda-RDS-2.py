import os
import pymysql
import json

# Database settings from environment variables
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
new_db_name = "EmployeeDB"  # Database Name
table_name = "employees"    # Corrected Table Name

# Sample Employee Data
employees = [
    (1, "Alice Johnson", "Software Engineer", "alice.johnson@example.com"),
    (2, "Bob Smith", "Data Scientist", "bob.smith@example.com"),
    (3, "Charlie Brown", "DevOps Engineer", "charlie.brown@example.com"),
    (4, "Dana White", "Project Manager", "dana.white@example.com"),
    (5, "Eva Green", "QA Engineer", "eva.green@example.com"),
    (6, "Frank Miller", "Cloud Architect", "frank.miller@example.com"),
    (7, "Grace Lee", "Security Analyst", "grace.lee@example.com"),
    (8, "Henry Ford", "Business Analyst", "henry.ford@example.com"),
    (9, "Isla Fisher", "Database Administrator", "isla.fisher@example.com"),
    (10, "Jack Black", "Frontend Developer", "jack.black@example.com")
]

# Establish a database connection
def connect_to_rds():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        cursorclass=pymysql.cursors.DictCursor
    )

# Lambda function handler
def lambda_handler(event, context):
    try:
        connection = connect_to_rds()
        with connection.cursor() as cursor:
            # Create a new database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            cursor.execute(f"USE {new_db_name};")

            # Create the 'employees' table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_sql)

            # Insert Sample Employee Data
            insert_query = f"""
            INSERT INTO {table_name} (emp_id, name, role, email)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                role = VALUES(role),
                email = VALUES(email);
            """
            cursor.executemany(insert_query, employees)
            
            # Commit to finalize the insertion
            connection.commit()

            print(f"Database '{new_db_name}' and table '{table_name}' with employee data created successfully.")
            return {
                'statusCode': 200,
                'body': f"Database '{new_db_name}' and table '{table_name}' with employee data created successfully."
            }

    except pymysql.IntegrityError as e:
        print(f"Duplicate entry error: {e}")
        return {
            'statusCode': 400,
            'body': f"Duplicate entry error: {e}"
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        if 'connection' in locals():
            connection.close()
