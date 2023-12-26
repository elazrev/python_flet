import sqlite3

# Function to create the 'customers' table
conn = sqlite3.connect('customer_database.db')
cursor = conn.cursor()

# Creating the 'customers' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        phone_number TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        balance REAL
    )
''')

conn.commit()
conn.close()

# Function to add a customer to the 'customers' table
def add_customer(phone_number, first_name, last_name, balance):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO customers (phone_number, first_name, last_name, balance)
        VALUES (?, ?, ?, ?)
    ''', (phone_number, first_name, last_name, balance))

    conn.commit()
    conn.close()

# Function to remove a customer from the 'customers' table
def remove_customer(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM customers WHERE phone_number = ?', (phone_number,))

    conn.commit()
    conn.close()

# Function to change the balance of a customer
def change_balance(phone_number, new_balance):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET balance = ?
        WHERE phone_number = ?
    ''', (new_balance, phone_number))

    conn.commit()
    conn.close()

# Function to query the balance by phone number
def query_balance(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None
