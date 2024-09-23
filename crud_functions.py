import sqlite3
import random

def initiate_db():
    connection = sqlite3.connect('products.db')
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Products
                 (id INTEGER PRIMARY KEY, 
                 title TEXT NOT NULL, 
                 description TEXT, 
                 price INTEGER NOT NULL)''')
    c.execute("CREATE INDEX IF NOT title on Products (title)")
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products.db')
    c = connection.cursor()
    c.execute("SELECT * FROM Products")
    rows = c.fetchall()
    c.close()
    return rows

def add_product(title, description, price):
    initiate_db()
    connection = sqlite3.connect('products.db')
    conn = connection.cursor()
    conn.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (title, description, price))
    connection.commit()
    connection.close()


    add_product('Product1', 'Продуке1', 100)
    add_product('Product2', 'Продуке2', 200)
    add_product('Product3', 'Продуке3', 300)
    add_product('Product4', 'Продуке4', 400)


def is_included(username):
    connection = sqlite3.connect('users.db')
    connection = connection.cursor()
    check_user= connection.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        connection.close()
        return False
    else:
        connection.close()
        return True

def add_user(username, email, age):
    connection = sqlite3.connect('users.db')
    conn = connection.cursor()
    conn.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                    (username, email, age, 1000))
    connection.commit()
    connection.close()
    
