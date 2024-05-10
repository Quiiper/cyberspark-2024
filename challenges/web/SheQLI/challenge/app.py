from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

app.config['DATABASE'] = 'app.db'
def init_db():
    with app.app_context():
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username VARCHAR(100),
                            password VARCHAR(100)
                        );''')
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'a8cb9d3d5318958035c6ac28d0386e9e')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")
        conn.commit()
        conn.close()

if not os.path.exists('app.db'):
    init_db()

@app.route("/register", methods=["POST"])
def register():
    user = request.form.get('user')
    pwd = request.form.get('pass')

    if user == 'admin':
        return render_template("index.html", data="You can't register with admin username")

    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?);", (user, pwd))
    conn.commit()
    conn.close()

    return render_template("index.html", data="Registered successfully !")

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("user")
    pwd = request.form.get("pass")

    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username= ? AND password='%s'" % pwd, (user,))
    user_data = cur.fetchone()
    print(user_data)
    conn.close()
    if user_data:
        if user_data[1] == 'admin':
            return redirect(url_for("admin"))
        else:
            return "Hello " + user_data[1]
    else:
        return render_template("index.html", data="Invalid Login/Password !!")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
