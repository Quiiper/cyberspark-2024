from flask import Flask, render_template, request, send_from_directory, g, make_response, redirect, jsonify
from models.db import ProductDB
from dotenv import load_dotenv
import os
import python_jwt as jwt
from jwcrypto import jwk
import datetime
from functools import wraps
from uuid import uuid4
from crawler.crawler import visit

load_dotenv()
with open('./jwt_secret_key.pem') as f:
    pem_data = f.read()

pem_data_decoded = pem_data.encode('utf-8')
JWT_SECRET_KEY = jwk.JWK.from_pem(pem_data_decoded)

USR = os.getenv('USR')
PASS = os.getenv('PASS')

app = Flask(__name__)

db = ProductDB()
db.create_tables()
db.insert_products()
db.insert_user(USR, PASS)

def authorize_roles(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('token')

            if not token:
                return jsonify({'message': 'JWT token is missing or invalid.'}), 401

            try:
                token = jwt.verify_jwt(token, JWT_SECRET_KEY, ['PS256'])
                user_role = token[1]['role']

                if user_role not in roles:
                    return jsonify({'message': f'{user_role} user does not have the required authorization to access the resource.'}), 403

                return func(*args, **kwargs)
            except Exception as e:
                return jsonify({'message': 'JWT token verification failed.', 'error': str(e)}), 401
        return wrapper
    return decorator

@app.before_request
def before_request():
    g.db = ProductDB()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'POST':
        ss = request.form['search']
        products = g.db.select_products(ss)
        print(products)
        return render_template('shop.html', products=products)
    products = g.db.get_all()
    return render_template('shop.html', products=products)

@app.route('/product/<id>')
def product(id):
    product = g.db.get_product(id)
    return render_template('shop-details.html', product=product)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if g.db.login(username, password):
            r = make_response(redirect('/manager'))
            claims = {'user': username, "role": "manager"}
            cookie = jwt.generate_jwt(claims, JWT_SECRET_KEY, 'PS256', datetime.timedelta(minutes=60))
            r.set_cookie('token', cookie)
            return r
    return render_template('signin.html')

@app.route('/manager')
@authorize_roles(['manager', 'administrator'])
def manager():
    return render_template('manager.html')

@app.route('/add', methods=['GET', 'POST'])
@authorize_roles(['manager', 'administrator'])
def add():
    if request.method == 'POST':
        id = str(uuid4())
        title = request.form['title']
        description = request.form['description']
        img = request.form['img']
        price = request.form['price']
        if g.db.insert_product(id, title, description, price, img):
            return jsonify({'message': 'Product added successfully.', 'id': id}), 200
        return jsonify({'message': 'Failed to add product. Contact administrator.'}), 500
    return render_template('add.html')

@app.route('/verify', methods=['GET', 'POST'])
@authorize_roles([ 'administrator'])
def verify():
    if request.method == 'POST':
        id = request.form['id']
        if visit(id):
            return jsonify({'message': 'Product visited successfully.'}), 200
        return jsonify({'message': 'Failed to visit product. Contact administrator.'}), 500
    return render_template('verify.html')

@app.route('/public/<path:path>')
def public(path):
    return send_from_directory('public', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)