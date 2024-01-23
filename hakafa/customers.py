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
    try:
        cursor.execute('''
            INSERT INTO customers (phone_number, first_name, last_name, balance)
            VALUES (?, ?, ?, ?)
        ''', (phone_number, first_name, last_name, balance_json))
    except Exception as e:
        print(e)
        conn.commit()
        conn.close()

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

    cursor.execute('SELECT first_name, last_name, balance, comments  FROM customers WHERE phone_number = ?', (phone_number,))
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
    result_dict = [{'phone': i[0], 'first_name': i[1], 'last_name': i[2], 'balance': i[3], 'comments': (i[4])}for i in sorted_result]

    return result_dict

def search_customer_partial(query):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    # Use a wildcard '%' to match any characters before or after the query
    cursor.execute('''
        SELECT phone_number, first_name, last_name, balance
        FROM customers
        WHERE phone_number LIKE ? OR first_name LIKE ? OR last_name LIKE ?
    ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))

    result = cursor.fetchall()

    conn.close()

    result_dict = [{'phone': i[0], 'first_name': i[1], 'last_name': i[2], 'balance': i[3]} for i in result]

    return result_dict


def add_comment(phone_number, comment_text):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    # Fetch existing comments for the customer
    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    if not comment_text:
        conn.commit()
        conn.close()
        raise Exception

    if result and result[0] is not None:
        existing_comments = json.loads(result[0])
    else:
        existing_comments = []

    # Add the new comment with timestamp
    new_comment = {
        'text': comment_text,
        'timestamp': datetime.now().strftime('%d-%m-%y, %H:%M')
    }
    existing_comments.append(new_comment)

    # Update the comments in the database
    cursor.execute('''
        UPDATE customers
        SET comments = ?
        WHERE phone_number = ?
    ''', (json.dumps(existing_comments), phone_number))

    conn.commit()
    conn.close()


def edit_comment(phone_number, index, new_text):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    # Fetch existing comments for the customer
    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    existing_comments = json.loads(cursor.fetchone()[0]) if cursor.fetchone() else []

    # Check if the index is valid
    if 0 <= index < len(existing_comments):
        # Edit the comment with the new text and update timestamp
        existing_comments[index]['text'] = new_text
        existing_comments[index]['timestamp'] = datetime.now().strftime('%d-%m-%y, %H:%M')

        # Update the comments in the database
        cursor.execute('''
            UPDATE customers
            SET comments = ?
            WHERE phone_number = ?
        ''', (json.dumps(existing_comments), phone_number))

        conn.commit()
    else:
        print("Invalid comment index.")

    conn.close()


def delete_comment(phone_number, index):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    # Fetch existing comments for the customer
    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    try:
        existing_comments = json.loads(cursor.fetchone()[0])
    except Exception as e:
        print(e)

    # Check if the index is valid

    deleted_comment = existing_comments.pop(index)

    # Update the comments in the database
    cursor.execute('''
        UPDATE customers
        SET comments = ?
        WHERE phone_number = ?
    ''', (json.dumps(existing_comments), phone_number))

    conn.commit()
    conn.close()




def customer_comment_list(phone_number):

    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    # Fetch existing comments for the customer
    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    try:
        result = json.loads(cursor.fetchone()[0])
        conn.close()

        return result
    except Exception as e:
        print(e)

    conn.close()


def request_bool(phone_number):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    try:
        result = json.loads(cursor.fetchone()[0])
        conn.close()
        if result:
            return True
    except Exception as e:
        return False


if __name__ == "__main__":
    #add_customer("0522837081", "Elazar", "Revach")
    #add_customer("0505577928", "Rami", "Revach")
    """print(get_name("0505577928"))
    change_balance('0505577928', -20)
    print(json.loads(get_name('0522837081')[2]))
    print(json.loads(get_name('0522837081')[2]))
    print(json.loads(get_name('0505577928')[2])["balance"])
    print(get_balance('0522837081'))
    print(get_balance('0505577928'))"""

    print(search_customer_partial("r"))

