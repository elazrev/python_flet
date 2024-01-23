from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import json
import sqlite3
from fastapi.responses import JSONResponse

app = FastAPI()

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


class Customer(BaseModel):
    phone_number: str
    first_name: str
    last_name: str


class BalanceUpdate(BaseModel):
    new_balance: int


class Comment(BaseModel):
    comment_text: str


# Function to add a customer to the 'customers' table
@app.post("/add_customer")
async def add_customer(customer: Customer):
    balance = {"balance": 0, "update_date": None}
    balance_json = json.dumps(balance)

    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO customers (phone_number, first_name, last_name, balance)
            VALUES (?, ?, ?, ?)
        ''', (customer.phone_number, customer.first_name, customer.last_name, balance_json))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        conn.commit()
        conn.close()

    return {"message": "Customer added successfully"}


# Function to remove a customer from the 'customers' table
@app.delete("/remove_customer")
async def remove_customer(phone_number: str):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM customers WHERE phone_number = ?', (phone_number,))

    conn.commit()
    conn.close()

    return {"message": "Customer removed successfully"}


# Function to change the balance of a customer
@app.put("/change_balance")
async def change_balance(phone_number: str, balance_update: BalanceUpdate):
    now = datetime.now()
    update_balance = json.dumps({
        'balance': balance_update.new_balance,
        'update_date': f"{datetime.now().strftime('%d-%m-%y, %H:%M')}"
    })

    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE customers
        SET balance = ?
        WHERE phone_number = ?
    ''', (update_balance, phone_number))

    conn.commit()
    conn.close()

    return {"message": "Balance updated successfully"}


# Function to query the balance by phone number
@app.get("/query_balance/{phone_number}")
async def query_balance(phone_number: str):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {"balance": json.loads(result[0])}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# Function to list all customers
@app.get("/customers_list")
async def customers_list():
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM customers""")
    result = cursor.fetchall()

    conn.close()

    sorted_result = sorted(result, key=lambda x: x[1])
    result_dict = [{'phone': i[0], 'first_name': i[1], 'last_name': i[2], 'balance': i[3], 'comments': json.loads(i[4])} for i in sorted_result]

    return result_dict


# Function to search for customers based on a partial query
@app.get("/search_customer_partial/{query}")
async def search_customer_partial(query: str):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT phone_number, first_name, last_name, balance
        FROM customers
        WHERE phone_number LIKE ? OR first_name LIKE ? OR last_name LIKE ?
    ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))

    result = cursor.fetchall()

    conn.close()

    result_dict = [{'phone': i[0], 'first_name': i[1], 'last_name': i[2], 'balance': json.loads(i[3])} for i in result]

    return result_dict


# Function to add a comment to a customer
@app.post("/add_comment/{phone_number}")
async def add_comment(phone_number: str, comment: Comment):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    if not comment.comment_text:
        return JSONResponse(content={"error": "Comment text cannot be empty"}, status_code=400)

    if result and result[0] is not None:
        existing_comments = json.loads(result[0])
    else:
        existing_comments = []

    new_comment = {
        'text': comment.comment_text,
        'timestamp': datetime.now().strftime('%d-%m-%y, %H:%M')
    }
    existing_comments.append(new_comment)

    cursor.execute('''
        UPDATE customers
        SET comments = ?
        WHERE phone_number = ?
    ''', (json.dumps(existing_comments), phone_number))

    conn.commit()
    conn.close()

    return {"message": "Comment added successfully"}


# ... (other functions for editing and deleting comments)

# Function to get a customer's comment list
@app.get("/customer_comment_list/{phone_number}")
async def customer_comment_list(phone_number: str):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    if result and result[0] is not None:
        return json.loads(result[0])
    else:
        return {"comments": []}


# Function to check if a customer has comments
@app.get("/request_bool/{phone_number}")
async def request_bool(phone_number: str):
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT comments FROM customers WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()

    conn.close()

    if result and result[0] is not None:
        return {"has_comments": True}
    else:
        return {"has_comments": False}
