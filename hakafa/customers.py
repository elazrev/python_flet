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


def add_customer(phone_number, first_name, last_name, balance=0):
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


def is_customer(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return True
    else:
        return f'This number is not available'


def get_name(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, balance FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    return result


def customers_list():
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM customers""")
    result = cursor.fetchall()

    conn.close()

    # Sort the result by the 'first_name' column
    sorted_result = sorted(result, key=lambda x: x[1])  # Assumes 'first_name' is the second column (index 1)

    return sorted_result



if __name__ == "__main__":
    #add_customer("0522837081", "Elazar", "Revach", 0)
    #add_customer("0505577928", "Rami", "Revach", 0)
    print(get_name("0505577928"))
    change_balance('0505577928', -20)
    for i in customers_list():
        print(list(i))
