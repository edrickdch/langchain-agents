import sqlite3
import random


def create_connection():
    """create a database connection to an SQLite database"""
    conn = sqlite3.connect("data/main.db")
    return conn


def close_connection(conn):
    """close the database connection"""
    if conn:
        conn.close()


def execute_query(conn, query, data=None):
    """execute a single query"""
    cursor = conn.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    cursor.close()


def execute_many_query(conn, query, data):
    """execute a single query with multiple data rows"""
    cursor = conn.cursor()
    cursor.executemany(query, data)
    conn.commit()
    cursor.close()


def select_query(conn, query):
    """execute a select query and return the result"""
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def main(email):
    # Establish a database connection
    conn = create_connection()

    # Create employee table
    employee_table_query = """
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    """
    execute_query(conn, employee_table_query)

    # Create sales_transaction table
    sales_transaction_table_query = """
        CREATE TABLE IF NOT EXISTS sales_transaction (
            id INTEGER PRIMARY KEY,
            seller_id INTEGER,
            revenue REAL,
            FOREIGN KEY(seller_id) REFERENCES employee(id)
        );
    """
    execute_query(conn, sales_transaction_table_query)

    # Upsert employee records
    employees = [
        (1, "John Doe", "head of sales", email),
        (2, "Jane Smith", "sales", "janesmith@example.com"),
        (3, "Bob Johnson", "sales", "bobjohnson@example.com"),
        (4, "Alice Williams", "sales", "alicewilliams@example.com"),
    ]

    employee_query = "INSERT OR REPLACE INTO employee VALUES (?, ?, ?, ?);"
    execute_many_query(conn, employee_query, employees)

    # Upsert sales_transaction records
    transactions = [
        (i, random.choice([2, 3, 4]), round(random.uniform(100, 1000), 2))
        for i in range(1, 11)
    ]

    sales_transaction_query = (
        "INSERT OR REPLACE INTO sales_transaction VALUES (?, ?, ?);"
    )
    execute_many_query(conn, sales_transaction_query, transactions)

    # Select and print all records from both tables for verification
    employee_select_query = "SELECT * FROM employee;"
    sales_transaction_select_query = "SELECT * FROM sales_transaction;"
    print("Employee Records:")
    print(select_query(conn, employee_select_query))
    print("Sales Transaction Records:")
    print(select_query(conn, sales_transaction_select_query))

    # Close the database connection
    close_connection(conn)


if __name__ == "__main__":
    email = input("What is the gmail address you intend your agent to use?")
    main(email)
