import sqlite3
import bcrypt
import requests
from uuid import uuid4


class ProductDB():
    def __init__(self):
        self.con = sqlite3.connect('./database.db')
        self.cur = self.con.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)
        self.con.commit()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id VARCHAR(50) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                price VARCHAR(255) NOT NULL,
                rating VARCHAR(255) NOT NULL,
                image VARCHAR(255) NOT NULL
            )""")
        self.con.commit()

    def login(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        hash = self.cur.fetchone()[2]
        return bcrypt.checkpw(password.encode('utf-8'), hash)

    def insert_products(self):
        r = requests.get('https://fakestoreapi.com/products')
        data = r.json()
        for i in data:
            id = str(uuid4())
            title = i['title']
            price = i['price']
            description = i['description']
            img = i['image']
            rate = i['rating']['rate']
            self.cur.execute("INSERT INTO products (id, title, description, price, rating, image) VALUES (?, ?, ?, ?, ?, ?)", (id, title, description, price, rate, img))
        self.con.commit()

    def insert_user(self, username, password):
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.con.commit()

    def select_products(self, title):
        self.cur.execute(f"SELECT id, title, price, image FROM products WHERE title LIKE '{title}%'")
        return self.cur.fetchall()

    def get_all(self):
        self.cur.execute("SELECT * FROM products")
        return self.cur.fetchall()

    def get_product(self, id):
        self.cur.execute(f"SELECT * FROM products WHERE id = ?", (id,))
        return self.cur.fetchone()
    
    def insert_product(self, id, title, description, price, image, rating=0):
        try:
            self.cur.execute("INSERT INTO products (id, title, description, price, rating, image) VALUES (?, ?, ?, ?, ?, ?)", (id, title, description, price, rating, image))
            self.con.commit()
            return True
        except:
            return False