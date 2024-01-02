import sqlite3
import json
from datetime import datetime

# Function to create the 'customers' table
conn = sqlite3.connect('customer_database.db')
cursor = conn.cursor()

# Creating the 'customers' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        phone_number TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        balance JSON,
        comments JSON 
    )
''')

conn.commit()
conn.close()
# Function to add a customer to the 'customers' table


def add_customer(phone_number, first_name, last_name,):
    balance = {"balance": 0, "update_date": None}
    balance_json = json.dumps(balance)

    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO customers (phone_number, first_name, last_name, balance)
        VALUES (?, ?, ?, ?)
    ''', (phone_number, first_name, last_name, balance_json))

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
    now = datetime.now()
    update_balance = json.dumps({'balance': new_balance, 'update_date': f"{datetime.now().strftime('%d-%m-%y, %H:%M')}"})
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET balance = ?
        WHERE phone_number = ?
    ''', (update_balance, phone_number))

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

def get_balance(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()[0]

    conn.close()

    return json.loads(result)



def customers_list():
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM customers""")
    result = cursor.fetchall()

    conn.close()

    # Sort the result by the 'first_name' column
    sorted_result = sorted(result, key=lambda x: x[1])  # Assumes 'first_name' is the second column (index 1)
    result_dict = [{'phone': i[0], 'first_name': i[1], 'last_name': i[2], 'balance': i[3]} for i in sorted_result]

    return result_dict


def add_comment(phone_number):
    pass


def edit_comment(phone_number, index):
    pass


def delete_comment(phone_number):
    pass


if __name__ == "__main__":
    #add_customer("0522837081", "Elazar", "Revach")
    #add_customer("0505577928", "Rami", "Revach")
    print(get_name("0505577928"))
    change_balance('0505577928', -20)
    print(json.loads(get_name('0522837081')[2]))
    print(json.loads(get_name('0522837081')[2]))
    print(json.loads(get_name('0505577928')[2])["balance"])
    print(get_balance('0522837081'))
    print(get_balance('0505577928'))
    print(customers_list())

